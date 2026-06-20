import os
import qrcode
import urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

# --- PHYSICAL SIZE ---
STICKER_W_CM = 5.0
STICKER_H_CM = 2.0
DPI = 600  # high DPI since label is tiny and will be viewed up close on a curved cup

PX_PER_CM = DPI / 2.54
W = int(round(STICKER_W_CM * PX_PER_CM))
H = int(round(STICKER_H_CM * PX_PER_CM))

BASE_URL = "https://ease-aquatics.co.za"
LOGO_FILE = "dist/img/logo_white.png"

CYAN_BACKGROUND = (34, 187, 187)
TEXT_DARK_LABEL = (255, 255, 255, 210)
TEXT_WHITE = (255, 255, 255, 255)
CORNER_RADIUS = int(round(0.12 * PX_PER_CM))

# --- AUTOMATIC FONT LOGIC FOR WSL ---
FONT_DIR = "dist/fonts"
FONT_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
FONT_SEMI = os.path.join(FONT_DIR, "Poppins-Medium.ttf")

def download_required_fonts():
    if not os.path.exists(FONT_DIR):
        os.makedirs(FONT_DIR)
    urls = {
        FONT_BOLD: "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
        FONT_SEMI: "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Medium.ttf"
    }
    for path, url in urls.items():
        if not os.path.exists(path):
            print(f"📥 Downloading missing font asset: {os.path.basename(path)}...")
            try:
                urllib.request.urlretrieve(url, path)
            except Exception as e:
                print(f"⚠️ Font fetch failed: {e}")

download_required_fonts()

plant = {"id": "weeping-moss", "name": "Weeping Moss", "growth": "Slow", "co2": "Optional", "type": "Moss", "place": "Hardscape"}

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

def fit_font(draw, text, font_path, max_width, start_size, min_size=10, step=1):
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

def create_sticker(plant):
    canvas = Image.new('RGBA', (W, H), CYAN_BACKGROUND)
    draw = ImageDraw.Draw(canvas)

    margin = int(round(0.1 * PX_PER_CM))

    qr_card_size = H - margin * 2
    pad = max(2, int(round(qr_card_size * 0.05)))
    qr_size = qr_card_size - pad * 2

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=1,
    )
    qr.add_data(f"{BASE_URL}/{plant['id']}/")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

    card = Image.new("RGBA", (qr_card_size, qr_card_size), (255, 255, 255, 255))
    card_rad = int(round(qr_card_size * 0.12))
    card = add_corners(card, card_rad)
    canvas.paste(card, (margin, margin), card)
    canvas.paste(qr_img, (margin + pad, margin + pad), qr_img)

    text_start_x = margin + qr_card_size + int(round(0.08 * PX_PER_CM))
    right_margin = margin
    text_max_width = W - right_margin - text_start_x

    name_text = plant['name'].upper()
    f_name, tw, th = fit_font(draw, name_text, FONT_BOLD, text_max_width, start_size=int(H * 0.34), min_size=24)
    title_y = int(round(H * 0.07))
    draw.text((text_start_x, title_y), name_text, fill=TEXT_WHITE, font=f_name)

    line_y = title_y + th + int(round(H * 0.05))
    line_w = max(2, int(round(H * 0.015)))
    draw.line([(text_start_x, line_y), (W - right_margin, line_y)], fill=(255, 255, 255, 160), width=line_w)

    def build_row_size(pairs, size):
        try:
            fb = ImageFont.truetype(FONT_BOLD, size)
        except:
            fb = ImageFont.load_default()
        total_w = 0
        for label, value in pairs:
            seg = f"{label}{value}"
            l, t, r, b = draw.textbbox((0, 0), seg, font=fb)
            total_w += (r - l)
        total_w += (len(pairs) - 1) * int(round(size * 1.0))
        return total_w

    def fit_row(pairs, max_width, start_size, min_size=10):
        size = start_size
        while size > min_size:
            if build_row_size(pairs, size) <= max_width:
                return size
            size -= 1
        return min_size

    row1_pairs = [("Growth: ", plant['growth']), ("CO2: ", plant['co2'])]
    row2_pairs = [("Type: ", plant['type']), ("Zone: ", plant['place'])]

    start_size = int(H * 0.17)
    size1 = fit_row(row1_pairs, text_max_width, start_size)
    size2 = fit_row(row2_pairs, text_max_width, start_size)
    common_size = max(10, min(size1, size2))
    
    try:
        f_label = ImageFont.truetype(FONT_SEMI, common_size)
        f_value = ImageFont.truetype(FONT_BOLD, common_size)
    except:
        f_label = f_value = ImageFont.load_default()

    def draw_rich_line(pairs, y_pos):
        current_x = text_start_x
        for i, (label, value) in enumerate(pairs):
            draw.text((current_x, y_pos), label, fill=TEXT_DARK_LABEL, font=f_label)
            l, t, r, b = draw.textbbox((0, 0), label, font=f_label)
            current_x += (r - l)
            sep = "  |  " if i < len(pairs) - 1 else ""
            val_text = value + sep
            draw.text((current_x, y_pos), val_text, fill=TEXT_WHITE, font=f_value)
            l, t, r, b = draw.textbbox((0, 0), val_text, font=f_value)
            current_x += (r - l)

    row_gap = common_size + int(round(H * 0.06))
    row1_y = line_y + int(round(H * 0.04))
    row2_y = row1_y + row_gap
    draw_rich_line(row1_pairs, row1_y)
    draw_rich_line(row2_pairs, row2_y)

    canvas = add_corners(canvas, CORNER_RADIUS)
    canvas.save("weeping_moss_5x2cm.png", "PNG", dpi=(DPI, DPI))
    print(f" Saved at {W}x{H}px, {DPI} DPI, physical size {STICKER_W_CM}cm x {STICKER_H_CM}cm")

create_sticker(plant)