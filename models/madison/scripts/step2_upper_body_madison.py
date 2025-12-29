#!/usr/bin/env python3
"""
STEP 2: Upper Body (Bikini Top) - Madison
Show face + breast size + upper body proportions while maintaining facial identity from Step 1
"""

from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
import json
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

MODEL_NAME = "madison"
PROFILE_PATH = f"models/{MODEL_NAME}/profile_v1.json"
FACE_REF_PATH = f"models/{MODEL_NAME}/01_face.jpeg"
OUTPUT_PATH = f"models/{MODEL_NAME}/02_upper_body.jpeg"

# Load profile
with open(PROFILE_PATH, 'r') as f:
    profile = json.load(f)

# Load face reference for identity locking
face_ref = PILImage.open(FACE_REF_PATH)

# Build upper body prompt with identity locking
PROMPT = f"""Generate a beautiful upper body beach portrait of the same woman from the reference image.

REFERENCE IMAGE: Her face close-up - preserve her exact facial identity.

THE WOMAN - {profile['model_name']}:

Her face (must match reference exactly):
- {profile['face']['eyes']['color']} eyes, {profile['face']['eyes']['shape']}
- {profile['face']['shape']} face with {profile['face']['face_structure']['cheekbones']}
- {profile['face']['lips']['fullness']}, {profile['face']['lips']['shape']}
- {profile['hair']['color']} hair, {profile['hair']['length']}, {profile['hair']['texture']}
- {profile['face']['skin']['tone']}, natural skin texture with visible pores

Her body (show clearly in this shot):

CHEST - VERY IMPORTANT: Full D-cup breasts. These are noticeably larger than average - voluptuous, prominent, and eye-catching. The bikini top should clearly show she has a full D-cup bust. This is bigger than a C-cup - make it obvious.

- {profile['body']['upper_body']['shoulders']['width']} shoulders, athletic but feminine
- {profile['body']['overall_build']}
- Narrow defined waist with visible abs

THE SHOT:
- Upper body portrait from waist to top of head
- White triangle bikini top showing her figure clearly
- Beach setting: ocean and palm trees in background
- Natural golden hour lighting, warm and flattering
- She's standing naturally, relaxed, looking at camera with a warm smile
- Hand on hip or in hair, confident beach pose
- 2:3 portrait aspect ratio, professional quality

IMPORTANT:
- Same woman as reference image - facial features identical
- Natural skin texture throughout, no beauty filter
- Her chest must be clearly D-cup size - larger and fuller than average
- Photorealistic beach photography style

This is a reference photo for her portfolio - show her beauty and proportions accurately, especially her full bust.
"""

def generate_step2():
    """Generate Step 2: Upper Body"""

    print(f"\n{'='*60}")
    print(f"STEP 2: UPPER BODY (BIKINI TOP)")
    print(f"{'='*60}")
    print(f"Model: {profile['model_name']}")
    print(f"\nUploading face reference for identity locking:")
    print(f"  - {FACE_REF_PATH}")
    print(f"\nGenerating upper body shot...")
    print(f"Using Gemini Pro (gemini-3-pro-image-preview)")
    print(f"\nThis may take 90-120 seconds...\n")

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

        # Save generated image
        for part in response.parts:
            if image := part.as_image():
                image.save(OUTPUT_PATH)
                print(f"✓ SUCCESS!")
                print(f"\nStep 2 complete: {OUTPUT_PATH}")
                print(f"\n{'='*60}")
                print(f"VERIFICATION:")
                print(f"{'='*60}")
                print(f"Check that:")
                print(f"  ✓ Face matches Step 1 reference")
                print(f"  ✓ Upper body proportions shown clearly")
                print(f"  ✓ Bikini top visible")
                print(f"  ✓ Natural skin texture maintained")
                print(f"\nIf approved, proceed to Step 3 (full body split)")
                print(f"\n")
                return OUTPUT_PATH

        print("❌ Error: No image generated in response")
        return None

    except Exception as e:
        print(f"❌ Error generating image: {str(e)}")
        return None

if __name__ == "__main__":
    generate_step2()
