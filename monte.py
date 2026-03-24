import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

# --- PIXEL LIMIT BYPASS ---
Image.MAX_IMAGE_PIXELS = None 

# --- SETTINGS ---
BASE_URL = "https://ease-aquatics.co.za"
LOGO_FILE = "dist/img/SimpleLogo.png" 
LABEL_DIR = "Final_Monte_Carlo_Tags"

# --- BRAND PALETTE ---
GRADIENT_TOP = (175, 225, 225) 
GRADIENT_BOTTOM = (255, 255, 255) 
TEXT_DARK = (28, 28, 30) 
CORNER_RADIUS = 35 

# Target Dimensions for 6.7cm Height (at 300 DPI)
# Width: ~4.2cm (496 px) | Height: 6.7cm (791 px)
WIDTH, HEIGHT = 496, 791

# Plant Data
plant = {
    "id": "monte-carlo", 
    "name": "MONTE CARLO", 
    "growth": "Fast", 
    "co2": "High", 
    "type": "Carpeting", 
    "place": "Foreground"
}

def create_gradient_canvas(w, h):
    base = Image.new('RGB', (w, h), GRADIENT_TOP)
    for y in range(h):
        r = int(GRADIENT_TOP[0] + (GRADIENT_BOTTOM[0] - GRADIENT_TOP[0]) * (y / h))
        g = int(GRADIENT_TOP[1] + (GRADIENT_BOTTOM[1] - GRADIENT_TOP[1]) * (y / h))
        b = int(GRADIENT_TOP[2] + (GRADIENT_BOTTOM[2] - GRADIENT_TOP[2]) * (y / h))
        for x in range(w):
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

def generate_tag():
    if not os.path.exists(LABEL_DIR): 
        os.makedirs(LABEL_DIR)
    
    # 1. Create Base
    canvas = create_gradient_canvas(WIDTH, HEIGHT).convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    
    # Font path logic
    font_path = "C:/Windows/Fonts/arialbd.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    try:
        f_name = ImageFont.truetype(font_path, 56)   # Title
        f_label = ImageFont.truetype(font_path, 38)  # Category (Growth, CO2)
        f_val = ImageFont.truetype(font_path, 36)    # Values (Fast, High) - Maxed out size
    except:
        f_name = f_label = f_val = ImageFont.load_default()

    # 2. Add Title
    draw.text((WIDTH//2, 65), plant['name'], fill=TEXT_DARK, font=f_name, anchor="ms")
    draw.line([(35, 85), (WIDTH-35, 85)], fill="black", width=6)

    # 3. Add Specs (Highly Readable Layout)
    specs = [
        ("Growth:", plant['growth']), 
        ("CO2:", plant['co2']), 
        ("Type:", plant['type']), 
        ("Zone:", plant['place'])
    ]
    
    for i, (label, val) in enumerate(specs):
        curr_y = 150 + (i * 85)
        # Category Label
        draw.text((45, curr_y), label, fill=TEXT_DARK, font=f_label)
        # The Value - Placed slightly further right to avoid overlapping labels
        draw.text((235, curr_y + 2), val, fill=TEXT_DARK, font=f_val)

    # 4. Generate QR Code
    qr_url = f"{BASE_URL}/{plant['id']}/"
    qr = qrcode.QRCode(version=1, box_size=6, border=1) 
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    
    # Paste QR Code
    qr_y = 490
    canvas.paste(qr_img, ((WIDTH - qr_img.width) // 2, qr_y), qr_img)

    # 5. Add Logo
    try:
        logo = Image.open(LOGO_FILE).convert("RGBA")
        logo.thumbnail((300, 110))
        logo_y = 700
        canvas.paste(logo, ((WIDTH - logo.width) // 2, logo_y), logo)
    except:
        draw.text((WIDTH//2, 740), "Ease-Aquatics™", fill=TEXT_DARK, font=f_label, anchor="ms")

    # 6. Finalize
    canvas = add_corners(canvas, CORNER_RADIUS)
    output_path = f"{LABEL_DIR}/monte_carlo_67mm_final.png"
    canvas.save(output_path)
    print(f"✅ Success! Label saved to: {output_path}")

if __name__ == "__main__":
    generate_tag()