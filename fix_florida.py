#!/usr/bin/env python3
"""Generate Florida V2 with variants and improvements."""
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def generate_florida_v2():
    """Generate Florida V2 using V1 as reference."""
    v1_ref = "bikinis/Florida/design_grids/florida_designs_20251227_211603.jpg"
    ref_img = Image.open(v1_ref)

    prompt = """Transform this Florida design grid with these specific changes:

CRITICAL FORMAT:
- Show each design as a BIKINI worn on an athletic female body form
- Patterns/designs should be ON THE BIKINI FABRIC ONLY, not the background
- Clean white background behind each model
- Professional fashion catalog style with clear grid separation

KEEP + ADD VARIANTS (EXACTLY 6 designs in 3 columns x 2 rows grid):

TOP ROW (3 designs):
1. Position 1 (top left) - Gator Scales Original: KEEP design EXACTLY as is from reference. BIKINI fabric with blue/orange reptilian scale texture. Pattern on bikini only, white background.
2. Position 2 (top middle) - Gator Scales Orange Variant: CREATE NEW color swap. Same BIKINI style, same reptilian scale texture, but ORANGE primary with blue accents. Pattern on bikini fabric only.
3. Position 3 (top right) - Block F Athletic Orange Variant: CREATE NEW color swap. ORANGE athletic crop top and bottom with BLUE "F" logo and BLUE "GATORS" text on waistband. Design on bikini only.

BOTTOM ROW (3 designs):
4. Position 4 (bottom left) - Gator Head Logo Original: KEEP design EXACTLY as is from reference. Orange BIKINI fabric with blue Florida Gator head logos printed on it. Design on bikini only.
5. Position 5 (bottom center) - Gator Head Logo Blue Variant: CREATE NEW color swap. BLUE BIKINI fabric with ORANGE Florida Gator head logos printed on it. Pattern on bikini only.
6. Position 6 (bottom right) - Block F Athletic Original: KEEP design EXACTLY as is from reference. Blue athletic crop top BIKINI with WHITE "F" and "GATORS" text. Design on bikini only.

TOTAL: EXACTLY 6 designs, NO MORE, NO LESS. 3x2 grid layout.

REMOVE COMPLETELY:
- Swamp Fever (old top right)
- Jersey Stripes (old bottom left)
- Chomp Chomp (old bottom middle)

CRITICAL:
- Each design is a BIKINI shown on a body form
- Patterns/prints are ON THE BIKINI FABRIC, not floating or in background
- Maintain EXACT same quality and professional style as reference image
- Clean white backgrounds for each cell"""

    print("🎨 Generating Florida V2 with variants...")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[ref_img, prompt],
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
            output_dir = "bikinis/Florida/design_grids"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{output_dir}/florida_v2_final_{timestamp}.jpg"
            img.save(output_path)
            print(f"✅ Saved: {output_path}")
            return output_path

    print("❌ Failed")
    return None

if __name__ == "__main__":
    print("🐊 Florida V2 Generation\n")
    generate_florida_v2()
    print("\n✅ Done!")
