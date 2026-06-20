"""
Lays the high-res sticker PNG onto an A4 sheet in a grid of 5cm x 2cm strips,
with thin cut guide lines, ready to print and slice for wrapping 70ml cups.
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PIL import Image

STICKER_PNG = "weeping_moss_5x2cm.png"
OUTPUT_PDF = "weeping_moss_sheet_A4.pdf"

STICKER_W = 5.0 * cm
STICKER_H = 2.0 * cm

PAGE_W, PAGE_H = A4

MARGIN = 1.0 * cm
GAP_X = 0.3 * cm
GAP_Y = 0.3 * cm

usable_w = PAGE_W - 2 * MARGIN
usable_h = PAGE_H - 2 * MARGIN

cols = int((usable_w + GAP_X) // (STICKER_W + GAP_X))
rows = int((usable_h + GAP_Y) // (STICKER_H + GAP_Y))

grid_w = cols * STICKER_W + (cols - 1) * GAP_X
grid_h = rows * STICKER_H + (rows - 1) * GAP_Y

start_x = (PAGE_W - grid_w) / 2
start_y = PAGE_H - MARGIN - STICKER_H  # top-left start, drawing downward

c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)

count = 0
for row in range(rows):
    for col in range(cols):
        x = start_x + col * (STICKER_W + GAP_X)
        y = start_y - row * (STICKER_H + GAP_Y)
        c.drawImage(STICKER_PNG, x, y, width=STICKER_W, height=STICKER_H,
                    preserveAspectRatio=False, mask='auto')
        # cut guide lines (hairline, light gray, just outside each sticker)
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setLineWidth(0.3)
        c.rect(x, y, STICKER_W, STICKER_H, stroke=1, fill=0)
        count += 1

c.showPage()
c.save()
print(f"Placed {count} stickers in a {cols} x {rows} grid on A4")
print(f"Sheet size used: {grid_w/cm:.1f}cm x {grid_h/cm:.1f}cm of {PAGE_W/cm:.1f}cm x {PAGE_H/cm:.1f}cm page")
