#!/usr/bin/env python3
"""
Generate Aria in LSU Purple Reign bikini at 9 Maui locations
Using google/nano-banana-pro on Replicate
"""

import replicate
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')

# Reference images
ARIA_BASE = "modle/aria/base.jpeg"
BIKINI_REF = "bikinis/LSU/ready/purple_reign.jpeg"

# Output directory
OUTPUT_DIR = Path("content/aria/maui_travel")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Maui Travel Grid Prompt
PROMPT = """MAUI TRAVEL GRID - 3x3 VARIATION SHEET (9 DISTINCT PANELS)

=== TECHNICAL ADAPTER INSTRUCTIONS ===

ADAPTER 1 - OUTFIT (IP-ADAPTER_CLOTHING / REFERENCE_ONLY | Medium Weight: 0.6):
IMAGE: [REFERENCE IMAGE 1 - Uploaded First]
TARGET: Bikini Pattern and Cut ONLY
INSTRUCTION: Extract ONLY the bikini design from this product image:
  - Purple and gold tiger stripe pattern (LSU colors)
  - Triangle halter top with gold bead details and tie straps
  - Matching bottoms with side ties and gold beads
  - This is a PRODUCT PHOTO with NO MODEL - extract pattern only
Apply this bikini design to the woman from Adapter 2 in all 9 panels.

ADAPTER 2 - IDENTITY (IP-ADAPTER_PLUS_FACE | Strong Weight: 0.8):
IMAGE: [REFERENCE IMAGE 2 - Uploaded Second - PRIORITIZED]
TARGET: Face and Body Structure
INSTRUCTION: This is the PRIMARY IDENTITY reference. Extract and apply:
  - Facial features: eye shape, nose, lips, facial structure, expressions
  - Body proportions: waist-to-hip ratio, bust size, body shape, physique
  - CRITICAL: Reference this image for the model's rear-view GLUTE SHAPE and proportions
  - Skin tone and texture
This person MUST appear in all 9 panels. No face or body swapping.
SECOND IMAGE = PRIORITY for identity.

=== LAYOUT SPECIFICATION ===
Create a 3x3 grid (9 separate panels) combined into ONE final square image. Each panel is a distinct photograph. Thin white borders between panels. Do NOT blend or merge panels.

=== SUBJECT DESCRIPTION ===
IDENTITY: Aria (Hawaiian Vacation Edition)
DEMOGRAPHICS: Young adult female, healthy athletic build, natural golden tan with Hawaiian sun glow
BODY TYPE: Athletic hourglass figure. Natural proportions. (Use physique from Adapter 2 / Reference Image 2 - THE SECOND IMAGE)
FACE: Natural beauty, confident expressions. Relaxed island vacation mood. (From Adapter 2 / Reference Image 2 - THE SECOND IMAGE)
HAIR: Long, flowing hair. Beach waves and wind-tousled in outdoor shots, wet in water shots, natural and beachy.
SKIN: Golden-bronze Hawaiian tan. Natural skin texture. Coconut oil sheen from sun protection.
APPAREL: The purple and gold tiger stripe swimwear from Adapter 1 / Reference Image 1 (LSU colors - product photo). SAME swimwear in all 9 panels.

=== THE 9 GRID PANELS ===

PANEL 1 - HALEAKALA CRATER (Sunrise):
VIEW: Front View
SCENE: Standing on volcanic crater rim at sunrise. Above the clouds at 10,000 feet elevation.
BACKGROUND: Haleakala volcanic crater with red and orange cinder cones. Sea of clouds below. Dramatic sunrise colors - pink, orange, purple sky.
POSE: Arms outstretched, embracing the sunrise. Hair windblown. Looking at camera with awe-struck expression. Three-quarter body shot.
LIGHTING: Golden sunrise light. Warm orange and pink tones. High altitude clear air.
MOOD: Spiritual, breathtaking, bucket-list moment, above the clouds.

PANEL 2 - ROAD TO HANA (Waterfall Pool):
VIEW: Full Body, Wide Shot
SCENE: Standing in crystal-clear waterfall pool. Lush tropical jungle waterfall behind.
BACKGROUND: Twin Falls or Wailua Falls cascading through dense green rainforest. Tropical plants, ferns, moss-covered rocks. Emerald water.
POSE: Standing in waist-deep water. Arms above head, hair wet and slicked back. Water droplets on skin. Confident goddess pose.
LIGHTING: Dappled jungle light. Soft diffused through canopy. Green tones reflecting off water.
MOOD: Tropical paradise, jungle adventure, refreshing, natural beauty.

PANEL 3 - MAKENA COVE (Secret Beach):
VIEW: Back view, walking into water
SCENE: Walking away from camera into turquoise water at secluded cove.
BACKGROUND: Makena Cove's crystal turquoise water. Black lava rocks framing the small beach. Palm trees. No crowds - private paradise.
POSE: Back to camera. Walking into water, looking back over shoulder. Hair flowing. Natural vacation photography from Reference Image 2 (THE SECOND IMAGE - Aria).
LIGHTING: Midday Hawaiian sun. Bright turquoise water. Strong shadows on golden sand.
MOOD: Secluded paradise, tropical escape, natural travel photography.

PANEL 4 - WAILEA BEACH (Golden Hour):
VIEW: Dynamic Walking Shot
SCENE: Walking along white sand beach at sunset. Waves gently lapping at feet.
BACKGROUND: Wailea's pristine white sand beach. Luxury resorts in distance. Palm trees. Golden hour sky with pink clouds. Calm turquoise water.
POSE: Mid-stride along water's edge. Hair blowing in ocean breeze. Holding a coconut drink. Natural movement. Looking at camera with bright smile. Full body shot.
LIGHTING: Golden hour. Warm peachy light. Soft shadows on sand.
MOOD: Luxurious, carefree island life, joyful, classic Hawaiian beach.

PANEL 5 - BLACK SAND BEACH (Waianapanapa):
VIEW: Relaxed beach pose
SCENE: Relaxing on dramatic black volcanic sand beach. Waves crashing on black rocks.
BACKGROUND: Waianapanapa's famous black sand beach. Dark volcanic rock formations. Bright turquoise water contrast against black sand. Sea caves visible.
POSE: Lying on side on black sand, propped up on elbow. Legs extended. Natural beach relaxation. Looking at camera with happy expression.
LIGHTING: Bright midday sun. High contrast - black sand, turquoise water, golden skin.
MOOD: Dramatic, volcanic power, unique natural wonder, striking contrast.

PANEL 6 - INFINITY POOL (Grand Wailea):
VIEW: Pool edge, looking over shoulder
SCENE: In luxury infinity pool overlooking the Pacific Ocean. Sunset time.
BACKGROUND: Infinity pool edge with Pacific Ocean horizon. Palm trees. Orange and pink sunset sky. No visible pool edge - water meets ocean meets sky.
POSE: In pool, arms resting on infinity edge. Looking over shoulder at camera. Wet hair. Silhouette against sunset. Portrait composition.
LIGHTING: Sunset backlight. Golden rim light. Purple and orange sky reflections.
MOOD: Luxurious, romantic, expensive resort life, Instagram-worthy.

PANEL 7 - MOLOKINI CRATER (Snorkeling):
VIEW: Swimming Action Shot
SCENE: Floating in crystal-clear water. Snorkel mask on head. Volcanic crater island visible behind.
BACKGROUND: Molokini Crater - crescent-shaped volcanic crater in ocean. Crystal-clear turquoise water. Boats visible in distance. Underwater visibility showing coral below.
POSE: Treading water, snorkel mask pushed up on forehead. Wet hair. Arms in water. Joyful expression. Medium close-up shot.
LIGHTING: Bright tropical sun. Intense blue water. High clarity.
MOOD: Adventure, snorkeling paradise, marine life, tropical fun.

PANEL 8 - NAKALELE BLOWHOLE (Dramatic Coast):
VIEW: Medium Portrait
SCENE: Standing on dramatic black lava rock coast. Ocean spray from blowhole erupting behind.
BACKGROUND: Nakalele Blowhole with ocean spray shooting up dramatically. Rugged black lava coastline. Crashing waves. Dramatic northern Maui coast. Cloudy dramatic sky.
POSE: Standing on lava rocks. Wind and ocean spray creating dramatic hair movement. Hand on hip. Powerful stance against dramatic ocean. Looking at camera.
LIGHTING: Overcast dramatic light. Moody. Ocean spray creating mist and atmosphere.
MOOD: Wild nature, powerful ocean, dramatic, adventurous, rugged beauty.

PANEL 9 - CATAMARAN SUNSET SAIL:
VIEW: Back view, facing sunset
SCENE: Sitting on catamaran net. Facing sunset over Pacific Ocean.
BACKGROUND: Endless Pacific Ocean. Orange and pink sunset. Maui coastline in distance. White catamaran deck and rigging. Sailing at golden hour.
POSE: Sitting on boat's net facing away toward sunset. Hands in hair. Natural sailing vacation photography from Reference Image 2 (THE SECOND IMAGE - Aria). Hair windblown.
LIGHTING: Golden sunset light. Warm orange glow on skin. Backlighting creating silhouette.
MOOD: Ultimate island luxury, sailing life, expensive vacation, romantic sunset.

=== ENVIRONMENT & AESTHETIC ===
OVERALL VIBE: Expensive, Dreamy, Hawaiian Paradise. High-end Maui influencer campaign.
STYLE: Editorial travel photography. Shot on Sony A7R IV with 35mm and 85mm lenses. Professional color grading. Travel magazine quality.
COLOR PALETTE: Predominantly turquoise (water), golden tones (sand, skin, sunset), lush greens (jungle), dramatic blacks (volcanic rock, lava), vibrant sunset colors (orange, pink, purple), LSU purple and gold (bikini).
LIGHTING: Varied across panels - Sunrise (Panel 1), Jungle Diffused (Panel 2), Midday Bright (Panels 3, 5, 7), Golden Hour (Panels 4, 6, 9), Overcast Dramatic (Panel 8).
CONSISTENCY: SAME WOMAN (from Adapter 2 - SECOND IMAGE) in all 9 panels. SAME BIKINI (from Adapter 1 - FIRST IMAGE pattern) in all 9 panels. Different Maui locations, poses, angles, and lighting.

TECHNICAL SPECS:
- 8K resolution final image
- 3x3 grid layout (3 panels across, 3 panels down)
- Thin white borders separating each panel clearly
- Each panel is a complete, separate photograph
- Camera Framing: Mix of Close-ups (Panels 1, 7, 8), Full Body Landscapes (Panels 2, 3, 5, 9), Dynamic Motion (Panel 4)
- Hyper-realistic skin texture with visible pores and natural imperfections
- Professional photography quality throughout

=== CRITICAL REQUIREMENTS ===
ADAPTER ENFORCEMENT:
- IMAGE ORDER: First = Bikini pattern (Adapter 1), Second = Aria identity (Adapter 2 - PRIORITIZED)
- ADAPTER 2 (IP-ADAPTER_PLUS_FACE, Weight 0.8) = THE SECOND IMAGE = Face AND body structure MUST match in ALL 9 panels
- ADAPTER 1 (IP-ADAPTER_CLOTHING, Weight 0.6) = THE FIRST IMAGE = ONLY bikini pattern (product photo, no model)
- ONLY extract and apply the purple/gold tiger stripe bikini pattern to the woman from Adapter 2 (SECOND IMAGE)

CONSISTENCY:
- Same woman (from Adapter 2 - SECOND IMAGE - Aria) in all 9 panels - no face swapping
- Same swimwear (pattern from Adapter 1 - FIRST IMAGE) in all 9 panels
- Panels 3, 6, 9 include back-facing angles for variety

QUALITY:
- Each panel must be DISTINCT and SEPARATE (not blended or fused)
- Clear white borders between all 9 panels
- Natural skin texture with sun protection sheen
- Professional travel photography lighting matching each Maui scene
- Each Hawaiian/Maui location clearly identifiable and accurate
- Family-friendly vacation photography aesthetic

=== NEGATIVE PROMPT / FORBIDDEN ELEMENTS ===
using wrong person's face, face swapping, wrong woman, different woman's face, tourists in background, crowds, other people in frame, trash, litter, messy grid composition, blurred panels, fused panels, merged images, duplicate poses across panels, wrong swimwear design, face inconsistency between panels, different women between panels, cartoon style, anime, CGI, 3D render, plastic skin, airbrushed skin, fake tan, orange skin, bad anatomy, deformed body, extra limbs, missing limbs, fused fingers, distorted hands, malformed hands, text overlays, watermarks, logos, dates, timestamps, Instagram filters, tacky editing, low resolution, blurry, out of focus, overexposed, underexposed, unnatural stiff poses, inappropriate content, explicit content."""

def generate_maui_grid():
    """Generate 3x3 Maui travel grid"""
    print(f"\n{'='*60}")
    print(f"GENERATING: Aria - Maui Travel Grid (3x3)")
    print(f"{'='*60}")
    print(f"Model: google/nano-banana-pro")
    print(f"Reference images (SWAPPED ORDER):")
    print(f"  - Image 1 (First): {BIKINI_REF} - PATTERN ONLY (product photo)")
    print(f"  - Image 2 (Second - PRIORITIZED): {ARIA_BASE} - IDENTITY")

    try:
        print("\nCalling Replicate API...")

        output = replicate.run(
            "google/nano-banana-pro",
            input={
                "prompt": PROMPT,
                "image_input": [
                    open(BIKINI_REF, "rb"),      # First: Bikini pattern (product photo)
                    open(ARIA_BASE, "rb")         # Second: Aria identity (prioritized)
                ],
                "aspect_ratio": "1:1",  # Square for 3x3 grid
                "size": "2K"
            }
        )

        # Download and save image
        if output:
            image_url = output[0] if isinstance(output, list) else output

            print(f"Downloading image from: {image_url}")
            response = requests.get(image_url)

            # Save with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"maui_grid_{timestamp}.jpeg"

            with open(output_path, 'wb') as f:
                f.write(response.content)

            file_size = output_path.stat().st_size / (1024 * 1024)
            print(f"\n{'='*60}")
            print(f"✓ SUCCESS!")
            print(f"{'='*60}")
            print(f"Saved: {output_path}")
            print(f"Size: {file_size:.2f} MB")
            print(f"\nGrid contains 9 Maui panels:")
            print(f"  Row 1: Haleakala Sunrise | Waterfall Pool | Makena Cove (back)")
            print(f"  Row 2: Wailea Beach | Black Sand Beach | Infinity Pool (back)")
            print(f"  Row 3: Molokini Snorkel | Nakalele Blowhole | Catamaran (back)")
            return True
        else:
            print("✗ No output generated")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main execution"""
    print("="*60)
    print("ARIA - MAUI TRAVEL GRID")
    print("="*60)

    success = generate_maui_grid()

    if success:
        print(f"\n{'='*60}")
        print("GENERATION COMPLETE!")
        print(f"{'='*60}")
        print(f"\nOutput directory: {OUTPUT_DIR}")
    else:
        print("\n✗ Generation failed")

if __name__ == "__main__":
    main()
