#!/usr/bin/env python3
"""Generate V2 grids using V1 as reference (image-to-image)."""
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

V2_IMPROVEMENTS = {
    "Alabama": {
        "v1_reference": "bikinis/Alabama/design_grids/alabama_designs_20251227_211539.jpg",
        "improvements": """Keep the EXACT same grid layout and quality as the reference image.

SPECIFIC CHANGES:
1. Houndstooth Classic (top left) - Keep EXACTLY as is, no changes
2. Script A Logo (top middle) - Make the white A logos MUCH BIGGER and add more of them (15-20 logos instead of 5)
3. Elephant Stampede (top right) - Keep EXACTLY as is, no changes
4. Crimson Tide Waves (bottom left) - Make the waves more FUTURISTIC/geometric with holographic effect
5. Roll Tide Stripes (bottom middle) - Add GRAY color to the stripes (Crimson + Gray + White), make more elegant
6. Athletic Alabama (bottom right) - REPLACE with Big Al elephant mascot face print design

Keep everything else identical to reference."""
    },
    "Auburn": {
        "v1_reference": "bikinis/Auburn/design_grids/auburn_designs_20251227_213538.jpg",
        "improvements": """Keep the EXACT same grid layout and quality as the reference image.

SPECIFIC CHANGES:
1. War Eagle (top left) - Keep design but REMOVE any "War Eagle" text, just eagle graphics
2. Tiger Stripes (top middle) - Keep stripes but REMOVE any "Tigers" text, pure pattern
3. AU Logo (top right) - REPLACE with white colorway version of War Eagle design
4. Navy Orange Block (bottom left) - REPLACE with white colorway version of Tiger Stripes
5. Toomer's Oaks (bottom middle) - Keep but make the toilet paper streams more detailed/visible
6. Plains Stripes (bottom right) - Keep but improve the stripe proportions and balance

Keep everything else identical to reference."""
    }
}

def generate_v2_from_reference(school_name):
    """Generate V2 using V1 as reference."""
    print(f"\n{'='*60}")
    print(f"🎓 {school_name} - V2 (Image-to-Image)")
    print(f"{'='*60}")

    data = V2_IMPROVEMENTS[school_name]
    v1_img = Image.open(data['v1_reference'])

    prompt = f"""Transform this design grid with these specific improvements:

{data['improvements']}

CRITICAL: Maintain the EXACT same professional quality, style, and layout as the reference image. Only make the specific changes listed above."""

    print(f"\n🎨 Generating from V1 reference...")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[v1_img, prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="16:9",
                image_size="4K"
            )
        )
    )

    for part in response.parts:
        if img := part.as_image():
            output_dir = f"bikinis/{school_name}/design_grids"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{output_dir}/{school_name.lower()}_v2_{timestamp}.jpg"
            img.save(output_path)
            print(f"✅ Saved: {output_path}\n")
            return output_path

    print(f"❌ Failed\n")
    return None

if __name__ == "__main__":
    schools = ["Alabama", "Auburn"]

    print("🏈 V2 Design Grids - Image-to-Image from V1")

    for school in schools:
        try:
            generate_v2_from_reference(school)
        except Exception as e:
            print(f"\n❌ Error with {school}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*60)
    print("✅ V2 complete!")
    print("="*60)
