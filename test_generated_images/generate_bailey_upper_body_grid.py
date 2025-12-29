#!/usr/bin/env python3
"""
Generate Bailey upper body 1x2 grid with 2 breast size variations
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
- Same natural skin texture with visible pores
- Same age (19-20 years old)

CAMERA & FRAMING (IDENTICAL IN BOTH):
- 85mm portrait lens at f/1.8
- Eye level, straight on, directly facing camera
- FROM END OF BIKINI TOP TO TOP OF HEAD ONLY
- Do NOT show below the bikini top bottom edge
- Do NOT show waist or torso below bikini
- Head fills frame, face centered
- Professional upper body portrait

SETTING (SAME IN BOTH):
- Beach setting, ocean in background
- Golden hour lighting, warm and flattering
- Soft blur background
- Natural outdoor beach

POSE (SAME IN BOTH):
- Standing naturally facing camera
- Arms relaxed at sides or hand on hip
- Neutral or soft smile
- Natural confident energy
- Same pose in both panels

OUTFIT (SAME IN BOTH):
- White triangle bikini top
- Simple and clean

SKIN TEXTURE (SAME IN BOTH):
- Natural skin texture with visible pores
- Realistic, not smoothed
- Natural beauty marks okay

=== WHAT'S DIFFERENT BETWEEN PANELS ===

ONLY difference: Breast size description

PANEL 1 (LEFT):
- Chest: Full and prominent, shapely natural breasts, noticeable and attractive

PANEL 2 (RIGHT):
- Chest: Very large and voluptuous, very full breasts, exceptionally prominent, striking

=== CRITICAL REQUIREMENTS ===

- This is ONE image containing 2 panels side by side
- SAME woman (Bailey from reference) in both panels
- SAME framing: from END of bikini top to top of head (no lower)
- SAME pose, angle, setting, lighting
- ONLY difference: breast size as described
- Thin white border between panels
- Both panels equally sized
- Natural and realistic in both panels

Generate the 1x2 grid showing Bailey with 2 different breast size options."""

def generate_grid():
    """Generate 1x2 upper body grid"""

    print("="*60)
    print("GENERATING: Bailey Upper Body Grid (1x2)")
    print("="*60)
    print("Panel 1: Full and prominent")
    print("Panel 2: Very large and voluptuous")
    print("This may take 60-90 seconds...\n")

    output_path = "bailey_upper_body_grid.jpg"

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
                print(f"\nReview the grid and pick which breast size you prefer (left or right).\n")
                return output_path

        print("❌ Error: No image generated")
        return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    generate_grid()
