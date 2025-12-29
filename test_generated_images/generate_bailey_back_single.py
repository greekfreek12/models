#!/usr/bin/env python3
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

face_ref = PILImage.open("lsu_blonde_keeper_1.jpg")

PROMPT = """This is Bailey from the reference image.

Generate a full body beach photo of her from behind.

KEY REQUIREMENTS:
- Camera positioned directly behind her, butt centered in frame
- She looks back over her shoulder (we see her face)
- White bikini
- Beach setting, golden hour
- Athletic hourglass build with very full round glutes
- Same woman from reference - blonde hair, blue eyes, tan

Full body back view, butt clearly visible and centered."""

try:
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[face_ref, PROMPT],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(aspect_ratio="2:3", image_size="2K")
        )
    )
    
    for part in response.parts:
        if image := part.as_image():
            image.save("bailey_back_view_final.jpg")
            print("✓ SUCCESS: bailey_back_view_final.jpg")
            break
except Exception as e:
    print(f"Error: {e}")
