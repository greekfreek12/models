#!/usr/bin/env python3
"""
Generate Bailey's upper body reference shot
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

PROMPT = f"""This is Bailey. The uploaded reference image shows her face.

Generate a photo of the SAME WOMAN from the reference image.

WHAT'S THE SAME (from reference):
- Same woman, exact same face and facial features
- Same hair color, length, texture, style
- Same skin tone and texture
- Same age (19-20 years old)
- Natural skin texture with visible pores

WHAT'S DIFFERENT (new shot):
FRAMING: From chest/mid-torso up to top of head (show upper body)

UPPER BODY DETAILS (describe what we see):
- Chest: Natural D-cup, full and shapely, natural shape with lift
- Shoulders: Athletic and proportionate, feminine but strong, defined
- Upper body: Athletic hourglass build, fitness model physique
- Posture: Natural standing, relaxed shoulders, confident

OUTFIT:
- White triangle bikini top
- Shows upper body and chest clearly

SETTING:
- Beach setting, natural outdoor
- Golden hour lighting, warm and flattering
- Soft blur background

POSE & ANGLE:
- Standing naturally, one hand on hip (optional)
- Straight-on angle, directly facing camera
- Natural expression - soft smile or neutral
- Same natural, confident energy as face reference

CRITICAL:
- This is the SAME PERSON from the reference image
- Maintain 100% facial identity
- Natural skin texture, realistic
- Show upper body proportions clearly
- Athletic hourglass build, natural and realistic

Generate a stunning upper body reference photo of Bailey."""

def generate_upper_body():
    """Generate upper body shot"""

    print("="*60)
    print("GENERATING: Bailey Upper Body Reference")
    print("="*60)
    print("Using face reference for identity consistency")
    print("This may take 60-90 seconds...\n")

    output_path = "bailey_upper_body.jpg"

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[face_ref, PROMPT],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="2:3",
                    image_size="2K"
                )
            )
        )

        for part in response.parts:
            if image := part.as_image():
                image.save(output_path)
                print(f"✓ SUCCESS!")
                print(f"\nSaved: {output_path}")
                print(f"\nReview the upper body shot.")
                print(f"Check if facial identity matches and upper body proportions look good.\n")
                return output_path

        print("❌ Error: No image generated")
        return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    generate_upper_body()
