#!/usr/bin/env python3
"""
Crop left face from grid and cleanup test files
"""

from PIL import Image
import os
import glob

# Crop left face from the 1x2 grid
print("Cropping left face from grid...")
grid_img = Image.open("lsu_blonde_face_grid.jpg")
width, height = grid_img.size

# Grid is 1x2 (side by side), so left half is 0 to width/2
left_face = grid_img.crop((0, 0, width//2, height))
left_face.save("lsu_blonde_keeper_2.jpg", quality=95)
print(f"✓ Saved cropped left face: lsu_blonde_keeper_2.jpg")

# Keep the first good one
print("\nKeeping first blonde...")
if os.path.exists("lsu_blonde_southern_belle.jpg"):
    os.rename("lsu_blonde_southern_belle.jpg", "lsu_blonde_keeper_1.jpg")
    print(f"✓ Renamed to: lsu_blonde_keeper_1.jpg")

# Delete all test generation files
print("\nCleaning up test files...")
test_files = [
    "lsu_blonde_face_grid.jpg",
    "lsu_brunette_face_grid.jpg",
    "lsu_blonde_v2_neutral.jpg",
    "lsu_blonde_v3_neutral.jpg",
    "lsu_blonde_v4_creative.jpg",
    "lsu_blonde_grid_2x2_test.png",
    "lsu_brunette_grid_2x2_test.png",
    "generate_lsu_face_grids.py",
    "generate_lsu_blonde_single.py",
    "generate_lsu_blonde_v2.py",
    "generate_lsu_blonde_variations.py",
    "generate_lsu_test_grids.py"
]

for file in test_files:
    if os.path.exists(file):
        os.remove(file)
        print(f"  Deleted: {file}")

print("\n" + "="*60)
print("DONE!")
print("="*60)
print("\nKept:")
print("  - lsu_blonde_keeper_1.jpg (smiling one)")
print("  - lsu_blonde_keeper_2.jpg (neutral one, cropped from grid)")
print("\nAll test files cleaned up.\n")
