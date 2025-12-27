#!/usr/bin/env python3
from google import genai
from google.genai import types
import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Output directory
batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = Path(f"reference_batch_{batch_id}")
output_dir.mkdir(exist_ok=True)

# Define diverse combinations
variations = [
    {
        "name": "01_short_slim_bigboobs_bigbutt_blonde",
        "hair": "Long straight blonde hair",
        "eyes": "Blue eyes",
        "height": "5'2\" (Short/Petite)",
        "weight": "125 lbs",
        "body": "Slim athletic build with enhanced curves",
        "bust": "Large 34D bust - full and perky",
        "butt": "Large round glutes - prominent and lifted",
        "measurements": "34D - 24\" - 36\""
    },
    {
        "name": "02_average_smallboobs_bigbutt_brunette",
        "hair": "Long wavy dark brown hair",
        "eyes": "Hazel eyes",
        "height": "5'6\" (Average)",
        "weight": "140 lbs",
        "body": "Pear-shaped with emphasis on lower body",
        "bust": "Small 32B bust - natural and perky",
        "butt": "Very large round glutes - thick and prominent",
        "measurements": "32B - 26\" - 38\""
    },
    {
        "name": "03_tall_bigboobs_bigbutt_redhead",
        "hair": "Long wavy red hair",
        "eyes": "Green eyes",
        "height": "5'9\" (Tall)",
        "weight": "155 lbs",
        "body": "Athletic hourglass with strong curves",
        "bust": "Large 36D bust - full and natural",
        "butt": "Large round glutes - athletic and firm",
        "measurements": "36D - 26\" - 37\""
    },
    {
        "name": "04_short_curvy_medboobs_bigbutt_black",
        "hair": "Long straight black hair",
        "eyes": "Dark brown eyes",
        "height": "5'3\" (Short)",
        "weight": "145 lbs",
        "body": "Short and thick with heavy lower body",
        "bust": "Medium 34C bust - natural",
        "butt": "Very large glutes - thick and round",
        "measurements": "34C - 27\" - 39\""
    },
    {
        "name": "05_average_athletic_smallboobs_firmbutt_blonde",
        "hair": "Long blonde hair with highlights",
        "eyes": "Light blue eyes",
        "height": "5'7\" (Average)",
        "weight": "135 lbs",
        "body": "Athletic and toned overall",
        "bust": "Small 32B bust - athletic and perky",
        "butt": "Large firm glutes - athletic and lifted",
        "measurements": "32B - 25\" - 35\""
    },
    {
        "name": "06_short_thickthighs_smallboobs_bigbutt_brunette",
        "hair": "Shoulder-length brown hair",
        "eyes": "Brown eyes",
        "height": "5'4\" (Short)",
        "weight": "150 lbs",
        "body": "Bottom-heavy with very thick thighs",
        "bust": "Small 32A bust - petite",
        "butt": "Extra large glutes - very thick and round",
        "measurements": "32A - 26\" - 40\""
    },
    {
        "name": "07_tall_slim_bigboobs_roundbutt_dirty_blonde",
        "hair": "Long dirty blonde hair",
        "eyes": "Gray-blue eyes",
        "height": "5'8\" (Tall)",
        "weight": "140 lbs",
        "body": "Tall and slim with strategic curves",
        "bust": "Large 34DD bust - full",
        "butt": "Large round glutes - perky and lifted",
        "measurements": "34DD - 25\" - 36\""
    },
    {
        "name": "08_average_hourglass_medboobs_bigbutt_auburn",
        "hair": "Long auburn/red-brown hair",
        "eyes": "Hazel-green eyes",
        "height": "5'5\" (Average)",
        "weight": "145 lbs",
        "body": "Classic hourglass shape",
        "bust": "Medium 34C bust - balanced",
        "butt": "Large round glutes - proportional curves",
        "measurements": "34C - 24\" - 36\""
    }
]

def create_prompt(var):
    """Create detailed prompt for each variation"""
    prompt = {
        "task": {
            "type": "character_reference_sheet",
            "layout": "Side-by-side Diptych (Split Screen). Two full-body images of the same woman combined into one wide frame.",
            "composition": "LEFT PANEL: Full Body Front View. RIGHT PANEL: Full Body Back View (turned 180 degrees)."
        },
        "subject": {
            "demographics": f"Young adult female (20-25 years old). Height {var['height']}. Weight {var['weight']}. {var['hair']}. {var['eyes']}. No tattoos. No piercings.",
            "facial_features": "Naturally pretty face. Confident and happy expression. Healthy complexion.",
            "body_type": {
                "overall": var['body'],
                "measurements": f"Visual translation: {var['measurements']}",
                "bust_details": var['bust'],
                "glute_details": var['butt']
            },
            "skin_details": "Natural skin texture. Smooth with realistic softness."
        },
        "apparel": {
            "top": "Black sliding triangle bikini top.",
            "bottom": "Matte black string bikini bottoms. Brazilian cut.",
            "accessories": "NONE. No necklace. No earrings. Clean, natural look."
        },
        "pose": {
            "left_panel_front": "Standing upright facing camera, hands on hips.",
            "right_panel_back": "Standing upright facing away, showcasing physique."
        },
        "environment": {
            "location": "Backyard patio interface between tiled area and grass.",
            "background_continuity": "White weatherboard house siding and green artificial turf with tropical plants."
        },
        "camera": {
            "shot_type": "Wide Full-Body Shot.",
            "angle": "Eye-level.",
            "focal_length": "50mm.",
            "lighting": "Natural daylight. Even lighting."
        },
        "aspect_ratio_and_output": {
            "ratio": "16:9",
            "framing": "Wide landscape orientation."
        }
    }
    return json.dumps(prompt, indent=2)

# Generate each variation
print(f"Starting batch generation: {batch_id}")
print(f"Output directory: {output_dir}")
print(f"Generating {len(variations)} variations...\n")

for idx, var in enumerate(variations, 1):
    print(f"{'='*60}")
    print(f"[{idx}/{len(variations)}] Generating: {var['name']}")
    print(f"{'='*60}")

    prompt_text = create_prompt(var)

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt_text,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="2K"
                )
            )
        )

        # Save image
        for part in response.parts:
            if image := part.as_image():
                filepath = output_dir / f"{var['name']}.png"
                image.save(filepath)
                print(f"✓ Saved: {filepath}\n")

                # Save prompt for reference
                prompt_file = output_dir / f"{var['name']}_prompt.json"
                with open(prompt_file, 'w') as f:
                    f.write(prompt_text)

    except Exception as e:
        print(f"✗ Error: {e}\n")

print(f"{'='*60}")
print(f"BATCH COMPLETE")
print(f"{'='*60}")
print(f"Check folder: {output_dir}")
