import os
import qrcode
import urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

Image.MAX_IMAGE_PIXELS = None

# --- SETTINGS ---
BASE_URL = "https://ease-aquatics.co.za"
LOGO_FILE = "logo_white.png"
OUTPUT_IMG_DIR = "outputs_high_res"
OUTPUT_PDF_DIR = "outputs_print_sheets"

# --- PHYSICAL SIZE ---
STICKER_W_CM = 5.0
STICKER_H_CM = 3.0
DPI = 600

PX_PER_CM = DPI / 2.54
W = int(round(STICKER_W_CM * PX_PER_CM))
H = int(round(STICKER_H_CM * PX_PER_CM))

CYAN_BACKGROUND = (34, 187, 187)
TEXT_LABEL = (255, 255, 255, 215)
TEXT_WHITE = (255, 255, 255, 255)
CORNER_RADIUS = int(round(0.12 * PX_PER_CM))

# --- SYSTEM AUTOMATIC FONT LOGIC FOR WSL ---
FONT_DIR = "dist/fonts"
FONT_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
FONT_SEMI = os.path.join(FONT_DIR, "Poppins-Medium.ttf")

def download_required_fonts():
    """Automatically fetch Poppins fonts into project folder for seamless WSL execution."""
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
                print(f"⚠️ Font fetch missed: {e}")

# Run the font initialization check
download_required_fonts()

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

def fit_font(draw, text, font_path, max_width, start_size, min_size=14, step=1):
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
    canvas_img = Image.new('RGBA', (W, H), CYAN_BACKGROUND)
    draw = ImageDraw.Draw(canvas_img)

    margin = int(round(0.12 * PX_PER_CM))

    qr_card_size = int(round((H - margin * 2) * 0.68))
    qr_y = margin + ((H - margin * 2) - qr_card_size) // 2
    pad = max(2, int(round(qr_card_size * 0.07)))
    qr_size = qr_card_size - pad * 2

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
    qr.add_data(f"{BASE_URL}/{plant['id']}/")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

    card = Image.new("RGBA", (qr_card_size, qr_card_size), (255, 255, 255, 255))
    card = add_corners(card, int(round(qr_card_size * 0.14)))
    canvas_img.paste(card, (margin, qr_y), card)
    canvas_img.paste(qr_img, (margin + pad, qr_y + pad), qr_img)

    text_start_x = margin + qr_card_size + int(round(0.18 * PX_PER_CM))
    right_margin = margin
    text_max_width = W - right_margin - text_start_x

    # --- TITLE ---
    name_text = plant['name'].upper()
    f_name, tw, th = fit_font(draw, name_text, FONT_BOLD, text_max_width, start_size=int(H * 0.22), min_size=24)
    title_y = int(round(H * 0.06))
    draw.text((text_start_x, title_y), name_text, fill=TEXT_WHITE, font=f_name)

    line_y = title_y + th + int(round(H * 0.04))
    line_w = max(2, int(round(H * 0.01)))
    draw.line([(text_start_x, line_y), (W - right_margin, line_y)], fill=(255, 255, 255, 160), width=line_w)

    # --- INFO ROWS ---
    rows_flat = [
        ("Growth", plant['growth']),
        ("CO2", plant['co2']),
        ("Type", plant['type']),
        ("Zone", plant['place']),
    ]

    footer_reserve = int(round(H * 0.16))  
    available_h = H - line_y - footer_reserve - int(round(H * 0.02))

    def row_text(label, value):
        return f"{label}: {value}"

    def fits(size):
        try:
            f = ImageFont.truetype(FONT_BOLD, size)
        except:
            return True
        l, t, r, b = draw.textbbox((0, 0), "Ag", font=f)
        line_h = (b - t)
        gap = int(round(line_h * 0.55))
        total_h = line_h * 4 + gap * 3
        if total_h > available_h:
            return False
        for label, value in rows_flat:
            l, t, r, b = draw.textbbox((0, 0), row_text(label, value), font=f)
            if (r - l) > text_max_width:
                return False
        return True

    size = int(H * 0.14)
    min_size = 16
    while size > min_size and not fits(size):
        size -= 1
        
    try:
        f_label = ImageFont.truetype(FONT_SEMI, size)
        f_value = ImageFont.truetype(FONT_BOLD, size)
    except:
        f_label = f_value = ImageFont.load_default()

    l, t, r, b = draw.textbbox((0, 0), "Ag", font=f_value)
    line_h = (b - t)
    gap = int(round(line_h * 0.55))
    block_h = line_h * 4 + gap * 3
    extra_space = max(0, available_h - block_h)

    cur_y = line_y + int(round(H * 0.025)) + int(extra_space * 0.3)
    for label, value in rows_flat:
        x = text_start_x
        label_text = f"{label}: "
        draw.text((x, cur_y), label_text, fill=TEXT_LABEL, font=f_label)
        l, t, r, b = draw.textbbox((0, 0), label_text, font=f_label)
        x += (r - l)
        draw.text((x, cur_y), value, fill=TEXT_WHITE, font=f_value)
        cur_y += line_h + gap

    # --- LOGO STRIP ---
    try:
        logo = Image.open(LOGO_FILE).convert("RGBA")
        logo_h_target = int(round(H * 0.13))
        ratio = logo_h_target / logo.height
        logo = logo.resize((int(logo.width * ratio), logo_h_target), Image.LANCZOS)
        x_logo = (W - right_margin) - logo.width
        y_logo = H - margin - logo.height
        canvas_img.paste(logo, (x_logo, y_logo), logo)
    except FileNotFoundError:
        pass

    canvas_img = add_corners(canvas_img, CORNER_RADIUS)
    img_path = os.path.join(OUTPUT_IMG_DIR, f"{plant['id']}_5x3cm.png")
    canvas_img.save(img_path, "PNG", dpi=(DPI, DPI))
    return img_path

def generate_pdf_sheet(plant, img_path):
    pdf_path = os.path.join(OUTPUT_PDF_DIR, f"{plant['id']}_sheet_A4.pdf")

    sticker_w_pdf = STICKER_W_CM * cm
    sticker_h_pdf = STICKER_H_CM * cm
    page_w, page_h = A4

    margin_pdf = 1.0 * cm
    gap_x = 0.3 * cm
    gap_y = 0.3 * cm

    usable_w = page_w - 2 * margin_pdf
    usable_h = page_h - 2 * margin_pdf

    cols = int((usable_w + gap_x) // (sticker_w_pdf + gap_x))
    rows_n = int((usable_h + gap_y) // (sticker_h_pdf + gap_y))

    grid_w = cols * sticker_w_pdf + (cols - 1) * gap_x
    start_x = (page_w - grid_w) / 2
    start_y = page_h - margin_pdf - sticker_h_pdf

    pdf_canvas = canvas.Canvas(pdf_path, pagesize=A4)

    count = 0
    for row in range(rows_n):
        for col in range(cols):
            x = start_x + col * (sticker_w_pdf + gap_x)
            y = start_y - row * (sticker_h_pdf + gap_y)
            pdf_canvas.drawImage(img_path, x, y, width=sticker_w_pdf, height=sticker_h_pdf, mask='auto')
            pdf_canvas.setStrokeColorRGB(0.7, 0.7, 0.7)
            pdf_canvas.setLineWidth(0.3)
            pdf_canvas.rect(x, y, sticker_w_pdf, sticker_h_pdf, stroke=1, fill=0)
            count += 1

    pdf_canvas.showPage()
    pdf_canvas.save()
    return count, cols, rows_n

def main():
    for d in [OUTPUT_IMG_DIR, OUTPUT_PDF_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)

    for plant in plant_data:
        img_file = create_sticker(plant)
        count, cols, rows_n = generate_pdf_sheet(plant, img_file)
        print(f"Generated {plant['name']}: {count} stickers ({cols}x{rows_n} grid)")

if __name__ == "__main__":
    main()