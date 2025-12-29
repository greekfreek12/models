#!/usr/bin/env python3
"""
Generate single Veronica infinity pool image - closer framing
Using structured JSON prompt style
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Reference images
VERONICA_BASE = Path("models_2.0/veronica/base.jpeg")
VERONICA_FACE_GRID = Path("models_2.0/veronica/face_grid_2x3.png")
OUTPUT_PATH = Path("models_2.0/veronica/santorini_pool_closeup.jpeg")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# Structured prompt
prompt_data = {
    "meta": {
        "aspect_ratio": "9:16",
        "quality": "ultra_photorealistic",
        "resolution": "2K",
        "camera": "Sony A7R IV",
        "lens": "85mm portrait",
        "style": "high-end travel influencer photography, luxury resort aesthetic"
    },

    "identity_references": {
        "uploaded_images": "Two reference images of one model",
        "image_1": "Face from 6 different angles",
        "image_2": "Full body front and back views",
        "critical": "Use EXACT identity from uploaded references - same face, same body, same features"
    },

    "scene": {
        "location": "Luxury infinity pool in Santorini, Greece",
        "environment": [
            "White Cycladic architecture surrounding pool",
            "Infinity edge overlooking Santorini caldera",
            "Endless blue Aegean Sea in background",
            "White stone pool deck",
            "Clear turquoise pool water"
        ],
        "time": "late afternoon golden hour"
    },

    "lighting": {
        "type": "natural golden hour",
        "source": "warm afternoon sun",
        "effect": "soft warm glow, gentle highlights on skin and water, romantic dreamy quality"
    },

    "camera_perspective": {
        "angle": "eye level, slightly above",
        "distance": "medium-close shot",
        "framing": "from upper thighs to top of head, upper body focus",
        "depth_of_field": "shallow, background softly blurred"
    },

    "subject": {
        "identity": "From uploaded references - preserve exactly",
        "position": "sitting on infinity pool edge",

        "pose": {
            "position": "sitting on pool edge, legs in water",
            "upper_body": "leaning back, arms supporting behind",
            "posture": "relaxed, confident, vacation mood",
            "legs": "submerged in pool water to mid-thigh",
            "intent": "luxury vacation influencer shot"
        },

        "face": {
            "visibility": "fully visible, clear view",
            "expression": "warm genuine smile, relaxed happy",
            "eye_direction": "looking at camera, engaging",
            "features": "from uploaded reference images"
        },

        "outfit": {
            "type": "bikini",
            "style": "simple triangle bikini",
            "color": "black or neutral solid color"
        }
    },

    "photography_notes": [
        "Instagram luxury travel influencer aesthetic",
        "Natural skin texture with visible pores",
        "Realistic body proportions",
        "No AI smoothing or beauty filter",
        "Wet skin from pool water",
        "Natural vacation candid feeling",
        "Professional high-end photography quality"
    ],

    "critical_requirements": [
        "Use exact identity from uploaded reference images",
        "Same face as references",
        "Same body as references",
        "Do not change her features",
        "Closer framing than wide shot - focus on upper body",
        "Natural realistic skin texture"
    ]
}

# Convert to formatted string
PROMPT = json.dumps(prompt_data, indent=2)

def generate_pool_closeup():
    """Generate single infinity pool image with closer framing"""

    print(f"\n{'='*60}")
    print(f"VERONICA - SANTORINI POOL CLOSEUP")
    print(f"{'='*60}")
    print(f"Generating single image with closer framing")
    print(f"Scene: Infinity pool, Santorini")
    print(f"Framing: Medium-close (upper thighs to head)")
    print(f"Output: {OUTPUT_PATH}")
    print(f"")

    try:
        print("Uploading face reference...")
        with open(VERONICA_FACE_GRID, 'rb') as f:
            face_file = client.files.upload(
                file=f,
                config={"mime_type": "image/png"}
            )
        print(f"Face reference: {face_file.name}")

        print("Uploading body reference...")
        with open(VERONICA_BASE, 'rb') as f:
            body_file = client.files.upload(
                file=f,
                config={"mime_type": "image/jpeg"}
            )
        print(f"Body reference: {body_file.name}")

        print("Generating infinity pool closeup...")

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
                    aspect_ratio="9:16",
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
                print(f"\nSantorini infinity pool - closer framing")
                print(f"Veronica's identity from references preserved")
                return True

        print("❌ Error: No image generated")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generate_pool_closeup()
