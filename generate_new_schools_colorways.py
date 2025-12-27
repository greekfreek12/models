#!/usr/bin/env python3
"""Generate GameDay_Luxe and Poolside_Classic colorways for 4 new schools."""
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Reference images
GAMEDAY_LUXE_REF = "bikini_downloads/_thebikinibeauty_/3680166047550738239_71861451332.jpg"
POOLSIDE_CLASSIC_REF = "bikini_downloads/_thebikinibeauty_/3787441319040610369_71861451332.jpg"

# Color combinations for new schools
NEW_SCHOOL_COLORWAYS = {
    "Texas": [
        {"primary": "#BF5700", "secondary": "#FFFFFF", "name": "BurntOrange_White", "desc": "Texas Burnt Orange + White"}
    ],
    "Oklahoma": [
        {"primary": "#841617", "secondary": "#FDF9D8", "name": "Crimson_Cream", "desc": "Oklahoma Crimson + Cream"}
    ],
    "Texas_AM": [
        {"primary": "#500000", "secondary": "#FFFFFF", "name": "Maroon_White", "desc": "Texas A&M Maroon + White"}
    ],
    "Auburn": [
        {"primary": "#03244D", "secondary": "#DD550C", "name": "Navy_Orange", "desc": "Auburn Navy + Orange"},
        {"primary": "#DD550C", "secondary": "#03244D", "name": "Orange_Navy", "desc": "Auburn Orange + Navy"},
        {"primary": "#03244D", "secondary": "#FFFFFF", "name": "Navy_White", "desc": "Auburn Navy + White"},
        {"primary": "#DD550C", "secondary": "#FFFFFF", "name": "Orange_White", "desc": "Auburn Orange + White"}
    ]
}

def generate_colorway(reference_path, school, colorway, bikini_style):
    """Generate single colorway image."""
    prompt = f"""Transform this bikini to these EXACT colors:

PRIMARY COLOR (main fabric): {colorway['primary']}
SECONDARY COLOR (trim/outline): {colorway['secondary']}

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

def create_description(path, school, colorway, bikini_style):
    """Create description file."""
    content = f"""{bikini_style} - {colorway['desc']}

School: {school}
Style: {bikini_style}
Colorway: {colorway['name'].replace('_', ' ')}

Colors:
- Primary (main fabric): {colorway['primary']}
- Secondary (trim/outline): {colorway['secondary']}

Description:
Premium bikini in official {school} team colors.
{colorway['desc']} colorway.

Generated: {datetime.now().strftime('%Y-%m-%d')}
"""
    with open(path, 'w') as f:
        f.write(content)

def generate_school_colorways(school_name):
    """Generate both GameDay_Luxe and Poolside_Classic for a school."""
    print(f"\n{'='*60}")
    print(f"🎓 {school_name}")
    print(f"{'='*60}")

    colorways = NEW_SCHOOL_COLORWAYS[school_name]

    for bikini_style, ref_image in [
        ("GameDay_Luxe", GAMEDAY_LUXE_REF),
        ("Poolside_Classic", POOLSIDE_CLASSIC_REF)
    ]:
        print(f"\n  {bikini_style}:")

        for colorway in colorways:
            print(f"    [{colorway['name']}] Generating...")

            img = generate_colorway(ref_image, school_name, colorway, bikini_style)
            if img:
                # Save image
                output_dir = f"bikinis/universal/{bikini_style}/teams"
                os.makedirs(output_dir, exist_ok=True)

                img_path = f"{output_dir}/{school_name}_{colorway['name']}.jpg"
                img.save(img_path)

                # Save description
                txt_path = f"{output_dir}/{school_name}_{colorway['name']}.txt"
                create_description(txt_path, school_name, colorway, bikini_style)

                print(f"    ✓ Saved")
            else:
                print(f"    ❌ Failed")

# Main execution
if __name__ == "__main__":
    schools = ["Texas", "Oklahoma", "Texas_AM", "Auburn"]

    print("🏈 New Schools Colorway Generator")
    print("Generating GameDay_Luxe + Poolside_Classic for 4 schools\n")

    for school in schools:
        try:
            generate_school_colorways(school)
        except Exception as e:
            print(f"\n❌ Error with {school}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*60)
    print("✅ All colorways complete!")
    print("="*60)
