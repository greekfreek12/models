#!/usr/bin/env python3
"""
Extract LSU baseball/logo design from grid.
"""
from PIL import Image

def extract_grid_cell(grid_image_path, row, col, grid_rows=2, grid_cols=3):
    """Extract a specific cell from grid."""
    img = Image.open(grid_image_path)
    width, height = img.size

    cell_width = width // grid_cols
    cell_height = height // grid_rows

    left = col * cell_width
    top = row * cell_height
    right = left + cell_width
    bottom = top + cell_height

    return img.crop((left, top, right, bottom))

# Extract middle top (baseball/logo design)
grid_path = "bikinis/LSU/grids/lsu_bikini_grid_20251227_123117.jpg"
baseball = extract_grid_cell(grid_path, 0, 1)
baseball.save("bikinis/LSU/ready/lsu_logo_white_cream.png")
print("✓ Extracted baseball/logo design to ready/")
