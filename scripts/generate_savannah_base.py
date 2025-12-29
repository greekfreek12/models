#!/usr/bin/env python3
"""
Generate Savannah's Base Image (Split View: Front + Back)
Using face reference + Brooke's base for body/format reference
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv
import sys

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Reference images
SAVANNAH_FACE = Path("models_2.0/savannah/face_reference.jpg")  # Face to preserve
BROOKE_BASE = Path("models/brooke/base.jpeg")  # Body/format reference
OUTPUT_PATH = Path("models_2.0/savannah/base.jpeg")

# Ensure output directory exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

PROMPT = """Generate a SPLIT VIEW image showing the SAME WOMAN in two poses.

=== CRITICAL REFERENCE USAGE ===

REFERENCE IMAGE 1 (Face):
This shows the woman's FACE that MUST be preserved exactly.
- Keep her EXACT facial features, eye color, face shape, smile
- Keep her EXACT hair color, length, and texture
- This is the PRIMARY IDENTITY reference

REFERENCE IMAGE 2 (Body/Format):
This is ONLY a reference for:
- Body proportions and build (similar breast size, waist-hip ratio, glutes)
- Bikini style (same black bikini)
- Background setting and lighting
- Split view composition format
- Pose style

DO NOT copy the face from Reference Image 2. Only use it for body proportions and format.

=== SPLIT VIEW LAYOUT ===

Create ONE wide image split into TWO sections:

LEFT PANEL - FRONT VIEW:
- Woman standing facing camera
- Full body shot from head to thighs/knees
- One hand on hip, relaxed confident pose
- Looking at camera with natural friendly expression
- Black triangle bikini top and bottoms
- Body: Athletic hourglass with similar proportions to Reference 2

RIGHT PANEL - BACK VIEW:
- Same woman, turned 180 degrees
- Full body from back, head to thighs/knees
- Standing naturally, not looking at camera
- Shows back view, glutes, and legs
- Same black bikini from behind
- Natural standing pose

=== IDENTITY REQUIREMENTS ===

FACE (From Reference Image 1 - MUST PRESERVE):
- Keep exact facial features
- Keep exact eye color
- Keep exact hair color and texture
- Keep exact overall appearance
- This is the SAME PERSON in both left and right panels

BODY (Inspired by Reference Image 2, but natural):
- Athletic hourglass figure
- Similar proportions: full bust, narrow waist, wide hips, round lifted glutes
- Natural and realistic, not exaggerated
- Similar overall body type but not identical
- Realistic human proportions

=== SETTING & STYLE ===

BACKGROUND:
- Outdoor patio/backyard setting
- White/neutral house wall visible
- Green plants/tropical foliage
- Natural outdoor environment
- Similar to Reference Image 2

LIGHTING:
- Natural daylight
- Soft outdoor lighting
- Realistic shadows
- Even lighting on both panels

BIKINI:
- Black triangle bikini top with string ties
- Black bikini bottoms (high-cut or cheeky style)
- Same style in both front and back views
- Similar to Reference Image 2

=== CRITICAL NATURAL REALISM ===

SKIN TEXTURE:
- Natural skin texture with visible pores
- Real human skin, NOT AI-smoothed
- NO beauty filter applied
- NO artificial smoothing or perfection
- Realistic skin with natural texture
- Slight imperfections okay

OVERALL REALISM:
- Natural poses, not stiff or forced
- Realistic body proportions
- Natural lighting and shadows
- Real person, not AI-perfect
- Authentic and believable

=== COMPOSITION ===

- Aspect ratio: 16:9 (wide horizontal split)
- Left panel = front view
- Right panel = back view
- Thin border or natural separation between panels
- Both panels same height and similar width
- Professional photography quality
- Clean composition

=== CONSISTENCY ===

- SAME WOMAN in both panels (face from Reference 1)
- Body proportions similar to Reference 2 but natural
- Same bikini in both views
- Same setting/background style
- Same lighting quality
- Natural and cohesive split view

=== FINAL REMINDER ===

This is a reference sheet showing ONE woman (face from Reference Image 1) from front and back.
Body proportions inspired by Reference Image 2 but naturally adapted to this person.
Natural, realistic, and cohesive. Not a copy-paste, but an organic natural result.
Same black bikini and outdoor setting as Reference Image 2.
Professional quality split view for model reference purposes.
"""

def generate_base():
    """Generate split view base image with face + body references"""

    print(f"\n{'='*60}")
    print(f"SAVANNAH - BASE IMAGE GENERATION")
    print(f"{'='*60}")
    print(f"Model: gemini-3-pro-image-preview")
    print(f"Face reference: {SAVANNAH_FACE}")
    print(f"Body/format reference: {BROOKE_BASE}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"\nGenerating split view (front + back)...")
    print(f"This may take 90-120 seconds...")
    print(f"")

    try:
        # Check if face reference exists
        if not SAVANNAH_FACE.exists():
            print(f"❌ Error: Face reference not found: {SAVANNAH_FACE}")
            print(f"Please save Savannah's face image as: {SAVANNAH_FACE}")
            return False

        # Upload reference images
        print("Uploading face reference...")
        with open(SAVANNAH_FACE, 'rb') as f:
            face_file = client.files.upload(
                file=f,
                config={"mime_type": "image/jpeg"}
            )
        print(f"Face reference uploaded: {face_file.name}")

        print("Uploading body/format reference...")
        with open(BROOKE_BASE, 'rb') as f:
            body_file = client.files.upload(
                file=f,
                config={"mime_type": "image/jpeg"}
            )
        print(f"Body reference uploaded: {body_file.name}")

        print("Generating split view base image...")

        # Generate with both references
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
                    aspect_ratio="16:9",
                    image_size="2K"
                )
            )
        )

        # Save generated image
        for part in response.parts:
            if image := part.as_image():
                image.save(OUTPUT_PATH)
                file_size = OUTPUT_PATH.stat().st_size / (1024 * 1024)

                print(f"\n{'='*60}")
                print(f"✓ SUCCESS!")
                print(f"{'='*60}")
                print(f"Saved: {OUTPUT_PATH}")
                print(f"Size: {file_size:.2f} MB")
                print(f"\nSplit view base image created:")
                print(f"  Left: Front view")
                print(f"  Right: Back view")
                print(f"\nSavannah's base reference is ready!")
                return True

        print("❌ Error: No image generated in response")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generate_base()
