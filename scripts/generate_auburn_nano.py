#!/usr/bin/env python3
"""Generate Auburn bikini designs using nano-banana-pro"""
import replicate
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Verify token loaded
token = os.getenv('REPLICATE_API_TOKEN')
if not token:
    raise ValueError("REPLICATE_API_TOKEN not found in .env.local")
print(f"🔑 Using token: {token[:10]}...")

# Create Replicate client
client = replicate.Client(api_token=token)

# Auburn design prompts
AUBURN_DESIGNS = {
    "tiger_stripes_navy": "Replace the bikini with my Auburn Tiger Stripes design - bold diagonal tiger stripes in deep navy blue and burnt orange that run across the entire suit. I want that fierce tiger print energy with irregular stripe widths to mimic real tiger fur. This is our statement piece - aggressive, bold, unmistakably Auburn Tigers. Keep everything else exactly the same - same pose, model, background, lighting.",

    "tiger_stripes_white": "Replace the bikini with my Tiger Stripes White variation - it's a fresh white base with navy and burnt orange tiger stripes layered on top. The white peeks through between the stripes for a lighter, cleaner look while still having that tiger ferocity. Perfect for gameday pool parties. Keep everything else exactly the same - same pose, model, background, lighting.",

    "toomers_oaks": "Replace the bikini with my Toomer's Oaks design celebrating Auburn's iconic tradition - white bikini with navy oak tree silhouettes and burnt orange and white toilet paper streamers dramatically draped from the branches. Small oak trees on the top cups, larger centerpiece tree on the bottom with TP flowing down. Every Auburn fan knows Toomer's Corner - this is that celebration captured on a bikini. Keep everything else exactly the same - same pose, model, background, lighting.",

    "war_eagle_navy": "Replace the bikini with my War Eagle Navy design - deep navy blue base covered with burnt orange eagle silhouettes in dynamic flight poses. Eagles scattered across the top and bottom, all positioned at different angles like they're soaring through the sky. Pure Auburn mascot pride, no text needed. Keep everything else exactly the same - same pose, model, background, lighting.",

    "war_eagle_white": "Replace the bikini with my War Eagle White design - clean white base with navy blue and burnt orange eagle silhouettes flying across it. The eagles alternate colors and flight positions for visual interest. It's the lighter, more versatile version of our War Eagle collection while still being unmistakably Auburn. Keep everything else exactly the same - same pose, model, background, lighting."
}

# Base image
BASE_IMAGE = "modle/amber/base.jpeg"

def generate_design(design_name, prompt, base_image_path):
    """Generate single Auburn design"""
    print(f"\n🎨 Generating: {design_name}")

    try:
        # Open and upload the base image
        with open(base_image_path, "rb") as image_file:
            output = client.run(
                "google/nano-banana-pro",
                input={
                    "prompt": prompt,
                    "image_input": [image_file],
                    "resolution": "2K",
                    "aspect_ratio": "match_input_image",
                    "output_format": "png",
                    "safety_filter_level": "block_only_high"
                }
            )

        # Get image URL
        if isinstance(output, list):
            image_url = output[0]
        else:
            image_url = str(output)

        print(f"✅ Generated: {image_url}")

        # Download the image
        output_dir = Path("bikinis/Auburn/on_models")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{design_name}.png"

        print(f"⬇️  Downloading to: {output_path}")
        response = requests.get(image_url)
        output_path.write_bytes(response.content)

        print(f"💾 Saved: {output_path}")
        return str(output_path)

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🏈 Auburn Bikini Generator - nano-banana-pro")
    print("=" * 60)
    print(f"Base image: {BASE_IMAGE}")
    print(f"Designs: {len(AUBURN_DESIGNS)}")
    print("=" * 60)

    results = {}
    for design_name, prompt in AUBURN_DESIGNS.items():
        result = generate_design(design_name, prompt, BASE_IMAGE)
        results[design_name] = result

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    for name, path in results.items():
        status = "✅" if path else "❌"
        print(f"{status} {name}: {path}")

if __name__ == "__main__":
    main()
