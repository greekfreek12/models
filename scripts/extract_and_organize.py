#!/usr/bin/env python3
"""Extract individual colorways from grids and organize with descriptions."""
import os
from PIL import Image
from datetime import datetime

BIKINI_NAME = "GameDay_Luxe"

# Define what to keep from each school
SELECTIONS = {
    "Alabama": {
        "grid": "bikinis/Alabama/grids/alabama_grid_20251227_202552.jpg",
        "layout": "1x2",
        "keep": [0, 1],  # Both
        "colorways": [
            {"name": "Crimson_Gray", "desc": "Alabama Crimson + Gray", "primary": "#9E1B32", "secondary": "#828A8F"},
            {"name": "Crimson_White", "desc": "Alabama Crimson + White", "primary": "#9E1B32", "secondary": "#FFFFFF"}
        ]
    },
    "Tennessee": {
        "grid": "bikinis/Tennessee/grids/tennessee_grid_20251227_202521.jpg",
        "layout": "1x2",
        "keep": [1],  # Right one
        "colorways": [
            None,  # Skip left
            {"name": "Orange_White", "desc": "Tennessee Orange + White", "primary": "#FF8200", "secondary": "#FFFFFF"}
        ]
    },
    "Florida": {
        "grid": "bikinis/Florida/grids/florida_grid_20251227_203102.jpg",
        "layout": "2x2",
        "keep": [0, 1],  # Top 2
        "colorways": [
            {"name": "Blue_Orange", "desc": "Florida Blue + Orange", "primary": "#0021A5", "secondary": "#FA4616"},
            {"name": "Orange_Blue", "desc": "Florida Orange + Blue", "primary": "#FA4616", "secondary": "#0021A5"},
            None,
            None
        ]
    },
    "Ole_Miss": {
        "grid": "bikinis/Ole_Miss/grids/ole_miss_grid_20251227_203137.jpg",
        "layout": "2x2",
        "keep": [0, 1],  # Top 2
        "colorways": [
            {"name": "Red_PowderBlue", "desc": "Ole Miss Red + Powder Blue", "primary": "#CE1126", "secondary": "#006BA6"},
            {"name": "PowderBlue_Red", "desc": "Ole Miss Powder Blue + Red", "primary": "#006BA6", "secondary": "#CE1126"},
            None,
            None
        ]
    },
    "Georgia": {
        "grid": "bikinis/Georgia/grids/georgia_grid_20251227_203625.jpg",
        "layout": "2x2",
        "keep": [0, 1],  # Top 2
        "colorways": [
            {"name": "Red_Black", "desc": "Georgia Red + Black", "primary": "#BA0C2F", "secondary": "#000000"},
            {"name": "Black_Red", "desc": "Georgia Black + Red", "primary": "#000000", "secondary": "#BA0C2F"},
            None,
            None
        ]
    },
    "LSU": {
        "grid": "bikinis/LSU/grids/lsu_grid_20251227_204522.jpg",
        "layout": "2x2",
        "keep": [0, 1],  # Top 2
        "colorways": [
            {"name": "Purple_Gold", "desc": "LSU Purple + Gold", "primary": "#461D7C", "secondary": "#FDD023"},
            {"name": "Gold_Purple", "desc": "LSU Gold + Purple", "primary": "#FDD023", "secondary": "#461D7C"},
            None,
            None
        ]
    },
    "Vanderbilt": {
        "grid": "bikinis/Vanderbilt/grids/vanderbilt_grid_20251227_203702.jpg",
        "layout": "2x2",
        "keep": [0, 1],  # Top 2
        "colorways": [
            {"name": "Gold_Black", "desc": "Vanderbilt Gold + Black", "primary": "#866D4B", "secondary": "#000000"},
            {"name": "Black_Gold", "desc": "Vanderbilt Black + Gold", "primary": "#000000", "secondary": "#866D4B"},
            None,
            None
        ]
    }
}

def crop_from_grid(grid_path, layout, position):
    """Crop a specific position from a grid."""
    img = Image.open(grid_path)
    width, height = img.size

    if layout == "1x2":
        # 1 row, 2 columns
        cell_w = width // 2
        cell_h = height
        col = position % 2
        box = (col * cell_w, 0, (col + 1) * cell_w, cell_h)
    else:  # 2x2
        # 2 rows, 2 columns
        cell_w = width // 2
        cell_h = height // 2
        row = position // 2
        col = position % 2
        box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)

    return img.crop(box)

def create_description_file(path, school, colorway_info):
    """Create a txt file with colorway description."""
    content = f"""{BIKINI_NAME} - {colorway_info['desc']}

School: {school}
Style: {BIKINI_NAME}
Colorway: {colorway_info['name'].replace('_', ' ')}

Colors:
- Primary (main fabric): {colorway_info['primary']}
- Secondary (trim/outline): {colorway_info['secondary']}

Description:
Premium minimal coverage triangle bikini in official {school} team colors.
Features ultra-thin straps and barely-there brazilian cut bottom.
{colorway_info['desc']} colorway.

Generated: {datetime.now().strftime('%Y-%m-%d')}
"""

    with open(path, 'w') as f:
        f.write(content)

def extract_and_organize():
    """Extract colorways and organize into new structure."""

    # Create output directory
    output_base = f"bikinis/universal/{BIKINI_NAME}/teams"
    os.makedirs(output_base, exist_ok=True)

    # Copy reference image
    ref_src = "bikini_downloads/_thebikinibeauty_/3680166047550738239_71861451332.jpg"
    ref_dst = f"bikinis/universal/{BIKINI_NAME}/reference.jpg"
    os.makedirs(os.path.dirname(ref_dst), exist_ok=True)
    Image.open(ref_src).save(ref_dst)
    print(f"✓ Reference saved: {ref_dst}")

    print(f"\n{'='*60}")
    print(f"Extracting colorways for {BIKINI_NAME}")
    print(f"{'='*60}\n")

    total = 0

    for school, data in SELECTIONS.items():
        print(f"\n{school}:")

        for position in data['keep']:
            colorway = data['colorways'][position]
            if colorway is None:
                continue

            # Crop image
            cropped = crop_from_grid(data['grid'], data['layout'], position)

            # Save image
            img_filename = f"{school}_{colorway['name']}.jpg"
            img_path = os.path.join(output_base, img_filename)
            cropped.save(img_path, quality=95)

            # Save description
            txt_filename = f"{school}_{colorway['name']}.txt"
            txt_path = os.path.join(output_base, txt_filename)
            create_description_file(txt_path, school, colorway)

            print(f"  ✓ {img_filename}")
            print(f"  ✓ {txt_filename}")
            total += 1

    print(f"\n{'='*60}")
    print(f"✅ Extracted {total} colorways to:")
    print(f"   {output_base}/")
    print(f"{'='*60}")

if __name__ == "__main__":
    extract_and_organize()
