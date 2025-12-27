#!/usr/bin/env python3
"""
Generate 5 blonde model variations to choose from
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv('.env.local')

def create_variation_prompt(variation_num: int) -> str:
    """Create prompts with slight variations"""

    # Vary hair shades and small details
    hair_options = [
        "natural honey blonde hair, long and straight with subtle waves",
        "warm golden blonde hair, straight with center part",
        "sandy blonde hair, sleek and straight",
        "light blonde hair with caramel highlights, long and flowing",
        "sun-kissed blonde hair, straight with natural shine"
    ]

    ages = [22, 23, 22, 24, 23]

    hair = hair_options[variation_num - 1]
    age = ages[variation_num - 1]

    prompt = f"""Professional photo reference sheet: Side-by-side view showing front and back of the same woman.

SUBJECT: Beautiful {age}-year-old blonde woman with {hair}. Golden-bronze tan skin. NO TATTOOS. NO TEXT OR LABELS ON IMAGE.

BODY TYPE: Extremely voluptuous hourglass figure with:
- LARGE natural full bust (heavy, realistic breast physics and skin texture)
- MASSIVE thick round glutes (prominent butt)
- Wide flared hips and thick athletic thighs
- Tiny defined waist creating dramatic curves

FACE: CLEARLY VISIBLE, well-lit face. Natural beauty with visible skin texture, pores, fine details. Hazel or light brown eyes with sparkle. Full natural lips. Warm, confident expression looking at camera. Natural makeup. FACE MUST BE IN FOCUS AND CLEARLY VISIBLE.

BIKINI: Black triangle string bikini with minimal coverage. High-cut thong bottom showing curves.

POSE:
- LEFT SIDE: Front view, standing upright, arms relaxed at sides, facing camera directly, FACE CLEARLY VISIBLE
- RIGHT SIDE: Back view, standing straight, hair down back, showcasing glutes and figure from behind

ENVIRONMENT: Bright outdoor backyard patio with white house siding, green grass, tropical plants. Clean, upscale setting.

LIGHTING: Bright natural daylight, well-lit face and body, high contrast, professional photography lighting.

CAMERA: Full body shot with clear face visibility, Canon EOS R5, 85mm f/1.8, ultra-sharp detail, RAW quality, 8K resolution.

CRITICAL REQUIREMENTS:
- Face must be clearly visible, well-lit, and in focus
- Hyper-realistic skin texture with pores and natural details
- NO text, labels, watermarks, or descriptions on the image
- NO plastic CGI look
- Clean professional photo

AVOID: tattoos, body art, plastic skin, airbrushed, cgi, 3d render, cartoon, small breasts, flat chest, skinny, thigh gap, small butt, flat butt, text overlays, labels, watermarks, fused bodies, bad anatomy, obscured face, dark face, blurry face"""

    return prompt

def generate_option(option_num: int, output_dir: Path) -> bool:
    """Generate one variation option"""
    print(f"\n{'='*60}")
    print(f"GENERATING OPTION {option_num}/5")
    print(f"{'='*60}")

    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

        prompt = create_variation_prompt(option_num)
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
                print(f"Response: {part.text[:100]}...")
            elif image := part.as_image():
                output_path = output_dir / f"option_{option_num}.jpeg"
                image.save(output_path)
                file_size = output_path.stat().st_size / (1024 * 1024)  # MB
                print(f"✓ Saved: {output_path}")
                print(f"  Size: {file_size:.2f} MB")
                return True

        print("✗ No image generated")
        return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Generate 5 blonde model options"""
    print("="*60)
    print("GENERATING 5 BLONDE MODEL OPTIONS")
    print("="*60)
    print("Creating slight variations for you to choose from...")

    # Create output directory
    output_dir = Path("modle/options")
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0

    for i in range(1, 6):
        if generate_option(i, output_dir):
            success_count += 1

        # Wait between generations to avoid rate limiting
        if i < 5:
            print("\nWaiting 3 seconds...")
            time.sleep(3)

    print("\n" + "="*60)
    print(f"COMPLETE! {success_count}/5 options generated")
    print("="*60)
    print("\nGenerated files:")
    for i in range(1, 6):
        print(f"  - modle/options/option_{i}.jpeg")
    print("\nCheck them out and let me know which one you like!")

if __name__ == "__main__":
    main()
