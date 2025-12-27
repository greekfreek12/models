#!/usr/bin/env python3
"""
Refine bikini sketches from grid into photorealistic product shots using Gemini 3 Pro Image Preview.
"""
from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')

def extract_grid_cell(grid_image_path, row, col, grid_rows=2, grid_cols=3):
    """
    Extract a specific cell from a grid image.

    Args:
        grid_image_path: Path to the grid image
        row: Row index (0-based, 0 = top)
        col: Column index (0-based, 0 = left)
        grid_rows: Total number of rows in grid
        grid_cols: Total number of columns in grid

    Returns:
        PIL Image of the extracted cell
    """
    img = Image.open(grid_image_path)
    width, height = img.size

    cell_width = width // grid_cols
    cell_height = height // grid_rows

    left = col * cell_width
    top = row * cell_height
    right = left + cell_width
    bottom = top + cell_height

    return img.crop((left, top, right, bottom))

def refine_sketch_to_product(sketch_image, design_description, client):
    """
    Transform a bikini sketch into a photorealistic product shot.

    Args:
        sketch_image: PIL Image of the sketch
        design_description: Brief description of the design (for context)
        client: Gemini API client

    Returns:
        PIL Image of the refined product
    """
    prompt = f"""Transform this bikini sketch into a photorealistic product shot.

Design: {design_description}

Requirements:
- Professional swimwear photography quality
- Detailed fabric texture and material realism
- Realistic construction (stitching, seams, hardware)
- Flat lay on white background or on form/mannequin
- High-end luxury swimwear brand aesthetic
- Sharp details, proper lighting and shadows
- Show the bikini as a real, manufactured product

Keep the EXACT design, colors, patterns, and style from the sketch.
Just make it look like a real bikini you could purchase."""

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[sketch_image, prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="1:1",  # Product shot format
                image_size="4K"      # High detail
            )
        )
    )

    # Extract the image from response
    for part in response.parts:
        if part.text:
            print(f"Model response: {part.text}")
        elif image := part.as_image():
            return image

    return None

def main():
    # Initialize Gemini client
    client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

    # Grid source
    grid_path = "bikinis/LSU/lsu_bikini_grid_20251227_123117.jpg"

    # Designs to refine (from user's selection)
    designs = [
        {
            "row": 0,
            "col": 1,
            "name": "lsu_logo_white_cream",
            "description": "White and cream bikini with LSU logos and purple trim"
        },
        {
            "row": 1,
            "col": 1,
            "name": "lsu_tiger_stripe_black_gold",
            "description": "Black tiger stripe bikini with gold belt and chain details"
        }
    ]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for design in designs:
        print(f"\n{'='*60}")
        print(f"Processing: {design['name']}")
        print(f"Position: Row {design['row']}, Col {design['col']}")
        print(f"{'='*60}")

        # Step 1: Extract from grid
        print("Extracting design from grid...")
        sketch = extract_grid_cell(grid_path, design['row'], design['col'])

        # Save extracted sketch
        sketch_filename = f"bikinis/LSU/{design['name']}_sketch.png"
        sketch.save(sketch_filename)
        print(f"✓ Sketch saved: {sketch_filename}")

        # Step 2: Refine to product
        print("Refining sketch to photorealistic product...")
        product = refine_sketch_to_product(sketch, design['description'], client)

        if product:
            product_filename = f"bikinis/LSU/{design['name']}_product_{timestamp}.png"
            product.save(product_filename)
            print(f"✓ Product saved: {product_filename}")
        else:
            print(f"✗ Failed to generate product for {design['name']}")

    print(f"\n{'='*60}")
    print("All designs processed!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
