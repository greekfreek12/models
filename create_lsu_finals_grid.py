#!/usr/bin/env python3
"""
Create a grid of LSU final designs from ready folder.
"""
from PIL import Image
import os

def create_grid(image_paths, output_path, cols=3):
    """Create a grid from list of images."""
    images = [Image.open(p) for p in image_paths]

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
        img_resized = img.resize((max_w, max_h))

        x = col * max_w
        y = row * max_h
        grid.paste(img_resized, (x, y))

    grid.save(output_path)
    print(f"✓ Grid saved: {output_path}")

# Get all LSU ready designs
ready_dir = "bikinis/LSU/ready"
designs = [
    f"{ready_dir}/purple_reign.jpeg",
    f"{ready_dir}/gameday_classic.png",
    f"{ready_dir}/eye_of_the_tiger.jpeg",
    f"{ready_dir}/royal_gator.jpeg",
    f"{ready_dir}/royal_gator_v2.png"
]

create_grid(designs, "bikinis/LSU/grids/finals_grid.jpg", cols=3)
