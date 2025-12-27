#!/usr/bin/env python3
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

bucket_name = 'models-aria-bikini'

# Remove block public access settings
print(f"Removing block public access settings for {bucket_name}...")
try:
    s3_client.delete_public_access_block(Bucket=bucket_name)
    print("✓ Public access block removed")
except Exception as e:
    print(f"Note: {e}")

# Set bucket policy to allow public read
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }
    ]
}

print(f"\nSetting bucket policy for public read access...")
try:
    s3_client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(bucket_policy)
    )
    print("✓ Bucket policy set successfully")
    print(f"\n✓ Bucket {bucket_name} is now publicly accessible for reading")
except Exception as e:
    print(f"✗ Error: {e}")
