#!/usr/bin/env python3
"""
Generate Bailey full body back view 1x2 grid with 2 butt size variations
"""

from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Load face reference
face_ref_path = "lsu_blonde_keeper_1.jpg"
print(f"Loading reference image: {face_ref_path}")
face_ref = PILImage.open(face_ref_path)
print(f"✓ Loaded\n")

PROMPT = f"""Generate a 1x2 GRID (2 panels side by side) of the SAME WOMAN from the reference image.

REFERENCE IMAGE: This is Bailey. Use her face for both panels.

=== GRID LAYOUT - 1x2 (2 PANELS SIDE BY SIDE) ===

Create ONE image with 2 panels arranged horizontally (left and right).
Both panels show the SAME WOMAN (Bailey from reference) in the SAME POSE and FRAMING.

=== CONSISTENT ACROSS BOTH PANELS ===

IDENTITY (SAME IN BOTH):
- Same woman from reference image - Bailey
- Same face, exact facial features
- Same blonde hair with golden highlights, long beachy waves
- Same blue eyes
- Same really tan skin, golden bronze tone
- Same natural skin texture
- Same age (19-20 years old)

CAMERA & FRAMING (IDENTICAL IN BOTH):
- Full body shot from head to feet (or close to feet)
- Back view - showing her full backside
- She's looking back over her shoulder at the camera (so we see her face)
- Standing naturally, confident pose
- Show her full back, glutes, and legs clearly

SETTING (SAME IN BOTH):
- Beach setting, ocean in background
- Golden hour lighting, warm and flattering
- Soft blur background
- Natural outdoor beach

POSE (SAME IN BOTH):
- Standing facing away from camera
- Looking back over her shoulder with soft smile
- One hand on hip or relaxed at side
- Natural confident energy
- Full backside visible
- Same pose in both panels

OUTFIT (SAME IN BOTH):
- White bikini (triangle top + bikini bottoms)
- Simple and clean

BODY (SAME IN BOTH):
- Athletic hourglass build
- Narrow waist, toned midsection
- Long legs
- Athletic shoulders
- Overall fit and toned physique

SKIN TEXTURE (SAME IN BOTH):
- Natural skin texture with visible pores
- Realistic, not smoothed
- Natural beauty marks okay

=== WHAT'S DIFFERENT BETWEEN PANELS ===

ONLY difference: Glute/butt size and shape description

PANEL 1 (LEFT):
- Glutes: Full and round, shapely natural butt, toned and lifted, athletic bubble butt, prominent and attractive

PANEL 2 (RIGHT):
- Glutes: Very large and round, exceptionally full and lifted, elite bubble butt, dramatic curve and projection, very prominent feature, striking

=== CRITICAL REQUIREMENTS ===

- This is ONE image containing 2 panels side by side
- SAME woman (Bailey from reference) in both panels
- SAME pose: back view, looking over shoulder, full body visible
- SAME setting, lighting, outfit, angle
- ONLY difference: glute size and shape as described
- Thin white border between panels
- Both panels equally sized
- Natural and realistic in both panels
- Show full backside clearly including glutes and legs

Generate the 1x2 grid showing Bailey's back view with 2 different glute size options."""

def generate_grid():
    """Generate 1x2 back view grid"""

    print("="*60)
    print("GENERATING: Bailey Back View Grid (1x2)")
    print("="*60)
    print("Panel 1: Full and round athletic bubble butt")
    print("Panel 2: Very large elite bubble butt")
    print("This may take 60-90 seconds...\n")

    output_path = "bailey_back_view_grid.jpg"

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[face_ref, PROMPT],
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
                image.save(output_path)
                print(f"✓ SUCCESS!")
                print(f"\nSaved: {output_path}")
                print(f"\nReview the grid and pick which glute size you prefer (left or right).\n")
                return output_path

        print("❌ Error: No image generated")
        return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    generate_grid()
