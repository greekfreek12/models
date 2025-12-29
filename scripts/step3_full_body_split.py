from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

print("=== TASK 1: Age Regression (30 -> 18 years old) ===")
ref_30yo = PILImage.open("/workspaces/models/archived_images/28a419a0-c968-4a99-b91a-9540e03f9f4e.jpeg")

PROMPT_AGE = """This reference shows a 30-year-old woman.

Generate a face portrait of the same woman when she was 18 years old.

KEY REQUIREMENTS:
- Same facial structure and features
- Same hair color and eye color
- Younger, softer facial features (less defined bone structure)
- Slightly fuller cheeks, more youthful skin
- Natural skin texture with visible pores
- Neutral expression
- 2:3 portrait framing

Make her look 18, not 30."""

response1 = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[ref_30yo, PROMPT_AGE],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="2:3", image_size="2K")
    )
)

if response1.candidates and response1.candidates[0].content.parts:
    for part in response1.candidates[0].content.parts:
        if hasattr(part, 'inline_data'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"age_regression_18yo_{timestamp}.jpg"
            with open(filename, "wb") as f:
                f.write(part.inline_data.data)
            print(f"✓ Saved: {filename}")

print("\n=== TASK 2: Crop Top Panel ===")
grid = PILImage.open("/workspaces/models/archived_images/28a419a0-c968-4a99-b91a-9540e03f9f4e.jpeg")
width, height = grid.size
top_panel = grid.crop((0, 0, width, height//3))
top_panel.save("cropped_top_panel.jpg")
print(f"✓ Saved: cropped_top_panel.jpg")

print("\n=== TASK 3: Enhanced Realistic Texture ===")
ref_texture = PILImage.open("/workspaces/models/archived_images/e6a6421a-a9d6-4d71-82dc-a265288b6392.jpeg")

PROMPT_TEXTURE = """Same exact person, same pose, same setting, same lighting, same everything.

ONLY enhance the skin texture:
- More visible pores across face and body
- More realistic skin texture
- Natural imperfections
- Slightly more detailed skin surface

Keep everything else identical - same face, same pose, same bikini, same background, same composition."""

response3 = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[ref_texture, PROMPT_TEXTURE],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="2:3", image_size="2K")
    )
)

if response3.candidates and response3.candidates[0].content.parts:
    for part in response3.candidates[0].content.parts:
        if hasattr(part, 'inline_data'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_texture_{timestamp}.jpg"
            with open(filename, "wb") as f:
                f.write(part.inline_data.data)
            print(f"✓ Saved: {filename}")

print("\n=== All tasks completed ===")
