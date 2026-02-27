import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

# --- PIXEL LIMIT BYPASS ---
Image.MAX_IMAGE_PIXELS = None 

# --- SETTINGS ---
GITHUB_USERNAME = "KILLSH0T007" 
REPO_NAME = "ease-aquatics-catalog"

# This matches your live GitHub Pages structure
BASE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/dist"
# Update this to .jpg to match your uploaded "Logo_Clean.jpg"
LOGO_FILE = "dist/img/SimpleLogo.png" 
LABEL_DIR = "Final_Branded_Stickers"

# --- BRAND PALETTE ---
SILVER_METALLIC = (196, 198, 199, 255) 
TRANSPARENT = (255, 255, 255, 0)
WHITE = (255, 255, 255, 255)
TEAL = (74, 158, 158, 255)
TEXT_DARK = (45, 45, 48, 255) 
BORDER_SILVER = (160, 162, 164, 255) 

# --- FULL PLANT DATA (Synced with aquatics.py) ---
plant_data = [
    {"id": "monte-carlo", "name": "Monte Carlo", "care": "Medium", "light": "High", "temp": "22-28°C", "co2": "High"},
    {"id": "pogo-helferi", "name": "Pogostemon Helferi", "care": "Medium", "light": "Med/High", "temp": "22-30°C", "co2": "Required"},
    {"id": "crypt-wendtii", "name": "Cryptocoryne Wendtii", "care": "Easy", "light": "Low-Med", "temp": "20-28°C", "co2": "Optional"},
    {"id": "anubias-nana-petite", "name": "Anubias Nana Petite", "care": "Very Easy", "light": "Low", "temp": "20-30°C", "co2": "Optional"},
    {"id": "crypt-flamingo", "name": "Cryptocoryne Flamingo", "care": "Hard", "light": "High", "temp": "22-28°C", "co2": "High"},
    {"id": "hairgrass-mini", "name": "Hairgrass Mini", "care": "Medium", "light": "Medium", "temp": "20-28°C", "co2": "Recommended"},
    {"id": "staurogyne-repens", "name": "Staurogyne Repens", "care": "Easy", "light": "Medium", "temp": "20-28°C", "co2": "Recommended"},
    {"id": "rotala-green", "name": "Rotala Green", "care": "Easy", "light": "Medium", "temp": "20-30°C", "co2": "Recommended"},
    {"id": "weeping-moss", "name": "Weeping Moss", "care": "Easy", "light": "Low-Med", "temp": "18-26°C", "co2": "Optional"}
]

def create_branded_sticker(plant):
    # 1. Canvas Setup (RGBA)
    canvas = Image.new('RGBA', (500, 800), color=TRANSPARENT)
    draw = ImageDraw.Draw(canvas)
    
    # 2. Draw Silver Sticker Body
    sticker_shape = [15, 15, 485, 785]
    radius = 35
    draw.rounded_rectangle(sticker_shape, radius=radius, fill=SILVER_METALLIC)
    
    # 3. Border Details
    draw.rounded_rectangle(sticker_shape, radius=radius, outline=BORDER_SILVER, width=3)
    draw.rounded_rectangle([22, 22, 478, 778], radius=30, outline=BORDER_SILVER, width=1)
    
    # 4. Add Logo
    try:
        logo = Image.open(LOGO_FILE).convert("RGBA")
        logo.thumbnail((380, 160)) 
        x_logo = (500 - logo.width) // 2
        y_logo = 35 
        canvas.paste(logo, (x_logo, y_logo), logo)
    except:
        draw.text((250, 80), "Ease-Aquatics™", fill=TEAL, anchor="ms")

    # 5. Load Fonts
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        f_name = ImageFont.truetype(font_path, 35)
        f_label = ImageFont.truetype(font_path, 28)
        f_val = ImageFont.truetype(font_path, 28)
        f_btn = ImageFont.truetype(font_path, 24)
    except:
        f_name = f_label = f_val = f_btn = ImageFont.load_default()

    # 6. Plant Name & Manual Underline
    name_text = plant['name']
    name_pos = (250, 230)
    draw.text(name_pos, name_text, fill=TEXT_DARK, font=f_name, anchor="ms")
    left, top, right, bottom = draw.textbbox(name_pos, name_text, font=f_name, anchor="ms")
    underline_y = bottom + 5
    draw.line([(left, underline_y), (right, underline_y)], fill=TEAL, width=3)

    # 7. Care Info Section
    start_y = 310
    spacing = 62
    specs = [
        ("Care Level:", plant['care']),
        ("Light:", plant['light']),
        ("Temp:", plant['temp']),
        ("CO2:", plant['co2'])
    ]

    for i, (label, val) in enumerate(specs):
        curr_y = start_y + (i * spacing)
        draw.text((65, curr_y), label, fill=TEXT_DARK, font=f_label)
        draw.text((255, curr_y), val, fill=TEXT_DARK, font=f_val)

    # 8. QR Code pointing to live GitHub site
    qr_url = f"{BASE_URL}/{plant['id']}.html"
    qr = qrcode.QRCode(box_size=5, border=1) 
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    
    qr_x = (500 - qr_img.width) // 2
    canvas.paste(qr_img, (qr_x, 540), qr_img) 

    # 9. Teal Bottom Button
    btn_rect = [40, 715, 460, 775]
    draw.rounded_rectangle(btn_rect, radius=12, fill=TEAL)
    draw.text((250, 745), "SCAN FOR INFO", fill=WHITE, font=f_btn, anchor="ms")

    # 10. Save
    canvas.save(f"{LABEL_DIR}/{plant['id']}_pro_silver.png", "PNG")

def main():
    if not os.path.exists(LABEL_DIR): os.makedirs(LABEL_DIR)
    print(f"🚀 Generating Underlined Silver Stickers for Ease-Aquatics...")
    for plant in plant_data:
        create_branded_sticker(plant)
        print(f"✅ Created: {plant['name']}")

if __name__ == "__main__":
    main()