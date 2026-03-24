import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

# --- SETTINGS ---
BASE_URL = "https://ease-aquatics.co.za"
LOGO_FILE = "dist/img/SimpleLogo.png" 
LABEL_DIR = "Readable_Side_Stickers"

# --- BRAND PALETTE ---
GRADIENT_LEFT = (175, 225, 225) 
GRADIENT_RIGHT = (255, 255, 255) 
TEXT_DARK = (28, 28, 30) 
CORNER_RADIUS = 30 

plant_data = [
    {"id": "weeping-moss", "name": "WEEPING MOSS", "growth": "Slow", "co2": "Optional", "type": "Moss", "place": "Hardscape"}
]

def create_horizontal_gradient(width, height):
    base = Image.new('RGB', (width, height), GRADIENT_LEFT)
    for x in range(width):
        r = int(GRADIENT_LEFT[0] + (GRADIENT_RIGHT[0] - GRADIENT_LEFT[0]) * (x / width))
        g = int(GRADIENT_LEFT[1] + (GRADIENT_RIGHT[1] - GRADIENT_LEFT[1]) * (x / width))
        b = int(GRADIENT_LEFT[2] + (GRADIENT_RIGHT[2] - GRADIENT_LEFT[2]) * (x / width))
        for y in range(height):
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

def create_readable_sticker(plant):
    width, height = 800, 350
    canvas = create_horizontal_gradient(width, height).convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    
    # Path logic
    font_path = "C:/Windows/Fonts/arialbd.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    try:
        f_name = ImageFont.truetype(font_path, 52)   # Increased title size
        f_specs = ImageFont.truetype(font_path, 28)  # Increased from 22 for readability
        f_brand = ImageFont.truetype(font_path, 26)
    except:
        f_name = f_specs = f_brand = ImageFont.load_default()

    # 1. QR Code (Left)
    qr_url = f"{BASE_URL}/{plant['id']}/"
    qr = qrcode.QRCode(version=1, box_size=8, border=1) # Smaller border to save space
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    canvas.paste(qr_img, (25, (height - qr_img.height) // 2), qr_img)

    # 2. Plant Name (Top Middle)
    draw.text((310, 50), plant['name'], fill=TEXT_DARK, font=f_name)
    draw.line([(310, 110), (760, 110)], fill="black", width=5)

    # 3. Enhanced Specs (Stacked for readability)
    # Using larger, bold text for the actual values
    spec_line_1 = f"Growth: {plant['growth']}  |  CO2: {plant['co2']}"
    spec_line_2 = f"Type: {plant['type']}  |  Zone: {plant['place']}"
    
    draw.text((310, 135), spec_line_1, fill=TEXT_DARK, font=f_specs)
    draw.text((310, 185), spec_line_2, fill=TEXT_DARK, font=f_specs)

    # 4. Branding (Bottom Right)
    try:
        logo = Image.open(LOGO_FILE).convert("RGBA")
        logo.thumbnail((220, 70))
        canvas.paste(logo, (width - logo.width - 30, height - logo.height - 25), logo)
    except:
        draw.text((width - 240, height - 60), "Ease-Aquatics™", fill=TEXT_DARK, font=f_brand)

    canvas = add_corners(canvas, CORNER_RADIUS)
    canvas.save(f"{LABEL_DIR}/{plant['id']}_side_readable.png", "PNG")

def main():
    if not os.path.exists(LABEL_DIR): os.makedirs(LABEL_DIR)
    for plant in plant_data:
        create_readable_sticker(plant)
        print(f"✅ Readable Label Created: {plant['name']}")

if __name__ == "__main__":
    main()