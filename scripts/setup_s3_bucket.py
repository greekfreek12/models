#!/usr/bin/env python3
import boto3
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Get AWS credentials
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

print(f"AWS Region: {aws_region}")

# Create S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

bucket_name = 'models-aria-bikini'

# Create the bucket
try:
    print(f"\nCreating S3 bucket: {bucket_name}")
    if aws_region == 'us-east-1':
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': aws_region}
        )
    print(f"✓ Bucket '{bucket_name}' created successfully")
except s3_client.exceptions.BucketAlreadyOwnedByYou:
    print(f"✓ Bucket '{bucket_name}' already exists and is owned by you")
except s3_client.exceptions.BucketAlreadyExists:
    print(f"✗ Bucket '{bucket_name}' already exists (owned by someone else)")
    exit(1)
except Exception as e:
    print(f"Error creating bucket: {e}")
    exit(1)

# Upload Aria's base image
base_image_path = Path("modle/aria/base.jpeg")
s3_key = "aria/base.jpeg"

print(f"\nUploading {base_image_path} to s3://{bucket_name}/{s3_key}")
try:
    s3_client.upload_file(
        str(base_image_path),
        bucket_name,
        s3_key,
        ExtraArgs={'ContentType': 'image/jpeg'}
    )
    print(f"✓ Uploaded successfully")

    # Generate URL
    url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{s3_key}"
    print(f"\nImage URL: {url}")

except Exception as e:
    print(f"✗ Error uploading file: {e}")
    exit(1)

print("\n✓ Setup complete!")
print(f"  Bucket: {bucket_name}")
print(f"  Model: aria")
print(f"  Base image: {s3_key}")
