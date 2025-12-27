#!/usr/bin/env python3
import boto3
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')

# AWS setup
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
bucket = 'models-aria-bikini'
region = os.getenv('AWS_REGION')

# Model definitions
models = {
    'aria': {
        'current_file': 'modle/aria/base.jpeg',
        'new_name': 'base.jpeg'
    },
    'bella': {  # Brunette
        'current_file': 'Generated Image December 27, 2025 - 9_56AM.jpeg',
        'new_name': 'base.jpeg'
    },
    'chloe': {  # Blonde
        'current_file': 'Generated Image December 27, 2025 - 9_57AM.jpeg',
        'new_name': 'base.jpeg'
    }
}

# Face variation names
face_variations = {
    'face_1.jpeg': 'neutral.jpeg',
    'face_2.jpeg': 'smile_teeth.jpeg',
    'face_3.jpeg': 'smile_soft.jpeg',
    'face_4.jpeg': 'threequarter_left.jpeg',
    'face_5.jpeg': 'threequarter_right.jpeg'
}

print("Setting up model structure...\n")

# Setup Aria (already exists, just rename variations)
print("1. Renaming Aria's face variations...")
aria_face_dir = Path('modle/aria/face_variations')
if aria_face_dir.exists():
    for old_name, new_name in face_variations.items():
        old_path = aria_face_dir / old_name
        new_path = aria_face_dir / new_name
        if old_path.exists():
            shutil.move(str(old_path), str(new_path))
            print(f"  ✓ Renamed: {old_name} → {new_name}")

            # Update S3
            old_s3_key = f"aria/face_variations/{old_name}"
            new_s3_key = f"aria/face_variations/{new_name}"
            try:
                s3.copy_object(
                    Bucket=bucket,
                    CopySource={'Bucket': bucket, 'Key': old_s3_key},
                    Key=new_s3_key
                )
                s3.delete_object(Bucket=bucket, Key=old_s3_key)
                print(f"    ✓ Updated S3: {new_s3_key}")
            except:
                pass

# Setup Bella (brunette)
print("\n2. Setting up Bella (brunette)...")
bella_dir = Path('modle/bella')
bella_dir.mkdir(parents=True, exist_ok=True)
bella_base = bella_dir / 'base.jpeg'
shutil.copy(models['bella']['current_file'], bella_base)
print(f"  ✓ Created: {bella_base}")

# Upload to S3
with open(bella_base, 'rb') as f:
    s3.put_object(
        Bucket=bucket,
        Key='bella/base.jpeg',
        Body=f,
        ContentType='image/jpeg'
    )
print(f"  ✓ Uploaded to S3: bella/base.jpeg")

# Setup Chloe (blonde)
print("\n3. Setting up Chloe (blonde)...")
chloe_dir = Path('modle/chloe')
chloe_dir.mkdir(parents=True, exist_ok=True)
chloe_base = chloe_dir / 'base.jpeg'
shutil.copy(models['chloe']['current_file'], chloe_base)
print(f"  ✓ Created: {chloe_base}")

# Upload to S3
with open(chloe_base, 'rb') as f:
    s3.put_object(
        Bucket=bucket,
        Key='chloe/base.jpeg',
        Body=f,
        ContentType='image/jpeg'
    )
print(f"  ✓ Uploaded to S3: chloe/base.jpeg")

# Clean up temp files
print("\n4. Cleaning up...")
os.remove(models['bella']['current_file'])
os.remove(models['chloe']['current_file'])
print("  ✓ Removed temporary image files")

print("\n✓ Setup complete!")
print(f"\nModel structure:")
print(f"  Local: modle/aria/, modle/bella/, modle/chloe/")
print(f"  S3: s3://{bucket}/aria/, s3://{bucket}/bella/, s3://{bucket}/chloe/")
print(f"\nFace variation names:")
for new_name in face_variations.values():
    print(f"  - {new_name}")
