#!/usr/bin/env python3
"""
Generate portrait with text description only - no references
"""

from google import genai
from google.genai import types
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

OUTPUT_PATH = Path("models_2.0/veronica/random_portrait.jpeg")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

PROMPT = """Generate a close-up portrait of a woman.

COMPOSITION:
- Close-up portrait shot
- Face centered in frame
- From shoulders/upper chest to top of head
- Face is the main focus
- Tight framing with face filling most of frame

SUBJECT:
- Young adult woman
- Natural beauty
- Warm genuine smile
- Engaging eye contact with camera
- Friendly approachable expression

FRAMING:
- Eye level perspective
- Well-centered composition
- Portrait orientation
- Professional headshot style

SETTING:
- Outdoor natural setting
- Soft blurred background
- Beach or scenic terrace
- Natural environment

LIGHTING:
- Natural golden hour light
- Soft warm glow on face
- Flattering portrait lighting
- Gentle shadows and highlights

STYLE:
- High-end portrait photography
- Professional quality
- Instagram influencer aesthetic
- Natural and authentic

TECHNICAL:
- 9:16 portrait aspect ratio
- Shallow depth of field
- Natural skin texture with visible pores
- No beauty filter or AI smoothing
- Realistic and photorealistic
- High resolution 2K

Generate a beautiful close-up portrait with face centered and zoomed in.
"""

def generate_portrait():
    """Generate portrait from text description only"""

    print(f"\n{'='*60}")
    print(f"GENERATE PORTRAIT - TEXT ONLY")
    print(f"{'='*60}")
    print(f"No references - pure text generation")
    print(f"Close portrait - face centered and zoomed")
    print(f"Output: {OUTPUT_PATH}")
    print(f"")

    try:
        print("Generating portrait from text description...")

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=PROMPT,
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
                print(f"\nClose portrait generated from description only")
                return True

        print("❌ Error: No image generated")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generate_portrait()
