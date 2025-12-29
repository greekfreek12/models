#!/usr/bin/env python3
"""
Generate Veronica Face Angles Grid (2x3 - 6 variations)
Using Gemini 3 Pro with identity reference upload
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Reference image
VERONICA_BASE = Path("models_2.0/veronica/base.jpeg")
OUTPUT_PATH = Path("models_2.0/veronica/face_grid_2x3.png")

# Ensure output directory exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

GRID_PROMPT = """Generate a 2x3 GRID (6 panels) showing the SAME WOMAN in different face angles.

=== CRITICAL IDENTITY PRESERVATION ===

UPLOADED REFERENCE IMAGE:
This image shows the woman whose EXACT identity you MUST preserve across all 6 panels.

IDENTITY REQUIREMENTS:
- This is the SAME PERSON in all 6 panels
- DO NOT change her face, features, or appearance
- DO NOT alter her eye color, eye shape, nose, lips, face shape, or any facial features
- DO NOT change her skin tone or complexion
- DO NOT change her hair color, length, or texture
- Preserve her EXACT identity from the reference image
- Only the camera angle and facial expression change between panels
- Everything else about her appearance stays IDENTICAL

Use the reference image to maintain 100% facial identity consistency across all panels.

=== GRID LAYOUT - 2x3 (6 PANELS) ===

Create ONE image with 6 panels arranged in 2 rows and 3 columns.
Thin white borders separating each panel.

ROW 1:
- Panel 1 (Top Left): Front view, neutral expression
- Panel 2 (Top Center): Front view, warm genuine smile
- Panel 3 (Top Right): 3/4 angle facing left

ROW 2:
- Panel 4 (Bottom Left): 3/4 angle facing right
- Panel 5 (Bottom Center): Profile view (side view)
- Panel 6 (Bottom Right): Over-the-shoulder look back

=== PANEL SPECIFICATIONS ===

PANEL 1 - FRONT NEUTRAL:
- Looking directly at camera
- Head straight on, no tilt
- Neutral expression, soft relaxed face
- Eyes open, calm gaze
- Lips closed naturally

PANEL 2 - FRONT SMILE:
- Looking directly at camera
- Head straight on, no tilt
- Warm genuine smile showing teeth
- Eyes bright and friendly
- Natural happy expression

PANEL 3 - 3/4 LEFT:
- Head turned approximately 45 degrees to her left
- Eyes looking at camera
- Slight smile
- Shows both eyes but emphasizes left side of face

PANEL 4 - 3/4 RIGHT:
- Head turned approximately 45 degrees to her right
- Eyes looking at camera
- Slight smile
- Shows both eyes but emphasizes right side of face

PANEL 5 - PROFILE:
- Full side view (90 degrees)
- Looking to the side (not at camera)
- Clean profile showing nose bridge, jawline, lips
- Neutral or slight smile
- Hair behind ear or arranged to show face clearly

PANEL 6 - OVER SHOULDER:
- Back of head visible
- Looking back over shoulder at camera
- Sultry or playful expression
- Hair cascading down back
- Shows face from behind angle

=== CONSISTENT ACROSS ALL PANELS ===

FRAMING (ALL PANELS):
- Face close-up from upper neck/shoulders to top of head
- Head fills frame, face is the focus
- 85mm portrait lens equivalent
- Soft blur background (neutral outdoor setting)

LIGHTING (ALL PANELS):
- Natural soft daylight, golden hour quality
- Soft shadows, flattering light on face
- Even lighting across all panels
- Professional headshot lighting

APPEARANCE (ALL PANELS):
- Keep the EXACT SAME appearance from reference image
- Same hairstyle as in reference
- Same overall styling as in reference
- Simple neutral top (not the focus)
- Clean professional headshot style

=== CRITICAL SKIN TEXTURE (ALL PANELS) ===

- Natural skin texture with VISIBLE PORES
- Real human skin with realistic texture
- Slight imperfections present (natural beauty marks, subtle texture variations)
- NOT AI-smoothed or filtered
- NO beauty filter applied
- NO artificial smoothing or perfection
- NO glowing or plastic skin
- Realistic lighting behavior on skin

This is a real person, not magazine-perfect.

=== QUALITY REQUIREMENTS ===

TECHNICAL:
- 16:9 aspect ratio for grid layout
- High resolution (2K)
- Each panel is equally sized
- Clean grid with thin white borders between panels
- Professional headshot photography quality

CONSISTENCY:
- SAME WOMAN in all 6 panels (from reference image)
- SAME facial features in all panels
- SAME skin tone in all panels
- SAME hair in all panels
- SAME person from reference - DO NOT CHANGE HER
- ONLY angle and expression vary between panels

=== FINAL REMINDER ===

This is ONE image containing 6 face angle variations of the SAME WOMAN from the reference image.

CRITICAL: Maintain 100% identity consistency across all panels. This is the EXACT SAME PERSON from the reference image in all 6 panels. DO NOT change her appearance, features, coloring, or any aspect of her identity. Only the camera angle and facial expression change between panels.

Natural skin texture with visible pores - realistic beauty, not AI perfection.
Clean professional grid layout with 6 equally-sized panels.

Generate a stunning reference sheet showing this woman from multiple angles.
"""

def generate_face_grid():
    """Generate 2x3 face angles grid with reference image"""

    print(f"\n{'='*60}")
    print(f"VERONICA - FACE ANGLES GRID GENERATION")
    print(f"{'='*60}")
    print(f"Model: gemini-3-pro-image-preview")
    print(f"Reference: {VERONICA_BASE}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"\nGenerating 6 face angle variations:")
    print(f"  Panel 1: Front neutral")
    print(f"  Panel 2: Front smile")
    print(f"  Panel 3: 3/4 left")
    print(f"  Panel 4: 3/4 right")
    print(f"  Panel 5: Profile")
    print(f"  Panel 6: Over shoulder")
    print(f"\nThis may take 90-120 seconds...")
    print(f"")

    try:
        # Upload reference image
        print("Uploading reference image...")
        with open(VERONICA_BASE, 'rb') as f:
            uploaded_file = client.files.upload(
                file=f,
                config={"mime_type": "image/jpeg"}
            )

        print(f"Reference uploaded: {uploaded_file.name}")
        print("Generating grid...")

        # Generate grid with reference
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[
                types.Part.from_uri(
                    file_uri=uploaded_file.uri,
                    mime_type=uploaded_file.mime_type
                ),
                GRID_PROMPT
            ],
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
                image.save(OUTPUT_PATH)
                file_size = OUTPUT_PATH.stat().st_size / (1024 * 1024)

                print(f"\n{'='*60}")
                print(f"✓ SUCCESS!")
                print(f"{'='*60}")
                print(f"Saved: {OUTPUT_PATH}")
                print(f"Size: {file_size:.2f} MB")
                print(f"\nGrid contains 6 panels (2x3 layout):")
                print(f"  Row 1: Front neutral | Front smile | 3/4 left")
                print(f"  Row 2: 3/4 right | Profile | Over shoulder")
                print(f"\nSame woman (Veronica) across all panels.")
                print(f"Ready for use as face angle references!")
                return True

        print("❌ Error: No image generated in response")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generate_face_grid()
