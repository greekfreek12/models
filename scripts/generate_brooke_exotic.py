#!/usr/bin/env python3
"""
Generate Brooke in Elephant Stampede bikini at 4 exotic locations
Using google/nano-banana-pro on Replicate
"""

import replicate
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')

# Reference images
BROOKE_BASE = "modle/brooke/base.jpeg"
BIKINI_REF = "bikinis/Alabama/on_models/elephant_stampede_white.png"

# Output directory
OUTPUT_DIR = Path("content/brooke/exotic_locations")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Location prompts
LOCATIONS = {
    "1_african_safari": """Professional photo: Side-by-side diptych showing front and back views of stunning woman.

SUBJECT: Beautiful 21-year-old woman with long sleek jet black hair. Smooth bronze tan. Extremely voluptuous hourglass figure with massive bust, tiny waist, wide hips, thick thighs, huge round glutes.

FACE: Clearly visible, sultry deep brown eyes, sharp cheekbones, full lips. Confident expression looking at camera.

BIKINI: White bandeau bikini top with crimson red elephant pattern. Matching high-waisted bottoms with elephant pattern. (Reference provided in images)

POSE:
- LEFT: Front view, standing next to large African elephant, one hand on hip, golden hour lighting
- RIGHT: Back view near elephant, hair down, showcasing curves

ENVIRONMENT: African safari savanna at golden hour. Large elephant in frame. Acacia trees. Dry grass. Warm sunset lighting. Vast plains.

LIGHTING: Golden hour sunset, warm amber tones, dramatic lighting, natural sunlight.

STYLE: National Geographic wildlife photography, 8K, ultra-sharp, professional.

CRITICAL: Face clearly visible, elephant prominent, hyper-realistic skin with pores and texture, NO text/labels.

AVOID: tattoos, plastic skin, airbrushed, cgi, cartoon, text, watermarks, bad anatomy.""",

    "2_luxury_safari_lodge": """Professional photo: Side-by-side diptych showing front and back views of stunning woman.

SUBJECT: Beautiful 21-year-old woman with long sleek jet black hair. Smooth bronze tan. Extremely voluptuous hourglass figure with massive bust, tiny waist, wide hips, thick thighs, huge round glutes.

FACE: Clearly visible, sultry deep brown eyes, sharp cheekbones, full lips. Confident expression.

BIKINI: White bandeau bikini top with crimson red elephant pattern. Matching high-waisted bottoms. (Reference provided in images)

POSE:
- LEFT: Front view at edge of infinity pool, one leg bent, savanna view behind
- RIGHT: Back view at pool edge, hair down, African landscape background

ENVIRONMENT: Luxury safari lodge infinity pool overlooking African savanna. Modern architecture with wood and stone. Distant elephants on plains. Teak deck. Late afternoon.

LIGHTING: Natural bright daylight, blue sky, luxury resort photography.

STYLE: Luxury travel magazine, 8K, ultra-sharp, professional.

CRITICAL: Face visible, vista with elephants, infinity pool prominent, realistic skin texture, NO text.

AVOID: tattoos, plastic skin, airbrushed, cgi, cartoon, text, watermarks.""",

    "3_desert_oasis": """Professional photo: Side-by-side diptych showing front and back views of stunning woman.

SUBJECT: Beautiful 21-year-old woman with long sleek jet black hair. Smooth bronze tan. Extremely voluptuous hourglass figure with massive bust, tiny waist, wide hips, thick thighs, huge round glutes.

FACE: Clearly visible, sultry deep brown eyes, sharp cheekbones, full lips. Confident expression.

BIKINI: White bandeau bikini top with crimson red elephant pattern. Matching high-waisted bottoms. (Reference provided in images)

POSE:
- LEFT: Front view in desert oasis, confident pose, palm trees and luxury architecture behind
- RIGHT: Back view, hair down, curves against exotic backdrop

ENVIRONMENT: Luxury desert oasis Dubai/Middle East. Modern architecture with gold accents. Palm trees. Turquoise pool. Sandy dunes background. Arabic details. Bright sunny day.

LIGHTING: Bright desert sunlight, high contrast, dramatic shadows, intense blue sky.

STYLE: Luxury destination photography, 8K, ultra-sharp, professional.

CRITICAL: Face visible, Middle Eastern luxury aesthetic, desert/oasis clear, realistic skin, NO text.

AVOID: tattoos, plastic skin, airbrushed, cgi, cartoon, text, watermarks.""",

    "4_jungle_waterfall": """Professional photo: Side-by-side diptych showing front and back views of stunning woman.

SUBJECT: Beautiful 21-year-old woman with long sleek jet black hair, slightly wet from mist. Smooth bronze tan. Extremely voluptuous hourglass figure with massive bust, tiny waist, wide hips, thick thighs, huge round glutes.

FACE: Clearly visible, sultry deep brown eyes, sharp cheekbones, full lips. Confident expression.

BIKINI: White bandeau bikini top with crimson red elephant pattern. Matching high-waisted bottoms. Slightly glistening from mist. (Reference provided in images)

POSE:
- LEFT: Front view on rocks near waterfall, hair slightly wet, dramatic waterfall behind
- RIGHT: Back view, hair wet down back, rushing water background

ENVIRONMENT: Lush tropical jungle with massive waterfall. Dense green foliage, tropical plants, moss rocks. Crystal water cascading. Mist in air. Dramatic lighting through canopy.

LIGHTING: Dramatic natural lighting through jungle, soft diffused light with bright highlights from water.

STYLE: Adventure travel photography, 8K, ultra-sharp, professional.

CRITICAL: Face visible, waterfall prominent, jungle environment, realistic dewy skin, NO text.

AVOID: tattoos, plastic skin, airbrushed, cgi, cartoon, text, watermarks, fake waterfall."""
}

def generate_location(location_name: str, prompt: str):
    """Generate image for one exotic location"""
    print(f"\n{'='*60}")
    print(f"GENERATING: {location_name.replace('_', ' ').title()}")
    print(f"{'='*60}")

    try:
        # Run nano-banana-pro with image references
        print("Calling Replicate (google/nano-banana-pro)...")

        output = replicate.run(
            "google/nano-banana-pro",
            input={
                "prompt": prompt,
                "image_input": [
                    open(BROOKE_BASE, "rb"),
                    open(BIKINI_REF, "rb")
                ],
                "aspect_ratio": "16:9",
                "size": "2K"
            }
        )

        # Download and save image
        if output:
            # output is typically a URL or list of URLs
            image_url = output[0] if isinstance(output, list) else output

            print(f"Downloading image...")
            response = requests.get(image_url)

            output_path = OUTPUT_DIR / f"{location_name}.jpeg"
            with open(output_path, 'wb') as f:
                f.write(response.content)

            file_size = output_path.stat().st_size / (1024 * 1024)
            print(f"✓ Saved: {output_path}")
            print(f"  Size: {file_size:.2f} MB")
            return True
        else:
            print("✗ No output generated")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Generate all 4 exotic location images"""
    print("="*60)
    print("BROOKE - EXOTIC LOCATIONS")
    print("="*60)
    print(f"Model: google/nano-banana-pro")
    print(f"Reference images:")
    print(f"  - Brooke: {BROOKE_BASE}")
    print(f"  - Bikini: {BIKINI_REF}")
    print(f"\nGenerating 4 locations...")

    success_count = 0

    for location_name, prompt in LOCATIONS.items():
        if generate_location(location_name, prompt):
            success_count += 1

        # Wait between generations
        if location_name != list(LOCATIONS.keys())[-1]:
            print("\nWaiting 5 seconds...")
            import time
            time.sleep(5)

    print("\n" + "="*60)
    print(f"COMPLETE! {success_count}/{len(LOCATIONS)} locations generated")
    print("="*60)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("\nGenerated:")
    for location_name in LOCATIONS.keys():
        print(f"  - {location_name}.jpeg")

if __name__ == "__main__":
    main()
