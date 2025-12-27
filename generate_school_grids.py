#!/usr/bin/env python3
"""Generate school bikini color grids."""
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Define color combinations for each school
SCHOOL_COMBOS = {
    "Alabama": [
        {"primary": "#9E1B32", "secondary": "#828A8F", "name": "Crimson + Gray"},
        {"primary": "#9E1B32", "secondary": "#FFFFFF", "name": "Crimson + White"}
    ],
    "Tennessee": [
        {"primary": "#FF8200", "secondary": "#58595B", "name": "Orange + Smoky"},
        {"primary": "#FF8200", "secondary": "#FFFFFF", "name": "Orange + White"}
    ],
    "Florida": [
        {"primary": "#0021A5", "secondary": "#FA4616", "name": "Blue + Orange"},
        {"primary": "#FA4616", "secondary": "#0021A5", "name": "Orange + Blue"},
        {"primary": "#0021A5", "secondary": "#FFFFFF", "name": "Blue + White"},
        {"primary": "#FA4616", "secondary": "#FFFFFF", "name": "Orange + White"}
    ],
    "Ole_Miss": [
        {"primary": "#CE1126", "secondary": "#006BA6", "name": "Red + Powder Blue"},
        {"primary": "#006BA6", "secondary": "#CE1126", "name": "Powder Blue + Red"},
        {"primary": "#CE1126", "secondary": "#FFFFFF", "name": "Red + White"},
        {"primary": "#006BA6", "secondary": "#FFFFFF", "name": "Powder Blue + White"}
    ],
    "Georgia": [
        {"primary": "#BA0C2F", "secondary": "#000000", "name": "Red + Black"},
        {"primary": "#000000", "secondary": "#BA0C2F", "name": "Black + Red"},
        {"primary": "#BA0C2F", "secondary": "#FFFFFF", "name": "Red + White"},
        {"primary": "#000000", "secondary": "#FFFFFF", "name": "Black + White"}
    ],
    "LSU": [
        {"primary": "#461D7C", "secondary": "#FDD023", "name": "Purple + Gold"},
        {"primary": "#FDD023", "secondary": "#461D7C", "name": "Gold + Purple"},
        {"primary": "#461D7C", "secondary": "#FFFFFF", "name": "Purple + White"},
        {"primary": "#FDD023", "secondary": "#FFFFFF", "name": "Gold + White"}
    ],
    "Vanderbilt": [
        {"primary": "#866D4B", "secondary": "#000000", "name": "Gold + Black"},
        {"primary": "#000000", "secondary": "#866D4B", "name": "Black + Gold"},
        {"primary": "#866D4B", "secondary": "#FFFFFF", "name": "Gold + White"},
        {"primary": "#000000", "secondary": "#FFFFFF", "name": "Black + White"}
    ]
}

def generate_school_grid(school_name, reference_image_path):
    """Generate ONE grid image with all color combos for a school."""
    print(f"\n{'='*60}")
    print(f"🎓 {school_name}")
    print(f"{'='*60}")

    combos = SCHOOL_COMBOS[school_name]
    num_combos = len(combos)

    print(f"Combinations: {num_combos}")
    for combo in combos:
        print(f"  - {combo['name']}: {combo['primary']} + {combo['secondary']}")

    # Determine grid layout
    if num_combos == 2:
        grid_layout = "1x2 (1 row, 2 columns)"
        aspect_ratio = "16:9"
    else:  # 4 combos
        grid_layout = "2x2 (2 rows, 2 columns)"
        aspect_ratio = "1:1"

    # Build combo descriptions for prompt
    combo_text = "\n".join([
        f"{i+1}. Main fabric: {c['primary']}, Trim/outline: {c['secondary']}"
        for i, c in enumerate(combos)
    ])

    # Load reference image
    ref_img = Image.open(reference_image_path)

    # Create prompt
    prompt = f"""Create a professional product catalog grid showing {num_combos} bikini color variations in a {grid_layout} layout.

REFERENCE: Use the EXACT style, cut, and design of this bikini. Only change the colors.

COLOR COMBINATIONS (EXACT HEX COLORS):
{combo_text}

REQUIREMENTS:
- EXACT same minimal triangle bikini style as reference (same cut, coverage, straps)
- Same athletic blonde model, same pose and setting
- Each grid cell = ONE bikini with specified colors
- Professional fashion photography, outdoor poolside
- Natural lighting, same background style
- Clear grid layout with separation between cells

Generate all {num_combos} variations in ONE grid image."""

    print(f"\n🎨 Generating {grid_layout} grid...")

    # Generate with Gemini
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[ref_img, prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size="4K"
            )
        )
    )

    # Save output
    for part in response.parts:
        if img := part.as_image():
            output_dir = f"bikinis/{school_name}/grids"
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{output_dir}/{school_name.lower()}_grid_{timestamp}.jpg"

            img.save(output_path)
            print(f"✅ Saved: {output_path}\n")
            return output_path

    print(f"❌ Failed\n")
    return None

# Main execution
if __name__ == "__main__":
    reference_image = "bikini_downloads/_thebikinibeauty_/3680166047550738239_71861451332.jpg"

    # Remaining schools
    all_schools = ["Georgia", "Vanderbilt"]

    print("🏈 SEC School Bikini Grid Generator")
    print(f"Reference: {reference_image}\n")

    for school in all_schools:
        try:
            generate_school_grid(school, reference_image)
        except Exception as e:
            print(f"❌ Error with {school}: {e}\n")
            import traceback
            traceback.print_exc()

    print("\n" + "="*60)
    print("✅ All schools complete!")
    print("="*60)
