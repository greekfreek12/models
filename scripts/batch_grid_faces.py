#!/usr/bin/env python3
"""
BATCH GRID FACE GENERATION
Generate 6 model faces in ONE 2x3 grid image for quick review
"""

from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Load batch config
with open('scripts/batch_hot_blondes_brunettes.json', 'r') as f:
    models = json.load(f)

# Build grid prompt with all 6 models
panel_descriptions = []
for i, model in enumerate(models):
    panel_num = i + 1
    panel_desc = f"""
PANEL {panel_num} - {model['model_name'].upper()}:
Age {model['age']}, {model['ethnicity']}
- Face: {model['face_shape']}
- Eyes: {model['eye_color']}, {model['eye_shape']}
- Lips: {model['lip_description']}
- Hair: {model['hair_color']}, {model['hair_length']}, {model['hair_texture']}
- Skin: {model['skin_tone']}
- Vibe: {model['vibe']}
"""
    panel_descriptions.append(panel_desc)

GRID_PROMPT = f"""Generate a 2x3 GRID (6 panels) showing 6 DIFFERENT BEAUTIFUL WOMEN.

=== GRID LAYOUT - 2x3 (6 PANELS) ===

Create ONE image with 6 panels arranged in 2 rows and 3 columns.
Each panel is a professional headshot portrait of a different woman.

ROW 1:
- Panel 1 (Top Left)
- Panel 2 (Top Center)
- Panel 3 (Top Right)

ROW 2:
- Panel 4 (Bottom Left)
- Panel 5 (Bottom Center)
- Panel 6 (Bottom Right)

=== SPECIFICATIONS FOR EACH PANEL ===

{''.join(panel_descriptions)}

=== CONSISTENT ACROSS ALL PANELS ===

CAMERA & FRAMING (ALL PANELS):
- 85mm portrait lens at f/1.8
- Eye level, straight on, 3-4 feet distance
- FROM NECK UP TO TOP OF HEAD ONLY
- Head fills frame, face centered
- Looking directly at camera with warm genuine smile
- Thin white borders between panels

LIGHTING & STYLE (ALL PANELS):
- Natural golden hour daylight
- Soft blur background
- Minimal natural makeup
- Simple casual top
- Professional headshot composition

CRITICAL SKIN TEXTURE (ALL PANELS):
- Natural skin texture with VISIBLE PORES
- Slight imperfections present (natural beauty marks, subtle texture)
- Real human skin, NOT AI-smoothed
- NO beauty filter applied
- NO artificial smoothing or perfection
- This is real people, not magazine-perfect

=== QUALITY REQUIREMENTS ===

BEAUTY LEVEL:
- Each woman is attractive with model-like features
- Large expressive eyes, full natural lips (not exaggerated)
- Defined cheekbones and bone structure
- Beautiful but realistic and believable as real people
- Balance between attractive and natural

TECHNICAL:
- 16:9 aspect ratio for grid layout
- High resolution (2K or 8K)
- Each panel is equally sized
- Clean grid with thin borders
- 6 distinct women, each unique and beautiful

=== FINAL REMINDER ===

This is ONE image containing 6 separate headshot portraits of 6 DIFFERENT women.
Each woman should match her specified features above.
All must have natural skin texture with visible pores - realistic beauty, not AI perfection.
Clean professional grid layout with 6 equally-sized panels.

Generate a stunning contact sheet of 6 beautiful, realistic women.
"""

def generate_grid():
    """Generate grid with all 6 model faces"""

    print(f"\n{'='*60}")
    print(f"BATCH GRID FACE GENERATION")
    print(f"{'='*60}")
    print(f"Generating 6 model faces in ONE 2x3 grid image")
    print(f"")
    for i, model in enumerate(models):
        print(f"  Panel {i+1}: {model['model_name']} - {model['vibe']}")
    print(f"\nGenerating grid...")
    print(f"Using Gemini Pro (gemini-3-pro-image-preview)")
    print(f"\nThis may take 90-120 seconds...\n")

    output_path = "models/batch_grid_6_faces.png"

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=GRID_PROMPT,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="2K"
                )
            )
        )

        # Save generated grid
        for part in response.parts:
            if image := part.as_image():
                image.save(output_path)
                print(f"✓ SUCCESS!")
                print(f"\nGrid generated: {output_path}")
                print(f"\n{'='*60}")
                print(f"REVIEW THE GRID:")
                print(f"{'='*60}")
                print(f"One image with 6 model faces")
                print(f"Tell me which panels/models you like")
                print(f"I'll generate full reference sets for approved models\n")
                return output_path

        print("❌ Error: No image generated in response")
        return None

    except Exception as e:
        print(f"❌ Error generating image: {str(e)}")
        return None

if __name__ == "__main__":
    generate_grid()
