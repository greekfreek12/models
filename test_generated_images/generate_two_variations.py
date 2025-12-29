#!/usr/bin/env python3
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# TASK 1: BB with blonde hair
ref1 = PILImage.open("bb.jpeg")

PROMPT1 = """Generate the SAME PERSON from reference image with these specific changes ONLY:

KEEP EXACTLY THE SAME:
- Same face structure and proportions
- Same facial features (nose, lips, eyes, bone structure)
- Same skin tone
- Same eye shape and size
- Same overall appearance

CHANGE ONLY:
- Hair color: Blonde instead of black
- Eye color: Brown eyes (keep same shape)
- Makeup: Natural minimal makeup (not heavy)
- Expression: Neutral (no smile)
- Skin: Natural with visible pores
- Eyebrows: Slightly bushier (but natural)

This is the SAME WOMAN, just with blonde hair and natural makeup.
Close-up portrait, neck to top of head, straight-on, natural lighting.
Keep her face IDENTICAL to reference."""

# TASK 2: Merge two faces
ref2a = PILImage.open("IMG_0610.png.jpeg")
ref2b = PILImage.open("bb.jpeg")

PROMPT2 = """Merge these TWO reference images into ONE realistic woman's face.

Blend features from BOTH women to create a new unified face:
- Take facial structure elements from both
- Blend skin tones (medium between the two)
- Combine best features from each
- Create one cohesive realistic face

STYLE:
- Natural minimal makeup
- Visible pores, realistic skin
- Neutral expression
- Age 19-21

Close-up portrait, natural lighting, create ONE realistic merged face."""

print("Generating Task 1: BB with blonde hair...")
try:
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[ref1, PROMPT1],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(aspect_ratio="2:3", image_size="2K")
        )
    )
    for part in response.parts:
        if image := part.as_image():
            image.save("bb_blonde_version.jpg")
            print("✓ Task 1 SUCCESS: bb_blonde_version.jpg")
            break
except Exception as e:
    print(f"Task 1 Error: {e}")

print("\nGenerating Task 2: Merged faces...")
try:
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[ref2a, ref2b, PROMPT2],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(aspect_ratio="2:3", image_size="2K")
        )
    )
    for part in response.parts:
        if image := part.as_image():
            image.save("merged_faces.jpg")
            print("✓ Task 2 SUCCESS: merged_faces.jpg")
            break
except Exception as e:
    print(f"Task 2 Error: {e}")

print("\nDone! Review both results.")
