#!/usr/bin/env python3
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

combos = [
    {"primary": "#461D7C", "secondary": "#FDD023", "name": "Purple + Gold"},
    {"primary": "#FDD023", "secondary": "#461D7C", "name": "Gold + Purple"},
    {"primary": "#461D7C", "secondary": "#FFFFFF", "name": "Purple + White"},
    {"primary": "#FDD023", "secondary": "#FFFFFF", "name": "Gold + White"}
]

combo_text = "\n".join([f"{i+1}. Main: {c['primary']}, Trim: {c['secondary']}" for i, c in enumerate(combos)])

ref_img = Image.open("bikini_downloads/_thebikinibeauty_/3680166047550738239_71861451332.jpg")

prompt = f"""Create a 2x2 grid showing 4 LSU bikini colorways:
{combo_text}

Same style as reference, blonde model, same pose, professional photography."""

print("Generating LSU...")
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[ref_img, prompt],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="1:1", image_size="4K")
    )
)

for part in response.parts:
    if img := part.as_image():
        os.makedirs("bikinis/LSU/grids", exist_ok=True)
        path = f"bikinis/LSU/grids/lsu_grid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        img.save(path)
        print(f"✅ {path}")
