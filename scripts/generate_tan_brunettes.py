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
output_dir = Path(f"tan_brunettes_{batch_id}")
output_dir.mkdir(exist_ok=True)

# Tan brunette variations with detailed natural features
variations = [
    {
        "name": "01_petite_large_chest_huge_bubble_butt",
        "description": "Petite brunette with deep bronze tan. Large perky chest. Huge round bubble butt. Thick thighs. Beautiful face with confident smile."
    },
    {
        "name": "02_average_large_chest_big_round_butt",
        "description": "Athletic brunette with rich bronze tan. Large full chest. Big round lifted bubble butt. Toned body. Beautiful face with bright smile."
    },
    {
        "name": "03_tall_large_chest_massive_shelf_butt",
        "description": "Tall brunette with deep mahogany tan. Large chest. Massive protruding shelf butt. Very thick lower body. Stunning face."
    },
    {
        "name": "04_short_athletic_medium_chest_firm_bubble_butt",
        "description": "Short athletic brunette with warm bronze tan. Medium perky chest. Firm lifted bubble butt. Toned muscular legs. Pretty face with confident expression."
    },
    {
        "name": "05_average_extra_large_chest_heart_shaped_bubble_butt",
        "description": "Voluptuous brunette with deep bronze tan. Extra large chest with cleavage. Huge heart-shaped bubble butt. Thick curvy body. Beautiful face with happy smile."
    },
    {
        "name": "06_petite_full_chest_wide_bubble_butt",
        "description": "Petite brunette with golden bronze tan. Full perky chest. Very wide bubble butt with wide hips. Thick lower body. Beautiful face."
    }
]

def create_prompt(var):
    """Simple natural description"""
    prompt = f"""Side-by-side reference image. LEFT: Front view. RIGHT: Back view.

{var['description']}

Young woman (20-25 years old). Long dark brown hair. Dark brown eyes. Wearing black triangle bikini top and black Brazilian-cut string bikini bottoms.

Standing in backyard patio. White house siding and green grass with tropical plants in background.

Camera positioned 8-10 feet away showing full body head to toe. Eye-level angle. Face clearly visible with details. Natural outdoor lighting. Professional photography. 16:9 format.

Photorealistic. Natural skin texture. Beautiful clear face."""

    return prompt

# Generate variations
print(f"Generating Tan Brunettes Batch: {batch_id}")
print(f"Output: {output_dir}")
print(f"Variations: {len(variations)}\n")

for idx, var in enumerate(variations, 1):
    print(f"{'='*70}")
    print(f"[{idx}/{len(variations)}] {var['name']}")
    print(f"{'='*70}")

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

        for part in response.parts:
            if image := part.as_image():
                filepath = output_dir / f"{var['name']}.png"
                image.save(filepath)
                print(f"✓ Saved: {filepath}\n")

                # Save prompt
                prompt_file = output_dir / f"{var['name']}_prompt.txt"
                with open(prompt_file, 'w') as f:
                    f.write(prompt_text)

    except Exception as e:
        print(f"✗ Error: {e}\n")

print(f"{'='*70}")
print(f"COMPLETE - Check: {output_dir}")
print(f"{'='*70}")
