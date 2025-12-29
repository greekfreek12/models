#!/usr/bin/env python3
"""
Generate both 2x2 grids (Batch 1 and Batch 2)
"""

import subprocess
import time

print("\n" + "="*60)
print("GENERATING BOTH 2x2 GRIDS")
print("="*60)
print("Batch 1: Models 1-4")
print("Batch 2: Models 5-8")
print("="*60 + "\n")

# Generate Batch 1
print("Starting Batch 1...\n")
result1 = subprocess.run(['python', 'generate_grid.py', '1'])

if result1.returncode == 0:
    print("\n✓ Batch 1 complete")
    time.sleep(3)
else:
    print("\n❌ Batch 1 failed")

# Generate Batch 2
print("\nStarting Batch 2...\n")
result2 = subprocess.run(['python', 'generate_grid.py', '2'])

if result2.returncode == 0:
    print("\n✓ Batch 2 complete")
else:
    print("\n❌ Batch 2 failed")

print("\n" + "="*60)
print("BOTH GRIDS COMPLETE")
print("="*60)
print("Review:")
print("  - grid_batch1.png (Models 1-4)")
print("  - grid_batch2.png (Models 5-8)")
print("\nTell me which faces you like!\n")
