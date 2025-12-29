#!/usr/bin/env python3
"""Generate V2 design grids with improvements."""
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

V2_DESIGNS = {
    "Alabama": {
        "colors": "Crimson (#9E1B32), Gray (#828A8F), White (#FFFFFF)",
        "designs": [
            {
                "name": "Houndstooth Classic",
                "desc": "Triangle bikini top and brazilian bottom in iconic crimson and white houndstooth pattern. Classic Bear Bryant pattern covering entire bikini. Thin straps, minimal coverage. Sophisticated preppy style. UNCHANGED from V1."
            },
            {
                "name": "Script A Logo V2",
                "desc": "Solid crimson bikini with LARGE white Alabama Script A logos printed all over in dense repeated pattern. MUCH BIGGER logos than V1, covering more surface area (15-20 logos total). Varied logo sizes from small to large. Triangle top with tie sides. Bold team branding."
            },
            {
                "name": "Elephant Stampede",
                "desc": "Gray bikini with subtle crimson elephant silhouettes scattered across fabric. Minimalist mascot design. Bandeau top with matching high-waisted bottom. Elegant animal print. UNCHANGED from V1."
            },
            {
                "name": "Crimson Tide Waves V2",
                "desc": "White base with FUTURISTIC crimson wave patterns. Geometric angular waves with holographic iridescent effect. Neon crimson glow on wave edges. Modern sci-fi aesthetic. String bikini style with side ties. HIGH-TECH UPGRADE from V1."
            },
            {
                "name": "Roll Tide Stripes V2",
                "desc": "ELEGANT diagonal stripes in Crimson, Gray, and White (triple color). Thin refined stripes at 45-degree angle with subtle shimmer finish. Triangle top and cheeky bottom. Sophisticated preppy aesthetic. MORE REFINED than V1 with added gray color."
            },
            {
                "name": "Big Al Mascot",
                "desc": "White bikini with large crimson Big Al elephant mascot face prints. Cute cartoon Alabama elephant graphics scattered across. Triangle top with brazilian bottom. Playful team spirit. NEW DESIGN for V2."
            }
        ]
    },
    "Auburn": {
        "colors": "Navy Blue (#03244D), Burnt Orange (#DD550C), White (#FFFFFF)",
        "designs": [
            {
                "name": "War Eagle Navy",
                "desc": "Navy blue bikini with burnt orange eagle silhouettes flying across fabric. NO TEXT, just pure eagle graphics. Fierce bird of prey theme. Triangle top with brazilian bottom. Bold mascot print."
            },
            {
                "name": "War Eagle White",
                "desc": "WHITE bikini with navy blue and burnt orange eagle silhouettes flying across. NO TEXT, just eagle graphics. Clean colorway variation. Triangle top with brazilian bottom. Fresh take on War Eagle design."
            },
            {
                "name": "Tiger Stripes Navy",
                "desc": "Navy and burnt orange bold tiger stripe pattern. NO TEXT, pure animal print. Diagonal stripes mimicking tiger fur. Bandeau top with matching cheeky bottom. Fierce Auburn Tigers aesthetic."
            },
            {
                "name": "Tiger Stripes White",
                "desc": "WHITE base with navy and burnt orange tiger stripe pattern overlay. NO TEXT, pure pattern. Clean fresh colorway. Triangle top with brazilian bottom. Light version of tiger stripes."
            },
            {
                "name": "Toomer's Oaks V2",
                "desc": "White bikini with ENHANCED Toomer's Corner celebration design. Navy oak tree silhouettes with orange and white toilet paper streams flowing dramatically. MORE DETAILED than V1 with better toilet paper texture. Iconic Auburn tradition celebration. Halter top with tie-side bottom."
            },
            {
                "name": "Plains Stripes V2",
                "desc": "IMPROVED Navy, burnt orange, and white horizontal stripes. Better balanced color proportions and stripe widths than V1. Classic Auburn plains pattern with modern clean lines. Triangle top with tie-side bottom. Refined vintage athletic style."
            }
        ]
    }
}

def generate_v2_grid(school_name):
    """Generate V2 grid with improvements."""
    print(f"\n{'='*60}")
    print(f"🎓 {school_name} - V2 Design Grid")
    print(f"{'='*60}")

    data = V2_DESIGNS[school_name]
    design_list = ""
    for i, design in enumerate(data['designs'], 1):
        design_list += f"\n{i}. {design['name']}: {design['desc']}"

    prompt = f"""Create a professional product catalog showing 6 IMPROVED bikini designs for {school_name} in a 3x2 grid (3 columns, 2 rows).

This is VERSION 2 with specific improvements from V1.

SCHOOL COLORS: {data['colors']}

DETAILED DESIGNS V2 (each with specific improvements):
{design_list}

CRITICAL REQUIREMENTS:
- 3x2 grid layout (3 columns, 2 rows) = 6 designs
- Each cell shows ONE complete bikini design
- All 6 designs must be VISUALLY DIFFERENT from each other
- Use ONLY the specified school colors
- Professional fashion illustration style
- Show designs on athletic female body forms
- Clean white background with clear grid separation
- Follow ALL improvement notes from descriptions
- Pay attention to V2 changes: bigger logos, added colors, improved details

Generate all 6 IMPROVED {school_name} V2 designs in ONE grid image."""

    print(f"\n🎨 Generating V2 improvements...")
    print(f"Colors: {data['colors']}\n")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="16:9",
                image_size="2K"
            )
        )
    )

    for part in response.parts:
        if img := part.as_image():
            output_dir = f"bikinis/{school_name}/design_grids"
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{output_dir}/{school_name.lower()}_v2_designs_{timestamp}.jpg"

            img.save(output_path)
            print(f"✅ Saved: {output_path}\n")
            return output_path

    print(f"❌ Failed\n")
    return None

if __name__ == "__main__":
    schools = ["Alabama", "Auburn"]

    print("🏈 V2 Design Grids - Improved Versions")

    for school in schools:
        try:
            generate_v2_grid(school)
        except Exception as e:
            print(f"\n❌ Error with {school}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*60)
    print("✅ V2 grids complete!")
    print("="*60)
