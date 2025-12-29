#!/usr/bin/env python3
"""
Step 1: Verify your Instagram API token and get your Instagram Business Account ID
"""

import requests
import json
from config import ACCESS_TOKEN

def verify_token():
    """Verify the access token and get account information"""

    print("🔍 Verifying your Instagram API token...\n")

    # First, get the Facebook Page ID
    url = f"https://graph.facebook.com/v18.0/me/accounts"
    params = {"access_token": ACCESS_TOKEN}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            page = data["data"][0]
            page_id = page["id"]
            page_name = page["name"]

            print(f"✅ Found Facebook Page: {page_name}")
            print(f"   Page ID: {page_id}\n")

            # Now get the Instagram Business Account ID
            ig_url = f"https://graph.facebook.com/v18.0/{page_id}"
            ig_params = {
                "fields": "instagram_business_account",
                "access_token": ACCESS_TOKEN
            }

            ig_response = requests.get(ig_url, params=ig_params)
            ig_response.raise_for_status()
            ig_data = ig_response.json()

            if "instagram_business_account" in ig_data:
                ig_account_id = ig_data["instagram_business_account"]["id"]

                # Get Instagram account details
                ig_details_url = f"https://graph.facebook.com/v18.0/{ig_account_id}"
                ig_details_params = {
                    "fields": "username,name,profile_picture_url,followers_count,follows_count,media_count",
                    "access_token": ACCESS_TOKEN
                }

                details_response = requests.get(ig_details_url, params=ig_details_params)
                details_response.raise_for_status()
                details = details_response.json()

                print("✅ Instagram Business Account Found!")
                print(f"   Account ID: {ig_account_id}")
                print(f"   Username: @{details.get('username', 'N/A')}")
                print(f"   Name: {details.get('name', 'N/A')}")
                print(f"   Followers: {details.get('followers_count', 0)}")
                print(f"   Following: {details.get('follows_count', 0)}")
                print(f"   Posts: {details.get('media_count', 0)}\n")

                print("📝 Next steps:")
                print(f"   1. Update config.py and set:")
                print(f"      INSTAGRAM_ACCOUNT_ID = '{ig_account_id}'")
                print("   2. Run post_image.py to make your first post!")

                return ig_account_id
            else:
                print("❌ No Instagram Business Account linked to this page")
                print("   Make sure your Instagram account is:")
                print("   1. A Business or Creator account")
                print("   2. Linked to your Facebook Page")

        else:
            print("❌ No Facebook Pages found")
            print("   Make sure your app has access to your Facebook Page")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    verify_token()
