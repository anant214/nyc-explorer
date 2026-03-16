"""
NYC Explorer — 8-bit retro edition
"""
import json
import streamlit as st
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote_plus
from data import ATTRACTIONS, RESTAURANTS

# ── Load Instagram places ─────────────────────────────────────────────────────
_INSTA_JSON = Path(__file__).parent / "insta_places.json"

ATTRACTION_KEYWORDS = {
    "attraction", "store", "shop", "market", "flea", "stationery",
    "bookstore", "gallery", "museum", "pop-up", "gift", "lifestyle",
    "home goods", "library", "tram", "observatory", "park", "vintage",
    "trinket", "poster", "design",
}

def _is_attraction(cuisine: str) -> bool:
    return any(kw in cuisine.lower() for kw in ATTRACTION_KEYWORDS)

def load_insta_places() -> int:
    if not _INSTA_JSON.exists():
        return 0
    try:
        places = json.loads(_INSTA_JSON.read_text())
    except Exception:
        return 0
    added = 0
    for p in places:
        area    = p.get("area", "Unknown")
        name    = p.get("name", "")
        cuisine = p.get("cuisine", "Other")
        price   = p.get("price", "$$")
        tip     = p.get("tip", "")
        if not name:
            continue
        if _is_attraction(cuisine):
            ATTRACTIONS.setdefault(area, [])
            if name.lower() not in {a[0].lower() for a in ATTRACTIONS[area]}:
                ATTRACTIONS[area].append((name, "Instagram Find", "📱", "free", tip, False))
                added += 1
        else:
            RESTAURANTS.setdefault(area, [])
            if name.lower() not in {r[0].lower() for r in RESTAURANTS[area]}:
                RESTAURANTS[area].append((name, cuisine, price, tip, "instagram"))
                added += 1
    return added

_insta_count = load_insta_places()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="NYC Explorer", page_icon="🗽", layout="centered")

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&family=Inter:wght@400;600;700&display=swap');

:root {
    --bg:     #FAFAF0;
    --dark:   #111111;
    --yellow: #FFD700;
    --red:    #CC2200;
    --blue:   #0044BB;
    --green:  #1A8A00;
    --purple: #6600CC;
    --orange: #DD5500;
    --cream:  #FFFEF2;
    --border: 3px solid #111;
    --shadow: 4px 4px 0 0 #111;
    --shadow-sm: 3px 3px 0 0 #111;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: var(--bg) !important;
    color: var(--dark) !important;
}
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 0 120px 0 !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}
section[data-testid="stMain"] > div { padding: 0 !important; }
[data-testid="stAppViewContainer"],
[data-testid="stVerticalBlock"],
.stApp { background: var(--bg) !important; }

/* ── HEADER ── */
.px-header {
    background: var(--dark);
    position: sticky; top: 0; z-index: 100;
    border-bottom: 4px solid var(--yellow);
}
.px-header-inner {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 18px 10px;
}
.px-logo {
    font-size: 2rem; line-height: 1;
    filter: drop-shadow(2px 2px 0 var(--yellow));
}
.px-title {
    font-family: 'Press Start 2P', cursive;
    font-size: 0.65rem; color: var(--yellow);
    letter-spacing: 0.05em; line-height: 1.6;
    text-shadow: 2px 2px 0 rgba(0,0,0,0.5);
}
.px-subtitle {
    font-family: 'Press Start 2P', cursive;
    font-size: 0.48rem; color: #666;
    letter-spacing: 0.05em; margin-top: 3px;
}
.px-coins {
    margin-left: auto;
    font-family: 'Press Start 2P', cursive;
    font-size: 0.4rem; color: var(--yellow);
    background: #222; border: 2px solid var(--yellow);
    padding: 5px 8px; white-space: nowrap;
    text-align: center; line-height: 1.8;
}

/* ── TICKER ── */
.px-ticker-wrap {
    background: var(--yellow);
    border-top: 3px solid var(--dark);
    overflow: hidden;
    display: flex; align-items: center;
}
.px-ticker-label {
    flex-shrink: 0;
    background: var(--dark); color: var(--yellow);
    font-family: 'Press Start 2P', cursive;
    font-size: 0.35rem; padding: 7px 10px;
    letter-spacing: 0.08em; white-space: nowrap;
    border-right: 3px solid var(--yellow);
}
.px-ticker-track { overflow: hidden; flex: 1; }
.px-ticker-content {
    display: inline-block; white-space: nowrap;
    font-family: 'Press Start 2P', cursive;
    font-size: 0.35rem; color: var(--dark);
    letter-spacing: 0.1em; padding: 7px 0;
    animation: ticker-scroll 20s linear infinite;
}
@keyframes ticker-scroll {
    0%   { transform: translateX(0%); }
    100% { transform: translateX(-200%); }
}

/* ── TAB TOGGLE ── */
div[data-testid="stRadio"] { padding: 14px 16px 0 !important; }
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div {
    background: transparent !important;
    border: none !important; box-shadow: none !important;
    border-radius: 0 !important; padding: 0 !important;
    gap: 6px !important; width: 100% !important;
}
div[data-testid="stRadio"] > div > label {
    border-radius: 0 !important;
    padding: 14px 6px !important;
    font-family: 'Press Start 2P', cursive !important;
    font-size: 0.40rem !important;
    flex: 1 !important; text-align: center !important;
    color: var(--dark) !important;
    background: var(--cream) !important;
    cursor: pointer !important; margin: 0 !important;
    display: flex !important; align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    letter-spacing: 0.04em !important;
    border: 3px solid var(--dark) !important;
    box-shadow: 4px 4px 0 0 var(--dark) !important;
    transition: none !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: var(--yellow) !important;
    color: var(--dark) !important;
    border: 3px solid var(--dark) !important;
    box-shadow: none !important;
    transform: translate(4px, 4px) !important;
}
div[data-testid="stRadio"] > div > label:has(input:not(:checked)):hover {
    background: #f0ede6 !important;
    box-shadow: 2px 2px 0 0 var(--dark) !important;
    transform: translate(2px, 2px) !important;
}
div[data-testid="stRadio"] input { display: none !important; }
div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

/* ── SELECTBOX ── */
div[data-testid="stSelectbox"] { padding: 10px 16px 0 !important; }
div[data-testid="stSelectbox"] > label {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 0.38rem !important; color: #888 !important;
    letter-spacing: 0.08em !important; margin-bottom: 6px !important;
    text-transform: uppercase !important;
}
div[data-testid="stSelectbox"] > div > div {
    border-radius: 0 !important;
    border: var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
    background: var(--cream) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important; color: var(--dark) !important;
}

/* ── FILTER LABEL ── */
.px-filter-label {
    font-family: 'Press Start 2P', cursive;
    font-size: 0.5rem; color: #888;
    letter-spacing: 0.08em; text-transform: uppercase;
    display: block; padding: 0 16px; margin-top: 4px;
}

/* ── HUD STATS ── */
.px-hud {
    display: flex; gap: 8px; flex-wrap: wrap;
    padding: 14px 16px 0;
}
.px-stat {
    background: var(--dark); color: var(--yellow);
    font-family: 'Press Start 2P', cursive;
    font-size: 0.65rem; padding: 10px 16px;
    border: 2px solid var(--yellow);
    white-space: nowrap; line-height: 1.8;
}
.px-stat.green { border-color: var(--green); color: var(--green); }
.px-stat.red   { border-color: #ff6666; color: #ff6666; }

/* ── SECTION LABEL ── */
.px-section {
    padding: 18px 16px 8px;
    font-family: 'Press Start 2P', cursive;
    font-size: 0.63rem; color: var(--dark);
    letter-spacing: 0.06em;
    display: flex; align-items: center; gap: 10px;
}
.px-section::after { content: ''; flex: 1; height: 3px; background: var(--dark); }

/* ── PLACE CARD ── */
.px-card {
    background: var(--cream);
    border: var(--border);
    box-shadow: var(--shadow);
    padding: 14px 14px 12px;
    margin: 0 16px 14px;
    position: relative;
    border-left: 5px solid var(--accent, #111);
}
/* Card left part — accent left border only; structural borders live on the column */
.px-card-left {
    background: var(--cream);
    border-left: 5px solid var(--accent, #111);
    padding: 14px 14px 12px !important;
    margin: 0;
    position: relative;
}
.px-card-area {
    font-family: 'Press Start 2P', cursive;
    font-size: 0.42rem; color: #aaa;
    letter-spacing: 0.1em; margin-bottom: 6px;
    text-transform: uppercase;
}
.px-card-name {
    font-weight: 700; font-size: 0.93rem;
    color: var(--dark); margin-bottom: 6px; line-height: 1.3;
}
.px-card-tip {
    font-size: 0.78rem; color: #444;
    line-height: 1.6; margin-bottom: 10px;
}
.px-tags { display: flex; flex-wrap: wrap; gap: 5px; }
.px-tag {
    font-family: 'Press Start 2P', cursive;
    font-size: 0.42rem; padding: 4px 9px;
    border: 2px solid currentColor; white-space: nowrap;
}
.tag-free     { color: var(--green); background: #e8fce8; }
.tag-paid     { color: var(--orange); background: #fff3e0; }
.tag-budget   { color: var(--green); background: #e8fce8; }
.tag-upscale  { color: var(--purple); background: #f3e8ff; }
.tag-category { color: var(--blue); background: #e8f0ff; }
.tag-book     { color: var(--red); background: #ffe8e8; }
.tag-insta    { color: #cc0088; background: #ffe8f8; }
.tag-saved    { color: var(--blue); background: #e8f0ff; }

/* ── EMPTY STATE ── */
.px-empty { text-align: center; padding: 60px 24px 40px; }
.px-empty-icon { font-size: 2.5rem; margin-bottom: 14px; }
.px-empty-title {
    font-family: 'Press Start 2P', cursive;
    font-size: 0.55rem; color: var(--dark);
    margin-bottom: 10px; letter-spacing: 0.05em; line-height: 1.8;
}
.px-empty-sub {
    font-family: 'Press Start 2P', cursive;
    font-size: 0.35rem; color: #aaa;
    letter-spacing: 0.05em; line-height: 2;
}

/* ── DIVIDER ── */
.px-divider { margin: 14px 16px 4px; border: none; border-top: 3px solid var(--dark); }

/* ── SEARCH BAR ── */
.px-search-wrap { padding: 14px 16px 0; }
div[data-testid="stTextInput"] { padding: 0 !important; }
div[data-testid="stTextInput"] > label { display: none !important; }
div[data-testid="stTextInput"] > div > div > input {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 0.42rem !important;
    border-radius: 0 !important;
    border: var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
    background: var(--cream) !important;
    color: var(--dark) !important;
    padding: 14px 12px !important;
    letter-spacing: 0.06em !important;
}
div[data-testid="stTextInput"] > div > div > input::placeholder {
    color: #aaa !important; font-size: 0.38rem !important;
}
div[data-testid="stTextInput"] > div { border: none !important; box-shadow: none !important; }

/* ── SAVED TOGGLE ── */
div[data-testid="stCheckbox"] { padding: 10px 16px 0 !important; }
div[data-testid="stCheckbox"] label {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 0.42rem !important; gap: 10px !important;
    color: var(--dark) !important;
}
div[data-testid="stCheckbox"] label span[data-testid="stMarkdownContainer"] p {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 0.42rem !important;
}

/* ── CARD + HEART STRIP (column layout) ── */
/* stHorizontalBlock = card container with all borders/shadow */
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    gap: 0 !important;
    margin: 0 16px 14px !important;
    position: relative !important;         /* anchor for absolute right column */
    border-top: 3px solid #111 !important;
    border-right: 3px solid #111 !important;
    border-bottom: 3px solid #111 !important;
    border-left: none !important;           /* accent left border from .px-card-left */
    box-shadow: 4px 4px 0 0 #111, inset 0 -3px 0 0 #111 !important;
    overflow: visible !important;
    background: var(--cream) !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    padding: 0 !important;
    min-width: 0 !important;
}
/* Left card column: 90% of width in normal flow */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child {
    flex: 0 0 90% !important;
}
/* Strip padding/margin/gap from ALL wrapper layers inside the left column */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child > div,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child > div > div,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child > div > div > div {
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
    min-height: 0 !important;
}
/* Also target by testid in case Streamlit adds stVerticalBlock / stMarkdownContainer */
div[data-testid="stHorizontalBlock"] [data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"] [data-testid="stMarkdownContainer"] {
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
    min-height: 0 !important;
}
/* Right heart strip: absolutely positioned so it ALWAYS fills the full block height */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child {
    position: absolute !important;
    top: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 10% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: transparent !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child > div,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child > div > div {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    height: 100% !important;
    padding: 0 !important;
    gap: 0 !important;
    background: transparent !important;
}
/* Heart button — passthrough container, clickable button */
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] {
    pointer-events: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
    padding: 0 !important;
}
div[data-testid="stHorizontalBlock"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 4px !important;
    min-width: 0 !important;
    width: auto !important;
    margin: 0 !important;
    cursor: pointer !important;
    line-height: 1 !important;
    pointer-events: all !important;
    transition: transform 0.15s ease, color 0.15s ease !important;
}
/* Unsaved ♡ */
div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-secondary"],
div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-secondary"] * {
    font-size: 1.4rem !important;
    color: #bbb !important;
    background: transparent !important;
}
div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-secondary"]:hover,
div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-secondary"]:hover * {
    color: #ff3366 !important;
}
div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-secondary"]:hover {
    transform: scale(1.3) !important;
}
/* Saved ❤️ — larger, background cleared (emoji provides its own red color) */
div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-primary"],
div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-primary"] * {
    font-size: 1.8rem !important;
    background: transparent !important;
    border-color: transparent !important;
}
div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-primary"]:hover {
    transform: scale(1.15) !important;
}
div[data-testid="stHorizontalBlock"] button:active {
    transform: scale(0.8) !important;
}
.tag-sfp    { color: #0055cc; background: #e8f0ff; }
.tag-rating { color: #CC8800; background: #fff8e0; }
.px-card-name a {
    color: inherit; text-decoration: none;
    border-bottom: 1.5px dotted rgba(0,0,0,0.25);
}
.px-card-name a:hover { border-bottom-color: #111; }
</style>
""", unsafe_allow_html=True)

# ── Curated shopping places ───────────────────────────────────────────────────
# Tuple: (name, shop_type, emoji, price, tip, book_ahead)
SHOPPING = {
    "East Village": [
        ("Obscura Antiques & Oddities", "Curiosities",   "💀", "free", "Taxidermy, Victorian medical gear, oddities galore. The most fascinating shop in NYC.", False),
        ("Search & Destroy",            "Vintage",        "👗", "free", "Punk and vintage clothing since 1991. Leather, band tees, platform boots.", False),
        ("Strand Bookstore",            "Books",          "📚", "free", "18 miles of books. The NYC bookstore. Basement bargains start at $1.", False),
        ("Otherwild",                   "Lifestyle",      "🌈", "free", "Queer-owned gift shop and gallery. Unique prints, ceramics and zines.", False),
    ],
    "West Village": [
        ("Three Lives & Company",       "Books",          "📚", "free", "One of NYC's most beloved indie bookshops. Beautifully curated, knowledgeable staff.", False),
        ("Aedes de Venustas",           "Lifestyle",      "🌹", "free", "The finest niche perfumery in NYC. Rare fragrances you won't find anywhere else.", False),
        ("Birgitt Lopez Flowers",       "Lifestyle",      "🌸", "free", "Wildly beautiful flower arrangements. Even window-shopping is worth the detour.", False),
    ],
    "SoHo": [
        ("Housing Works Bookstore",     "Books",          "📚", "free", "Second-hand books in a stunning space. All profits support HIV/AIDS services.", False),
        ("De Vera",                     "Art & Objects",  "🎨", "free", "Museum-quality antiques and jewellery. Just browsing is a full experience.", False),
        ("McNally Jackson",             "Books",          "📚", "free", "Premier NYC indie bookshop. Excellent events calendar and zine selection.", False),
        ("Goods for the Study",         "Stationery",     "✏️", "free", "Sleek stationery and desk objects. A beautiful shop for paper lovers.", False),
    ],
    "Lower East Side": [
        ("Economy Candy",               "Food & Specialty","🍬", "free", "Candy shop since 1937. Floor-to-ceiling sweets, nuts and chocolates. An LES institution.", False),
        ("Bluestockings",               "Books",          "📚", "free", "Radical community bookstore, café and activist space. Fascinating and welcoming.", False),
        ("Russ & Daughters",            "Food & Specialty","🐟", "free", "Legendary appetising shop since 1914. Smoked fish, caviar, babka. A NYC treasure.", False),
    ],
    "Chinatown": [
        ("Pearl River Mart",            "Lifestyle",      "🏮", "free", "Beloved Chinese goods emporium. Ceramics, tea sets, lanterns. NYC institution since 1971.", False),
        ("Ten Thousand Things",         "Art & Objects",  "💍", "free", "Extraordinary jewellery studio. Delicate, one-of-a-kind pieces by local designers.", False),
    ],
    "Greenwich Village": [
        ("The Evolution Store",         "Curiosities",    "🦕", "free", "Natural history curiosities — fossils, taxidermy, minerals. A genuine fascination.", False),
        ("Forbidden Planet",            "Books",          "🤖", "free", "Sci-fi, comics, graphic novels and collectibles. The nerd Mecca of Manhattan.", False),
        ("Printed Matter",              "Books",          "📖", "free", "Artist books, zines and publications. The best gift destination for creative types.", False),
        ("The Compleat Strategist",     "Specialty",      "♟", "free", "Board games, role-playing games and war games since 1976. A wonderfully nerdy haven.", False),
    ],
    "Midtown": [
        ("Rizzoli Bookstore",           "Books",          "📚", "free", "The most beautiful bookshop in NYC. Art, design and photography books in a stunning 1894 building.", False),
        ("Kinokuniya",                  "Books",          "📚", "free", "Japanese bookstore on 6th Ave. Manga, stationery, art books and Japanese snacks.", False),
        ("Harry Potter Store",          "Specialty",      "🧙", "free", "World's largest Harry Potter store. No entry fee — budget for impulse buys.", False),
        ("FAO Schwarz",                 "Specialty",      "🪀", "free", "Iconic toy store. The giant piano floor is still there.", False),
        ("Fifth Avenue Flagship Stores","Flagship",       "🛍", "free", "Gucci, Prada, Saks — window shopping is free. Peak crowds at weekends.", False),
    ],
    "Upper West Side": [
        ("Zabar's",                     "Food & Specialty","🧀", "free", "Iconic Upper West Side deli and gourmet grocery since 1934. The smoked fish counter is legendary.", False),
        ("Westsider Books",             "Books",          "📚", "free", "Floor-to-ceiling used books in a wonderfully chaotic townhouse. A true neighbourhood gem.", False),
        ("Book Culture",                "Books",          "📚", "free", "Independent bookshop beloved by Columbia students. Strong humanities and fiction sections.", False),
    ],
    "Harlem": [
        ("Hats by Bunn",                "Vintage",        "🎩", "free", "Custom millinery and vintage hats in Harlem. A completely unique NYC experience.", False),
        ("Guidance",                    "Records",        "🎵", "free", "Deep house and electronic record shop. One of the best crate-digging spots in the city.", False),
    ],
    "Williamsburg": [
        ("Beacon's Closet",             "Vintage",        "👗", "free", "The best vintage shop in Brooklyn. Huge, well-priced, constantly rotating stock.", False),
        ("Rough Trade NYC",             "Records",        "🎵", "free", "Legendary record store with a live music venue inside. Excellent new and used vinyl.", False),
        ("Word Bookstores",             "Books",          "📚", "free", "Beloved Brooklyn indie bookshop. Great staff picks and strong community events.", False),
        ("Catbird",                     "Art & Objects",  "💍", "free", "Delicate, reasonably-priced jewellery made in Brooklyn. Very giftable.", False),
    ],
    "DUMBO": [
        ("Powerhouse Arena",            "Books",          "📚", "free", "Bookshop in a stunning converted warehouse. Art, photography and design titles.", False),
        ("Front General Store",         "Lifestyle",      "🏠", "free", "Beautifully curated homewares and gifts in a DUMBO loft space.", False),
    ],
    "Park Slope": [
        ("Community Bookstore",         "Books",          "📚", "free", "Park Slope's anchor indie bookshop since 1974. Excellent events and children's section.", False),
        ("Bklyn Larder",                "Food & Specialty","🧀", "free", "Artisan grocery and cheese shop. Exceptional charcuterie and local products.", False),
    ],
    "Chelsea": [
        ("192 Books",                   "Books",          "📚", "free", "Tiny art-world bookshop curated by gallerists. Excellent art and theory selection.", False),
        ("Chelsea Market Shops",        "Market",         "🛒", "free", "Artisan vendors inside the old Nabisco factory. Browse and snack in equal measure.", False),
    ],
    "Nolita": [
        ("Café Gitane Gifts",           "Lifestyle",      "✨", "free", "French-Moroccan inspired objects and gifts adjacent to the famous café.", False),
        ("Archestratus Books + Foods",  "Books",          "📚", "free", "Cookbook and food-writing bookshop with an in-store café. A total delight.", False),
    ],
}

# ── Google ratings (approximate) ─────────────────────────────────────────────
RATINGS: dict[str, float] = {
    # Restaurants
    "Katz's Delicatessen": 4.5, "Joe's Pizza": 4.7, "Lombardi's": 4.4,
    "L'Artusi": 4.6, "Via Carota": 4.7, "Gramercy Tavern": 4.6,
    "Smalls Jazz Club": 4.8, "Russ & Daughters Cafe": 4.7,
    "Xi'an Famous Foods": 4.5, "Prince Street Pizza": 4.6,
    "Lucali": 4.7, "Di Fara Pizza": 4.6, "Peter Luger Steak House": 4.4,
    "The Spotted Pig": 4.2, "Mission Chinese Food": 4.3,
    "Superiority Burger": 4.5, "Cafe Mogador": 4.5,
    "Roberta's": 4.5, "Lilia": 4.7, "Don Angie": 4.7,
    # Attractions
    "Central Park": 4.8, "The High Line": 4.7, "Brooklyn Bridge": 4.8,
    "MoMA": 4.6, "The Metropolitan Museum of Art": 4.7,
    "Whitney Museum of American Art": 4.5, "9/11 Memorial": 4.8,
    "One World Observatory": 4.6, "Brooklyn Botanic Garden": 4.8,
    "New York Botanical Garden": 4.7, "Coney Island": 4.3,
    "The Vessel": 4.2, "Rockefeller Center": 4.7,
    "Grand Central Terminal": 4.8, "The Frick Collection": 4.7,
    # Shopping
    "Strand Bookstore": 4.6, "Economy Candy": 4.7,
    "Russ & Daughters": 4.8, "Beacon's Closet": 4.4,
    "Rough Trade NYC": 4.6, "Zabar's": 4.7,
    "McNally Jackson": 4.6, "Kinokuniya": 4.6,
    "Rizzoli Bookstore": 4.7, "Chelsea Market Shops": 4.5,
    "Housing Works Bookstore": 4.7, "Obscura Antiques & Oddities": 4.8,
    # Phil Rosenthal picks
    "Ice and Vice": 4.6, "Ganesh Temple Canteen": 4.8,
    "Totonno's": 4.6, "Peter Luger Steak House": 4.4,
}

def rating_tag(name: str) -> str:
    r = RATINGS.get(name)
    if r is None:
        return ""
    return f'<span class="px-tag tag-rating">★ {r:.1f}</span>'

# ── Flatten all places ────────────────────────────────────────────────────────
# Exclude Store-category from Sights (they live in Shopping now)
all_attractions_flat = [
    (area, *p) for area, places in ATTRACTIONS.items() for p in places
    if p[1] != "Store"
]
all_restaurants_flat = [(area, *p) for area, places in RESTAURANTS.items() for p in places]
all_shopping_flat    = [(area, *p) for area, places in SHOPPING.items() for p in places]
total = len(all_attractions_flat) + len(all_restaurants_flat) + len(all_shopping_flat)

# ── Session state ─────────────────────────────────────────────────────────────
if "favourites" not in st.session_state:
    st.session_state.favourites = set()

def toggle_fav(name: str):
    if name in st.session_state.favourites:
        st.session_state.favourites.discard(name)
    else:
        st.session_state.favourites.add(name)

# ── Header ────────────────────────────────────────────────────────────────────
insta_line = f" ★ +{_insta_count} FROM INSTAGRAM" if _insta_count else ""
st.markdown(f"""
<div class="px-header">
  <div class="px-header-inner">
    <div class="px-logo">🗽</div>
    <div>
      <div class="px-title">NYC EXPLORER</div>
      <div class="px-subtitle">▸ INSERT QUARTER TO EXPLORE</div>
    </div>
    <div class="px-coins">🪙 PLACES<br>{total}</div>
  </div>
  <div class="px-ticker-wrap">
    <div class="px-ticker-label">◆ NYC</div>
    <div class="px-ticker-track">
      <span class="px-ticker-content">★ WELCOME TO NEW YORK CITY ★ PICK YOUR QUEST ★ EAT ★ DRINK ★ SEE ★ EXPLORE &amp; DISCOVER{insta_line} ★ WELCOME TO NEW YORK CITY ★</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── JS: fix card styles — uses setProperty('important') to beat Streamlit CSS ──
st.markdown("""
<img src="x" style="display:none" onerror="(function(){
  var doc=document;
  function sp(el,p,v){el.style.setProperty(p,v,'important');}
  function fix(){
    doc.querySelectorAll('[data-testid=stHorizontalBlock]').forEach(function(b){
      var cs=b.querySelectorAll(':scope>[data-testid=stColumn]');
      if(cs.length===2){
        sp(b,'position','relative');
        sp(b,'padding','0');
        sp(b,'border-top','3px solid #111');
        sp(b,'border-right','3px solid #111');
        sp(b,'border-bottom','3px solid #111');
        sp(b,'border-left','none');
        sp(b,'box-shadow','4px 4px 0 0 #111');
        b.querySelectorAll('[data-testid=stVerticalBlock],[data-testid=stMarkdownContainer]').forEach(function(w){
          sp(w,'padding','0');sp(w,'margin','0');sp(w,'gap','0');sp(w,'min-height','0');
        });
        sp(cs[0],'flex','0 0 90%');
        sp(cs[0],'max-width','90%');
        sp(cs[1],'position','absolute');
        sp(cs[1],'top','0');
        sp(cs[1],'right','0');
        sp(cs[1],'bottom','0');
        sp(cs[1],'width','10%');
        sp(cs[1],'display','flex');
        sp(cs[1],'align-items','center');
        sp(cs[1],'justify-content','center');
        sp(cs[1],'border-left','none');
        sp(cs[1],'background','transparent');
      }
    });
  }
  if(!window._hObs){
    window._hObs=new MutationObserver(fix);
    window._hObs.observe(doc.body,{subtree:true,childList:true,attributes:true,attributeFilter:['style','class']});
  }
  if(!window._hInt){window._hInt=setInterval(fix,300);}
  fix();
})();">
""", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
view = st.radio("view", ["◆ SIGHTS", "♥ FOOD", "🛍 SHOP", "❤ SAVED"],
                horizontal=True, label_visibility="collapsed")
is_sights    = "SIGHTS" in view
is_food      = "FOOD"   in view
is_shopping  = "SHOP"   in view
is_saved     = "SAVED"  in view

# ── Accent colours ────────────────────────────────────────────────────────────
CUISINE_ACCENT = {
    "Italian": "#DD5500", "Mexican": "#1A8A00", "French": "#0044BB",
    "Korean": "#CC0066", "Japanese": "#CC0099", "Chinese": "#CC8800",
    "American": "#445566", "Pizza": "#DD5500", "Indian": "#BB6600",
    "Bar": "#6600CC", "Cocktail Bar": "#6600CC", "Wine Bar": "#6600CC",
    "Rooftop Bar": "#6600CC", "Bakery": "#CC0044", "Desserts": "#CC0044",
    "Seafood": "#0055AA", "Mediterranean": "#007766", "Lebanese": "#CC8800",
    "Greek": "#0044BB", "Vegan": "#1A8A00", "Vegan Mexican": "#1A8A00",
    "Thai": "#1A8A00", "Vietnamese": "#1A8A00", "Peruvian": "#773322",
    "Caribbean": "#BB6600", "West African": "#BB6600", "Ramen": "#DD5500",
    "Jewish Deli": "#445566", "Deli": "#445566", "Café": "#7C5A2D",
    "South Indian": "#BB6600", "Pakistani": "#BB6600",
}
ATTR_ACCENT = {
    "Attraction": "#0044BB", "Museum": "#6600CC", "History": "#886600",
    "Observation": "#007755", "Store": "#CC0066", "Zoo": "#1A8A00",
    "Architecture": "#0055AA", "Instagram Find": "#CC0088",
}
CAT_ICONS = {
    "Attraction": "🎯", "Museum": "🏛", "History": "📜",
    "Observation": "🔭", "Store": "🛍", "Zoo": "🦁",
    "Architecture": "🏗", "Instagram Find": "📱",
}
SHOP_ACCENT = {
    "Books": "#0044BB", "Vintage": "#CC0066", "Records": "#6600CC",
    "Curiosities": "#886600", "Lifestyle": "#1A8A00", "Art & Objects": "#CC8800",
    "Stationery": "#0055AA", "Food & Specialty": "#DD5500", "Specialty": "#773322",
    "Market": "#BB6600", "Flagship": "#CC0044",
}
PRICE_TAG = {"$": "tag-budget", "$$": "tag-budget",
             "$$$": "tag-upscale", "$$$$": "tag-upscale"}

# ── Filters ───────────────────────────────────────────────────────────────────
if is_sights:
    raw = all_attractions_flat
elif is_shopping:
    raw = all_shopping_flat
elif is_saved:
    raw = []
else:
    raw = all_restaurants_flat

if not is_saved:
    # Search
    st.markdown('<div class="px-search-wrap">', unsafe_allow_html=True)
    st.markdown('<span class="px-filter-label">🔍 Search</span>', unsafe_allow_html=True)
    search_term = st.text_input("Search", placeholder="TYPE TO SEARCH...",
                                label_visibility="collapsed", key="search_term")
    st.markdown('</div>', unsafe_allow_html=True)

    all_areas = sorted({r[0] for r in raw})
    st.markdown('<span class="px-filter-label">📍 Neighbourhood</span>', unsafe_allow_html=True)
    area_sel = st.selectbox("Neighbourhood", ["All areas"] + all_areas,
                            label_visibility="collapsed", key="area_sel")

    if is_sights:
        all_cats = sorted({r[2] for r in raw})
        st.markdown('<span class="px-filter-label">🏷 Category</span>', unsafe_allow_html=True)
        cat_sel = st.selectbox("Category", ["All categories"] + all_cats,
                               label_visibility="collapsed", key="cat_sel")
        st.markdown('<span class="px-filter-label">🎟 Entry</span>', unsafe_allow_html=True)
        entry_sel = st.selectbox("Entry", ["All", "Free only", "Paid only"],
                                 label_visibility="collapsed", key="entry_sel")
        st.markdown('<span class="px-filter-label">📲 Source</span>', unsafe_allow_html=True)
        source_sel = st.selectbox("Source", ["All sources", "My list", "Instagram"],
                                  label_visibility="collapsed", key="source_sel")
    elif is_shopping:
        all_shop_types = sorted({r[2] for r in raw})
        st.markdown('<span class="px-filter-label">🏷 Shop Type</span>', unsafe_allow_html=True)
        shoptype_sel = st.selectbox("Shop Type", ["All types"] + all_shop_types,
                                    label_visibility="collapsed", key="shoptype_sel")
    else:
        all_cuisines = sorted({r[2] for r in raw})
        st.markdown('<span class="px-filter-label">🍴 Cuisine</span>', unsafe_allow_html=True)
        cuisine_sel = st.selectbox("Cuisine", ["All cuisines"] + all_cuisines,
                                   label_visibility="collapsed", key="cuisine_sel")
        st.markdown('<span class="px-filter-label">💰 Price</span>', unsafe_allow_html=True)
        price_sel = st.selectbox("Price", ["All prices", "Budget ($ · $$)", "Upscale ($$$ · $$$$)"],
                                 label_visibility="collapsed", key="price_sel")
        st.markdown('<span class="px-filter-label">📲 Source</span>', unsafe_allow_html=True)
        source_sel = st.selectbox("Source", ["All sources", "My list", "Instagram", "Phil's Pick"],
                                  label_visibility="collapsed", key="source_sel")

# ── Apply filters ─────────────────────────────────────────────────────────────
if is_saved:
    filtered          = []   # not used in saved view
    saved_sights_list = [r for r in all_attractions_flat if r[1] in st.session_state.favourites]
    saved_food_list   = [r for r in all_restaurants_flat if r[1] in st.session_state.favourites]
    saved_shop_list   = [r for r in all_shopping_flat    if r[1] in st.session_state.favourites]
else:
    q = search_term.strip().lower()

    def _matches_search(name: str, tip: str) -> bool:
        if not q:
            return True
        return q in name.lower() or q in tip.lower()

    if is_sights:
        filtered = [
            r for r in raw
            if (area_sel == "All areas"      or r[0] == area_sel)
            and (cat_sel == "All categories" or r[2] == cat_sel)
            and (entry_sel == "All"
                 or (entry_sel == "Free only" and r[4] == "free")
                 or (entry_sel == "Paid only" and r[4] != "free"))
            and (source_sel == "All sources"
                 or (source_sel == "Instagram" and r[2] == "Instagram Find")
                 or (source_sel == "My list"   and r[2] != "Instagram Find"))
            and _matches_search(r[1], r[5])
        ]
    elif is_shopping:
        filtered = [
            r for r in raw
            if (area_sel == "All areas"       or r[0] == area_sel)
            and (shoptype_sel == "All types"  or r[2] == shoptype_sel)
            and _matches_search(r[1], r[5])
        ]
    else:
        filtered = [
            r for r in raw
            if (area_sel == "All areas"        or r[0] == area_sel)
            and (cuisine_sel == "All cuisines" or r[2] == cuisine_sel)
            and (price_sel == "All prices"
                 or (price_sel == "Budget ($ · $$)"      and r[3] in ("$", "$$"))
                 or (price_sel == "Upscale ($$$ · $$$$)" and r[3] in ("$$$", "$$$$")))
            and (source_sel == "All sources"
                 or (source_sel == "Instagram"    and (len(r) > 5 and r[5] == "instagram"))
                 or (source_sel == "Phil's Pick"  and (len(r) > 5 and r[5] == "sfp"))
                 or (source_sel == "My list"      and not (len(r) > 5 and r[5] in ("instagram", "sfp"))))
            and _matches_search(r[1], r[4])
        ]

# ── HUD stats ─────────────────────────────────────────────────────────────────
saved_n = len(st.session_state.favourites)
if is_saved:
    total_saved = len(saved_sights_list) + len(saved_food_list) + len(saved_shop_list)
    st.markdown(f"""
<div class="px-hud">
  <div class="px-stat" style="border-color:#cc0088;color:#cc0088">♥ {total_saved} SAVED</div>
  <div class="px-stat green">◆ {len(saved_sights_list)} SIGHTS</div>
  <div class="px-stat">♥ {len(saved_food_list)} FOOD</div>
  <div class="px-stat">🛍 {len(saved_shop_list)} SHOPS</div>
</div>""", unsafe_allow_html=True)
elif is_sights:
    free_n = sum(1 for r in filtered if r[4] == "free")
    st.markdown(f"""
<div class="px-hud">
  <div class="px-stat">▸ {len(filtered)} PLACES</div>
  <div class="px-stat green">✓ {free_n} FREE</div>
  <div class="px-stat red">$ {len(filtered)-free_n} PAID</div>
</div>""", unsafe_allow_html=True)
elif is_shopping:
    types_n = len({r[2] for r in filtered})
    st.markdown(f"""
<div class="px-hud">
  <div class="px-stat">▸ {len(filtered)} SHOPS</div>
  <div class="px-stat green">✓ {types_n} TYPES</div>
</div>""", unsafe_allow_html=True)
else:
    budget_n = sum(1 for r in filtered if r[3] in ("$", "$$"))
    st.markdown(f"""
<div class="px-hud">
  <div class="px-stat">▸ {len(filtered)} PLACES</div>
  <div class="px-stat green">$ {budget_n} BUDGET</div>
  <div class="px-stat red">$$ {len(filtered)-budget_n} UPSCALE</div>
</div>""", unsafe_allow_html=True)

# ── Card render helpers ────────────────────────────────────────────────────────
def render_sight(row):
    p_area, p_name, p_cat, p_emoji, p_entry, p_tip, p_book = row
    is_fav    = p_name in st.session_state.favourites
    accent    = ATTR_ACCENT.get(p_cat, "#111")
    entry_tag = '<span class="px-tag tag-free">FREE</span>' if p_entry == "free" \
                else '<span class="px-tag tag-paid">PAID</span>'
    book_tag  = '<span class="px-tag tag-book">BOOK AHEAD</span>' if p_book else ""
    insta_tag = '<span class="px-tag tag-insta">INSTAGRAM</span>' if p_cat == "Instagram Find" else ""
    rt        = rating_tag(p_name)
    maps_url  = f"https://www.google.com/maps/search/?api=1&query={quote_plus(p_name + ' New York City')}"
    col_card, col_heart = st.columns([9, 1])
    with col_card:
        st.markdown(f"""
<div class="px-card-left" style="--accent:{accent}">
  <div class="px-card-area">📍 {p_area}</div>
  <div class="px-card-name"><a href="{maps_url}" target="_blank" rel="noopener">{p_emoji} {p_name}</a></div>
  <div class="px-card-tip">{p_tip}</div>
  <div class="px-tags">{entry_tag}{book_tag}{insta_tag}{rt}</div>
</div>""", unsafe_allow_html=True)
    with col_heart:
        st.button("❤️" if is_fav else "♡", key=f"fav_{p_name}",
                  type="primary" if is_fav else "secondary",
                  on_click=toggle_fav, args=(p_name,))

def render_food(row):
    r_area    = row[0]; r_name = row[1]; r_cuisine = row[2]
    r_price   = row[3]; r_tip  = row[4]
    r_source  = row[5] if len(row) > 5 else ""
    is_fav    = r_name in st.session_state.favourites
    accent    = CUISINE_ACCENT.get(r_cuisine, "#445566")
    price_cls = PRICE_TAG.get(r_price, "tag-budget")
    src_tag   = '<span class="px-tag tag-insta">INSTAGRAM</span>' if r_source == "instagram" \
                else '<span class="px-tag tag-sfp">PHIL\'S PICK</span>' if r_source == "sfp" \
                else '<span class="px-tag tag-saved">MY LIST</span>'
    rt        = rating_tag(r_name)
    maps_url  = f"https://www.google.com/maps/search/?api=1&query={quote_plus(r_name + ' New York City')}"
    col_card, col_heart = st.columns([9, 1])
    with col_card:
        st.markdown(f"""
<div class="px-card-left" style="--accent:{accent}">
  <div class="px-card-area">📍 {r_area}</div>
  <div class="px-card-name"><a href="{maps_url}" target="_blank" rel="noopener">{r_name}</a></div>
  <div class="px-card-tip">{r_tip}</div>
  <div class="px-tags">
    <span class="px-tag tag-category">{r_cuisine}</span>
    <span class="px-tag {price_cls}">{r_price}</span>
    {src_tag}{rt}
  </div>
</div>""", unsafe_allow_html=True)
    with col_heart:
        st.button("❤️" if is_fav else "♡", key=f"fav_{r_name}",
                  type="primary" if is_fav else "secondary",
                  on_click=toggle_fav, args=(r_name,))

def render_shop(row):
    s_area, s_name, s_type, s_emoji, s_price, s_tip, s_book = row
    is_fav   = s_name in st.session_state.favourites
    accent   = SHOP_ACCENT.get(s_type, "#445566")
    book_tag = '<span class="px-tag tag-book">BOOK AHEAD</span>' if s_book else ""
    rt       = rating_tag(s_name)
    maps_url  = f"https://www.google.com/maps/search/?api=1&query={quote_plus(s_name + ' New York City')}"
    col_card, col_heart = st.columns([9, 1])
    with col_card:
        st.markdown(f"""
<div class="px-card-left" style="--accent:{accent}">
  <div class="px-card-area">📍 {s_area}</div>
  <div class="px-card-name"><a href="{maps_url}" target="_blank" rel="noopener">{s_emoji} {s_name}</a></div>
  <div class="px-card-tip">{s_tip}</div>
  <div class="px-tags">
    <span class="px-tag tag-category">{s_type}</span>
    <span class="px-tag tag-free">FREE ENTRY</span>
    {book_tag}{rt}
  </div>
</div>""", unsafe_allow_html=True)
    with col_heart:
        st.button("❤️" if is_fav else "♡", key=f"fav_{s_name}",
                  type="primary" if is_fav else "secondary",
                  on_click=toggle_fav, args=(s_name,))

# ── Content ───────────────────────────────────────────────────────────────────
if is_saved:
    total_saved = len(saved_sights_list) + len(saved_food_list) + len(saved_shop_list)
    if total_saved == 0:
        st.markdown("""
<div class="px-empty">
  <div class="px-empty-icon">♡</div>
  <div class="px-empty-title">NO SAVES YET</div>
  <div class="px-empty-sub">TAP ♡ ON ANY CARD<br>TO SAVE A PLACE</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown('<hr class="px-divider">', unsafe_allow_html=True)
        if saved_sights_list:
            st.markdown('<div class="px-section">◆ SIGHTS</div>', unsafe_allow_html=True)
            for row in saved_sights_list:
                render_sight(row)
        if saved_food_list:
            st.markdown('<div class="px-section">♥ FOOD & BARS</div>', unsafe_allow_html=True)
            for row in saved_food_list:
                render_food(row)
        if saved_shop_list:
            st.markdown('<div class="px-section">🛍 SHOPPING</div>', unsafe_allow_html=True)
            for row in saved_shop_list:
                render_shop(row)

elif not filtered:
    st.markdown("""
<div class="px-empty">
  <div class="px-empty-icon">🔍</div>
  <div class="px-empty-title">NO RESULTS</div>
  <div class="px-empty-sub">TRY ADJUSTING<br>YOUR FILTERS</div>
</div>""", unsafe_allow_html=True)

elif is_sights:
    st.markdown('<hr class="px-divider">', unsafe_allow_html=True)
    by_cat = defaultdict(list)
    for r in filtered:
        by_cat[r[2]].append(r)
    for category, items in by_cat.items():
        icon = CAT_ICONS.get(category, "📍")
        st.markdown(f'<div class="px-section">{icon} {category}</div>', unsafe_allow_html=True)
        for row in items:
            render_sight(row)

elif is_shopping:
    st.markdown('<hr class="px-divider">', unsafe_allow_html=True)
    by_type = defaultdict(list)
    for r in filtered:
        by_type[r[2]].append(r)
    for shop_type, items in by_type.items():
        st.markdown(f'<div class="px-section">🛍 {shop_type}</div>', unsafe_allow_html=True)
        for row in items:
            render_shop(row)

else:
    st.markdown('<hr class="px-divider">', unsafe_allow_html=True)
    by_cuisine = defaultdict(list)
    for r in filtered:
        by_cuisine[r[2]].append(r)
    for cuisine, items in by_cuisine.items():
        st.markdown(f'<div class="px-section">🍴 {cuisine}</div>', unsafe_allow_html=True)
        for row in items:
            render_food(row)
