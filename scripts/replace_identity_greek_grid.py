#!/usr/bin/env python3
"""
Replace person in Greek grid with Veronica's identity
Use existing grid as composition/pose template
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Reference images
EXISTING_GRID = Path("models_2.0/veronica/greek_island_grid_3x3.png")
VERONICA_BASE = Path("models_2.0/veronica/base.jpeg")
VERONICA_FACE_GRID = Path("models_2.0/veronica/face_grid_2x3.png")
OUTPUT_PATH = Path("models_2.0/veronica/greek_grid_identity_replaced.png")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

PROMPT = """Replace the person in this 3x3 grid with the specific woman from the uploaded references.

=== UPLOADED REFERENCES ===

Reference 1: Existing 3x3 grid showing poses, locations, and compositions
Reference 2: Face angles of the woman to use (6 different angles)
Reference 3: Body reference of the woman to use (front and back views)

=== TASK ===

Take the EXACT same grid layout, poses, locations, and compositions from Reference 1 (the existing grid).

But REPLACE the person in every panel with the woman from References 2 & 3.

Keep everything the same:
- Same 3x3 grid layout
- Same Greek island locations in each panel
- Same poses and camera angles
- Same lighting and mood
- Same compositions

ONLY change the person's identity:
- Use the exact face from Reference 2 (face angles grid)
- Use the exact body from Reference 3 (body reference)
- Same woman in all 9 panels (from References 2 & 3)

=== CRITICAL REQUIREMENTS ===

PRESERVE FROM REFERENCE 1 (existing grid):
- All 9 locations/scenes
- All 9 poses
- All 9 camera angles
- Grid layout and composition
- Lighting style
- Background elements
- Overall aesthetic

REPLACE WITH REFERENCES 2 & 3:
- Person's face (use Reference 2)
- Person's body (use Reference 3)
- Person's identity (same woman in all 9 panels)

This is like taking the same photoshoot but with a different model.

=== OUTPUT ===

Generate a 3x3 grid that matches Reference 1's composition exactly, but with the woman from References 2 & 3 in every panel.

Square 1:1 aspect ratio, high resolution, thin white borders between panels.
"""

def replace_identity():
    """Replace person in grid with Veronica's identity"""

    print(f"\n{'='*60}")
    print(f"REPLACE IDENTITY IN GREEK GRID")
    print(f"{'='*60}")
    print(f"Taking existing grid composition...")
    print(f"Replacing person with Veronica's identity...")
    print(f"Output: {OUTPUT_PATH}")
    print(f"")

    try:
        print("Uploading existing grid template...")
        with open(EXISTING_GRID, 'rb') as f:
            grid_file = client.files.upload(
                file=f,
                config={"mime_type": "image/png"}
            )
        print(f"Grid template: {grid_file.name}")

        print("Uploading Veronica's face reference...")
        with open(VERONICA_FACE_GRID, 'rb') as f:
            face_file = client.files.upload(
                file=f,
                config={"mime_type": "image/png"}
            )
        print(f"Face reference: {face_file.name}")

        print("Uploading Veronica's body reference...")
        with open(VERONICA_BASE, 'rb') as f:
            body_file = client.files.upload(
                file=f,
                config={"mime_type": "image/jpeg"}
            )
        print(f"Body reference: {body_file.name}")

        print("Generating new grid with identity replacement...")

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[
                types.Part.from_uri(
                    file_uri=grid_file.uri,
                    mime_type=grid_file.mime_type
                ),
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
                print(f"\nSame poses & locations, but with Veronica's identity!")
                return True

        print("❌ Error: No image generated")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    replace_identity()
