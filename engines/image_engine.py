# image_engine.py — Smart Visual Asset Generator v2
# One strong image per platform — no SVG clutter, no fake visuals
# Uses Unsplash Source API (free, no key needed) for real photos
# + SVG quote card as fallback

import html as html_lib
from engines.intent_parser import parse_intent

# ── UNSPLASH SOURCE QUERIES ───────────────────────────────────────────────────
# Maps niche + mode to the best Unsplash search queries
# Unsplash Source: https://source.unsplash.com/WxWxW/query

_QUERY_MAP = {
    # (niche, mode) → [queries in priority order]
    ("career",    "product"):    ["resume career professional", "job interview office"],
    ("career",    "career"):     ["career growth professional", "job opportunity"],
    ("career",    "personal"):   ["professional workspace laptop", "career development"],
    ("ai",        "product"):    ["technology artificial intelligence", "futuristic tech"],
    ("ai",        "personal"):   ["coding computer technology", "developer workspace"],
    ("tech",      "product"):    ["technology startup workspace", "coding developer"],
    ("tech",      "personal"):   ["developer coding laptop", "tech workspace"],
    ("tech",      "topic"):      ["technology digital innovation", "computer science"],
    ("saas",      "product"):    ["startup office technology", "software product"],
    ("startup",   "product"):    ["startup team office", "entrepreneur working"],
    ("startup",   "personal"):   ["founder working laptop", "startup journey"],
    ("fitness",   "product"):    ["fitness gym workout", "healthy lifestyle"],
    ("fitness",   "creator"):    ["gym training fitness", "sports motivation"],
    ("finance",   "product"):    ["finance investment business", "money growth"],
    ("finance",   "topic"):      ["financial planning charts", "investment growth"],
    ("education", "product"):    ["learning education books", "online course study"],
    ("education", "personal"):   ["student studying books", "learning growth"],
    ("marketing", "product"):    ["marketing strategy digital", "business growth"],
    ("freelancer","freelancer"):  ["freelancer working creative", "creative workspace"],
    ("general",   "topic"):      ["professional workspace minimal", "growth mindset"],
    ("general",   "product"):    ["modern office startup", "business technology"],
    ("general",   "personal"):   ["professional development", "personal growth"],
}

def _get_query(niche: str, mode: str) -> str:
    # Try exact match first
    key = (niche, mode)
    if key in _QUERY_MAP:
        return _QUERY_MAP[key][0]
    # Try niche with "product" as fallback mode
    key2 = (niche, "product")
    if key2 in _QUERY_MAP:
        return _QUERY_MAP[key2][0]
    # Final fallback
    return "professional workspace minimal"


# ── MAIN FUNCTION ─────────────────────────────────────────────────────────────

def generate_images(goal: str, niche: str, tone: str, mind: dict = None) -> dict:
    """
    Returns ONE image per platform.
    Each image: { url, fallback_svg, prompt, label, source }
    """
    intent = parse_intent(goal)
    mode   = intent["mode"]
    subj   = intent["subject"]
    p      = intent["product"]

    # Best hook text for SVG fallback
    hook_text = ""
    if mind and mind.get("top_hooks"):
        hook_text = mind["top_hooks"][0].split(".")[0][:55]
    if not hook_text:
        hook_text = subj[:55]

    style = _detect_style(goal, tone, niche, mode)

    return {
        "linkedin":  _make_image("linkedin",  niche, mode, hook_text, style, p),
        "instagram": _make_image("instagram", niche, mode, hook_text, style, p),
        "twitter":   _make_image("twitter",   niche, mode, hook_text, style, p),
    }


def _make_image(platform: str, niche: str, mode: str, hook: str, style: dict, product: str) -> dict:
    query    = _platform_query(platform, niche, mode)
    dims     = {"linkedin": "1200x630", "instagram": "1080x1080", "twitter": "1200x628"}
    dim      = dims.get(platform, "1200x630")
    w, h     = dim.split("x")

    # Unsplash Source URL (free, no API key)
    url = f"https://source.unsplash.com/{dim}/?{query.replace(' ', ',')}"

    # SVG fallback card (shown while image loads or if network fails)
    svg = _svg_card(platform, hook, style, int(w), int(h))

    # AI image generation prompt (for Midjourney, Firefly, etc.)
    prompt = _ai_prompt(platform, niche, mode, hook, style)

    labels = {"linkedin": "LinkedIn Cover", "instagram": "Instagram Post", "twitter": "Twitter Card"}

    return {
        "url":          url,
        "fallback_svg": svg,
        "prompt":       prompt,
        "label":        labels.get(platform, platform.title()),
        "query":        query,
        "source":       "unsplash",
        "dims":         dim,
    }


def _platform_query(platform: str, niche: str, mode: str) -> str:
    base = _get_query(niche, mode)
    # Platform-specific adjustments
    if platform == "instagram":
        # Instagram = more aesthetic, visual
        ig_overrides = {
            "career":    "professional aesthetic modern",
            "tech":      "dark technology aesthetic",
            "fitness":   "fitness aesthetic gym",
            "startup":   "startup aesthetic minimal",
        }
        return ig_overrides.get(niche, base + " aesthetic")
    if platform == "twitter":
        # Twitter = bold, minimal
        return base.split()[0] + " minimal bold"
    return base


# ── STYLE DETECTOR ────────────────────────────────────────────────────────────

def _detect_style(goal: str, tone: str, niche: str, mode: str) -> dict:
    g = goal.lower()

    if any(w in g for w in ["luxury", "premium", "elite", "gold"]):
        palette = "luxury"
    elif any(w in g for w in ["meme", "funny", "humor"]):
        palette = "meme"
    elif niche in ("tech", "ai", "saas"):
        palette = "tech"
    elif niche == "fitness":
        palette = "energy"
    elif niche == "finance":
        palette = "finance"
    else:
        palette = "default"

    palettes = {
        "luxury":  {"bg":"#0a0806","acc":"#d4a853","acc2":"#8b6914","txt":"#f5e6c8","muted":"#9a8060"},
        "meme":    {"bg":"#0f0f0f","acc":"#ff6b6b","acc2":"#ffd93d","txt":"#ffffff","muted":"#aaaaaa"},
        "tech":    {"bg":"#060818","acc":"#7c3aed","acc2":"#2563eb","txt":"#e8e4ff","muted":"#7080aa"},
        "energy":  {"bg":"#060f0a","acc":"#22c55e","acc2":"#16a34a","txt":"#dcfce7","muted":"#6b9e7a"},
        "finance": {"bg":"#020c18","acc":"#38bdf8","acc2":"#0284c7","txt":"#e0f2fe","muted":"#5a8fab"},
        "default": {"bg":"#07050f","acc":"#8b5cf6","acc2":"#3b82f6","txt":"#f0ecfc","muted":"#7878a8"},
    }
    return {"palette": palette, **palettes.get(palette, palettes["default"])}


# ── SVG FALLBACK CARD ─────────────────────────────────────────────────────────

def _svg_card(platform: str, hook: str, style: dict, w: int, h: int) -> str:
    bg   = style["bg"]
    acc  = style["acc"]
    acc2 = style["acc2"]
    txt  = style["txt"]
    mut  = style["muted"]
    h_text = html_lib.escape(hook[:52] + ("..." if len(hook) > 52 else ""))

    # Wrap text into lines
    words = hook[:52].split()
    lines, line = [], ""
    for word in words:
        if len(line) + len(word) + 1 <= (24 if w > 800 else 18):
            line = (line + " " + word).strip()
        else:
            lines.append(line); line = word
    if line: lines.append(line)

    font_size  = 42 if w > 800 else 34
    y_start    = h // 2 - (len(lines) - 1) * (font_size * 0.6)
    tspans     = "".join(
        f'<tspan x="{w*0.08}" dy="{0 if i==0 else font_size*1.15}">{html_lib.escape(l)}</tspan>'
        for i, l in enumerate(lines)
    )
    plat_label = {"linkedin": "LINKEDIN", "instagram": "INSTAGRAM", "twitter": "TWITTER / X"}.get(platform, platform.upper())

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="bg{platform}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{acc2}" stop-opacity="0.15"/>
    </linearGradient>
    <linearGradient id="ac{platform}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{acc}"/><stop offset="100%" stop-color="{acc2}"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg{platform})"/>
  <circle cx="{w*0.85}" cy="{h*0.2}" r="{min(w,h)*0.35}" fill="{acc}" fill-opacity="0.06"/>
  <rect x="0" y="0" width="6" height="{h}" fill="url(#ac{platform})"/>
  <rect x="{w*0.08}" y="{h*0.1}" width="110" height="24" rx="12" fill="{acc}" fill-opacity="0.15"/>
  <text x="{w*0.08+55}" y="{h*0.1+16}" font-family="sans-serif" font-size="10" font-weight="700"
        fill="{acc}" text-anchor="middle" letter-spacing="2">{plat_label}</text>
  <text font-family="Georgia,serif" font-size="{font_size}" font-weight="700" fill="{txt}" y="{y_start}">{tspans}</text>
  <rect x="{w*0.08}" y="{h*0.88}" width="50" height="3" rx="2" fill="url(#ac{platform})"/>
  <text x="{w*0.08+58}" y="{h*0.89}" font-family="sans-serif" font-size="11" fill="{mut}">DropMeOnline</text>
</svg>"""


# ── AI PROMPT GENERATOR ───────────────────────────────────────────────────────

def _ai_prompt(platform: str, niche: str, mode: str, hook: str, style: dict) -> str:
    palette = style.get("palette", "dark")
    dims = {"linkedin": "1200x630 landscape", "instagram": "1080x1080 square", "twitter": "1200x628 landscape"}
    dim  = dims.get(platform, "1200x630")
    plat_style = {
        "linkedin":  "professional, clean, authority aesthetic, minimal, premium dark",
        "instagram": "bold, vibrant, scroll-stopping, high contrast, aesthetic",
        "twitter":   "stark minimal, quote card feel, dark background, single bold element",
    }.get(platform, "professional dark")
    return f"{dim}, {plat_style}, {palette} color palette, text: '{hook[:40]}', no people, photorealistic, high quality"