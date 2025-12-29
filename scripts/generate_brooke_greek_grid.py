#!/usr/bin/env python3
"""
Generate Brooke in Greek Travel Grid (3x3 - 9 locations)
Using google/nano-banana-pro on Replicate
"""

import replicate
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')

# Reference images
BROOKE_BASE = "modle/brooke/base.jpeg"
BIKINI_REF = "bikinis/Alabama/on_models/houndstooth_classic.png"

# Output directory
OUTPUT_DIR = Path("content/brooke/greek_travel")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Greek Travel Grid Prompt
PROMPT = """GREEK TRAVEL GRID - 3x3 VARIATION SHEET (9 DISTINCT PANELS)

=== TECHNICAL ADAPTER INSTRUCTIONS ===

ADAPTER 1 - OUTFIT (IP-ADAPTER_CLOTHING / REFERENCE_ONLY | Medium Weight: 0.6):
IMAGE: [REFERENCE IMAGE 1 - Uploaded First]
TARGET: Bikini Pattern and Cut ONLY
INSTRUCTION: Extract ONLY the clothing from this image:
  - The pink and white houndstooth pattern bikini
  - Triangle halter top with tie straps
  - High-waisted bottoms with side ties
  - Bikini cut and style details
DO NOT use this image for: face, body, skin tone, proportions, or identity
This image shows a DIFFERENT person - IGNORE that person completely
Apply ONLY this bikini design to the woman from Adapter 2 in all 9 panels.

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
IDENTITY: Brooke (Greek Goddess Edition)
DEMOGRAPHICS: Stunning young adult female, deep golden-bronze Mediterranean tan
BODY TYPE: Hyper-voluptuous hourglass. Massive hips, tiny waist, very large bust, large round glutes. (Pull physique STRICTLY from Adapter 2 / Reference Image 2 - THE SECOND IMAGE)
FACE: Sultry eyes, defined cheekbones, full lips. Confident and relaxed vacation expressions. (From Adapter 2 / Reference Image 2 - THE SECOND IMAGE)
HAIR: Long, flowing hair. Sun-bleached lighter tones from Greek sun exposure. Hair natural and beachy in some shots, wet in water shots, windblown in outdoor shots.
SKIN: Deep golden-bronze tan. Glistening with body oil and sweat. Hyper-realistic skin texture with visible pores. Natural tan lines.
APPAREL: The specific pink and white houndstooth bikini from Adapter 1 / Reference Image 1 (FIRST IMAGE - pattern only). Wet texture in water shots. SAME bikini in all 9 panels.

=== THE 9 GRID PANELS ===

PANEL 1 - SANTORINI (Oia Sunset):
VIEW: Front View
SCENE: Leaning back against warm white stucco wall with blue trim. Golden hour light hits face directly.
BACKGROUND: Blurry blue-domed churches and pink sunset sky. Famous Santorini Oia caldera view.
POSE: One hand shielding eyes from golden light. Sultry expression. One hip popped. Three-quarter body shot showing hourglass figure.
LIGHTING: Golden hour - warm orange and pink sunset light cascading over skin and white buildings.
MOOD: Dreamy, romantic, classic Greek island aesthetic.

PANEL 2 - MILOS (Sarakiniko Moonscape):
VIEW: Full Body, Wide Shot
SCENE: Standing powerfully on smooth chalk-white volcanic rocks. The famous lunar landscape of Milos.
BACKGROUND: Sarakiniko's alien white volcanic formations. Deep blue sky contrast. Turquoise water in carved coves below.
POSE: "Hero" stance - standing with one leg forward, popping one hip to emphasize the hourglass curve. Hand on hip. Confident gaze.
LIGHTING: High noon hard lighting. Bright sharp shadows. Intense contrast white rock vs blue sky.
MOOD: High fashion editorial, otherworldly, powerful, striking.

PANEL 3 - ZAKYNTHOS (Navagio Cliff Edge):
VIEW: BACK VIEW (Focus on Glutes and Body from Adapter 2 - SECOND IMAGE)
SCENE: Standing on edge of limestone cliff 200 meters above Shipwreck Beach. Looking down at the famous wreck far below.
BACKGROUND: Electric turquoise water far below. Iconic rusted shipwreck on white sand. Towering cliffs on sides.
POSE: Back to camera. Standing confidently at cliff edge. Hair blowing wild in wind. Emphasizing the rear physique and glute shape from Reference Image 2 (THE SECOND IMAGE - Brooke). Body curves silhouetted against the vista.
LIGHTING: Midday sun. Bright clear light. Vivid turquoise water below.
MOOD: Adventurous, breathtaking vista, bucket-list moment, showcasing body proportions.

PANEL 4 - MYKONOS (Little Venice):
VIEW: Dynamic Walking Shot
SCENE: Walking toward camera along wet stone waterfront path. Waves crash against colorful buildings behind.
BACKGROUND: Little Venice district - white buildings with bright blue, red, and green balconies built to water's edge. Waves splashing.
POSE: Mid-stride, hair flowing behind. Laughing candidly. Holding woven straw bag. Natural movement. Full body shot.
LIGHTING: Late afternoon warm golden light. Wave spray creating sparkle effect.
MOOD: Carefree, energetic, joyful, classic Greek island charm.

PANEL 5 - CRETE (Elafonisi Pink Sand):
VIEW: Lying Down / Crawling Pose
SCENE: Lying on stomach in shallow crystal-clear water on the famous pink sand beach.
BACKGROUND: Elafonisi's unique PINK SAND visible through clear turquoise water (only inches deep). Pink coral sand. Blue sky.
POSE: Lying on stomach/crawling pose in shallow water. Looking up at camera with wet hair. Water ripples over back. Sensual beach pose.
LIGHTING: Bright midday sun. Water glistening. Skin wet and shimmering.
MOOD: Serene, tropical paradise, unique natural wonder, playful.

PANEL 6 - SANTORINI (Cave Pool):
VIEW: BACK VIEW / Side Profile
SCENE: Sitting on edge of private luxury cave pool carved into cliff. Looking over shoulder at camera.
BACKGROUND: White Cycladic cave architecture. Stone arch framing infinity pool. View of caldera through opening. Blue pool water.
POSE: Sitting on pool edge. Back arched, looking over shoulder at camera. Silhouette against bright cave opening. Wet hair. Intimate portrait emphasizing curves.
LIGHTING: Soft diffused light from cave opening. Blue reflections from pool. Romantic shadowing.
MOOD: Intimate, luxurious, exclusive, sultry.

PANEL 7 - CORFU (Canal d'Amour):
VIEW: Swimming Action Shot
SCENE: Treading water in narrow turquoise channel between dramatic sandstone cliffs.
BACKGROUND: Canal d'Amour's eroded golden-brown sandstone formations. Bright turquoise and emerald green water. Natural rock tunnels.
POSE: Active swimming/treading water. Wet skin, hair slicked back. Water droplets flying. Joyful expression. Medium to close-up shot.
LIGHTING: Bright natural daylight. Water droplets catching light. Sparkle and dynamic motion.
MOOD: Fun, adventurous, playful, natural wonder.

PANEL 8 - MYKONOS (The Windmills):
VIEW: Medium Portrait
SCENE: Standing in front of the iconic Kato Mili white windmills with straw conical roofs.
BACKGROUND: Row of 5 famous 16th-century windmills against bright blue sky. View of Mykonos town below.
POSE: Facing camera. Wind blowing blonde hair across face slightly (messy/sexy windblown look). Hand holding hair back. Other hand on hip.
LIGHTING: Soft afternoon light. Blue sky. Windy conditions creating movement.
MOOD: Iconic tourist moment, windswept, Instagram-worthy landmark.

PANEL 9 - LUXURY YACHT (Aegean Sea):
VIEW: BACK VIEW (Focus on Glutes and Bikini Bottom Fit from Adapter 2 - SECOND IMAGE)
SCENE: Kneeling on white leather sunbed of luxury catamaran. Facing away toward open ocean.
BACKGROUND: Endless deep blue Aegean Sea in all directions. White yacht deck. Chrome and teak details. No land - complete ocean solitude.
POSE: Kneeling, facing away from camera toward ocean. Hands tying hair up. This panel STRICTLY showcases the bikini bottom fit and rear physique from Reference Image 2 (THE SECOND IMAGE - Brooke). Hair windblown.
LIGHTING: High noon sun. Harsh bright light. Strong shadows. Skin glistening with sun oil.
MOOD: Ultimate luxury, yacht life, expensive vacation, showcasing body proportions.

=== ENVIRONMENT & AESTHETIC ===
OVERALL VIBE: Expensive, Dreamy, Mediterranean Summer. High-end Greek influencer campaign.
STYLE: Editorial travel photography. Shot on Sony A7R IV with 35mm and 85mm lenses. Professional color grading. Travel magazine quality.
COLOR PALETTE: Predominantly white (buildings, rocks, yacht), deep blue (sky, Aegean Sea), turquoise (water), golden tones (sunset, lighting), pops of pink (bougainvillea, Elafonisi sand).
LIGHTING: Varied across panels - Golden Hour (Panels 1, 4), High Noon (Panels 2, 3, 5, 9), Soft Afternoon (Panel 8), Diffused (Panels 6, 7).
CONSISTENCY: SAME WOMAN (from Adapter 2 - SECOND IMAGE) in all 9 panels. SAME BIKINI (from Adapter 1 - FIRST IMAGE pattern) in all 9 panels. Different locations, poses, angles, and lighting.

TECHNICAL SPECS:
- 8K resolution final image
- 3x3 grid layout (3 panels across, 3 panels down)
- Thin white borders separating each panel clearly
- Each panel is a complete, separate photograph
- Camera Framing: Mix of Close-ups (Panels 1, 7, 8), Full Body Landscapes (Panels 2, 3, 5, 9), Dynamic Motion (Panels 4)
- Hyper-realistic skin texture with visible pores and natural imperfections
- Professional photography quality throughout

=== CRITICAL REQUIREMENTS ===
ADAPTER ENFORCEMENT:
- IMAGE ORDER: First = Bikini pattern (Adapter 1), Second = Brooke identity (Adapter 2 - PRIORITIZED)
- ADAPTER 2 (IP-ADAPTER_PLUS_FACE, Weight 0.8) = THE SECOND IMAGE = Face AND body structure MUST match in ALL 9 panels
- ADAPTER 1 (IP-ADAPTER_CLOTHING, Weight 0.6) = THE FIRST IMAGE = ONLY bikini pattern - DO NOT use this person's face or body
- The woman wearing the bikini in Adapter 1 (FIRST IMAGE) is NOT the subject
- ONLY extract and apply the houndstooth bikini pattern to the woman from Adapter 2 (SECOND IMAGE)

CONSISTENCY:
- Same woman (from Adapter 2 - SECOND IMAGE - Brooke) in all 9 panels - no face or body swapping
- Same bikini (pattern from Adapter 1 - FIRST IMAGE) in all 9 panels
- Panels 3, 6, 9 are BACK VIEWS showcasing glute shape from Adapter 2 (SECOND IMAGE)

QUALITY:
- Each panel must be DISTINCT and SEPARATE (not blended or fused)
- Clear white borders between all 9 panels
- Realistic skin with texture, pores, sweat, oil sheen
- Professional photography lighting matching each scene
- Each Greek location clearly identifiable and accurate

=== NEGATIVE PROMPT / FORBIDDEN ELEMENTS ===
using wrong person's face, using face from Adapter 1/bikini reference image (FIRST IMAGE), using body from bikini reference image (FIRST IMAGE), face swapping, wrong woman, different woman's face, tourists in background, crowds, other people in frame, trash, litter, messy grid composition, blurred panels, fused panels, merged images, duplicate poses across panels, wrong bikini design, wrong bikini pattern, face inconsistency between panels, different women between panels, flat butt, small hips, narrow waist-hip ratio, cartoon style, anime, CGI, 3D render, plastic skin, airbrushed skin, fake tan, orange skin, bad anatomy, deformed body, extra limbs, missing limbs, fused fingers, distorted hands, malformed hands, text overlays, watermarks, logos, dates, timestamps, Instagram filters, tacky editing, low resolution, blurry, out of focus, overexposed, underexposed, unnatural stiff poses."""

def generate_greek_grid():
    """Generate 3x3 Greek travel grid"""
    print(f"\n{'='*60}")
    print(f"GENERATING: Greek Travel Grid (3x3)")
    print(f"{'='*60}")
    print(f"Model: google/nano-banana-pro")
    print(f"Reference images (NEW ORDER):")
    print(f"  - Image 1 (First): {BIKINI_REF} - PATTERN ONLY")
    print(f"  - Image 2 (Second - PRIORITIZED): {BROOKE_BASE} - IDENTITY")

    try:
        print("\nCalling Replicate API...")

        output = replicate.run(
            "google/nano-banana-pro",
            input={
                "prompt": PROMPT,
                "image_input": [
                    open(BIKINI_REF, "rb"),      # First: Bikini pattern reference
                    open(BROOKE_BASE, "rb")      # Second: Brooke identity (prioritized)
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
            output_path = OUTPUT_DIR / f"greek_grid_{timestamp}.jpeg"

            with open(output_path, 'wb') as f:
                f.write(response.content)

            file_size = output_path.stat().st_size / (1024 * 1024)
            print(f"\n{'='*60}")
            print(f"✓ SUCCESS!")
            print(f"{'='*60}")
            print(f"Saved: {output_path}")
            print(f"Size: {file_size:.2f} MB")
            print(f"\nGrid contains 9 panels:")
            print(f"  Row 1: Santorini Oia | Milos | Zakynthos")
            print(f"  Row 2: Mykonos Venice | Crete Pink Beach | Santorini Pool")
            print(f"  Row 3: Corfu | Mykonos Windmills | Yacht")
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
    print("BROOKE - GREEK TRAVEL GRID")
    print("="*60)

    success = generate_greek_grid()

    if success:
        print(f"\n{'='*60}")
        print("GENERATION COMPLETE!")
        print(f"{'='*60}")
        print(f"\nOutput directory: {OUTPUT_DIR}")
    else:
        print("\n✗ Generation failed")

if __name__ == "__main__":
    main()
