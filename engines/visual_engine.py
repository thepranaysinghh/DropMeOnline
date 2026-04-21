# visual_engine.py — Upgraded Visual Production Engine
# Now powered by autopilot content + mastermind intelligence
# Every visual is matched to the actual post — not generic templates

def generate_visual_assets(
    goal:         str,
    auto_content: dict = None,
    mind:         dict = None,
    platform:     str  = "linkedin",
) -> dict:
    """
    Input:
        goal         — e.g. "Promote AI resume tool"
        auto_content — output from autopilot_content_engine (hook, post, image_idea, angle, tone)
        mind         — output from mastermind_engine (core_angle, trigger, tone, hook_style)
        platform     — "linkedin" | "instagram" | "twitter" | "facebook"
    Output:
        { headline, format, image_prompt, style_notes, why_it_works }
    """

    auto_content = auto_content or {}
    mind         = mind         or {}
    platform     = platform.lower().strip()

    # --- Pull intelligence from inputs ---
    hook      = auto_content.get("hook",        "")
    post      = auto_content.get("post",        "")
    image_idea = auto_content.get("image_idea", "")
    angle     = auto_content.get("angle")   or mind.get("core_angle",          "")
    tone      = auto_content.get("tone")    or mind.get("tone",                 "")
    trigger   = mind.get("psychology_trigger", "curiosity")
    hook_style = mind.get("hook_style",        "")

    # --- Build visual package ---
    headline    = _build_headline(hook, platform, trigger)
    fmt         = _pick_format(platform, image_idea, tone, trigger)
    img_prompt  = _build_image_prompt(platform, headline, hook, tone, trigger, fmt)
    style_notes = _build_style_notes(platform, tone, trigger, fmt)
    why         = _build_why(platform, fmt, trigger, tone, headline)

    return {
        "headline":    headline,
        "format":      fmt,
        "image_prompt": img_prompt,
        "style_notes": style_notes,
        "why_it_works": why,
    }


# ══════════════════════════════════════════════════════════════════════════════
# HEADLINE BUILDER — derived from actual hook, not generic
# ══════════════════════════════════════════════════════════════════════════════

def _build_headline(hook: str, platform: str, trigger: str) -> str:
    if not hook:
        return _fallback_headline(platform, trigger)

    # Extract strongest phrase from hook (first sentence)
    first_sentence = hook.split(".")[0].split("—")[0].split("—")[0].strip()

    # Trim to visual-friendly length
    if len(first_sentence) > 72:
        words = first_sentence.split()
        first_sentence = " ".join(words[:10]) + "..."

    # Platform shaping
    if platform == "linkedin":
        return first_sentence  # Clean authority — let the words speak

    elif platform == "instagram":
        # Add energy markers for Instagram
        energy = {
            "fear":      " 👀",
            "curiosity": " 🤯",
            "relief":    " ✨",
            "ambition":  " 🚀",
            "funny":     " 💀",
        }
        suffix = energy.get(trigger, " 🔥")
        return first_sentence + suffix

    elif platform == "twitter":
        # Twitter: sharp, no trailing punctuation fluff
        return first_sentence.rstrip(".").rstrip(",")

    return first_sentence


def _fallback_headline(platform: str, trigger: str) -> str:
    fallbacks = {
        ("linkedin",  "fear"):      "Most people won't see this coming.",
        ("linkedin",  "curiosity"): "The pattern nobody talks about — until now.",
        ("linkedin",  "status"):    "What high performers already figured out.",
        ("instagram", "curiosity"): "Nobody told you this 👀",
        ("instagram", "funny"):     "POV: You finally found what actually works 💀",
        ("instagram", "ambition"):  "Your next level starts here 🚀",
        ("twitter",   "controversial"): "Unpopular opinion nobody wants to say out loud.",
        ("twitter",   "curiosity"): "Something most people never figure out:",
    }
    return fallbacks.get((platform, trigger), "The thing that changes everything.")


# ══════════════════════════════════════════════════════════════════════════════
# FORMAT PICKER — matches actual content mood and platform
# ══════════════════════════════════════════════════════════════════════════════

def _pick_format(platform: str, image_idea: str, tone: str, trigger: str) -> str:
    idea = image_idea.lower() if image_idea else ""

    # Trust image_idea from autopilot if it's specific
    if "carousel" in idea:
        return "carousel"
    if "meme" in idea:
        return "meme"
    if "quote" in idea:
        return "quote_card"
    if "infographic" in idea:
        return "infographic"
    if "no image" in idea or "text-only" in idea:
        return "text_only"

    # Platform + trigger matrix
    matrix = {
        ("linkedin",  "fear"):      "carousel",
        ("linkedin",  "educational"): "carousel",
        ("linkedin",  "status"):    "quote_card",
        ("linkedin",  "emotional"): "quote_card",
        ("linkedin",  "curiosity"): "carousel",
        ("linkedin",  "controversial"): "text_only",
        ("instagram", "funny"):     "meme",
        ("instagram", "emotional"): "quote_card",
        ("instagram", "curiosity"): "carousel",
        ("instagram", "ambition"):  "bold_graphic",
        ("instagram", "savage"):    "bold_graphic",
        ("twitter",   "controversial"): "quote_card",
        ("twitter",   "educational"): "text_only",
        ("twitter",   "funny"):     "text_only",
        ("twitter",   "curiosity"): "quote_card",
    }
    return matrix.get((platform, trigger), _default_format(platform))


def _default_format(platform: str) -> str:
    return {
        "linkedin":  "carousel",
        "instagram": "bold_graphic",
        "twitter":   "quote_card",
        "facebook":  "bold_graphic",
    }.get(platform, "quote_card")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE PROMPT BUILDER — AI-generation ready, specific to actual content
# ══════════════════════════════════════════════════════════════════════════════

def _build_image_prompt(
    platform: str,
    headline: str,
    hook:     str,
    tone:     str,
    trigger:  str,
    fmt:      str,
) -> str:

    # Tone-to-visual-mood mapping
    tone_visual = "clean and professional"
    t = tone.lower() if tone else ""
    if "vulnerability" in t or "emotional" in t:
        tone_visual = "soft, warm, intimate"
    elif "wit" in t or "funny" in t:
        tone_visual = "playful, high-contrast, irreverent"
    elif "authority" in t or "confident" in t:
        tone_visual = "premium, minimal, commanding"
    elif "sharp" in t or "bold" in t:
        tone_visual = "stark, high-impact, no decoration"

    # Format-specific prompt templates
    prompts = {

        "carousel": (
            f"Professional presentation slide. "
            f"Dark navy or deep charcoal background (#0a0a1a). "
            f"Large bold white headline text: \"{headline}\". "
            f"Subtle purple-to-blue gradient accent line at bottom. "
            f"Minimalist layout — one idea per frame, lots of breathing room. "
            f"Tone: {tone_visual}. No stock photo people. No clutter. "
            f"Font feel: Syne or DM Sans Bold. "
            f"This is for {platform.capitalize()} — premium authority aesthetic."
        ),

        "meme": (
            f"Classic meme format. High contrast background. "
            f"Top white bold text. Bottom punchline text. "
            f"Related to: \"{headline}\". "
            f"Tone: {tone_visual}. "
            f"Feels instantly recognisable and shareable. "
            f"No corporate logos. Bold Impact or Anton font. "
            f"Black background or extremely high contrast image."
        ),

        "quote_card": (
            f"Minimal quote card design. "
            f"Dark background (#0f0f0f or #0a0a1a). "
            f"Single white text line: \"{headline}\". "
            f"No decoration. No icons. No border gradients. "
            f"The words carry the entire visual weight. "
            f"Font: Inter Bold or Space Grotesk. "
            f"Tone: {tone_visual}. "
            f"Feels like a screenshot someone would share unedited."
        ),

        "bold_graphic": (
            f"Eye-catching social media graphic. "
            f"High contrast split or gradient background (purple-to-blue or dark-to-neon). "
            f"Oversized bold headline: \"{headline}\". "
            f"Strong visual energy — scroll-stopping in 0.5 seconds. "
            f"Tone: {tone_visual}. "
            f"Suitable for Instagram feed. "
            f"Font: Anton, Bebas Neue or Impact. "
            f"No soft pastels. Pure confidence visually."
        ),

        "infographic": (
            f"Clean data infographic. "
            f"Dark background. White text. Purple accent for data points. "
            f"Title: \"{headline}\". "
            f"3 to 5 key insight blocks with icons. "
            f"Tone: {tone_visual}. "
            f"Premium consulting aesthetic — no clip art, no comic sans energy. "
            f"Suitable for {platform.capitalize()} carousel slide."
        ),

        "text_only": (
            f"No image needed for this post. "
            f"The hook is: \"{headline}\". "
            f"Design direction: let the words dominate. "
            f"If a background is used, keep it solid dark with one accent colour. "
            f"Tone: {tone_visual}."
        ),
    }

    return prompts.get(fmt, prompts["quote_card"])


# ══════════════════════════════════════════════════════════════════════════════
# STYLE NOTES — specific to the actual tone and platform
# ══════════════════════════════════════════════════════════════════════════════

def _build_style_notes(platform: str, tone: str, trigger: str, fmt: str) -> str:
    t = tone.lower() if tone else ""

    # Base style per platform
    base = {
        "linkedin":  "Premium and restrained. Every element earns its place. Dark > light. Authority > decoration.",
        "instagram": "Visual-first. If it doesn't stop the scroll in half a second, redesign it.",
        "twitter":   "The visual should feel like something someone would screenshot and send to a friend.",
        "facebook":  "Warm and community-facing. Slightly more approachable than LinkedIn.",
    }.get(platform, "Clean, high contrast, text-led.")

    # Tone modifier
    tone_mod = ""
    if "vulnerability" in t or "emotional" in t:
        tone_mod = " Lean into soft gradients and generous white space — warmth over sharpness."
    elif "wit" in t or "funny" in t:
        tone_mod = " Contrast and energy. Meme format if possible — don't be precious about it."
    elif "authority" in t:
        tone_mod = " Zero decoration. Bold typography carries the whole thing."
    elif "sharp" in t or "bold" in t:
        tone_mod = " Black and white preferred. One strong accent colour maximum."

    # Trigger note
    trigger_note = {
        "fear":      " Use tension in the visual — dark colours, stark contrast.",
        "curiosity": " Visual should feel incomplete — make them want to read the caption.",
        "relief":    " Warm palette. Something that feels like a sigh of relief.",
        "status":    " Aspirational aesthetic — this is what premium looks like.",
        "ambition":  " Energy and forward motion — gradients that go upward.",
        "belonging": " Community warmth — not cold, not corporate.",
    }.get(trigger, "")

    return f"{base}{tone_mod}{trigger_note}"


# ══════════════════════════════════════════════════════════════════════════════
# WHY IT WORKS — self-evaluation specific to format + platform + trigger
# ══════════════════════════════════════════════════════════════════════════════

def _build_why(platform: str, fmt: str, trigger: str, tone: str, headline: str) -> str:
    fmt_reason = {
        "carousel":    "Carousels on LinkedIn get the highest dwell time of any format — the algorithm rewards it.",
        "meme":        "Memes get shared without asking. If it's relatable, people send it before they think about it.",
        "quote_card":  "Quote cards get saved and reshared. They travel outside your original audience.",
        "bold_graphic": "Bold graphics stop the thumb. On Instagram, the visual decides in 0.3 seconds.",
        "infographic": "Infographics get saved at 3x the rate of regular posts — people return to useful things.",
        "text_only":   "Text-only posts on LinkedIn outperform images when the first line is strong enough to earn the click.",
    }.get(fmt, "Format matches content energy and platform behaviour.")

    trigger_reason = {
        "fear":      " Fear triggers are the highest-engagement psychology — people act to avoid loss.",
        "curiosity": " An open loop the brain wants closed keeps people reading past the hook.",
        "status":    " Status content gets shared by people who want to be associated with it.",
        "relief":    " Relief content gets saved — people come back to things that made them feel understood.",
        "ambition":  " Ambition content gets saved and revisited when motivation is needed.",
        "belonging": " Belonging content gets shared in communities and group chats.",
    }.get(trigger, "")

    return f"{fmt_reason}{trigger_reason}"