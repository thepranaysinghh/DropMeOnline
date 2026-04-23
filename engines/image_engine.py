# image_engine.py — Smart Visual Asset Generator
# Generates platform-specific SVG graphics + AI prompts
# No external API needed — SVGs are real downloadable assets

from datetime import datetime
import html as html_lib

def generate_images(goal: str, niche: str, tone: str, mind: dict = None) -> dict:
    """
    Input:
        goal  — user's goal string
        niche — detected niche (ai, career, startup, etc.)
        tone  — detected tone (bold, emotional, funny, etc.)
        mind  — mastermind output (optional, for hook text)
    Output:
        dict with linkedin, instagram, twitter image data
        Each: { svg, prompt, style, label }
    """
    mind     = mind or {}
    hook     = mind.get("top_hooks", [""])[0] if mind.get("top_hooks") else ""
    headline = hook.split(".")[0][:52] if hook else _headline_from_goal(goal)
    sub      = _subtitle_from_niche(niche)
    style    = _detect_style(goal, tone)

    return {
        "linkedin":  _linkedin_image(headline, sub, style, goal),
        "instagram": _instagram_image(headline, sub, style, goal, tone),
        "twitter":   _twitter_image(headline, style, goal),
    }


# ── STYLE DETECTOR ────────────────────────────────────────────────────────────

def _detect_style(goal: str, tone: str) -> dict:
    g = goal.lower()
    t = tone.lower() if tone else ""

    # Palette detection
    if any(w in g for w in ["luxury", "premium", "elite", "gold"]):
        palette = "luxury"
    elif any(w in g for w in ["meme", "funny", "humor", "lol", "gen z"]):
        palette = "meme"
    elif any(w in g for w in ["startup", "saas", "tech", "ai", "build"]):
        palette = "tech"
    elif any(w in g for w in ["fitness", "health", "energy", "strong"]):
        palette = "energy"
    elif any(w in g for w in ["fashion", "style", "aesthetic", "minimal"]):
        palette = "minimal"
    elif any(w in g for w in ["finance", "money", "invest", "wealth"]):
        palette = "finance"
    else:
        palette = "default"

    palettes = {
        "luxury":  {"bg": "#0a0806", "bg2": "#1a1208", "accent": "#d4a853", "accent2": "#8b6914", "text": "#f5e6c8", "muted": "#9a8060"},
        "meme":    {"bg": "#0f0f0f", "bg2": "#1a1a2e", "accent": "#ff6b6b", "accent2": "#ffd93d", "text": "#ffffff", "muted": "#aaaaaa"},
        "tech":    {"bg": "#060818", "bg2": "#0d1530", "accent": "#7c3aed", "accent2": "#2563eb", "text": "#e8e4ff", "muted": "#7080aa"},
        "energy":  {"bg": "#060f0a", "bg2": "#0d1f14", "accent": "#22c55e", "accent2": "#16a34a", "text": "#dcfce7", "muted": "#6b9e7a"},
        "minimal": {"bg": "#0c0c0c", "bg2": "#181818", "accent": "#e2e8f0", "accent2": "#94a3b8", "text": "#ffffff", "muted": "#64748b"},
        "finance": {"bg": "#020c18", "bg2": "#041428", "accent": "#38bdf8", "accent2": "#0284c7", "text": "#e0f2fe", "muted": "#5a8fab"},
        "default": {"bg": "#07050f", "bg2": "#120e28", "accent": "#8b5cf6", "accent2": "#3b82f6", "text": "#f0ecfc", "muted": "#7878a8"},
    }
    colors = palettes.get(palette, palettes["default"])
    return {"palette": palette, **colors}


# ── TEXT HELPERS ──────────────────────────────────────────────────────────────

def _headline_from_goal(goal: str) -> str:
    words = goal.strip().split()
    short = " ".join(words[:7])
    return short[:52] if len(short) <= 52 else short[:49] + "..."

def _subtitle_from_niche(niche: str) -> str:
    subs = {
        "ai":       "AI-powered growth",
        "career":   "Career & Personal Brand",
        "startup":  "Founder-led marketing",
        "saas":     "SaaS Growth Strategy",
        "fitness":  "Fitness & Wellness",
        "finance":  "Financial Intelligence",
        "tech":     "Tech & Developer",
        "marketing":"Growth Marketing",
        "education":"Learning & Skills",
        "fashion":  "Style & Aesthetics",
        "general":  "Growth Strategy",
    }
    return subs.get(niche, "Growth Strategy")

def _esc(text: str) -> str:
    return html_lib.escape(str(text))

def _wrap_text(text: str, max_chars: int) -> list:
    """Splits text into lines of max_chars for SVG tspan."""
    words = text.split()
    lines, line = [], ""
    for w in words:
        if len(line) + len(w) + 1 <= max_chars:
            line = (line + " " + w).strip()
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


# ── LINKEDIN SVG ──────────────────────────────────────────────────────────────

def _linkedin_image(headline: str, sub: str, style: dict, goal: str) -> dict:
    bg    = style["bg"]
    bg2   = style["bg2"]
    acc   = style["accent"]
    acc2  = style["accent2"]
    txt   = style["text"]
    muted = style["muted"]
    h     = _esc(headline)
    s     = _esc(sub)

    lines  = _wrap_text(headline, 26)
    y_base = 260 - (len(lines) - 1) * 22

    tspans = ""
    for i, line in enumerate(lines):
        tspans += f'<tspan x="60" dy="{0 if i==0 else 48}">{_esc(line)}</tspan>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 420" width="700" height="420">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{acc}"/>
      <stop offset="100%" stop-color="{acc2}"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <!-- Background -->
  <rect width="700" height="420" fill="url(#bg)"/>
  <!-- Grid lines -->
  <line x1="0" y1="140" x2="700" y2="140" stroke="{acc}" stroke-opacity="0.06" stroke-width="1"/>
  <line x1="0" y1="280" x2="700" y2="280" stroke="{acc}" stroke-opacity="0.06" stroke-width="1"/>
  <line x1="233" y1="0" x2="233" y2="420" stroke="{acc}" stroke-opacity="0.04" stroke-width="1"/>
  <line x1="466" y1="0" x2="466" y2="420" stroke="{acc}" stroke-opacity="0.04" stroke-width="1"/>
  <!-- Orb glow -->
  <circle cx="600" cy="80" r="150" fill="{acc}" fill-opacity="0.07" filter="url(#glow)"/>
  <circle cx="100" cy="360" r="100" fill="{acc2}" fill-opacity="0.06" filter="url(#glow)"/>
  <!-- Accent bar -->
  <rect x="0" y="0" width="6" height="420" fill="url(#acc)"/>
  <!-- Top label -->
  <rect x="60" y="52" width="140" height="28" rx="14" fill="{acc}" fill-opacity="0.15"/>
  <rect x="60" y="52" width="140" height="28" rx="14" fill="none" stroke="{acc}" stroke-opacity="0.35" stroke-width="1"/>
  <text x="130" y="70" font-family="'DM Sans',sans-serif" font-size="11" font-weight="700"
        fill="{acc}" text-anchor="middle" letter-spacing="2">LINKEDIN POST</text>
  <!-- Headline -->
  <text font-family="'Georgia',serif" font-size="42" font-weight="700"
        fill="{txt}" y="{y_base}">{tspans}</text>
  <!-- Sub label -->
  <text x="60" y="340" font-family="'DM Sans',sans-serif" font-size="14"
        fill="{muted}" letter-spacing="1">{s}</text>
  <!-- Bottom accent line -->
  <rect x="60" y="370" width="80" height="3" rx="2" fill="url(#acc)"/>
  <text x="155" y="373" font-family="'DM Sans',sans-serif" font-size="12"
        fill="{muted}">DropMeOnline</text>
  <!-- Corner marks -->
  <rect x="640" y="380" width="40" height="40" rx="8" fill="{acc}" fill-opacity="0.12"/>
  <text x="660" y="405" font-family="'DM Sans',sans-serif" font-size="11"
        fill="{acc}" text-anchor="middle" font-weight="700">LI</text>
</svg>"""

    prompt = (
        f"Professional LinkedIn carousel cover. {style['palette'].title()} aesthetic. "
        f"Dark background {bg}. Bold serif headline: '{headline}'. "
        f"Accent color {acc}. Minimal premium layout. No people. Clean typography. "
        f"Authority graphic style."
    )

    return {"svg": svg, "prompt": prompt, "style": style["palette"], "label": "LinkedIn Cover"}


# ── INSTAGRAM SVG ─────────────────────────────────────────────────────────────

def _instagram_image(headline: str, sub: str, style: dict, goal: str, tone: str) -> dict:
    bg    = style["bg"]
    bg2   = style["bg2"]
    acc   = style["accent"]
    acc2  = style["accent2"]
    txt   = style["text"]
    muted = style["muted"]

    lines  = _wrap_text(headline, 22)
    y_base = 520 - (len(lines) - 1) * 26

    tspans = ""
    for i, line in enumerate(lines):
        tspans += f'<tspan x="50" dy="{0 if i==0 else 52}">{_esc(line)}</tspan>'

    # Tone-specific decorative element
    is_meme = tone in ("funny", "bold") or style["palette"] == "meme"
    deco = ""
    if is_meme:
        deco = f"""
  <text x="530" y="120" font-size="72" text-anchor="middle" opacity="0.25">👀</text>"""
    else:
        deco = f"""
  <circle cx="530" cy="100" r="60" fill="{acc}" fill-opacity="0.1"/>
  <circle cx="530" cy="100" r="40" fill="{acc}" fill-opacity="0.08"/>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.7" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{acc}"/>
      <stop offset="100%" stop-color="{acc2}"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="20" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <!-- Background -->
  <rect width="600" height="600" fill="url(#bg)"/>
  <!-- Large orb -->
  <circle cx="480" cy="140" r="200" fill="{acc}" fill-opacity="0.09" filter="url(#glow)"/>
  <circle cx="120" cy="480" r="140" fill="{acc2}" fill-opacity="0.07" filter="url(#glow)"/>
  {deco}
  <!-- Top bar -->
  <rect x="0" y="0" width="600" height="5" fill="url(#acc)"/>
  <!-- Platform badge -->
  <rect x="50" y="48" width="130" height="28" rx="14" fill="{acc}" fill-opacity="0.15"/>
  <rect x="50" y="48" width="130" height="28" rx="14" fill="none" stroke="{acc}" stroke-opacity="0.4" stroke-width="1"/>
  <text x="115" y="66" font-family="'DM Sans',sans-serif" font-size="11" font-weight="700"
        fill="{acc}" text-anchor="middle" letter-spacing="2">INSTAGRAM</text>
  <!-- Headline -->
  <text font-family="'Georgia',serif" font-size="54" font-weight="700"
        fill="{txt}" y="{y_base}">{tspans}</text>
  <!-- Sub text -->
  <text x="50" y="{y_base + len(lines)*56 + 30}" font-family="'DM Sans',sans-serif"
        font-size="16" fill="{muted}">{_esc(sub)}</text>
  <!-- Bottom bar -->
  <rect x="0" y="565" width="600" height="35" fill="{acc}" fill-opacity="0.08"/>
  <text x="50" y="587" font-family="'DM Sans',sans-serif" font-size="12"
        fill="{muted}" letter-spacing="1">DropMeOnline · AI Growth Platform</text>
  <!-- Gradient bottom accent -->
  <rect x="0" y="595" width="600" height="5" fill="url(#acc)"/>
</svg>"""

    prompt = (
        f"Viral Instagram post graphic. {style['palette'].title()} aesthetic. "
        f"Square 1:1 format. Dark background {bg}. "
        f"Bold oversized headline: '{headline}'. Accent: {acc}. "
        f"High contrast, scroll-stopping. {'Meme energy, bold text overlay.' if is_meme else 'Premium editorial feel.'}"
    )

    return {"svg": svg, "prompt": prompt, "style": style["palette"], "label": "Instagram Post"}


# ── TWITTER SVG ───────────────────────────────────────────────────────────────

def _twitter_image(headline: str, style: dict, goal: str) -> dict:
    bg    = style["bg"]
    bg2   = style["bg2"]
    acc   = style["accent"]
    acc2  = style["accent2"]
    txt   = style["text"]
    muted = style["muted"]

    lines  = _wrap_text(headline, 30)
    y_base = 160 - (len(lines) - 1) * 20

    tspans = ""
    for i, line in enumerate(lines):
        tspans += f'<tspan x="50" dy="{0 if i==0 else 44}">{_esc(line)}</tspan>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 350" width="700" height="350">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{acc}"/>
      <stop offset="100%" stop-color="{acc2}"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <!-- Background -->
  <rect width="700" height="350" fill="url(#bg)"/>
  <!-- Subtle orb -->
  <circle cx="580" cy="60" r="120" fill="{acc}" fill-opacity="0.08" filter="url(#glow)"/>
  <!-- Left accent bar -->
  <rect x="0" y="0" width="5" height="350" fill="url(#acc)"/>
  <!-- X/Twitter label -->
  <rect x="50" y="44" width="110" height="26" rx="13" fill="{acc}" fill-opacity="0.12"/>
  <rect x="50" y="44" width="110" height="26" rx="13" fill="none" stroke="{acc}" stroke-opacity="0.3" stroke-width="1"/>
  <text x="105" y="61" font-family="'DM Sans',sans-serif" font-size="11" font-weight="700"
        fill="{acc}" text-anchor="middle" letter-spacing="2">TWITTER / X</text>
  <!-- Quote mark -->
  <text x="50" y="{y_base - 30}" font-family="'Georgia',serif" font-size="60"
        fill="{acc}" fill-opacity="0.25">"</text>
  <!-- Headline -->
  <text font-family="'Georgia',serif" font-size="36" font-weight="700"
        fill="{txt}" y="{y_base}">{tspans}</text>
  <!-- Bottom line -->
  <rect x="50" y="298" width="60" height="3" rx="2" fill="url(#acc)"/>
  <text x="122" y="301" font-family="'DM Sans',sans-serif" font-size="12"
        fill="{muted}">DropMeOnline</text>
  <!-- Right corner badge -->
  <text x="640" y="330" font-family="'DM Sans',sans-serif" font-size="28"
        fill="{acc}" fill-opacity="0.2" text-anchor="middle" font-weight="900">𝕏</text>
</svg>"""

    prompt = (
        f"Twitter/X quote card. {style['palette'].title()} aesthetic. "
        f"Dark minimal background {bg}. Single bold line: '{headline}'. "
        f"Accent {acc}. Feels like a screenshot someone would share. "
        f"No decoration, pure typographic power."
    )

    return {"svg": svg, "prompt": prompt, "style": style["palette"], "label": "Twitter Card"}