# intent_parser.py — Converts raw user prompt into clean structured intent
# The single source of truth for what the user actually means
# Used by all content engines — no raw goal string ever touches post copy

import re

def parse_intent(goal: str) -> dict:
    """
    Input:  raw user goal string
    Output: structured intent dict

    Keys:
        product     — short clean product/brand name  e.g. "AI Resume Tool"
        product_ref — ultra-short ref for inline use  e.g. "the tool"
        action      — what they want to achieve       e.g. "grow on LinkedIn"
        audience    — inferred audience               e.g. "job seekers"
        platforms   — list of platforms mentioned
        tone        — detected tone style
        length      — short / thread / long / default
        niche       — detected niche category
        duration    — e.g. "30 days" or None
    """
    text  = goal.strip()
    lower = text.lower()

    product     = _extract_product(text, lower)
    product_ref = _short_ref(product)
    action      = _extract_action(lower, product)
    audience    = _extract_audience(lower)
    platforms   = _extract_platforms(lower)
    tone        = _extract_tone(lower)
    length      = _extract_length(lower)
    niche       = _extract_niche(lower)
    duration    = _extract_duration(lower)

    return {
        "product":     product,
        "product_ref": product_ref,
        "action":      action,
        "audience":    audience,
        "platforms":   platforms,
        "tone":        tone,
        "length":      length,
        "niche":       niche,
        "duration":    duration,
        "raw":         text,           # kept for fallback only — never paste into posts
    }


# ══════════════════════════════════════════════════════════════════════════════
# PRODUCT EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════

def _extract_product(text: str, lower: str) -> str:
    """
    Priority order:
    1. Quoted product name  e.g. "ResumeAI" or 'CareerBot'
    2. 'my X' pattern
    3. Known product keyword
    4. Clean fallback
    """
    # Quoted name
    quoted = re.search(r'["\']([A-Za-z0-9 ]{2,30})["\']', text)
    if quoted:
        return quoted.group(1).strip().title()

    # "my X" pattern — extract X (2-5 words)
    my_match = re.search(
        r'\bmy\s+((?:ai\s+|saas\s+|new\s+|online\s+)?[a-z]+(?:\s+[a-z]+){0,3})',
        lower
    )
    if my_match:
        raw_product = my_match.group(1).strip()
        # Strip noise words from end AND common platform/goal words
        noise = {
            "on","for","with","using","to","and","in","at","the","a","an",
            "linkedin","instagram","twitter","facebook","youtube","tiktok",
            "with","about","through","via","across","bold","startup","vibe",
            "fast","quick","free","paid","new","best","good","great",
        }
        words = raw_product.split()
        # Remove trailing noise
        while words and words[-1].lower() in noise:
            words.pop()
        # Remove leading noise
        while words and words[0].lower() in {"my","the","a","an","our"}:
            words.pop(0)
        if words:
            result = " ".join(words).title()
            # Fix common abbreviations mangled by .title()
            for fix_from, fix_to in [("Ai ", "AI "), ("Saas", "SaaS"), ("Llm", "LLM"), ("Seo", "SEO"), ("Ui ", "UI "), ("Ux ", "UX ")]:
                result = result.replace(fix_from, fix_to)
            return result

    # Known product type keywords
    product_map = [
        ("resume",      "AI Resume Tool"),
        ("cv",          "CV Builder"),
        ("portfolio",   "Portfolio Builder"),
        ("chatbot",     "AI Chatbot"),
        ("saas",        "SaaS Product"),
        ("web app",     "Web App"),
        ("mobile app",  "Mobile App"),
        ("app",         "App"),
        ("course",      "Online Course"),
        ("newsletter",  "Newsletter"),
        ("agency",      "Agency"),
        ("store",       "Online Store"),
        ("shop",        "Shop"),
        ("blog",        "Blog"),
        ("startup",     "Startup"),
        ("product",     "Product"),
        ("tool",        "Tool"),
        ("platform",    "Platform"),
        ("service",     "Service"),
        ("brand",       "Brand"),
    ]
    for kw, label in product_map:
        if kw in lower:
            # Check if there's an adjective before it
            pat = re.search(rf'((?:ai|smart|new|free|premium|online|digital|modern)\s+)?{re.escape(kw)}', lower)
            if pat and pat.group(1):
                return (pat.group(1) + label.split()[-1]).title()
            return label

    # Fallback: take first 3 meaningful words of goal
    words = [w for w in lower.split() if w not in {
        "grow", "build", "launch", "promote", "market", "create", "make",
        "my", "the", "a", "an", "on", "for", "with", "to", "and", "in"
    }]
    if words:
        return " ".join(words[:3]).title()

    return "the product"


def _short_ref(product: str) -> str:
    """
    Creates a natural inline reference — avoids long product names mid-sentence.
    'AI Resume Tool' → 'the tool'
    'Newsletter' → 'the newsletter'
    'SaaS Product' → 'the platform'
    """
    lower = product.lower()
    if any(w in lower for w in ["app", "tool", "builder", "bot", "ai"]):
        return "the tool"
    if any(w in lower for w in ["platform", "saas", "software"]):
        return "the platform"
    if any(w in lower for w in ["course", "program", "training"]):
        return "the course"
    if any(w in lower for w in ["store", "shop"]):
        return "the store"
    if any(w in lower for w in ["newsletter", "blog", "content"]):
        return "the newsletter"
    if any(w in lower for w in ["agency", "service", "studio"]):
        return "the agency"
    if any(w in lower for w in ["brand", "startup", "company"]):
        return "the brand"
    # Default: use product name itself (it's short enough)
    return product if len(product) <= 18 else "this"


# ══════════════════════════════════════════════════════════════════════════════
# ACTION EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════

def _extract_action(lower: str, product: str) -> str:
    if any(w in lower for w in ["launch", "launching", "just launched"]):
        return f"launch {product}"
    if any(w in lower for w in ["100 user", "1000 user", "first user", "get user"]):
        m = re.search(r'(\d+)\s*users?', lower)
        n = m.group(1) if m else "first"
        return f"get {n} users for {product}"
    if any(w in lower for w in ["viral", "go viral"]):
        return f"make {product} go viral"
    if any(w in lower for w in ["follower", "audience", "community"]):
        return f"build an audience around {product}"
    if any(w in lower for w in ["sale", "revenue", "customer", "convert"]):
        return f"drive sales for {product}"
    if any(w in lower for w in ["brand", "awareness", "known", "visibility"]):
        return f"build the brand for {product}"
    return f"grow {product}"


# ══════════════════════════════════════════════════════════════════════════════
# AUDIENCE EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════

def _extract_audience(lower: str) -> str:
    audience_map = [
        ("fresher",      "college freshers and early career job seekers"),
        ("student",      "students"),
        ("developer",    "developers and engineers"),
        ("programmer",   "developers and engineers"),
        ("founder",      "startup founders"),
        ("entrepreneur", "entrepreneurs"),
        ("freelancer",   "freelancers"),
        ("creator",      "content creators"),
        ("marketer",     "marketers"),
        ("professional", "working professionals"),
        ("executive",    "business executives"),
        ("business",     "business owners"),
        ("gen z",        "Gen Z audience"),
        ("teenager",     "teenagers"),
        ("parent",       "parents"),
        ("fitness",      "fitness enthusiasts"),
        ("investor",     "investors"),
    ]
    for kw, label in audience_map:
        if kw in lower:
            return label

    # Infer from niche
    if any(w in lower for w in ["resume", "job", "career", "hiring"]):
        return "job seekers and professionals"
    if any(w in lower for w in ["saas", "startup", "product"]):
        return "startup founders and product builders"
    if any(w in lower for w in ["fitness", "health", "gym"]):
        return "fitness enthusiasts"
    if any(w in lower for w in ["finance", "invest", "money"]):
        return "people building financial independence"
    if any(w in lower for w in ["course", "learn", "education"]):
        return "learners and skill builders"

    return "people looking to grow"


# ══════════════════════════════════════════════════════════════════════════════
# PLATFORM EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════

def _extract_platforms(lower: str) -> list:
    platforms = []
    if "linkedin" in lower:
        platforms.append("linkedin")
    if "instagram" in lower or " ig " in lower:
        platforms.append("instagram")
    if "twitter" in lower or " x " in lower or "tweet" in lower:
        platforms.append("twitter")
    if "facebook" in lower:
        platforms.append("facebook")
    if "youtube" in lower:
        platforms.append("youtube")
    return platforms


# ══════════════════════════════════════════════════════════════════════════════
# TONE EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════

def _extract_tone(lower: str) -> str:
    if any(w in lower for w in ["funny", "humor", "meme", "sarcastic", "witty", "playful"]):
        return "funny"
    if any(w in lower for w in ["bold", "savage", "controversial", "hot take", "direct", "startup vibe", "startup energy"]):
        return "bold"
    if any(w in lower for w in ["emotional", "story", "vulnerable", "personal", "honest", "raw"]):
        return "emotional"
    if any(w in lower for w in ["educational", "tips", "how to", "guide", "learn", "teach"]):
        return "educational"
    if any(w in lower for w in ["professional", "corporate", "formal", "authoritative"]):
        return "professional"
    if any(w in lower for w in ["motivational", "inspire", "energetic", "uplifting"]):
        return "inspirational"
    if any(w in lower for w in ["curious", "mysterious", "intrigue", "hook"]):
        return "curiosity"
    return "default"


# ══════════════════════════════════════════════════════════════════════════════
# LENGTH EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════

def _extract_length(lower: str) -> str:
    if any(w in lower for w in ["short", "quick", "brief", "one line", "1 line", "concise"]):
        return "short"
    if any(w in lower for w in ["thread", "series", "breakdown", "multi part"]):
        return "thread"
    if any(w in lower for w in ["long", "detailed", "deep", "comprehensive", "in depth"]):
        return "long"
    return "default"


# ══════════════════════════════════════════════════════════════════════════════
# NICHE EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════

def _extract_niche(lower: str) -> str:
    niche_map = [
        ("resume", "career"), ("job", "career"), ("career", "career"), ("hiring", "career"),
        ("ai", "ai"), ("machine learning", "ai"), ("llm", "ai"), ("chatgpt", "ai"),
        ("saas", "saas"), ("software", "saas"),
        ("startup", "startup"), ("founder", "startup"), ("venture", "startup"),
        ("fitness", "fitness"), ("gym", "fitness"), ("health", "fitness"), ("workout", "fitness"),
        ("finance", "finance"), ("invest", "finance"), ("money", "finance"), ("wealth", "finance"),
        ("fashion", "fashion"), ("style", "fashion"), ("clothing", "fashion"),
        ("food", "food"), ("restaurant", "food"), ("recipe", "food"),
        ("course", "education"), ("learn", "education"), ("skill", "education"),
        ("developer", "tech"), ("coding", "tech"), ("programming", "tech"),
        ("marketing", "marketing"), ("growth", "marketing"), ("seo", "marketing"),
    ]
    for kw, niche in niche_map:
        if kw in lower:
            return niche
    return "general"


# ══════════════════════════════════════════════════════════════════════════════
# DURATION EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════

def _extract_duration(lower: str) -> str:
    m = re.search(r'(\d+)\s*(day|week|month|year)s?', lower)
    if m:
        return f"{m.group(1)} {m.group(2)}s"
    return None