from engines.intent_parser import parse_intent
# platform_adapter.py — Smart platform adapter
# Reads intent from content_generator output and applies platform-native polish
# Does NOT repeat the post — adds finishing layer only

def adapt_platform(content: dict) -> dict:
    """
    Input:  content dict from generate_content() —
            {"linkedin": "...", "instagram": "...", "twitter": "...", "_intent": {...}}
    Output: polished platform-ready dict
    """
    intent  = content.get("_intent", {})
    tone    = intent.get("tone", "default")
    length  = intent.get("length", "default")

    # Get clean product ref if available
    _p   = intent.get("product", "")
    _ref = intent.get("product_ref", "the tool")

    adapted = {}

    # ── LinkedIn ─────────────────────────────────────────────────────────────
    li = content.get("linkedin", "")
    # Only add CTA if it's not a short post and doesn't already have one
    needs_cta = length != "short" and not any(
        x in li.lower() for x in ["thoughts?", "comment", "discuss", "what do you think", "drop a"]
    )
    if needs_cta:
        ctas = [
            "\n\nWhat's your take? Drop it below.",
            "\n\nHave you experienced this? I'd love to hear your version.",
            "\n\nAgree or disagree — genuinely curious what others are seeing.",
            "\n\nSave this if it resonates. Share it if someone needs it.",
        ]
        from datetime import datetime
        li += ctas[int(datetime.now().second) % len(ctas)]
    adapted["linkedin"] = li

    # ── Instagram ────────────────────────────────────────────────────────────
    ig = content.get("instagram", "")
    # Add hashtags only if there aren't already hashtags
    if "#" not in ig:
        hashtag_sets = {
            "ai":        "#ai #artificialintelligence #aitools #futureofwork #techstartup",
            "career":    "#career #careertips #linkedin #jobsearch #personalbrand",
            "startup":   "#startup #founder #buildinpublic #entrepreneurship #indiehacker",
            "fitness":   "#fitness #healthylifestyle #workout #mindset #motivation",
            "finance":   "#personalfinance #investing #moneymindset #financialfreedom",
            "education": "#learning #selfimprovement #skills #growthmindset #education",
            "tech":      "#tech #developer #coding #softwareengineering #buildinpublic",
            "marketing": "#marketing #digitalmarketing #contentmarketing #growthhacking",
        }
        niche = intent.get("niche", "general")
        tags  = hashtag_sets.get(niche, "#growth #mindset #motivation #growthmindset #realtalk")
        ig    = ig.rstrip() + f"\n\n{tags}"
    adapted["instagram"] = ig

    # ── Twitter ──────────────────────────────────────────────────────────────
    tw = content.get("twitter", "")
    # Twitter: trim to sharp single statement if it's very long and not a thread
    if length != "thread" and len(tw) > 280:
        lines = [l for l in tw.split("\n") if l.strip()]
        tw    = "\n\n".join(lines[:4])
    adapted["twitter"] = tw

    return adapted