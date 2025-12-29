#!/usr/bin/env python3
"""
Step 2: Post a single image to Instagram

Usage:
    python post_image.py path/to/image.jpg "Your caption here"
"""

import requests
import sys
import time
from config import ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID

def post_image(image_url, caption):
    """
    Post a single image to Instagram

    Args:
        image_url: Public URL to your image (must be hosted online)
        caption: Caption for your post
    """

    if not INSTAGRAM_ACCOUNT_ID:
        print("❌ Error: INSTAGRAM_ACCOUNT_ID not set in config.py")
        print("   Run verify_token.py first to get your account ID")
        return False

    print(f"📸 Posting image to Instagram...\n")

    # Step 1: Create a media container
    create_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
    create_params = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }

    try:
        print("⏳ Creating media container...")
        response = requests.post(create_url, data=create_params)
        response.raise_for_status()
        container_id = response.json()["id"]
        print(f"✅ Container created: {container_id}\n")

        # Step 2: Publish the container
        # Wait a moment for Instagram to process the image
        print("⏳ Waiting for Instagram to process image...")
        time.sleep(5)

        publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        publish_params = {
            "creation_id": container_id,
            "access_token": ACCESS_TOKEN
        }

        print("⏳ Publishing post...")
        publish_response = requests.post(publish_url, data=publish_params)
        publish_response.raise_for_status()
        media_id = publish_response.json()["id"]

        print(f"✅ Successfully posted to Instagram!")
        print(f"   Media ID: {media_id}")
        print(f"   Check your Instagram profile to see the post!\n")

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return False

def post_local_image(image_path, caption):
    """
    Post a local image file (you'll need to host it first)
    """
    print("❌ Error: Instagram API requires publicly accessible image URLs")
    print("   You need to:")
    print("   1. Upload your image to a hosting service (Imgur, AWS S3, etc.)")
    print("   2. Use the public URL with post_image()")
    print("\n   For local testing, you can use ngrok or a similar service")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python post_image.py <image_url> <caption>")
        print("\nExample:")
        print('  python post_image.py "https://example.com/image.jpg" "Check out my new AI-generated design!"')
        sys.exit(1)

    image_url = sys.argv[1]
    caption = sys.argv[2]

    post_image(image_url, caption)
