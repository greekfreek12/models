#!/usr/bin/env python3
"""
Generate 3 new blonde models (base images only) using Gemini API
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import time

load_dotenv('.env.local')

# Model names - starting with just 1 for testing
MODEL_NAMES = ["daisy"]  # Change to ["daisy", "ella", "fiona"] once you like the result

def create_base_image_prompt(model_name: str, age: int) -> str:
    """Create detailed prompt for generating base model image"""

    prompt = f"""Professional photo reference sheet: Side-by-side diptych showing front and back views of the same woman.

SUBJECT: Beautiful {age}-year-old blonde woman with platinum straight hair (dark roots, center part). Golden-bronze tan skin. NO TATTOOS.

BODY TYPE: Extremely voluptuous hourglass figure with:
- LARGE natural bust (massive, heavy breasts with realistic physics and skin texture)
- MASSIVE thick round glutes (prominent, protruding butt)
- Wide flared hips and thick athletic thighs
- Tiny defined waist creating dramatic curves

FACE: Hyper-realistic with visible pores, fine peach fuzz, natural skin texture. Hazel eyes with realistic wetness. Full lips. Calm, alluring expression looking at camera. No airbrushing.

BIKINI: Black triangle string bikini with wooden bead details. High-cut thong bottom showing curves.

POSE:
- LEFT PANEL: Front view, standing upright, arms at sides, facing camera
- RIGHT PANEL: Back view, standing straight, long blonde hair down back, showcasing glutes

ENVIRONMENT: Backyard patio with white house siding, green artificial turf, tropical plants.

LIGHTING: Natural hard noon sunlight, high contrast with white wall as reflector.

CAMERA: Full body shot, Canon EOS R5, 85mm f/1.8, ultra-sharp detail, RAW quality, 8K resolution.

CRITICAL: Hyper-realistic skin with biological texture, pores, natural imperfections. NO plastic CGI look.

AVOID: tattoos, ink, body art, plastic skin, airbrushed, cgi, 3d render, cartoon, small breasts, flat chest, skinny, thigh gap, small butt, flat butt, fused bodies, bad anatomy"""

    return prompt

def generate_base_image(model_name: str, age: int, output_dir: Path) -> bool:
    """Generate base reference image for a model"""
    print(f"\n{'='*60}")
    print(f"GENERATING: {model_name.upper()}")
    print(f"{'='*60}")

    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

        prompt = create_base_image_prompt(model_name, age)
        print(f"Age: {age}")
        print(f"Prompt length: {len(prompt)} characters")
        print(f"Calling Gemini API...")

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",  # Side-by-side diptych
                    image_size="4K"  # Highest quality
                )
            )
        )

        # Save the generated image
        for part in response.parts:
            if part.text:
                print(f"\nResponse: {part.text}")
            elif image := part.as_image():
                output_path = output_dir / "base.jpeg"
                # Save directly - Gemini API handles format conversion
                image.save(output_path)
                print(f"✓ Saved: {output_path}")
                # Get file size
                file_size = output_path.stat().st_size / (1024 * 1024)  # MB
                print(f"  File size: {file_size:.2f} MB")
                return True

        print("✗ No image generated")
        return False

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Generate 3 new blonde model base images"""
    print("="*60)
    print(f"GENERATING {len(MODEL_NAMES)} BLONDE MODEL (BASE IMAGE ONLY)")
    print("="*60)
    print(f"Models: {', '.join([m.capitalize() for m in MODEL_NAMES])}")

    # Ages for variety
    ages = [22, 23, 24]

    success_count = 0

    for model_name, age in zip(MODEL_NAMES, ages):
        # Create model directory
        model_dir = Path(f"modle/{model_name}")
        model_dir.mkdir(parents=True, exist_ok=True)

        # Generate base image
        if generate_base_image(model_name, age, model_dir):
            success_count += 1

        # Wait between models to avoid rate limiting
        if model_name != MODEL_NAMES[-1]:
            print("\nWaiting 5 seconds...")
            time.sleep(5)

    print("\n" + "="*60)
    print(f"COMPLETE! {success_count}/{len(MODEL_NAMES)} models generated")
    print("="*60)
    print("\nGenerated base images:")
    for model_name in MODEL_NAMES:
        print(f"  - modle/{model_name}/base.jpeg")
    print("\nCheck the images. If you like them, we can generate face variations next!")

if __name__ == "__main__":
    main()
