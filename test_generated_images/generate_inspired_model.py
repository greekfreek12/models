#!/usr/bin/env python3
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Load reference
ref = PILImage.open("IMG_0610.png.jpeg")

PROMPT = """Reference image shows the VIBE and appeal, but generate a DIFFERENT woman.

KEEP from reference:
- Same tan level (warm tan/brown skin tone)
- Same eye color (dark brown eyes)
- Dark hair (long)
- Age 19-21, youthful
- Overall attractive appeal

MAKE DIFFERENT (so she's clearly not the same person):
- Different eye shape (almond-shaped, slightly different)
- Different nose (more refined, smaller, different shape)
- Different face shape (oval instead of round, less full cheeks)
- Different hair texture and style
- Different specific facial proportions
- Different bone structure

EXPRESSION & STYLE:
- NEUTRAL expression (no smile, calm relaxed face)
- Natural makeup (minimal, not heavy)
- Natural skin texture with VISIBLE PORES
- Realistic, not smoothed

FRAMING:
- Close-up portrait from neck to top of head
- Straight-on angle, eye level
- Looking at camera
- Natural outdoor lighting

Generate a NEW woman inspired by reference but clearly different."""

try:
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[ref, PROMPT],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(aspect_ratio="2:3", image_size="2K")
        )
    )
    
    for part in response.parts:
        if image := part.as_image():
            image.save("inspired_model_neutral.jpg")
            print("✓ SUCCESS: inspired_model_neutral.jpg")
            break
except Exception as e:
    print(f"Error: {e}")
