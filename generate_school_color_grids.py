#!/usr/bin/env python3
"""
Generate school-themed bikini color combination grids.
Creates ONE grid per school showing all color variations.
"""
import os
import re
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from itertools import permutations

load_dotenv('.env.local')

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def parse_school_colors(school_name):
    """Parse school colors from txt file, excluding white."""
    file_path = f"school_colors/{school_name}.txt"

    if not os.path.exists(file_path):
        print(f"❌ Color file not found: {file_path}")
        return None

    with open(file_path, 'r') as f:
        content = f.read()

    # Extract hex colors
    all_colors = re.findall(r'#[0-9A-Fa-f]{6}', content)

    # Filter out white
    colors = [c for c in all_colors if c.upper() not in ['#FFFFFF', '#FFF']]

    if len(colors) < 2:
        print(f"❌ Need at least 2 non-white colors for {school_name}")
        return None

    return {
        'colors': colors,
        'name': school_name.replace('_', ' ')
    }

def get_color_combinations(colors):
    """Generate all (primary, secondary) color combinations."""
    combos = []
    # All permutations of 2 colors
    for perm in permutations(colors, 2):
        combos.append({'primary': perm[0], 'secondary': perm[1]})
    return combos

def generate_single_bikini(reference_image_path, primary_color, secondary_color):
    """Generate ONE bikini image with specific colors."""

    prompt = f"""Transform this bikini to match these EXACT colors:

PRIMARY COLOR (main bikini fabric): {primary_color}
SECONDARY COLOR (trim/outline/straps): {secondary_color}

Keep EVERYTHING else identical:
- Same exact cut, style, and coverage
- Same model, pose, and expression
- Same background and lighting
- ONLY change bikini colors to specified hex values

Professional fashion photography, 4K quality."""

    # Load reference image
    reference_img = Image.open(reference_image_path)

    # Generate with Gemini
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[reference_img, prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="3:4",
                image_size="2K"  # Using 2K for faster generation
            )
        )
    )

    # Extract image
    for part in response.parts:
        if image := part.as_image():
            return image

    return None

def create_color_grid(school_name, reference_image):
    """Generate ONE grid showing all color combinations for a school."""
    print(f"\n{'='*60}")
    print(f"🎓 {school_name} - Color Combination Grid")
    print(f"{'='*60}")

    # Get school colors
    school_data = parse_school_colors(school_name)
    if not school_data:
        return

    colors = school_data['colors']
    print(f"Colors: {', '.join(colors)}")

    # Get all color combinations
    combos = get_color_combinations(colors)
    print(f"Generating {len(combos)} combinations...")

    # Create output directory
    output_dir = f"bikinis/{school_name}/grids"
    os.makedirs(output_dir, exist_ok=True)

    # Generate each combination
    images = []
    for i, combo in enumerate(combos, 1):
        print(f"\n  [{i}/{len(combos)}] {combo['primary']} + {combo['secondary']}")

        img = generate_single_bikini(
            reference_image,
            combo['primary'],
            combo['secondary']
        )

        if img:
            # Save to temp location
            temp_path = f"{output_dir}/temp_{i}.png"
            img.save(temp_path)
            images.append(Image.open(temp_path))
            print(f"  ✓ Generated")
        else:
            print(f"  ❌ Failed")

    # Create grid layout
    if images:
        print(f"\n📐 Creating {len(images)}-image grid...")

        # Determine grid layout (2 or 3 columns)
        cols = 2 if len(images) <= 4 else 3
        rows = (len(images) + cols - 1) // cols

        # Get cell dimensions
        cell_w = images[0].width
        cell_h = images[0].height

        # Create grid canvas
        grid = Image.new('RGB', (cell_w * cols, cell_h * rows), 'white')

        # Paste images
        for idx, img in enumerate(images):
            row = idx // cols
            col = idx % cols
            x = col * cell_w
            y = row * cell_h
            grid.paste(img, (x, y))

        # Save final grid
        grid_path = f"{output_dir}/{school_name.lower()}_colorways.jpg"
        grid.save(grid_path, quality=95)
        print(f"✅ Grid saved: {grid_path}")

        # Clean up temp files
        for i in range(1, len(images) + 1):
            temp_path = f"{output_dir}/temp_{i}.png"
            if os.path.exists(temp_path):
                os.remove(temp_path)

    else:
        print(f"❌ No images generated for {school_name}")

# Main execution
if __name__ == "__main__":
    reference_image = "blonde_athletic_reference.png"

    schools = [
        "Alabama",
        "LSU",
        "Ole_Miss",
        "Georgia",
        "Texas_AM",
        "Florida"
    ]

    print("🏈 SEC School Color Grid Generator")
    print(f"Reference: {reference_image}")
    print(f"Schools: {', '.join(schools)}\n")

    for school in schools:
        try:
            create_color_grid(school, reference_image)
        except Exception as e:
            print(f"\n❌ Error with {school}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*60)
    print("✅ All school grids complete!")
    print("="*60)
