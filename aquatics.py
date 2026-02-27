import os
import shutil
import socket

# --- BRANDING & PALETTE ---
COLORS = {
    "primary_teal": "#4A9E9E",      
    "background_silver": "#F2F2F7", 
    "card_white": "#FFFFFF",        
    "text_main": "#1C1C1E",         
    "text_muted": "#636366",        
    "border": "#D1D1D6"             
}

LOGO_FILE = "/img/SimpleLogo.png"
IMG_SUBDIR = "img" # Subdirectory inside dist

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# --- FULL PLANT INVENTORY ---
plants = [
    {
        "id": "monte-carlo",
        "name": "Micranthemum tweediei 'Monte Carlo'",
        "image": "monte_carlo.jpg",
        "difficulty": "Medium",
        "light": "High",
        "co2": "High",
        "summary": "The ultimate carpeting plant for high-end scapes.",
        "full_description": "Monte Carlo is a versatile carpeting plant with small round leaves. It is remarkably similar to HC but far easier to grow. It creates a dense, lush green floor.",
        "specs": {"Growth": "Fast", "pH": "6.0-7.5", "Position": "Foreground"}
    },
    {
        "id": "pogo-helferi",
        "name": "Pogostemon helferi",
        "image": "pogo_helferi.jpg",
        "difficulty": "Medium",
        "light": "Med/High",
        "co2": "Required",
        "summary": "A unique star-shaped architectural plant.",
        "full_description": "Known as 'Downoi' in Thailand, this plant was discovered by aquarists only recently. Its unique 'star' shape and curly leaves make it a perfect focal point.",
        "specs": {"Growth": "Medium", "pH": "6.0-7.2", "Position": "Foreground/Mid"}
    },
    {
        "id": "crypt-wendtii",
        "name": "Cryptocoryne wendtii 'Compact'",
        "image": "crypt_wendtii.jpg",
        "difficulty": "Easy",
        "light": "Low-Med",
        "co2": "Optional",
        "summary": "Hardy midground plant with bronze/green tones.",
        "full_description": "A very forgiving plant that stays compact, making it ideal for filling gaps in the midground.",
        "specs": {"Growth": "Slow", "pH": "5.5-8.0", "Position": "Midground"}
    },
    {
        "id": "anubias-nana-petite",
        "name": "Anubias barteri var. Nana Petite",
        "image": "anubias_petite.jpg",
        "difficulty": "Very Easy",
        "light": "Low",
        "co2": "Optional",
        "summary": "Tiny epiphyte perfect for hardscape detailing.",
        "full_description": "Extremely hardy. Should be attached to wood or rock rather than buried in substrate.",
        "specs": {"Growth": "Very Slow", "pH": "6.0-7.5", "Position": "Hardscape"}
    },
    {
        "id": "crypt-flamingo",
        "name": "Cryptocoryne sp. 'Flamingo'",
        "image": "crypt_flamingo.jpg",
        "difficulty": "Hard",
        "light": "High",
        "co2": "High",
        "summary": "Rare cultivar with stunning pink coloration.",
        "full_description": "Highly sought after for its unique pink leaves. Requires stable water parameters and high light to keep its color.",
        "specs": {"Growth": "Slow", "pH": "6.0-7.0", "Position": "Midground"}
    },
    {
        "id": "hairgrass-mini",
        "name": "Eleocharis acicularis 'Mini'",
        "image": "hairgrass.jpg",
        "difficulty": "Medium",
        "light": "Medium",
        "co2": "Recommended",
        "summary": "Classic grass-like carpet that stays very low.",
        "full_description": "The mini version stays shorter than standard hairgrass, creating a neat lawn effect with less trimming.",
        "specs": {"Growth": "Medium", "pH": "6.0-7.5", "Position": "Foreground"}
    },
    {
        "id": "staurogyne-repens",
        "name": "Staurogyne repens",
        "image": "s_repens.jpg",
        "difficulty": "Easy",
        "light": "Medium",
        "co2": "Recommended",
        "summary": "Hardy, bushy green foreground plant.",
        "full_description": "Excellent for filling space between hardscape and carpets. Can be pruned heavily to maintain a low profile.",
        "specs": {"Growth": "Slow", "pH": "6.0-7.5", "Position": "Foreground"}
    },
    {
        "id": "rotala-green",
        "name": "Rotala rotundifolia 'Green'",
        "image": "rotala_green.jpg",
        "difficulty": "Easy",
        "light": "Medium",
        "co2": "Recommended",
        "summary": "Bright green stem plant for lush backgrounds.",
        "full_description": "Stays vibrant green even under high light. Forms thick bushes when pruned regularly.",
        "specs": {"Growth": "Fast", "pH": "5.0-7.0", "Position": "Background"}
    },
    {
        "id": "weeping-moss",
        "name": "Vesicularia ferriei 'Weeping' Moss",
        "image": "weeping_moss.jpg",
        "difficulty": "Easy",
        "light": "Low-Med",
        "co2": "Optional",
        "summary": "Drooping moss that creates a 'weeping' effect.",
        "full_description": "Best used on driftwood to simulate tree branches. Grows best in cool water.",
        "specs": {"Growth": "Slow", "pH": "5.5-7.5", "Position": "Hardscape"}
    }
]

CSS = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
body {{ font-family: 'Inter', -apple-system, sans-serif; background: {COLORS['background_silver']}; color: {COLORS['text_main']}; margin: 0; padding: 15px; overflow-x: hidden; }}
.container {{ max-width: 600px; margin: auto; }}
.logo {{ max-width: 140px; display: block; margin: 10px auto 25px auto; }}
.search-box {{ width: 100%; padding: 16px; border-radius: 12px; border: 1px solid {COLORS['border']}; background: {COLORS['card_white']}; margin-bottom: 20px; outline: none; box-sizing: border-box; font-size: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
.plant-card {{ display: flex; align-items: center; gap: 12px; background: {COLORS['card_white']}; padding: 12px; border-radius: 14px; margin-bottom: 12px; border: 1px solid {COLORS['border']}; text-decoration: none; color: inherit; box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: 0.2s; }}
.thumb {{ width: 75px; height: 75px; border-radius: 10px; object-fit: cover; background: #eee; flex-shrink: 0; }}
.card-content h2 {{ margin: 0; font-size: 1rem; line-height: 1.2; word-break: break-word; }}
.card-content p {{ margin: 3px 0 0 0; color: {COLORS['text_muted']}; font-size: 0.8rem; line-height: 1.3; }}
.btn-back {{ display: inline-flex; align-items: center; gap: 8px; color: {COLORS['primary_teal']}; text-decoration: none; font-weight: 600; font-size: 0.9rem; padding: 10px 16px; background: {COLORS['card_white']}; border: 1px solid {COLORS['border']}; border-radius: 8px; margin-bottom: 15px; }}
.hero-img {{ width: 100%; height: auto; border-radius: 15px; border: 1px solid {COLORS['border']}; margin-bottom: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }}
h1 {{ font-size: 1.5rem; line-height: 1.2; margin: 0 0 10px 0; word-break: break-word; }}
.full-desc {{ line-height: 1.6; font-size: 0.95rem; color: #3A3A3C; margin-bottom: 25px; }}
.spec-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }}
.spec-item {{ background: {COLORS['card_white']}; padding: 12px; border-radius: 12px; border: 1px solid {COLORS['border']}; }}
.spec-label {{ color: {COLORS['text_muted']}; font-size: 0.65rem; text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 2px; }}
.spec-value {{ color: {COLORS['primary_teal']}; font-weight: 600; font-size: 0.85rem; }}
.footer {{ text-align: center; color: {COLORS['text_muted']}; margin-top: 50px; font-size: 0.75rem; padding-bottom: 30px; }}
</style>
</head>
"""

SVG_ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>'

def generate_site():
    dist_dir = "dist"
    img_dir = os.path.join(dist_dir, IMG_SUBDIR)
    
    # Create dist and dist/img directories if they don't exist
    if not os.path.exists(img_dir): 
        os.makedirs(img_dir)
    
    if os.path.exists(LOGO_FILE):
        shutil.copy(LOGO_FILE, os.path.join(dist_dir, LOGO_FILE))

    # 1. Generate Catalog (Index)
    cat_html = f"""{CSS}<body><div class="container">
        <img src="{LOGO_FILE}" class="logo">
        <input type="text" id="s" class="search-box" placeholder="Search catalog..." onkeyup="filter()">
        <div id="g">
    """
    for p in plants:
        # Copy image to dist/img/
        if os.path.exists(p['image']):
            shutil.copy(p['image'], os.path.join(img_dir, p['image']))
        
        # Link the source in HTML to img/filename
        img_src = f"{IMG_SUBDIR}/{p['image']}"
        
        cat_html += f"""
        <a href="{p['id']}.html" class="plant-card">
            <img src="{img_src}" class="thumb">
            <div class="card-content">
                <h2>{p['name']}</h2>
                <p>{p['summary']}</p>
            </div>
        </a>
        """
    cat_html += f"""</div><div class="footer">EASE-AQUATICS&trade; | GAUTENG</div></div>
    <script>function filter(){{
        let v=document.getElementById('s').value.toLowerCase();
        for(let c of document.getElementsByClassName('plant-card')) {{
            c.style.display = c.innerText.toLowerCase().includes(v) ? 'flex' : 'none';
        }}
    }}</script></body></html>"""
    
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f: f.write(cat_html)

    # 2. Generate Detail Pages
    for p in plants:
        img_src = f"{IMG_SUBDIR}/{p['image']}"
        specs_html = "".join([f'<div class="spec-item"><span class="spec-label">{k}</span><span class="spec-value">{v}</span></div>' for k,v in p['specs'].items()])
        det_html = f"""{CSS}<body><div class="container">
            <a href="index.html" class="btn-back">{SVG_ARROW} Back</a>
            <h1>{p['name']}</h1>
            <img src="{img_src}" class="hero-img">
            <div class="full-desc">{p['full_description']}</div>
            <div class="spec-grid">
                <div class="spec-item"><span class="spec-label">Difficulty</span><span class="spec-value">{p['difficulty']}</span></div>
                <div class="spec-item"><span class="spec-label">Lighting</span><span class="spec-value">{p['light']}</span></div>
                <div class="spec-item"><span class="spec-label">CO2</span><span class="spec-value">{p['co2']}</span></div>
                {specs_html}
            </div>
            <div class="footer">EASE-AQUATICS&trade; | {p['name']}</div>
        </div></body></html>
        """
        with open(os.path.join(dist_dir, f"{p['id']}.html"), "w", encoding="utf-8") as f: f.write(det_html)

    print(f"\n🚀 Site Generated Successfully!")
    print(f"📡 To view on your phone, open Chrome and go to: {get_ip()}:8000\n")

if __name__ == "__main__":
    generate_site()