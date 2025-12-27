#!/usr/bin/env python3
"""
Test replacing bikini on model with sketch design using Gemini image-to-image.
"""
from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')

def replace_bikini_with_design(model_image, design_sketch, design_description):
    """
    Replace the bikini on a model with a new design from a sketch.

    Args:
        model_image: PIL Image of model wearing bikini
        design_sketch: PIL Image of the bikini design sketch
        design_description: Description of the design

    Returns:
        PIL Image of model wearing the new design
    """
    client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

    prompt = f"""Replace the bikini in the first image with the design shown in the second image.

Design to apply: {design_description}

Instructions:
- Keep the model, pose, background, and lighting exactly the same
- Only change the bikini design to match the sketch
- Maintain realistic fit, draping, and fabric behavior on the body
- Preserve all design details from the sketch (colors, patterns, hardware)
- Keep the same bikini style (triangle top, string bottom, etc.) from the sketch
- Make it look natural and photorealistic

The result should look like the model is wearing this specific bikini design."""

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[model_image, design_sketch, prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="16:9",  # Match model image
                image_size="2K"
            )
        )
    )

    # Extract image
    for part in response.parts:
        if part.text:
            print(f"Model response: {part.text}")
        elif image := part.as_image():
            return image

    return None

def main():
    print("Testing bikini replacement with sketch design...")

    # Load model image
    model_image = Image.open("modle/aria/base.jpeg")
    print("✓ Loaded model image: aria/base.jpeg")

    # Load sketch design
    design_sketch = Image.open("bikinis/LSU/lsu_tiger_stripe_black_gold_sketch.png")
    print("✓ Loaded sketch: lsu_tiger_stripe_black_gold")

    # Replace bikini
    print("\nReplacing bikini with tiger stripe design...")
    result = replace_bikini_with_design(
        model_image,
        design_sketch,
        "Black and dark purple tiger stripe bikini with gold chain and belt details"
    )

    if result:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"bikinis/LSU/aria_tiger_stripe_test_{timestamp}.png"
        result.save(output_path)
        print(f"✓ Result saved: {output_path}")
    else:
        print("✗ Failed to generate result")

if __name__ == "__main__":
    main()
