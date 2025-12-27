#!/usr/bin/env python3
import boto3
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
bucket = 'models-aria-bikini'

renames = {
    'face_1.jpeg': 'neutral.jpeg',
    'face_2.jpeg': 'smile_teeth.jpeg',
    'face_3.jpeg': 'smile_soft.jpeg',
    'face_4.jpeg': 'threequarter_left.jpeg',
    'face_5.jpeg': 'threequarter_right.jpeg'
}

for model in ['bella', 'chloe']:
    print(f"Renaming S3 files for {model}...")
    for old, new in renames.items():
        old_key = f"{model}/face_variations/{old}"
        new_key = f"{model}/face_variations/{new}"
        try:
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': old_key},
                Key=new_key
            )
            s3.delete_object(Bucket=bucket, Key=old_key)
            print(f"  ✓ {old} → {new}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

print("\n✓ Done!")
