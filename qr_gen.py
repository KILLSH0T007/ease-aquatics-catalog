import os
import qrcode
import urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

# --- SETTINGS ---
BASE_URL = "https://ease-aquatics.co.za"
LOGO_FILE = "dist/img/logo_white.png"
LABEL_DIR = "Final_Cyan_Stickers"

# --- BRAND PALETTE ---
CYAN_BACKGROUND = (34, 187, 187)
TEXT_DARK = (255, 255, 255, 215)   # soft white for labels
TEXT_WHITE = (255, 255, 255, 255)  # crisp white for values
CORNER_RADIUS = 45

# --- SYSTEM AUTOMATIC FONT LOGIC ---
FONT_DIR = "dist/fonts"
FONT_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
FONT_SEMI = os.path.join(FONT_DIR, "Poppins-Medium.ttf")

def download_required_fonts():
    """Automatically fetch pristine Poppins fonts into project directory for WSL execution."""
    if not os.path.exists(FONT_DIR):
        os.makedirs(FONT_DIR)
    
    urls = {
        FONT_BOLD: "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
        FONT_SEMI: "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Medium.ttf"
    }
    
    for path, url in urls.items():
        if not os.path.exists(path):
            print(f"📥 Downloading missing font asset to project directory: {os.path.basename(path)}...")
            try:
                urllib.request.urlretrieve(url, path)
            except Exception as e:
                print(f"⚠️ Font fetch failed. Defaulting to standard TrueType fallback paths: {e}")

# Trigger font setup check
download_required_fonts()

W, H = 1000, 420

plant_data = [
    {"id": "weeping-moss", "name": "Weeping Moss", "growth": "Slow", "co2": "Optional", "type": "Moss", "place": "Hardscape"},
    {"id": "monte-carlo", "name": "Monte Carlo", "growth": "Fast", "co2": "High", "type": "Carpeting", "place": "Foreground"},
    {"id": "pogo-helferi", "name": "Pogostemon Helferi", "growth": "Medium", "co2": "Required", "type": "Star Plant", "place": "Foreground/Mid"},
    {"id": "crypt-wendtii", "name": "Cryptocoryne Wendtii", "growth": "Slow", "co2": "Optional", "type": "Rosette", "place": "Midground"},
    {"id": "anubias-nana-petite", "name": "Anubias Nana Petite", "growth": "Very Slow", "co2": "Optional", "type": "Epiphyte", "place": "Hardscape"},
    {"id": "crypt-flamingo", "name": "Cryptocoryne Flamingo", "growth": "Slow", "co2": "High", "type": "Rare Rosette", "place": "Midground"},
    {"id": "hairgrass-mini", "name": "Hairgrass Mini", "growth": "Medium", "co2": "Recommended", "type": "Grass", "place": "Foreground"},
    {"id": "staurogyne-repens", "name": "Staurogyne Repens", "growth": "Slow", "co2": "Recommended", "type": "Stem/Bushy", "place": "Foreground"},
    {"id": "rotala-green", "name": "Rotala Green", "growth": "Fast", "co2": "Recommended", "type": "Stem", "place": "Background"},
]

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

def make_white_logo():
    """Knockout the brand logo to solid white, preserving anti-aliased alpha."""
    try:
        img = Image.open(LOGO_FILE).convert("RGBA")
        arr = np.array(img)
        a = arr[..., 3]
        white = np.zeros_like(arr)
        white[..., 0] = 255
        white[..., 1] = 255
        white[..., 2] = 255
        white[..., 3] = a
        return Image.fromarray(white, "RGBA")
    except Exception as e:
        print(f"⚠️ Could not load logo image file path '{LOGO_FILE}': {e}. Creating text placeholder configuration.")
        return None

WHITE_LOGO = make_white_logo()

def fit_font(draw, text, font_path, max_width, start_size, min_size=18, step=2):
    try:
        size = start_size
        while size > min_size:
            f = ImageFont.truetype(font_path, size)
            l, t, r, b = draw.textbbox((0, 0), text, font=f)
            if (r - l) <= max_width:
                return f, (r - l), (b - t)
            size -= step
        f = ImageFont.truetype(font_path, min_size)
        l, t, r, b = draw.textbbox((0, 0), text, font=f)
        return f, (r - l), (b - t)
    except:
        f = ImageFont.load_default()
        l, t, r, b = draw.textbbox((0, 0), text, font=f)
        return f, (r - l), (b - t)

def create_branded_sticker(plant):
    canvas = Image.new('RGBA', (W, H), CYAN_BACKGROUND)
    draw = ImageDraw.Draw(canvas)

    # ---- Layout constants ----
    qr_size_target = 330
    qr_margin = 45
    text_start_x = 420
    right_margin = 40
    text_max_width = (W - right_margin) - text_start_x  # available width for text block

    # 1. QR CODE
    qr_url = f"{BASE_URL}/{plant['id']}/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=9,
        border=2,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_img = qr_img.resize((qr_size_target, qr_size_target), Image.LANCZOS)

    # white rounded card behind QR for a cleaner frame
    pad = 14
    card = Image.new("RGBA", (qr_size_target + pad * 2, qr_size_target + pad * 2), (255, 255, 255, 255))
    card = add_corners(card, 20)
    card_x, card_y = qr_margin, (H - card.height) // 2
    canvas.paste(card, (card_x, card_y), card)
    canvas.paste(qr_img, (card_x + pad, card_y + pad), qr_img)

    # 2. TITLE — auto-fit to available width
    name_text = plant['name'].upper()
    f_name, tw, th = fit_font(draw, name_text, FONT_BOLD, text_max_width, start_size=52, min_size=26)
    title_y = 55
    draw.text((text_start_x, title_y), name_text, fill=TEXT_WHITE, font=f_name)

    line_y = title_y + th + 22
    draw.line([(text_start_x, line_y), (W - right_margin, line_y)], fill=(255, 255, 255, 160), width=4)

    # 3. INFO ROWS — auto-shrink font so each row always fits text_max_width
    f_label_size = 28

    def build_row(pairs, size):
        try:
            f = ImageFont.truetype(FONT_SEMI, size)
            fb = ImageFont.truetype(FONT_BOLD, size)
        except:
            f = fb = ImageFont.load_default()
            
        total_w = 0
        seg_widths = []
        for label, value, _ in pairs:
            seg = f"{label}{value}"
            l, t, r, b = draw.textbbox((0, 0), seg, font=fb)
            w = r - l
            seg_widths.append(w)
            total_w += w
        # spacing between segments
        total_w += (len(pairs) - 1) * 28
        return f, fb, total_w

    def fit_row(pairs, max_width, start_size, min_size=16):
        size = start_size
        while size > min_size:
            f, fb, total_w = build_row(pairs, size)
            if total_w <= max_width:
                return f, fb, size
            size -= 1
        f, fb, _ = build_row(pairs, min_size)
        return f, fb, min_size

    row1_pairs = [("Growth: ", plant['growth'], None), ("CO2: ", plant['co2'], None)]
    row2_pairs = [("Type: ", plant['type'], None), ("Zone: ", plant['place'], None)]

    # fit both rows to the SAME size (use the smaller of the two) for visual consistency
    f1, fb1, size1 = fit_row(row1_pairs, text_max_width, f_label_size)
    f2, fb2, size2 = fit_row(row2_pairs, text_max_width, f_label_size)
    common_size = min(size1, size2)
    
    try:
        f_label = ImageFont.truetype(FONT_SEMI, common_size)
        f_value = ImageFont.truetype(FONT_BOLD, common_size)
    except:
        f_label = f_value = ImageFont.load_default()

    def draw_rich_line(pairs, y_pos, font_label, font_value):
        current_x = text_start_x
        for label, value, _ in pairs:
            draw.text((current_x, y_pos), label, fill=TEXT_DARK, font=font_label)
            l, t, r, b = draw.textbbox((0, 0), label, font=font_label)
            current_x += (r - l)
            sep = "   |   " if (label, value, _) != pairs[-1] else ""
            val_text = value + sep
            draw.text((current_x, y_pos), val_text, fill=TEXT_WHITE, font=font_value)
            l, t, r, b = draw.textbbox((0, 0), val_text, font=font_value)
            current_x += (r - l)

    row_gap = common_size + 28
    row1_y = line_y + 28
    row2_y = row1_y + row_gap
    draw_rich_line(row1_pairs, row1_y, f_label, f_value)
    draw_rich_line(row2_pairs, row2_y, f_label, f_value)

    # 4. LOGO — white knockout, bottom-right, properly proportioned
    if WHITE_LOGO:
        logo = WHITE_LOGO.copy()
        logo.thumbnail((250, 80), Image.LANCZOS)
        x_logo = (W - right_margin) - logo.width
        y_logo = H - 30 - logo.height
        canvas.paste(logo, (x_logo, y_logo), logo)
    else:
        try:
            f_fallback = ImageFont.truetype(FONT_BOLD, 26)
        except:
            f_fallback = ImageFont.load_default()
        draw.text(((W - right_margin), H - 45), "EASE-AQUATICS™", fill=TEXT_WHITE, font=f_fallback, anchor="rs")

    canvas = add_corners(canvas, CORNER_RADIUS)
    out_path = f"{LABEL_DIR}/{plant['id']}_cyan_sticker.png"
    canvas.save(out_path, "PNG")
    return out_path

def main():
    if not os.path.exists(LABEL_DIR):
        os.makedirs(LABEL_DIR)
    print("Running sticker generation...")
    for plant in plant_data:
        p = create_branded_sticker(plant)
        print(f"Created: {p}")

if __name__ == "__main__":
    main()