#!/usr/bin/env python3
"""Generate Poolside_Classic colorways - same combos as GameDay_Luxe."""
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

BIKINI_NAME = "Poolside_Classic"
REFERENCE = "bikini_downloads/_thebikinibeauty_/3787441319040610369_71861451332.jpg"

# Same 13 colorways from GameDay_Luxe
COLORWAYS = [
    {"school": "Alabama", "name": "Crimson_Gray", "desc": "Alabama Crimson + Gray", "primary": "#9E1B32", "secondary": "#828A8F"},
    {"school": "Alabama", "name": "Crimson_White", "desc": "Alabama Crimson + White", "primary": "#9E1B32", "secondary": "#FFFFFF"},
    {"school": "Tennessee", "name": "Orange_White", "desc": "Tennessee Orange + White", "primary": "#FF8200", "secondary": "#FFFFFF"},
    {"school": "Florida", "name": "Blue_Orange", "desc": "Florida Blue + Orange", "primary": "#0021A5", "secondary": "#FA4616"},
    {"school": "Florida", "name": "Orange_Blue", "desc": "Florida Orange + Blue", "primary": "#FA4616", "secondary": "#0021A5"},
    {"school": "Ole_Miss", "name": "Red_PowderBlue", "desc": "Ole Miss Red + Powder Blue", "primary": "#CE1126", "secondary": "#006BA6"},
    {"school": "Ole_Miss", "name": "PowderBlue_Red", "desc": "Ole Miss Powder Blue + Red", "primary": "#006BA6", "secondary": "#CE1126"},
    {"school": "Georgia", "name": "Red_Black", "desc": "Georgia Red + Black", "primary": "#BA0C2F", "secondary": "#000000"},
    {"school": "Georgia", "name": "Black_Red", "desc": "Georgia Black + Red", "primary": "#000000", "secondary": "#BA0C2F"},
    {"school": "LSU", "name": "Purple_Gold", "desc": "LSU Purple + Gold", "primary": "#461D7C", "secondary": "#FDD023"},
    {"school": "LSU", "name": "Gold_Purple", "desc": "LSU Gold + Purple", "primary": "#FDD023", "secondary": "#461D7C"},
    {"school": "Vanderbilt", "name": "Gold_Black", "desc": "Vanderbilt Gold + Black", "primary": "#866D4B", "secondary": "#000000"},
    {"school": "Vanderbilt", "name": "Black_Gold", "desc": "Vanderbilt Black + Gold", "primary": "#000000", "secondary": "#866D4B"},
]

def generate_colorway(reference_path, colorway):
    """Generate single colorway image."""
    prompt = f"""Transform this bikini to these EXACT colors:

PRIMARY COLOR (main fabric - light pink): {colorway['primary']}
SECONDARY COLOR (trim/outline - hot pink): {colorway['secondary']}

Keep EVERYTHING else identical:
- Same exact style and cut
- Same model and pose
- Same background and lighting
- ONLY change the bikini colors

Professional fashion photography, 4K quality."""

    ref_img = Image.open(reference_path)

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[ref_img, prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="3:4",
                image_size="4K"
            )
        )
    )

    for part in response.parts:
        if img := part.as_image():
            return img
    return None

def create_description(path, colorway):
    """Create description file."""
    content = f"""{BIKINI_NAME} - {colorway['desc']}

School: {colorway['school']}
Style: {BIKINI_NAME}
Colorway: {colorway['name'].replace('_', ' ')}

Colors:
- Primary (main fabric): {colorway['primary']}
- Secondary (trim/outline): {colorway['secondary']}

Description:
Premium triangle top bikini with tie-side bottom in official {colorway['school']} team colors.
Classic silhouette with thin straps and moderate coverage.
{colorway['desc']} colorway.

Generated: {datetime.now().strftime('%Y-%m-%d')}
"""
    with open(path, 'w') as f:
        f.write(content)

def main():
    print(f"\n{'='*60}")
    print(f"Generating {BIKINI_NAME} Colorways")
    print(f"{'='*60}\n")

    # Setup directories
    base = f"bikinis/universal/{BIKINI_NAME}"
    teams_dir = f"{base}/teams"
    os.makedirs(teams_dir, exist_ok=True)

    # Copy reference
    ref_dst = f"{base}/reference.jpg"
    Image.open(REFERENCE).save(ref_dst)
    print(f"✓ Reference saved\n")

    # Generate each colorway
    for i, colorway in enumerate(COLORWAYS, 1):
        print(f"[{i}/13] {colorway['school']} - {colorway['name'].replace('_', ' ')}")

        img = generate_colorway(REFERENCE, colorway)
        if img:
            # Save image
            img_path = f"{teams_dir}/{colorway['school']}_{colorway['name']}.jpg"
            img.save(img_path)

            # Save description
            txt_path = f"{teams_dir}/{colorway['school']}_{colorway['name']}.txt"
            create_description(txt_path, colorway)

            print(f"  ✓ Saved\n")
        else:
            print(f"  ❌ Failed\n")

    print(f"{'='*60}")
    print(f"✅ Complete! Saved to:")
    print(f"   {teams_dir}/")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
