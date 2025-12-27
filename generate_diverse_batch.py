#!/usr/bin/env python3
"""
Generate 5 diverse college-age models with varied features
Same bikini, background, and pose - different everything else
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv('.env.local')

def create_diverse_prompt(variation_num: int) -> str:
    """Create diverse model prompts with variety"""

    # Define 10 distinct model profiles
    profiles = [
        {
            "age": 21,
            "hair": "long dark brown hair, sleek and straight with subtle shine",
            "skin": "fair porcelain skin with natural rosy undertones",
            "body": "Athletic build with toned abs, medium perky bust, firm athletic glutes, defined waist",
            "eyes": "bright blue eyes"
        },
        {
            "age": 23,
            "hair": "vibrant auburn red hair, long with natural waves",
            "skin": "pale fair skin with light freckles across nose and shoulders",
            "body": "Petite curvy figure, small frame with compact curves, full bust, round hips",
            "eyes": "green eyes"
        },
        {
            "age": 22,
            "hair": "jet black hair, long and straight with high shine",
            "skin": "warm olive complexion with golden undertones",
            "body": "Balanced hourglass with moderate curves, proportional bust and hips, soft feminine shape",
            "eyes": "dark brown eyes"
        },
        {
            "age": 24,
            "hair": "honey brown hair with caramel highlights, long with beach waves",
            "skin": "medium tan skin with sun-kissed glow",
            "body": "Bottom-heavy pear shape, smaller bust, thick powerful thighs, large round glutes",
            "eyes": "hazel eyes"
        },
        {
            "age": 20,
            "hair": "dark chocolate brown hair, long and silky straight",
            "skin": "deep bronze tan with rich warm tones",
            "body": "Voluptuous hourglass, full natural bust, wide hips, thick thighs, dramatic curves",
            "eyes": "light brown eyes"
        },
        {
            "age": 22,
            "hair": "platinum blonde hair with darker roots, straight and sleek",
            "skin": "light tan skin with golden glow",
            "body": "Slim athletic build with toned legs, small perky bust, firm athletic glutes",
            "eyes": "grey-blue eyes"
        },
        {
            "age": 21,
            "hair": "copper red hair with natural curls and waves",
            "skin": "very fair pale skin with freckles all over",
            "body": "Soft curvy hourglass, medium bust, wide hips, thick soft thighs",
            "eyes": "emerald green eyes"
        },
        {
            "age": 23,
            "hair": "dark brown hair with auburn lowlights, beach waves",
            "skin": "warm medium skin with olive undertones",
            "body": "Balanced athletic curves, moderate bust, toned waist, muscular legs",
            "eyes": "dark hazel eyes"
        },
        {
            "age": 24,
            "hair": "light ash blonde hair, long and straight with volume",
            "skin": "fair rosy skin with natural flush",
            "body": "Tall slender build with long legs, small bust, subtle hip curve",
            "eyes": "ice blue eyes"
        },
        {
            "age": 20,
            "hair": "dark espresso brown hair, wavy and thick",
            "skin": "deep tan with warm bronze undertones",
            "body": "Thick curvy build, large natural bust, extra wide hips, very thick thighs",
            "eyes": "deep brown eyes"
        }
    ]

    profile = profiles[variation_num - 1]

    prompt = f"""Professional photo reference sheet: Side-by-side view showing front and back of the same woman.

SUBJECT: Beautiful {profile['age']}-year-old college woman with {profile['hair']}. {profile['skin']}. NO TATTOOS. NO TEXT OR LABELS ON IMAGE.

BODY TYPE: {profile['body']}

FACE: CLEARLY VISIBLE, well-lit face. Natural beauty with {profile['eyes']}. Full natural lips. Warm, confident expression looking at camera. Natural minimal makeup. FACE MUST BE IN FOCUS AND CLEARLY VISIBLE.

SKIN REALISM (CRITICAL):
- Visible micro-pores across face, nose, forehead, and body
- Natural skin texture with fine lines and grain
- Subtle natural blemishes, beauty marks, tiny moles
- Real biological skin, NOT airbrushed or smoothed
- Light peach fuzz visible in sunlight
- Natural skin variations and slight color differences
- Subtle stretch marks on hips/thighs (realistic and natural)
- Very light natural cellulite texture on thighs (barely visible but present)
- Skin looks like actual human skin with imperfections, NOT magazine-perfect

BIKINI: Black triangle string bikini with minimal coverage. High-cut thong bottom showing figure.

POSE:
- LEFT SIDE: Front view, standing upright, arms relaxed at sides, facing camera directly, FACE CLEARLY VISIBLE
- RIGHT SIDE: Back view, standing straight, hair down back, showcasing figure from behind

ENVIRONMENT: Bright outdoor backyard patio with white house siding, green grass, tropical plants. Clean, upscale setting.

LIGHTING: Bright natural daylight, well-lit face and body, high contrast, professional photography lighting that shows real skin texture.

CAMERA: Full body shot with clear face visibility, Canon EOS R5, 85mm f/1.8, ultra-sharp detail showing natural skin imperfections, RAW quality, 8K resolution.

CRITICAL REQUIREMENTS:
- Face must be clearly visible, well-lit, and in focus
- HYPER-REALISTIC skin with visible pores, texture, and natural imperfections
- NO perfect smooth skin - must look like real biological human skin
- NO text, labels, watermarks, or descriptions on the image
- NO plastic CGI look or Instagram filter smoothing
- Real unretouched photography aesthetic

AVOID: tattoos, body art, plastic smooth skin, airbrushed skin, filtered skin, perfect skin, cgi, 3d render, cartoon, text overlays, labels, watermarks, fused bodies, bad anatomy, obscured face, beauty filter, skin smoothing"""

    return prompt

def generate_option(option_num: int, output_dir: Path) -> bool:
    """Generate one diverse model option"""
    print(f"\n{'='*60}")
    print(f"GENERATING MODEL {option_num}/5")
    print(f"{'='*60}")

    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

        prompt = create_diverse_prompt(option_num)
        print(f"Calling Gemini API...")

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="4K"
                )
            )
        )

        # Save the generated image
        for part in response.parts:
            if part.text:
                print(f"Response: {part.text[:100]}...")
            elif image := part.as_image():
                output_path = output_dir / f"batch2_option_{option_num}.jpeg"
                image.save(output_path)
                file_size = output_path.stat().st_size / (1024 * 1024)
                print(f"✓ Saved: {output_path}")
                print(f"  Size: {file_size:.2f} MB")
                return True

        print("✗ No image generated")
        return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Generate 10 diverse college-age models"""
    print("="*60)
    print("GENERATING BATCH 2: 10 DIVERSE MODELS")
    print("="*60)
    print("Variety: Different hair colors, body types, skin tones")
    print("Constant: Black bikini, backyard setting, front/back pose")

    output_dir = Path("modle/batch2")
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0

    for i in range(1, 11):
        if generate_option(i, output_dir):
            success_count += 1

        if i < 10:
            print("\nWaiting 3 seconds...")
            time.sleep(3)

    print("\n" + "="*60)
    print(f"COMPLETE! {success_count}/10 models generated")
    print("="*60)
    print("\nGenerated files:")
    for i in range(1, 11):
        print(f"  - modle/batch2/batch2_option_{i}.jpeg")
    print("\nCheck them out!")

if __name__ == "__main__":
    main()
