#!/usr/bin/env python3
"""
Generate 10 "hot" college-age models with striking features and appealing builds
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv('.env.local')

def create_hot_prompt(variation_num: int) -> str:
    """Create prompts for exceptionally attractive models"""

    # Define 10 "hot" model profiles with striking features
    profiles = [
        {
            "age": 22,
            "hair": "long silky platinum blonde hair with perfect waves, flowing past shoulders",
            "skin": "flawless golden tan skin with sun-kissed glow",
            "body": "Stunning hourglass figure with large full natural bust (D-cup), extremely narrow waist, dramatically wide hips, thick powerful thighs, massive round protruding glutes",
            "face": "Breathtakingly beautiful face with striking blue eyes, high sculpted cheekbones, perfect symmetry, full pouty lips, delicate nose",
            "eyes": "piercing bright blue eyes"
        },
        {
            "age": 21,
            "hair": "long sleek jet black hair, straight and shiny, cascading down back",
            "skin": "smooth bronze tan with warm golden undertones",
            "body": "Extremely voluptuous build with massive natural bust (DD-cup), tiny cinched waist, extra wide flared hips, very thick thighs, huge round bubble butt",
            "face": "Stunning exotic beauty with sultry dark brown eyes, sharp cheekbones, perfectly arched brows, full sensual lips",
            "eyes": "deep sultry brown eyes"
        },
        {
            "age": 23,
            "hair": "long honey blonde hair with caramel highlights, loose beachy waves",
            "skin": "perfect golden bronze tan, radiant and glowing",
            "body": "Incredible hourglass with large perky bust (D-cup), impossibly small waist, very wide hips, athletic thick thighs, large firm round glutes",
            "face": "Model-perfect face with captivating hazel eyes, prominent cheekbones, flawless bone structure, plump lips",
            "eyes": "mesmerizing hazel eyes"
        },
        {
            "age": 20,
            "hair": "long rich dark brown hair with red undertones, silky and voluminous",
            "skin": "deep warm tan with flawless bronze tone",
            "body": "Exaggerated hourglass with huge natural bust (E-cup), extremely narrow waist, massively wide hips, super thick thighs, exceptionally large round glutes",
            "face": "Gorgeous face with striking green eyes, high defined cheekbones, perfect facial proportions, full bee-stung lips",
            "eyes": "striking emerald green eyes"
        },
        {
            "age": 22,
            "hair": "long beach blonde hair with natural highlights, tousled waves",
            "skin": "beautiful golden tan with sun-kissed radiance",
            "body": "Perfect hourglass with full natural bust (DD-cup), tiny waist, dramatically curved hips, thick muscular thighs, massive protruding round glutes",
            "face": "Stunning beauty with bright blue eyes, sharp jawline, high cheekbones, perfect nose, luscious full lips",
            "eyes": "vivid blue eyes"
        },
        {
            "age": 24,
            "hair": "long chocolate brown hair, sleek and shiny with subtle waves",
            "skin": "gorgeous deep bronze tan with rich warm tones",
            "body": "Phenomenal curves with very large natural bust (DD-cup), extremely small waist, extra wide hips, super thick thighs, enormous round bubble butt",
            "face": "Beautiful face with captivating light brown eyes, sculpted cheekbones, perfect symmetry, full pouty lips",
            "eyes": "warm light brown eyes"
        },
        {
            "age": 21,
            "hair": "long sandy blonde hair with lighter streaks, flowing and wavy",
            "skin": "perfect light golden tan with luminous glow",
            "body": "Amazing hourglass with large perky bust (D-cup), very narrow waist, wide flared hips, thick toned thighs, large firm round glutes",
            "face": "Gorgeous face with stunning grey-blue eyes, high cheekbones, refined features, full sensual lips",
            "eyes": "stunning grey-blue eyes"
        },
        {
            "age": 23,
            "hair": "long dark auburn hair with copper highlights, thick and wavy",
            "skin": "flawless medium tan with golden undertones",
            "body": "Incredible build with huge natural bust (E-cup), tiny cinched waist, dramatically wide hips, very thick thighs, massive round protruding glutes",
            "face": "Striking beauty with intense hazel eyes, prominent cheekbones, perfect bone structure, plump full lips",
            "eyes": "intense hazel-green eyes"
        },
        {
            "age": 22,
            "hair": "long caramel blonde hair, perfectly straight and glossy",
            "skin": "beautiful bronze tan with radiant golden glow",
            "body": "Perfect hourglass with very large natural bust (DD-cup), extremely narrow waist, extra wide hips, thick powerful thighs, huge round bubble butt",
            "face": "Breathtaking face with bright green eyes, high sculpted cheekbones, flawless features, full pouty lips",
            "eyes": "bright emerald eyes"
        },
        {
            "age": 20,
            "hair": "long golden blonde hair with lighter highlights, big voluminous waves",
            "skin": "perfect deep golden tan with sun-kissed warmth",
            "body": "Jaw-dropping curves with massive natural bust (E-cup), impossibly small waist, massively wide hips, extra thick thighs, exceptionally large round protruding glutes",
            "face": "Stunning face with piercing blue eyes, sharp defined cheekbones, perfect symmetry, full luscious lips",
            "eyes": "piercing crystal blue eyes"
        }
    ]

    profile = profiles[variation_num - 1]

    prompt = f"""Professional photo reference sheet: Side-by-side view showing front and back of the same exceptionally attractive woman.

SUBJECT: Stunningly beautiful {profile['age']}-year-old college woman with {profile['hair']}. {profile['skin']}. NO TATTOOS. NO TEXT OR LABELS ON IMAGE.

BODY TYPE: {profile['body']} - emphasize dramatic feminine curves and appealing proportions.

FACE: CLEARLY VISIBLE, well-lit gorgeous face. {profile['face']}. {profile['eyes']} with captivating gaze looking directly at camera. Confident, alluring expression. Natural makeup enhancing features. FACE MUST BE IN FOCUS AND CLEARLY VISIBLE.

SKIN REALISM (CRITICAL):
- Visible micro-pores across face and body
- Natural skin texture with fine grain
- Subtle natural beauty marks
- Real biological skin, NOT overly airbrushed
- Light peach fuzz visible in sunlight
- Natural skin variations
- Very subtle natural marks on hips/thighs
- Skin looks like attractive real human skin with minimal but present imperfections

BIKINI: Black triangle string bikini with minimal coverage, showing off curves. High-cut thong bottom emphasizing figure.

POSE:
- LEFT SIDE: Front view, standing upright with confident posture, one hand on hip or arms relaxed, facing camera directly showing curves, FACE CLEARLY VISIBLE
- RIGHT SIDE: Back view, standing straight, hair cascading down back, showcasing glutes and dramatic curves from behind

ENVIRONMENT: Bright outdoor backyard patio with white house siding, green grass, tropical plants. Clean, upscale setting.

LIGHTING: Bright natural daylight, well-lit face and body highlighting curves, high contrast, professional photography lighting.

CAMERA: Full body shot with clear face visibility, Canon EOS R5, 85mm f/1.8, ultra-sharp detail, RAW quality, 8K resolution, professional glamour photography.

CRITICAL REQUIREMENTS:
- Face must be clearly visible, well-lit, and strikingly beautiful
- Body must have dramatic, appealing curves and proportions
- Hyper-realistic skin texture with natural details (not overly perfect but still attractive)
- NO text, labels, watermarks on image
- Professional glamour photography aesthetic
- Emphasize sex appeal and attractiveness while maintaining realism

AVOID: tattoos, body art, overly plastic smooth skin, heavy filters, cgi, 3d render, cartoon, text overlays, labels, watermarks, fused bodies, bad anatomy, obscured face, small breasts, flat butt, skinny, boyish figure, plain features"""

    return prompt

def generate_option(option_num: int, output_dir: Path) -> bool:
    """Generate one hot model option"""
    print(f"\n{'='*60}")
    print(f"GENERATING MODEL {option_num}/10")
    print(f"{'='*60}")

    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

        prompt = create_hot_prompt(option_num)
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
                output_path = output_dir / f"hot_option_{option_num}.jpeg"
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
    """Generate 10 exceptionally attractive models"""
    print("="*60)
    print("GENERATING BATCH 3: 10 'HOT' MODELS")
    print("="*60)
    print("Focus: Striking faces, dramatic curves, appealing builds")
    print("Constant: Black bikini, backyard setting, front/back pose")

    output_dir = Path("modle/batch3")
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
        print(f"  - modle/batch3/hot_option_{i}.jpeg")
    print("\nCheck them out!")

if __name__ == "__main__":
    main()
