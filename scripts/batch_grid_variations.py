#!/usr/bin/env python3
"""
Generate grid of 5 variations based on the face the user liked
"""

from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Load variations config
with open('scripts/batch_5_variations.json', 'r') as f:
    models = json.load(f)

# Build grid prompt with all 5 variations
panel_descriptions = []
for i, model in enumerate(models):
    panel_num = i + 1
    panel_desc = f"""
PANEL {panel_num}:
- Face: {model['face_shape']}
- Eyes: {model['eye_color']}, {model['eye_shape']}
- Lips: {model['lip_description']}
- Hair: {model['hair_color']}, {model['hair_length']}, {model['hair_texture']}
- Skin: {model['skin_tone']}
- Vibe: {model['vibe']}
"""
    panel_descriptions.append(panel_desc)

GRID_PROMPT = f"""Generate a 2x3 GRID (5 panels with 1 empty) showing 5 VARIATIONS of a beautiful woman.

=== GRID LAYOUT ===

Create ONE image with 5 headshot portraits arranged in a grid.
Row 1: 3 panels
Row 2: 2 panels (leave right spot empty or fill background)

=== BASE FEATURES (CONSISTENT ACROSS ALL 5) ===

All 5 women share these core features:
- Face structure: Oval with soft defined features, natural beauty
- Face shape and proportions are similar
- Lip fullness: Full natural lips, soft and defined (same size/shape)
- Overall bone structure and facial proportions similar
- Same warm, approachable, natural beauty vibe

=== WHAT VARIES (DIFFERENT IN EACH) ===

{''.join(panel_descriptions)}

=== CAMERA & FRAMING (ALL PANELS) ===

- 85mm portrait lens at f/1.8
- Eye level, straight on, 3-4 feet distance
- FROM NECK UP TO TOP OF HEAD ONLY
- Head fills frame, face centered
- Looking directly at camera with warm genuine smile
- Thin white borders between panels
- Natural golden hour daylight
- Soft blur background
- Minimal natural makeup
- Simple casual top

=== CRITICAL SKIN TEXTURE (ALL PANELS) ===

- Natural skin texture with VISIBLE PORES
- Slight imperfections present (natural beauty marks, subtle texture)
- Real human skin, NOT AI-smoothed
- NO beauty filter applied
- NO artificial smoothing or perfection

=== BEAUTY REQUIREMENTS ===

- Attractive with natural model-like features
- Large expressive eyes, full natural lips (not exaggerated)
- Defined cheekbones and bone structure
- Beautiful but realistic and believable as real people
- All 5 should look like they could be related or variations of the same person
- Natural, approachable beauty

Generate 5 beautiful variations with consistent facial structure but different coloring/styling.
"""

def generate_grid():
    """Generate grid with 5 face variations"""

    print(f"\n{'='*60}")
    print(f"GENERATING 5 VARIATIONS")
    print(f"{'='*60}")
    print(f"Based on the face you liked (bottom middle)")
    print(f"Creating 5 variations with different:")
    print(f"  - Eye colors")
    print(f"  - Hair colors/styles")
    print(f"  - Tan levels")
    print(f"\nKeeping consistent:")
    print(f"  - Face shape and structure")
    print(f"  - Lip size/shape")
    print(f"  - Overall vibe")
    print(f"\nGenerating grid...")
    print(f"This may take 90-120 seconds...\n")

    output_path = "models/variations_grid_5_faces.png"

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
                print(f"\nVariations grid: {output_path}")
                print(f"\n{'='*60}")
                print(f"REVIEW:")
                print(f"{'='*60}")
                print(f"5 variations of the face you liked")
                print(f"Different eye/hair colors, same facial structure")
                print(f"Tell me which ones you want to keep\n")
                return output_path

        print("❌ Error: No image generated in response")
        return None

    except Exception as e:
        print(f"❌ Error generating image: {str(e)}")
        return None

if __name__ == "__main__":
    generate_grid()
