#!/usr/bin/env python3
"""Fix specific designs - V3 targeted fixes."""
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def fix_alabama_roll_tide_stripes():
    """Fix Roll Tide Stripes - correct colors and enhance to championship version."""
    v2_ref = "bikinis/Alabama/design_grids/alabama_v2_final_20251227_223201.jpg"
    ref_img = Image.open(v2_ref)

    prompt = """Fix the Roll Tide Stripes design (bottom middle of grid):

CRITICAL COLOR CORRECTION:
- Use ONLY Alabama official colors: Crimson (#9E1B32), Gray (#828A8F), White (#FFFFFF)
- Create ELEGANT diagonal stripes using ALL THREE COLORS (Crimson, Gray, White)
- Thin refined stripes at 45-degree angle
- Add subtle shimmer/metallic finish for championship quality
- Triangle top and cheeky bottom
- Sophisticated preppy aesthetic

UPGRADE TO CHAMPIONSHIP VERSION:
- Premium fabric appearance with slight sheen
- More refined stripe proportions
- Elegant color balance between crimson, gray, and white

Keep all other designs in the grid exactly as they are."""

    print("🔧 Fixing Alabama Roll Tide Stripes (championship version)...")

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
            output_dir = "bikinis/Alabama/design_grids"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{output_dir}/alabama_v3_final_{timestamp}.jpg"
            img.save(output_path)
            print(f"✅ Saved: {output_path}")
            return output_path

    print("❌ Failed")
    return None

def fix_auburn_toomers_realistic():
    """Fix Toomer's Oaks - toilet paper must be attached to tree branches, not floating."""
    v2_ref = "bikinis/Auburn/design_grids/auburn_v2_fixed_20251227_223232.jpg"
    ref_img = Image.open(v2_ref)

    prompt = """Fix the Toomer's Oaks design (bottom middle of grid):

CRITICAL TOILET PAPER FIXES:
- Toilet paper MUST be ATTACHED to tree branches
- Toilet paper streams should FLOW NATURALLY from the branches
- Make the toilet paper look like it's DRAPED over and HANGING from the oak tree
- DO NOT have floating toilet paper disconnected from the design
- Show realistic toilet paper texture (white with subtle folds/wrinkles)
- Oak tree should be SMALLER and more proportional to bikini
- Better tree branch detail showing where TP is attached

This is the iconic Auburn Toomer's Corner tradition - toilet paper thrown over oak trees.

Keep all other designs in the grid exactly as they are."""

    print("🔧 Fixing Auburn Toomer's Oaks (attached toilet paper)...")

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
            output_dir = "bikinis/Auburn/design_grids"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{output_dir}/auburn_v3_fixed_{timestamp}.jpg"
            img.save(output_path)
            print(f"✅ Saved: {output_path}")
            return output_path

    print("❌ Failed")
    return None

def remove_auburn_duplicate_stripe():
    """Remove duplicate stripe design, keep only the better Plains Stripes."""
    v3_ref = "bikinis/Auburn/design_grids/auburn_v3_fixed_{timestamp}.jpg"

    # This will be run after the Toomer's fix, using the latest v3 file
    import glob
    auburn_files = sorted(glob.glob("bikinis/Auburn/design_grids/auburn_v3_*.jpg"))
    if not auburn_files:
        print("❌ No v3 Auburn file found")
        return None

    v3_ref = auburn_files[-1]
    ref_img = Image.open(v3_ref)

    prompt = """Remove duplicate stripe design from this Auburn grid:

KEEP THESE 5 DESIGNS:
1. War Eagle Navy (top left)
2. War Eagle White (top middle)
3. Tiger Stripes Navy (top right)
4. Tiger Stripes White (bottom left)
5. Toomer's Oaks (bottom middle)

REMOVE: Plains Stripes (bottom right) - we don't need two stripe versions

Rearrange to show only 5 unique designs in a clean grid layout (2x3 or 3x2).
Keep the exact same quality and style as reference."""

    print("🔧 Removing Auburn duplicate stripe design...")

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
            output_dir = "bikinis/Auburn/design_grids"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{output_dir}/auburn_v3_final_{timestamp}.jpg"
            img.save(output_path)
            print(f"✅ Saved: {output_path}")
            return output_path

    print("❌ Failed")
    return None

if __name__ == "__main__":
    print("🔧 V3 Targeted Fixes\n")

    # Fix Alabama stripes
    alabama_result = fix_alabama_roll_tide_stripes()
    print()

    # Fix Auburn toilet paper
    auburn_result = fix_auburn_toomers_realistic()
    print()

    # Remove Auburn duplicate stripe
    if auburn_result:
        remove_auburn_duplicate_stripe()
        print()

    print("\n✅ Done!")
