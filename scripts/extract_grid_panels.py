#!/usr/bin/env python3
"""
Extract individual panels from 3x3 grid
"""

from PIL import Image
from pathlib import Path

# Input grid
GRID_PATH = Path("models_2.0/veronica/greek_grid_identity_replaced.png")
OUTPUT_DIR = Path("models_2.0/veronica/panels")

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_panels():
    """Extract 9 panels from 3x3 grid"""

    print(f"\n{'='*60}")
    print(f"EXTRACTING GRID PANELS")
    print(f"{'='*60}")
    print(f"Input: {GRID_PATH}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"")

    # Load grid image
    print("Loading grid image...")
    img = Image.open(GRID_PATH)
    width, height = img.size
    print(f"Grid size: {width}x{height}")

    # Calculate panel dimensions (3x3 grid)
    panel_width = width // 3
    panel_height = height // 3
    print(f"Panel size: {panel_width}x{panel_height}")
    print(f"")

    # Panel labels for 3x3 grid
    panel_names = [
        "1_santorini_oia",
        "2_mykonos_windmills",
        "3_zakynthos_cliff",
        "4_crete_pink_sand",
        "5_milos_moonscape",
        "6_santorini_pool",
        "7_mykonos_venice",
        "8_corfu_canal",
        "9_paros_sunset"
    ]

    # Extract each panel
    panel_index = 0
    for row in range(3):
        for col in range(3):
            # Calculate crop coordinates
            left = col * panel_width
            top = row * panel_height
            right = left + panel_width
            bottom = top + panel_height

            # Crop panel
            panel = img.crop((left, top, right, bottom))

            # Save panel
            panel_name = panel_names[panel_index]
            output_path = OUTPUT_DIR / f"panel_{panel_name}.jpeg"
            panel.save(output_path, quality=95)

            print(f"✓ Extracted: panel_{panel_name}.jpeg")
            panel_index += 1

    print(f"\n{'='*60}")
    print(f"✓ SUCCESS!")
    print(f"{'='*60}")
    print(f"Extracted 9 panels to: {OUTPUT_DIR}")
    print(f"\nPanel files:")
    for i, name in enumerate(panel_names, 1):
        print(f"  {i}. panel_{name}.jpeg")

if __name__ == "__main__":
    extract_panels()
