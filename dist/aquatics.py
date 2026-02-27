import os
import shutil

# --- BRANDING & PALETTE ---
COLORS = {
    "primary_teal": "#4A9E9E",      
    "background_silver": "#F2F2F7", 
    "card_white": "#FFFFFF",        
    "text_main": "#1C1C1E",         
    "text_muted": "#636366",        
    "border": "#D1D1D6"             
}

# The files on your PC (ensure these are in the same folder as this script)
LOGO_FILE = "SimpleLogo.jpg"

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
        "full_description": "Known as 'Downoi', its unique curly leaves make it a perfect focal point for the midground or foreground transitions.",
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

# --- CSS (Optimized for Phone Browsers) ---
CSS = f"""
body {{ font-family: 'Inter', -apple-system, sans-serif; background: {COLORS['background_silver']}; color: {COLORS['text_main']}; margin: 0; padding: 20px; }}
.container {{ max-width: 800px; margin: auto; }}
.logo {{ max-width: 160px; display: block; margin: 20px auto 30px auto; }}
.search-box {{ 
    width: 100%; padding: 16px; border-radius: 12px; border: 1px solid {COLORS['border']}; 
    background: {COLORS['card_white']}; margin-bottom: 25px; outline: none; box-sizing: border-box; 
    font-size: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}}
.plant-card {{ 
    display: flex; align-items: center; gap: 15px; background: {COLORS['card_white']}; 
    padding: 15px; border-radius: 16px; margin-bottom: 15px; border: 1px solid {COLORS['border']}; 
    text-decoration: none; color: inherit; box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: 0.2s;
}}
.plant-card:active {{ transform: scale(0.98); }}
.thumb {{ width: 80px; height: 80px; border-radius: 10px; object-fit: cover; background: #eee; flex-shrink: 0; }}
.card-content h2 {{ margin: 0 0 4px 0; font-size: 1.1rem; }}
.card-content p {{ margin: 0; color: {COLORS['text_muted']}; font-size: 0.85rem; line-height: 1.3; }}

/* Detail Page */
.btn-back {{ color: {COLORS['primary_teal']}; text-decoration: none; font-weight: 600; padding: 10px 0; display: inline-block; }}
.hero-img {{ width: 100%; height: auto; max-height: 350px; border-radius: 18px; object-fit: cover; border: 1px solid {COLORS['border']}; margin: 15px 0; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }}
.full-desc {{ line-height: 1.6; font-size: 1rem; color: #3A3A3C; margin-bottom: 25px; }}
.spec-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
.spec-item {{ background: {COLORS['card_white']}; padding: 12px; border-radius: 12px; border: 1px solid {COLORS['border']}; }}
.spec-label {{ color: {COLORS['text_muted']}; font-size: 0.65rem; text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 2px; }}
.spec-value {{ color: {COLORS['primary_teal']}; font-weight: 600; font-size: 0.9rem; }}
.footer {{ text-align: center; color: {COLORS['text_muted']}; margin-top: 60px; font-size: 0.75rem; padding-bottom: 30px; }}
"""

def generate_site():
    # 1. Prepare Folder
    if not os.path.exists("dist"): os.makedirs("dist")
    
    # Copy Logo to dist
    if os.path.exists(LOGO_FILE):
        shutil.copy(LOGO_FILE, os.path.join("dist", LOGO_FILE))

    # 2. Generate Catalog (Index)
    cat_html = f"""
    <html><head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>{CSS}</style>
    </head><body><div class="container">
        <img src="{LOGO_FILE}" class="logo">
        <input type="text" id="s" class="search-box" placeholder="Search catalog..." onkeyup="filter()">
        <div id="g">
    """
    for p in plants:
        # Copy plant image to dist
        if os.path.exists(p['image']):
            shutil.copy(p['image'], os.path.join("dist", p['image']))
        
        cat_html += f"""
        <a href="{p['id']}.html" class="plant-card">
            <img src="{p['image']}" class="thumb">
            <div class="card-content">
                <h2>{p['name']}</h2>
                <p>{p['summary']}</p>
            </div>
        </a>
        """
    cat_html += """</div><div class="footer">EASE-AQUATICS™ | GAUTENG</div></div>
    <script>function filter(){
        let v=document.getElementById('s').value.toLowerCase();
        for(let c of document.getElementsByClassName('plant-card')) {
            c.style.display = c.innerText.toLowerCase().includes(v) ? 'flex' : 'none';
        }
    }</script></body></html>"""
    
    with open("dist/index.html", "w", encoding="utf-8") as f: f.write(cat_html)

    # 3. Generate Detail Pages
    for p in plants:
        specs_html = "".join([f'<div class="spec-item"><span class="spec-label">{k}</span><span class="spec-value">{v}</span></div>' for k,v in p['specs'].items()])
        det_html = f"""
        <html><head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>{CSS}</style>
        </head><body><div class="container">
            <a href="index.html" class="btn-back">← Back to Catalog</a>
            <h1 style="margin: 10px 0 5px 0; font-size: 1.6rem;">{p['name']}</h1>
            <img src="{p['image']}" class="hero-img">
            <div class="full-desc">{p['full_description']}</div>
            <div class="spec-grid">
                <div class="spec-item"><span class="spec-label">Difficulty</span><span class="spec-value">{p['difficulty']}</span></div>
                <div class="spec-item"><span class="spec-label">Lighting</span><span class="spec-value">{p['light']}</span></div>
                <div class="spec-item"><span class="spec-label">CO2</span><span class="spec-value">{p['co2']}</span></div>
                {specs_html}
            </div>
            <div class="footer">EASE-AQUATICS™ | {p['name']}</div>
        </div></body></html>
        """
        with open(f"dist/{p['id']}.html", "w", encoding="utf-8") as f: f.write(det_html)

    print("🚀 Site Updated! All images are now inside the 'dist' folder.")

if __name__ == "__main__":
    generate_site()