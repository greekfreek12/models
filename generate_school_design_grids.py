#!/usr/bin/env python3
"""Generate unique themed bikini design grids for each school."""
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.local')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

SCHOOL_DESIGNS = {
    "Alabama": {
        "colors": "Crimson (#9E1B32), Gray (#828A8F), White (#FFFFFF)",
        "designs": [
            {
                "name": "Houndstooth Classic",
                "desc": "Triangle bikini top and brazilian bottom in iconic crimson and white houndstooth pattern. Classic Bear Bryant pattern covering entire bikini. Thin straps, minimal coverage. Sophisticated preppy style."
            },
            {
                "name": "Script A Logo",
                "desc": "Solid crimson bikini with white Alabama Script A logos printed all over in repeated pattern. Triangle top with tie sides. Modern college spirit aesthetic."
            },
            {
                "name": "Elephant Stampede",
                "desc": "Gray bikini with subtle crimson elephant silhouettes scattered across fabric. Minimalist mascot design. Bandeau top with matching high-waisted bottom. Elegant animal print."
            },
            {
                "name": "Crimson Tide Waves",
                "desc": "White base with flowing crimson wave patterns representing the ocean tide. Abstract artistic waves in team colors. String bikini style with side ties."
            },
            {
                "name": "Athletic Alabama",
                "desc": "Sporty crimson crop top style with white block letters spelling ALABAMA across chest. Matching athletic short-style bottom with white side stripes. Jersey-inspired activewear look."
            },
            {
                "name": "Roll Tide Stripes",
                "desc": "Bold diagonal crimson and white stripes at 45-degree angle. Retro 80s style triangle top and cheeky bottom. High contrast striped pattern. Vintage athletic aesthetic."
            }
        ]
    },
    "Florida": {
        "colors": "Florida Blue (#0021A5), Orange (#FA4616), White (#FFFFFF)",
        "designs": [
            {
                "name": "Gator Scales",
                "desc": "Bikini with reptilian scale texture pattern in blue and orange gradient. Textured look mimicking alligator skin. Triangle top with brazilian bottom. Exotic animal-inspired print."
            },
            {
                "name": "Swamp Fever",
                "desc": "Camouflage pattern with blue, orange, and green swamp leaves and foliage. Tropical Florida wetlands theme. Bandeau top with matching tie-side bottom. Nature-inspired camo print."
            },
            {
                "name": "Gator Head Logo",
                "desc": "Orange bikini with repeated blue Florida Gator head mascot logos printed all over. Bold team spirit print. Classic triangle top and brazilian bottom. Iconic mascot showcase."
            },
            {
                "name": "Jersey Stripes",
                "desc": "Classic football jersey style with horizontal orange and blue stripes. Sporty athletic look with vintage team uniform aesthetic. Halter top with boyshort bottom. Retro sports style."
            },
            {
                "name": "Chomp Chomp",
                "desc": "Bright orange base with blue alligator jaw prints showing teeth. Fun graphic print of gator bites. String bikini with playful mascot theme. Bold graphic design."
            },
            {
                "name": "Block F Athletic",
                "desc": "Blue athletic crop top with large white block F on chest. GATORS text across waistband of matching athletic bottom. Modern sporty collegiate style. Performance wear inspired."
            }
        ]
    },
    "Georgia": {
        "colors": "Bulldog Red (#BA0C2F), Black (#000000), White (#FFFFFF)",
        "designs": [
            {
                "name": "Paw Print Power",
                "desc": "Red bikini with black bulldog paw prints scattered across fabric. Animal track pattern. Triangle top with tie-side brazilian bottom. Playful mascot motif."
            },
            {
                "name": "Power G Pattern",
                "desc": "Black base with repeated red Georgia Power G logos in allover print. Bold team branding. Bandeau top with matching cheeky bottom. Classic logo showcase."
            },
            {
                "name": "Uga Face",
                "desc": "White bikini with illustrated bulldog face (Uga mascot) printed on top and bottom. Cute cartoon mascot style. Triangle top with boy-short bottom. Character-driven design."
            },
            {
                "name": "Dawg Collar",
                "desc": "Red bikini with black collar and dog tag details. Metallic silver tag accent with DAWGS engraving. Edgy punk-inspired pet collar theme. Unique hardware details."
            },
            {
                "name": "Bone Zone",
                "desc": "Black base with red dog bone shapes scattered in pattern. Playful canine theme. String bikini with minimal coverage. Fun graphic bone motifs."
            },
            {
                "name": "Georgia Arch",
                "desc": "Red athletic crop top with black GEORGIA text in iconic arch lettering style. Matching high-waisted bottom with black trim. Collegiate letterman aesthetic. Classic campus style."
            }
        ]
    },
    "Ole_Miss": {
        "colors": "Cardinal Red (#CE1126), Powder Blue (#006BA6), White (#FFFFFF)",
        "designs": [
            {
                "name": "Rebel Powder Blue",
                "desc": "Powder blue base with red landshark mascot prints scattered across. Fierce shark graphics. Triangle top with tie-side brazilian bottom. Bold mascot showcase."
            },
            {
                "name": "Hotty Toddy Stripes",
                "desc": "Red and powder blue horizontal stripes in vintage pattern. Classic preppy collegiate style. Bandeau top with matching boy-short bottom. Retro aesthetic."
            },
            {
                "name": "Ole Miss Script",
                "desc": "White bikini with red and powder blue Ole Miss script logos repeated. Classic team branding. String bikini with minimal coverage. Logo-driven design."
            },
            {
                "name": "Magnolia Grove",
                "desc": "Powder blue with red magnolia flower prints (Mississippi state flower). Southern belle botanical theme. Halter top with tie-side bottom. Elegant floral pattern."
            },
            {
                "name": "Rebel Athletic",
                "desc": "Red athletic crop top with powder blue REBELS lettering. Matching high-waisted bottom with powder blue trim. Modern sporty collegiate style. Performance inspired."
            },
            {
                "name": "Diamond Checker",
                "desc": "Red and powder blue diamond checkerboard pattern. Bold geometric design. Triangle bikini with matching brazilian bottom. Preppy argyle-inspired print."
            }
        ]
    },
    "Tennessee": {
        "colors": "Tennessee Orange (#FF8200), Smoky Gray (#58595B), White (#FFFFFF)",
        "designs": [
            {
                "name": "Smoky Mountain",
                "desc": "Smoky gray with orange mountain silhouette pattern. Tennessee landscape theme. Bandeau top with matching high-waisted bottom. Nature-inspired scenic design."
            },
            {
                "name": "Power T Logo",
                "desc": "Orange bikini with white Power T logos repeated across fabric. Iconic team branding. Triangle top with tie-side brazilian bottom. Classic logo showcase."
            },
            {
                "name": "Checkerboard Vol",
                "desc": "Orange and white checkerboard pattern (Tennessee endzone design). Iconic team pattern. String bikini with minimal coverage. Bold checker print."
            },
            {
                "name": "Smokey Paws",
                "desc": "Orange base with gray Bluetick Coonhound paw prints. Smokey mascot theme. Halter top with matching cheeky bottom. Playful mascot motif."
            },
            {
                "name": "Rocky Top Athletic",
                "desc": "Orange athletic crop top with gray ROCKY TOP lettering. Matching athletic shorts with gray side panels. Sporty Volunteer spirit. Performance style."
            },
            {
                "name": "Orange Crush",
                "desc": "Solid bright orange with white and gray color block accents. Modern minimalist design. Triangle bikini with white trim details. Bold colorway showcase."
            }
        ]
    },
    "Vanderbilt": {
        "colors": "Gold (#866D4B), Black (#000000), White (#FFFFFF)",
        "designs": [
            {
                "name": "Anchor Pride",
                "desc": "Black bikini with gold anchor symbols (Vanderbilt Commodores nautical theme). Maritime heritage pattern. Triangle top with tie-side bottom. Elegant naval motif."
            },
            {
                "name": "Star V Logo",
                "desc": "Gold base with black Vanderbilt V-Star logo repeated print. Bold team branding. Bandeau top with matching brazilian bottom. Classic logo pattern."
            },
            {
                "name": "Commodore Stripes",
                "desc": "Black and gold horizontal nautical stripes. Classic sailor/maritime aesthetic. Halter top with matching boy-short bottom. Vintage naval uniform inspired."
            },
            {
                "name": "Gold Rush",
                "desc": "Metallic gold fabric with black trim details. Luxurious shimmering finish. Push-up underwire top with high-waisted bottom. Elegant premium aesthetic."
            },
            {
                "name": "Dores Athletic",
                "desc": "Black athletic crop top with gold DORES block lettering. Matching athletic shorts with gold waistband. Modern sporty collegiate style. Performance inspired."
            },
            {
                "name": "Nashville Star",
                "desc": "Black bikini with gold star patterns scattered across. Music city theme with star motifs. String bikini with minimal coverage. Celestial Nashville-inspired design."
            }
        ]
    },
    "Texas": {
        "colors": "Burnt Orange (#BF5700), White (#FFFFFF)",
        "designs": [
            {
                "name": "Longhorn Pride",
                "desc": "Burnt orange bikini with white longhorn silhouettes scattered across fabric. Texas cattle heritage theme. Triangle top with tie-side brazilian bottom. Bold mascot motif."
            },
            {
                "name": "Hook Em Horns",
                "desc": "White bikini with burnt orange hand gesture logos (hook em horns symbol). Iconic team gesture print. Bandeau top with matching cheeky bottom. Classic Texas spirit."
            },
            {
                "name": "Burnt Orange Block",
                "desc": "Solid burnt orange athletic crop top with white TEXAS block lettering. Matching high-waisted bottom with white side panels. Modern sporty collegiate style."
            },
            {
                "name": "Bevo Stripes",
                "desc": "Burnt orange and white vertical stripes. Bold classic pattern. Triangle halter top with matching brazilian bottom. Vintage athletic aesthetic."
            },
            {
                "name": "Lone Star State",
                "desc": "White bikini with burnt orange Texas stars scattered across. State pride theme. String bikini with minimal coverage. Patriotic Texas design."
            },
            {
                "name": "Tower Orange",
                "desc": "Burnt orange with white UT tower silhouette print. Campus landmark theme. Halter top with matching tie-side bottom. Iconic Austin imagery."
            }
        ]
    },
    "Oklahoma": {
        "colors": "Crimson (#841617), Cream (#FDF9D8)",
        "designs": [
            {
                "name": "Sooner Schooner",
                "desc": "Crimson bikini with cream covered wagon (Sooner Schooner) prints. Iconic mascot theme. Triangle top with brazilian bottom. Heritage Oklahoma spirit."
            },
            {
                "name": "Boomer Sooner",
                "desc": "Cream base with crimson BOOMER SOONER text repeated. Fight song theme. Bandeau top with matching cheeky bottom. Classic team chant print."
            },
            {
                "name": "Crimson Pride",
                "desc": "Solid crimson athletic crop top with cream OU logo. Matching athletic shorts with cream trim. Modern sporty style. Performance inspired."
            },
            {
                "name": "Prairie Stripes",
                "desc": "Crimson and cream horizontal stripes. Classic Oklahoma territory pattern. Halter top with matching boy-short bottom. Vintage prairie aesthetic."
            },
            {
                "name": "Interlocking OU",
                "desc": "Cream bikini with crimson interlocking OU logos repeated across. Bold team branding. Triangle top with tie-side bottom. Iconic logo showcase."
            },
            {
                "name": "Wagon Wheels",
                "desc": "Crimson with cream wagon wheel patterns. Pioneer heritage theme. String bikini with minimal coverage. Western Oklahoma motif."
            }
        ]
    },
    "Texas_AM": {
        "colors": "Maroon (#500000), White (#FFFFFF)",
        "designs": [
            {
                "name": "Aggie Maroon",
                "desc": "Deep maroon bikini with white ATM logo repeated print. Classic team branding. Triangle top with brazilian bottom. Bold Aggie pride."
            },
            {
                "name": "12th Man",
                "desc": "White bikini with maroon 12TH MAN text and graphics. Iconic Aggie tradition theme. Bandeau top with matching cheeky bottom. Fan spirit design."
            },
            {
                "name": "Gig Em",
                "desc": "Maroon athletic crop top with white GIG EM thumbs up symbol. Matching high-waisted bottom. Modern sporty collegiate style. Aggie gesture theme."
            },
            {
                "name": "Reveille Paws",
                "desc": "Maroon base with white collie paw prints scattered. Reveille mascot theme. Halter top with tie-side bottom. Playful dog motif."
            },
            {
                "name": "Military Stripes",
                "desc": "Maroon and white diagonal military-inspired stripes. Corps of Cadets heritage. Triangle bikini with matching bottom. Military academy aesthetic."
            },
            {
                "name": "Aggie Ring",
                "desc": "White bikini with maroon Aggie Ring symbols. Iconic class ring tradition. String bikini with minimal coverage. Heritage jewelry theme."
            }
        ]
    },
    "Auburn": {
        "colors": "Navy Blue (#03244D), Burnt Orange (#DD550C), White (#FFFFFF)",
        "designs": [
            {
                "name": "War Eagle",
                "desc": "Navy blue bikini with burnt orange eagle silhouettes. Fierce bird of prey theme. Triangle top with brazilian bottom. Bold mascot print."
            },
            {
                "name": "Tiger Stripes Auburn",
                "desc": "Navy and burnt orange tiger stripe pattern. Auburn Tigers theme with bold stripes. Bandeau top with matching cheeky bottom. Animal print aesthetic."
            },
            {
                "name": "AU Logo Pride",
                "desc": "Burnt orange athletic crop top with navy AU interlocking logo. Matching athletic shorts with navy panels. Modern sporty style."
            },
            {
                "name": "Navy Orange Block",
                "desc": "Navy and burnt orange color blocked design with geometric split. Modern two-tone style. Halter top with matching bottom. Bold colorway."
            },
            {
                "name": "Toomer's Oaks",
                "desc": "White bikini with navy and orange oak tree and toilet paper graphics (Toomer's Corner tradition). Campus tradition theme. String bikini. Iconic Auburn celebration."
            },
            {
                "name": "Plains Stripes",
                "desc": "Navy, burnt orange, and white horizontal stripes. Classic Auburn plains pattern. Triangle top with tie-side bottom. Vintage athletic style."
            }
        ]
    }
}

def generate_school_design_grid(school_name):
    """Generate a 3x2 grid of 6 unique bikini designs for a school."""
    print(f"\n{'='*60}")
    print(f"🎓 {school_name} - Themed Design Grid")
    print(f"{'='*60}")

    data = SCHOOL_DESIGNS[school_name]

    # Build detailed design list
    design_list = ""
    for i, design in enumerate(data['designs'], 1):
        design_list += f"\n{i}. {design['name']}: {design['desc']}"

    prompt = f"""Create a professional product catalog showing 6 DIFFERENT bikini designs for {school_name} in a 3x2 grid (3 columns, 2 rows).

SCHOOL COLORS: {data['colors']}

DETAILED DESIGNS (each must be completely unique):
{design_list}

CRITICAL REQUIREMENTS:
- 3x2 grid layout (3 columns, 2 rows) = 6 designs
- Each cell shows ONE complete bikini design
- All 6 designs must be VISUALLY DIFFERENT from each other
- Use ONLY the specified school colors
- Professional fashion illustration style
- Show designs on athletic female body forms
- Clean white background with clear grid separation
- Each design should match its description exactly
- Mix of cuts: triangle, bandeau, athletic, string, etc.
- Include patterns, logos, prints as described

Generate all 6 unique {school_name}-themed designs in ONE grid image."""

    print(f"\n🎨 Generating 6 unique themed designs...")
    print(f"Colors: {data['colors']}\n")

    # Generate with Gemini
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

    # Save output
    for part in response.parts:
        if img := part.as_image():
            output_dir = f"bikinis/{school_name}/design_grids"
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{output_dir}/{school_name.lower()}_designs_{timestamp}.jpg"

            img.save(output_path)
            print(f"✅ Saved: {output_path}\n")
            return output_path

    print(f"❌ Failed\n")
    return None

# Main execution
if __name__ == "__main__":
    schools = ["Texas", "Oklahoma", "Texas_AM", "Auburn"]

    print("🏈 School-Themed Bikini Design Grids")
    print(f"Generating 6 unique designs per school\n")

    for school in schools:
        try:
            generate_school_design_grid(school)
        except Exception as e:
            print(f"\n❌ Error with {school}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*60)
    print("✅ All design grids complete!")
    print("="*60)
