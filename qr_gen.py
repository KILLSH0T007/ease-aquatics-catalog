import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

# --- PIXEL LIMIT BYPASS ---
Image.MAX_IMAGE_PIXELS = None 

# --- SETTINGS ---
GITHUB_USERNAME = "KILLSH0T007" 
REPO_NAME = "ease-aquatics-catalog"
BASE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/dist"
LOGO_FILE = "dist/img/SimpleLogo.png" 
LABEL_DIR = "Final_Branded_Stickers"


# --- BRAND PALETTE ---
GRADIENT_TOP = (175, 225, 225) 
GRADIENT_BOTTOM = (255, 255, 255) 
TEXT_DARK = (28, 28, 30) 
CORNER_RADIUS = 45 

# --- UPDATED PLANT DATA ---
plant_data = [
    {"id": "monte-carlo", "name": "Monte Carlo", "growth": "Fast", "co2": "High", "type": "Carpeting", "place": "Foreground"},
    {"id": "pogo-helferi", "name": "Pogostemon Helferi", "growth": "Medium", "co2": "Required", "type": "Star Plant", "place": "Foreground/Mid"},
    {"id": "crypt-wendtii", "name": "Cryptocoryne Wendtii", "growth": "Slow", "co2": "Optional", "type": "Rosette", "place": "Midground"},
    {"id": "anubias-nana-petite", "name": "Anubias Nana Petite", "growth": "Very Slow", "co2": "Optional", "type": "Epiphyte", "place": "Hardscape"},
    {"id": "crypt-flamingo", "name": "Cryptocoryne Flamingo", "growth": "Slow", "co2": "High", "type": "Rare Rosette", "place": "Midground"},
    {"id": "hairgrass-mini", "name": "Hairgrass Mini", "growth": "Medium", "co2": "Recommended", "type": "Grass", "place": "Foreground"},
    {"id": "staurogyne-repens", "name": "Staurogyne Repens", "growth": "Slow", "co2": "Recommended", "type": "Stem/Bushy", "place": "Foreground"},
    {"id": "rotala-green", "name": "Rotala Green", "growth": "Fast", "co2": "Recommended", "type": "Stem", "place": "Background"},
    {"id": "weeping-moss", "name": "Weeping Moss", "growth": "Slow", "co2": "Optional", "type": "Moss", "place": "Hardscape"}
]

def create_gradient_canvas(width, height):
    base = Image.new('RGB', (width, height), GRADIENT_TOP)
    for y in range(height):
        r = int(GRADIENT_TOP[0] + (GRADIENT_BOTTOM[0] - GRADIENT_TOP[0]) * (y / height))
        g = int(GRADIENT_TOP[1] + (GRADIENT_BOTTOM[1] - GRADIENT_TOP[1]) * (y / height))
        b = int(GRADIENT_TOP[2] + (GRADIENT_BOTTOM[2] - GRADIENT_TOP[2]) * (y / height))
        for x in range(width):
            base.putpixel((x, y), (r, g, b))
    return base

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def create_branded_sticker(plant):
    canvas = create_gradient_canvas(500, 800)
    canvas = canvas.convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    # --- DYNAMIC FONT SCALING FOR NAME ---
    current_font_size = 52 # Starting size
    name_text = plant['name']
    
    while current_font_size > 10:
        try:
            temp_font = ImageFont.truetype(font_path, current_font_size)
        except:
            temp_font = ImageFont.load_default()
            
        left, top, right, bottom = draw.textbbox((0, 0), name_text, font=temp_font)
        text_width = right - left
        
        # If the text fits inside 440px (allowing margins), keep it
        if text_width <= 440:
            f_name = temp_font
            break
        current_font_size -= 2 # Shrink font size by 2px each loop

    # Other fonts
    try:
        f_label = ImageFont.truetype(font_path, 34) 
        f_val = ImageFont.truetype(font_path, 26)   
    except:
        f_label = f_val = ImageFont.load_default()

    # 1. Plant Name (Now fits regardless of length!)
    draw.text((250, 65), name_text, fill=TEXT_DARK, font=f_name, anchor="ms")
    draw.line([(35, 85), (465, 85)], fill="black", width=6)

    # 2. Specs Section
    start_y = 165 
    spacing = 75  
    specs = [
        ("Growth:", plant['growth']),
        ("CO2:", plant['co2']),
        ("Type:", plant['type']),
        ("Zone:", plant['place'])
    ]

    for i, (label, val) in enumerate(specs):
        curr_y = start_y + (i * spacing)
        draw.text((60, curr_y), label, fill=TEXT_DARK, font=f_label)
        draw.text((245, curr_y + 8), val, fill=TEXT_DARK, font=f_val)

    # 3. QR Code
    qr_url = f"{BASE_URL}/{plant['id']}.html"
    qr = qrcode.QRCode(box_size=5, border=1) 
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_x = (500 - qr_img.width) // 2
    canvas.paste(qr_img, (qr_x, 465), qr_img) 

    # 4. Logo
    try:
        logo = Image.open(LOGO_FILE).convert("RGBA")
        logo.thumbnail((340, 150))
        x_logo = (500 - logo.width) // 2
        y_logo = 685 
        canvas.paste(logo, (x_logo, y_logo), logo)
    except:
        draw.text((250, 740), "Ease-Aquatics™", fill=TEXT_DARK, font=f_label, anchor="ms")

    canvas = add_corners(canvas, CORNER_RADIUS)
    canvas.save(f"{LABEL_DIR}/{plant['id']}_branded.png", "PNG")

def main():
    if not os.path.exists(LABEL_DIR): os.makedirs(LABEL_DIR)
    print(f"🚀 Generating High-Impact Branded Stickers with Auto-Scaling...")
    for plant in plant_data:
        create_branded_sticker(plant)
        print(f"✅ Created: {plant['name']}")

if __name__ == "__main__":
    main()