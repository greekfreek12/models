#!/usr/bin/env python3
"""
Generate Bailey back view with CENTERED butt angle - 1x2 grid
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

CAMERA ANGLE & FRAMING (IDENTICAL IN BOTH) - CRITICAL:
- Shot from DIRECTLY BEHIND her, slightly above
- Camera positioned centered behind her butt
- Her butt is CENTERED in the frame, main focus
- Full body visible from head to feet (or close to feet)
- She's looking back over her shoulder so we see her face
- NOT a side view - this is a BACK view with butt centered
- Clear view of her full backside, glutes prominently featured

SETTING (SAME IN BOTH):
- Beach setting, ocean in background
- Golden hour lighting, warm and flattering
- Soft blur background
- Natural outdoor beach

POSE (SAME IN BOTH):
- Standing naturally facing away from camera
- Back fully to camera, butt centered
- Looking back over her shoulder with soft smile
- One hand on hip or relaxed
- Natural confident stance
- Show her backside clearly - butt, back, legs
- Same pose in both panels

OUTFIT (SAME IN BOTH):
- White bikini (triangle top + bikini bottoms)
- Bikini bottoms clearly show glute shape

BODY (SAME IN BOTH):
- Athletic hourglass build
- Narrow waist visible from back
- Long lean legs
- Toned athletic physique
- Athletic shoulders and back

SKIN TEXTURE (SAME IN BOTH):
- Natural skin texture
- Realistic, not smoothed

=== WHAT'S DIFFERENT BETWEEN PANELS ===

ONLY difference: Glute/butt size and shape

PANEL 1 (LEFT):
- Glutes: Full and round, shapely natural butt, toned and lifted, athletic bubble butt, prominent and attractive

PANEL 2 (RIGHT):
- Glutes: Very large and round, exceptionally full and lifted, elite bubble butt, dramatic curve and projection, very prominent standout feature, striking and impressive

=== CRITICAL REQUIREMENTS ===

- This is ONE image containing 2 panels side by side
- SAME woman (Bailey from reference) in both panels
- Camera angle: DIRECTLY from behind, butt CENTERED in frame (not side view)
- Her butt is the main focus, clearly visible and centered
- Looking back over shoulder so we see her face
- SAME everything except glute size
- Thin white border between panels
- Both panels equally sized
- Natural and realistic in both panels

Generate the 1x2 grid with proper centered back view angle."""

def generate_grid():
    """Generate 1x2 back view grid with better angle"""

    print("="*60)
    print("GENERATING: Bailey Back View Grid (Centered Angle)")
    print("="*60)
    print("Panel 1: Full athletic bubble butt")
    print("Panel 2: Very large elite bubble butt")
    print("Angle: Directly from behind, butt centered")
    print("This may take 60-90 seconds...\n")

    output_path = "bailey_back_view_centered.jpg"

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
                print(f"\nReview - butt should be centered, not side view.\n")
                return output_path

        print("❌ Error: No image generated")
        return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    generate_grid()
