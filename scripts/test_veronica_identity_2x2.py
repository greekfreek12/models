#!/usr/bin/env python3
"""
Test Veronica Identity Locking - 2x2 Grid at Greek Island
No identity descriptions, just upload references and preserve
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Reference images ONLY
VERONICA_BASE = Path("models_2.0/veronica/base.jpeg")
VERONICA_FACE_GRID = Path("models_2.0/veronica/face_grid_2x3.png")
OUTPUT_PATH = Path("models_2.0/veronica/test_2x2_santorini.png")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

PROMPT = """Generate a 2x2 GRID (4 panels) showing the SAME WOMAN at Santorini, Greece.

=== UPLOADED REFERENCES ===

We have uploaded images of ONE MODEL:
- First image: Shows her face from 6 different angles
- Second image: Shows her full body from front and back

=== CRITICAL: PRESERVE HER IDENTITY ===

Keep her EXACT identity from the uploaded references:
- Use her exact face from the references
- Use her exact body from the references
- Keep her exact hair, skin tone, features
- This is the SAME PERSON in all 4 panels
- Do NOT change anything about her appearance

=== SANTORINI SCENE - 2x2 GRID ===

All 4 panels are at SANTORINI, GREECE at different spots:

PANEL 1 (Top Left) - OIA VILLAGE STEPS:
- Standing on white staircase with blue railing
- Iconic white buildings and blue domes in background
- Golden hour sunset lighting
- Front view, one hand on railing
- Relaxed confident pose

PANEL 2 (Top Right) - INFINITY POOL:
- Sitting on edge of luxury infinity pool
- Caldera view behind, endless blue Aegean Sea
- White Cycladic architecture around pool
- Front view, looking at camera
- Legs in water, arms supporting behind

PANEL 3 (Bottom Left) - WHITE TERRACE:
- Walking on white stone terrace
- Bougainvillea flowers (pink) cascading on white walls
- Blue domed church visible in distance
- Side walking shot, mid-stride
- Natural movement, hair flowing

PANEL 4 (Bottom Right) - SUNSET OVERLOOK:
- Standing at cliffside overlooking caldera
- Back view looking over shoulder at camera
- Orange/pink sunset sky
- Dramatic vista of sea and cliffs below
- Hair blowing in wind

=== CONSISTENT ACROSS ALL PANELS ===

LOCATION: All in Santorini (white buildings, blue accents, caldera views)
LIGHTING: Golden hour warm light
OUTFIT: Bikini (any style, natural choice)
MOOD: Luxury Greek island vacation, dreamy, romantic

CRITICAL: Same woman from uploaded references in all 4 panels. Preserve her identity exactly.

=== TECHNICAL ===

- Square 1:1 aspect ratio
- 2x2 grid layout
- Thin white borders between panels
- High resolution
- Natural skin texture, realistic
- Professional photography quality

Generate this woman from the references in 4 Santorini poses.
"""

def generate_test_grid():
    """Test identity locking with 2x2 Santorini grid"""

    print(f"\n{'='*60}")
    print(f"VERONICA - IDENTITY TEST (2x2 Santorini)")
    print(f"{'='*60}")
    print(f"Testing identity preservation from references")
    print(f"Face reference: {VERONICA_FACE_GRID}")
    print(f"Body reference: {VERONICA_BASE}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"\n4 poses at Santorini, Greece")
    print(f"")

    try:
        print("Uploading face angles reference...")
        with open(VERONICA_FACE_GRID, 'rb') as f:
            face_file = client.files.upload(
                file=f,
                config={"mime_type": "image/png"}
            )
        print(f"Face reference uploaded: {face_file.name}")

        print("Uploading body reference...")
        with open(VERONICA_BASE, 'rb') as f:
            body_file = client.files.upload(
                file=f,
                config={"mime_type": "image/jpeg"}
            )
        print(f"Body reference uploaded: {body_file.name}")

        print("Generating 2x2 Santorini grid...")

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[
                types.Part.from_uri(
                    file_uri=face_file.uri,
                    mime_type=face_file.mime_type
                ),
                types.Part.from_uri(
                    file_uri=body_file.uri,
                    mime_type=body_file.mime_type
                ),
                PROMPT
            ],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                    image_size="2K"
                )
            )
        )

        for part in response.parts:
            if image := part.as_image():
                image.save(OUTPUT_PATH)
                file_size = OUTPUT_PATH.stat().st_size / (1024 * 1024)

                print(f"\n{'='*60}")
                print(f"✓ SUCCESS!")
                print(f"{'='*60}")
                print(f"Saved: {OUTPUT_PATH}")
                print(f"Size: {file_size:.2f} MB")
                print(f"\n4 Santorini poses:")
                print(f"  Top left: Oia steps | Top right: Infinity pool")
                print(f"  Bottom left: White terrace | Bottom right: Sunset overlook")
                print(f"\nCheck if identity matches Veronica's references!")
                return True

        print("❌ Error: No image generated")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generate_test_grid()
