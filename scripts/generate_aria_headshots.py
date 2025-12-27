#!/usr/bin/env python3
import replicate
import boto3
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def generate_face_variations(
    model_name: str,
    base_image_s3_key: str,
    output_subfolder: str,
    bucket_name: str = 'models-aria-bikini',
    variations: list = None
):
    """
    Generate face-only variations of a model using Seedream 4.5

    Args:
        model_name: Name of the model (e.g., 'aria')
        base_image_s3_key: S3 key for base image (e.g., 'aria/base.jpeg')
        output_subfolder: Subfolder for outputs (e.g., 'face_variations')
        bucket_name: S3 bucket name
        variations: List of expressions/angles to generate
    """
    # Load environment variables
    load_dotenv('.env.local')

    # Set up paths
    output_dir = Path(f"modle/{model_name}/{output_subfolder}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # AWS S3 setup
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    # Default variations if not provided
    if variations is None:
        variations = [
            "neutral expression",
            "smiling with teeth showing",
            "soft subtle smile",
            "three-quarter angle facing left",
            "three-quarter angle facing right"
        ]

    # Build base image URL
    aws_region = os.getenv('AWS_REGION')
    base_image_url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{base_image_s3_key}"

    print(f"Model: {model_name}")
    print(f"Base image: {base_image_url}")
    print(f"Generating {len(variations)} face variations...")

    # Build prompt
    variations_text = "\n".join([f"{i+1}. {v}" for i, v in enumerate(variations)])
    prompt = f"""Use this image and keep everything exactly the same. Generate close-up face portraits showing:
{variations_text}

Professional photography style, well-lit, clean background."""

    # Call Seedream 4.5 API
    input_params = {
        "prompt": prompt,
        "image_input": [base_image_url],
        "size": "2K",
        "aspect_ratio": "3:4",
        "sequential_image_generation": "auto",
        "max_images": len(variations)
    }

    print(f"\nRunning Seedream 4.5...")
    output = replicate.run("bytedance/seedream-4.5", input=input_params)

    # Save images locally and to S3
    print("\nProcessing generated images...")
    results = []

    for idx, image_output in enumerate(output, 1):
        print(f"\n  Image {idx}: {variations[idx-1] if idx <= len(variations) else 'variation'}")

        # Download image
        print(f"    Downloading...")
        response = requests.get(image_output)
        image_data = response.content

        # Save locally
        filename = f"face_{idx}.jpeg"
        local_path = output_dir / filename
        with open(local_path, "wb") as f:
            f.write(image_data)
        print(f"    ✓ Saved locally: {local_path}")

        # Upload to S3
        s3_key = f"{model_name}/{output_subfolder}/{filename}"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=image_data,
            ContentType='image/jpeg'
        )
        s3_url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{s3_key}"
        print(f"    ✓ Uploaded to S3: {s3_url}")

        results.append({
            'local_path': str(local_path),
            's3_url': s3_url,
            'variation': variations[idx-1] if idx <= len(variations) else 'variation'
        })

    print(f"\n✓ Done! Generated {len(results)} face variations")
    print(f"  Local: {output_dir}")
    print(f"  S3: s3://{bucket_name}/{model_name}/{output_subfolder}/")

    return results

if __name__ == "__main__":
    # Generate face variations for Aria
    results = generate_face_variations(
        model_name="aria",
        base_image_s3_key="aria/base.jpeg",
        output_subfolder="face_variations",
        variations=[
            "neutral expression, looking straight ahead",
            "smiling with teeth showing, looking straight ahead",
            "soft subtle smile, looking straight ahead",
            "three-quarter angle facing left, natural expression",
            "three-quarter angle facing right, natural expression"
        ]
    )
