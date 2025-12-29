#!/usr/bin/env python3
"""
Generate school-themed bikini variations from reference image.
Swaps yellow → school primary color, pink trim → school secondary color.
"""
import os
import re
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

load_dotenv('.env.local')

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def parse_school_colors(school_name):
    """Parse school colors from txt file."""
    file_path = f"school_colors/{school_name}.txt"

    if not os.path.exists(file_path):
        print(f"❌ Color file not found: {file_path}")
        return None

    with open(file_path, 'r') as f:
        content = f.read()

    # Extract hex colors
    colors = re.findall(r'#[0-9A-Fa-f]{6}', content)

    if len(colors) < 2:
        print(f"❌ Need at least 2 colors for {school_name}")
        return None

    return {
        'primary': colors[0],    # Main bikini color (replaces yellow)
        'secondary': colors[1],  # Trim color (replaces pink)
        'name': school_name.replace('_', ' ')
    }

def generate_bikini_variation(reference_image_path, school_colors, variation_num=1):
    """Generate a single bikini variation with school colors using Gemini."""

    prompt = f"""Transform this bikini to match these EXACT colors:

PRIMARY COLOR (main bikini fabric - currently yellow/lime): {school_colors['primary']}
SECONDARY COLOR (trim/outline - currently pink): {school_colors['secondary']}

Keep everything else IDENTICAL:
- Same exact cut and style
- Same model, pose, and expression
- Same background and lighting
- Only change the bikini colors to the specified hex values

Generate a professional high-quality fashion photograph, 4K resolution."""

    print(f"  → Generating variation {variation_num}...")
    print(f"     Colors: {school_colors['primary']} (main) / {school_colors['secondary']} (trim)")

    # Load reference image
    reference_img = Image.open(reference_image_path)

    # Generate with Gemini image-to-image
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[reference_im1g, prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="3:4",
                image_size="4K"
            )
        )
    )

    # Extract image from response
    for part in response.parts:
        if image := part.as_image():
            return image

    return None

def create_grid(images, output_path, cols=2):
    """Create a grid from list of PIL images."""
    if not images:
        print("❌ No images to create grid")
        return

    # Get max dimensions
    max_w = max(img.width for img in images)
    max_h = max(img.height for img in images)

    rows = (len(images) + cols - 1) // cols

    # Create grid
    grid_w = max_w * cols
    grid_h = max_h * rows
    grid = Image.new('RGB', (grid_w, grid_h), 'white')

    for idx, img in enumerate(images):
        row = idx // cols
        col = idx % cols

        # Resize to match max dimensions
        img_resized = img.resize((max_w, max_h), Image.Resampling.LANCZOS)

        x = col * max_w
        y = row * max_h
        grid.paste(img_resized, (x, y))

    grid.save(output_path, quality=95)
    print(f"✓ Grid saved: {output_path}")

def generate_school_grid(school_name, reference_image, num_variations=4):
    """Generate complete grid for a school."""
    print(f"\n{'='*60}")
    print(f"🎓 Generating {school_name} bikini variations")
    print(f"{'='*60}")

    # Parse colors
    colors = parse_school_colors(school_name)
    if not colors:
        return

    print(f"Primary (main): {colors['primary']}")
    print(f"Secondary (trim): {colors['secondary']}")

    # Create output directory
    output_dir = f"bikinis/{school_name}"
    os.makedirs(f"{output_dir}/variations", exist_ok=True)
    os.makedirs(f"{output_dir}/grids", exist_ok=True)

    # Generate variations
    images = []
    for i in range(num_variations):
        img = generate_bikini_variation(reference_image, colors, i+1)
        if img:
            # Save individual variation
            variation_path = f"{output_dir}/variations/{school_name.lower()}_v{i+1}.png"
            img.save(variation_path)
            print(f"  ✓ Saved: {variation_path}")
            images.append(img)

    # Create grid
    if images:
        grid_path = f"{output_dir}/grids/{school_name.lower()}_grid.jpg"
        create_grid(images, grid_path, cols=2)
        print(f"\n✅ Completed {school_name} - {len(images)} variations")
    else:
        print(f"\n❌ Failed to generate variations for {school_name}")

# Example usage
if __name__ == "__main__":
    # Reference image (yellow bikini with pink trim)
    reference_image = "blonde_athletic_reference.png"

    # Test with Ole Miss only
    print("🏈 SEC Bikini Grid Generator - Ole Miss Test")
    print("Reference:", reference_image)

    try:
        generate_school_grid("Ole_Miss", reference_image, num_variations=4)
    except Exception as e:
        print(f"❌ Error generating Ole Miss: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*60)
    print("✅ All grids generated!")
    print("="*60)
