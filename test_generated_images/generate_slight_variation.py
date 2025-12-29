#!/usr/bin/env python3
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Load CORRECT reference
ref = PILImage.open("bb.jpeg")

PROMPT = """Generate the SAME TYPE OF WOMAN from reference with SLIGHT variations.

KEEP VERY SIMILAR:
- Same ethnicity and skin tone (warm tan/brown)
- Same general facial structure and proportions  
- Same eye color (dark brown)
- Same hair color (dark/black)
- Same age (19-21)
- Same overall beauty and appeal

MAKE ONLY SLIGHTLY DIFFERENT:
- Eye shape slightly different (still large and beautiful, just minor variation)
- Nose shape minor variation (still refined, just slightly different)
- Lips slightly different fullness
- Face shape very minor difference
- Hair style/texture slightly different

EXPRESSION & STYLE:
- NEUTRAL expression (no smile, calm natural face)
- Natural minimal makeup
- Natural skin texture with visible pores
- Realistic skin, not smoothed

FRAMING:
- Close-up from neck to top of head
- Straight-on, eye level
- Natural outdoor lighting

She should look like she could be related to the reference but NOT the exact same person.
Very similar but with subtle differences."""

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
            image.save("slight_variation_neutral.jpg")
            print("✓ SUCCESS: slight_variation_neutral.jpg")
            break
except Exception as e:
    print(f"Error: {e}")
