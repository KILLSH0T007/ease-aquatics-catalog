import os
from pdf2image import convert_from_path
from PIL import Image

# --- SETTINGS ---
PDF_NAME = "easy_aquatics_vectored_logo.pdf" 
OUTPUT_NAME = "Logo_Clean.png"

# This line tells Python it's okay to open large images
Image.MAX_IMAGE_PIXELS = None 

def convert_pdf_to_transparent_png():
    if not os.path.exists(PDF_NAME):
        print(f"❌ Error: Could not find {PDF_NAME}")
        return

    print(f"⌛ Converting {PDF_NAME} to transparent image...")

    try:
        # Convert PDF page to image 
        images = convert_from_path(PDF_NAME, dpi=200)
        logo_img = images[0].convert("RGBA")
        
        # Create transparency by finding white pixels
        datas = logo_img.getdata()
        new_data = []
        for item in datas:
            # Change all white (or near-white) pixels to transparent
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        
        logo_img.putdata(new_data)
        
        # Crop to the actual logo content 
        bbox = logo_img.getbbox()
        if bbox:
            logo_img = logo_img.crop(bbox)
        
        # Save as PNG to preserve transparency
        logo_img.save(OUTPUT_NAME, "PNG")
        
        print(f"✅ Success! Transparent logo saved as: {OUTPUT_NAME}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    convert_pdf_to_transparent_png()