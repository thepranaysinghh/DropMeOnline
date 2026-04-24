# intent_parser.py — Structured intent extraction from raw user prompts
# Version 2: adds prompt_mode classification, fixes product name leakage,
# adds deep audience intelligence for tech/career/creator contexts

import re

# ── PROMPT MODE CLASSIFIER ────────────────────────────────────────────────────
# This is the most important addition — determines how content is generated

def classify_mode(lower: str) -> str:
    """
    Returns one of 6 modes:
      product      — user has a product/tool/SaaS/app to promote
      personal     — personal brand, student journey, learning in public
      freelancer   — agency, freelance services, consulting
      career       — job seeker, resume, interview, placement
      creator      — meme pages, viral content, humor, niche topics
      topic        — general topic post, no specific entity
    """
    # Career signals (check before product)
    career_signals = ["job seeker", "looking for job", "i am fresher", "i am a fresher",
                      "placement", "interview prep", "cracking interviews", "getting hired",
                      "job hunt", "no job", "unemployed"]
    if any(s in lower for s in career_signals):
        return "career"

    # Creator/meme signals — check BEFORE product so "meme for my startup" = creator
    creator_signals = ["meme", "viral content", "funny content", "humor content",
                        "niche page", "content creator", "grow my page",
                        "instagram page", "twitter page", "reels content",
                        "make content about", "meme content", "meme page"]
    if any(s in lower for s in creator_signals):
        return "creator"

    # Product signals — "my X" where X is something buildable
    product_signals = ["my app", "my tool", "my saas", "my product", "my startup",
                       "my platform", "my software", "my service", "my agency",
                       "our product", "our app", "our startup", "i built", "i made",
                       "i created", "we built", "we launched", "launching my",
                       "promote my", "grow my", "market my"]
    if any(s in lower for s in product_signals):
        return "product"

    # Freelancer/agency — even "a post about freelancing" = freelancer mode
    if any(w in lower for w in ["freelanc", "agency", "consulting", "client", "services",
                                  "hire me", "web design", "copywriter", "designer",
                                  "freelance mistakes", "freelancing tips", "freelancing errors"]):
        return "freelancer"

    # Personal brand / student journey
    personal_signals = ["i am a", "i am an", "i'm a", "i'm an", "personal brand",
                         "my journey", "learning", "studying", "i study", "i work at",
                         "building my brand", "sharing my", "document"]
    if any(s in lower for s in personal_signals):
        return "personal"

    # Creator / meme / viral
    creator_signals = ["meme", "viral", "funny content", "humor", "niche page",
                        "content creator", "grow my page", "instagram page",
                        "twitter page", "reels", "make content about"]
    if any(s in lower for s in creator_signals):
        return "creator"

    # Topic post (no entity, just a subject)
    # These are "give me a post about X" style
    topic_signals = ["give me", "write me", "create a post", "generate a post",
                     "post about", "content about", "tweet about", "a post on"]
    if any(s in lower for s in topic_signals):
        return "topic"

    # Default: if there's a product keyword, treat as product
    if any(w in lower for w in ["tool", "app", "saas", "platform", "product", "startup",
                                  "software", "course", "newsletter"]):
        return "product"

    return "topic"


# ── MAIN PARSER ───────────────────────────────────────────────────────────────

def parse_intent(goal: str) -> dict:
    text  = goal.strip()
    lower = text.lower()

    mode        = classify_mode(lower)
    niche       = _extract_niche(lower)
    audience    = _extract_audience(lower, mode, niche)
    platforms   = _extract_platforms(lower)
    tone        = _extract_tone(lower)
    length      = _extract_length(lower)
    duration    = _extract_duration(lower)

    # Product/entity extraction depends on mode
    if mode == "product":
        product     = _extract_product(text, lower)
        product_ref = _short_ref(product)
        subject     = product       # what we're talking about
        subject_ref = product_ref
    elif mode == "personal":
        subject     = _extract_personal_identity(lower)
        subject_ref = "you"
        product     = subject
        product_ref = subject_ref
    elif mode == "freelancer":
        subject     = _extract_freelancer_entity(lower)
        subject_ref = "your services"
        product     = subject
        product_ref = subject_ref
    elif mode == "career":
        subject     = "your career journey"
        subject_ref = "this"
        product     = subject
        product_ref = subject_ref
    elif mode == "creator":
        subject     = _extract_creator_topic(lower)
        subject_ref = "this"
        product     = subject
        product_ref = subject_ref
    else:  # topic
        subject     = _extract_topic(lower)
        subject_ref = "this"
        product     = subject
        product_ref = subject_ref

    action = _extract_action(lower, subject, mode)

    return {
        "mode":        mode,
        "product":     product,
        "product_ref": product_ref,
        "subject":     subject,
        "subject_ref": subject_ref,
        "action":      action,
        "audience":    audience,
        "platforms":   platforms,
        "tone":        tone,
        "length":      length,
        "niche":       niche,
        "duration":    duration,
        "raw":         text,
    }


# ── PRODUCT EXTRACTOR ─────────────────────────────────────────────────────────

def _extract_product(text: str, lower: str) -> str:
    # Quoted name first
    quoted = re.search(r'["\']([A-Za-z0-9 ]{2,30})["\']', text)
    if quoted:
        return _fix_case(quoted.group(1).strip().title())

    # "my X" — extract cleanly
    my_match = re.search(
        r'\bmy\s+((?:ai\s+|saas\s+|new\s+|online\s+)?[a-z]+(?:\s+[a-z]+){0,3})',
        lower
    )
    if my_match:
        raw = my_match.group(1).strip()
        noise = {
            "on","for","with","using","to","and","in","at","the","a","an",
            "linkedin","instagram","twitter","facebook","youtube","tiktok",
            "about","through","via","across","bold","startup","vibe",
            "fast","quick","free","paid","new","best","good","great",
            "page","account","profile","channel",
        }
        words = raw.split()
        while words and words[-1].lower() in noise:
            words.pop()
        while words and words[0].lower() in {"my","the","a","an","our"}:
            words.pop(0)
        if words:
            return _fix_case(" ".join(words).title())

    # Known type keywords
    known = [
        ("resume tool", "AI Resume Tool"), ("resume", "Resume Tool"),
        ("cv", "CV Builder"), ("portfolio", "Portfolio Builder"),
        ("chatbot", "AI Chatbot"), ("saas", "SaaS Product"),
        ("web app", "Web App"), ("mobile app", "Mobile App"),
        ("app", "App"), ("course", "Online Course"),
        ("newsletter", "Newsletter"), ("agency", "Agency"),
        ("store", "Online Store"), ("shop", "Shop"),
        ("blog", "Blog"), ("startup", "Startup"),
        ("platform", "Platform"), ("tool", "Tool"),
        ("service", "Service"), ("brand", "Brand"),
    ]
    for kw, label in known:
        if kw in lower:
            # Prepend adjective if present
            m = re.search(rf'((?:ai|smart|free|premium|online|digital|modern)\s+){re.escape(kw)}', lower)
            if m:
                return _fix_case((m.group(1) + label.split()[-1]).title())
            return label

    return "the product"


def _fix_case(s: str) -> str:
    for bad, good in [("Ai ","AI "),("Ai\n","AI\n"),("Saas","SaaS"),
                      ("Llm","LLM"),("Seo","SEO"),("Devops","DevOps"),
                      ("Aws","AWS"),("Gcp","GCP"),("Ui ","UI "),("Ux ","UX ")]:
        s = s.replace(bad, good)
    return s


def _short_ref(product: str) -> str:
    lower = product.lower()
    if any(w in lower for w in ["app","tool","builder","bot","ai"]):  return "the tool"
    if any(w in lower for w in ["platform","saas","software"]):        return "the platform"
    if any(w in lower for w in ["course","program","training"]):       return "the course"
    if any(w in lower for w in ["store","shop"]):                      return "the store"
    if any(w in lower for w in ["newsletter","blog"]):                 return "the newsletter"
    if any(w in lower for w in ["agency","service","studio"]):        return "the agency"
    if any(w in lower for w in ["brand","startup","company"]):         return "the brand"
    return product if len(product) <= 20 else "this"


# ── PERSONAL / FREELANCER / CREATOR / TOPIC EXTRACTORS ───────────────────────

def _extract_personal_identity(lower: str) -> str:
    patterns = [
        (r"i(?:'m| am) an? ([a-z]+(?: [a-z]+){0,3})", 1),
        (r"([a-z]+(?: [a-z]+){0,2}) (?:student|engineer|developer|designer|founder|marketer)", 0),
    ]
    for pat, grp in patterns:
        m = re.search(pat, lower)
        if m:
            raw = m.group(0) if grp == 0 else m.group(1)
            raw = re.sub(r'\b(i|am|a|an|the)\b', '', raw).strip()
            if raw:
                return _fix_case(raw.title())
    return "personal brand"


def _extract_freelancer_entity(lower: str) -> str:
    if "agency" in lower: return "the agency"
    if "design" in lower: return "design services"
    if "copywr" in lower: return "copywriting services"
    if "develop" in lower: return "development services"
    return "freelance services"


def _extract_creator_topic(lower: str) -> str:
    # "meme content for X" or "content about X"
    m = re.search(r'(?:about|for|on)\s+([a-z]+(?: [a-z]+){0,3})', lower)
    if m:
        raw = m.group(1).strip()
        noise = {"my","the","a","an","for","on","about","instagram","twitter","linkedin"}
        words = [w for w in raw.split() if w not in noise]
        if words:
            return _fix_case(" ".join(words).title())
    return "niche content"


def _extract_topic(lower: str) -> str:
    # "a post about X" / "give me X content"
    m = re.search(r'(?:about|on|regarding|for)\s+([a-z]+(?: [a-z]+){0,4})', lower)
    if m:
        raw = m.group(1).strip()
        noise = {"me","my","the","a","an","on","in","for","and","or","that","this"}
        words = [w for w in raw.split() if w not in noise]
        if words:
            return _fix_case(" ".join(words[:4]).title())
    # Fallback: meaningful words from prompt
    stop = {"give","write","create","generate","make","need","want","post","content",
            "tweet","linkedin","instagram","twitter","short","long","thread","a","an",
            "the","for","on","in","with","and","or","my","me","us","i"}
    words = [w for w in lower.split() if w not in stop][:4]
    return _fix_case(" ".join(words).title()) if words else "this topic"


# ── AUDIENCE INTELLIGENCE ─────────────────────────────────────────────────────

def _extract_audience(lower: str, mode: str, niche: str) -> str:
    # Explicit audience keywords — checked first
    explicit = [
        # Tech
        ("devops",        "DevOps engineers and cloud professionals"),
        ("cloud",         "cloud and infrastructure engineers"),
        ("kubernetes",    "DevOps and platform engineers"),
        ("aws",           "cloud engineers and architects"),
        ("docker",        "developers and DevOps engineers"),
        ("backend",       "backend developers"),
        ("frontend",      "frontend developers"),
        ("fullstack",     "fullstack developers"),
        ("developer",     "developers and engineers"),
        ("programmer",    "developers and engineers"),
        ("engineer",      "software engineers"),
        ("data science",  "data scientists and ML engineers"),
        ("machine learn", "ML engineers and AI researchers"),
        # Career
        ("fresher",       "college freshers entering the job market"),
        ("fresh grad",    "fresh graduates entering the workforce"),
        ("job seeker",    "active job seekers"),
        ("interview",     "candidates preparing for interviews"),
        ("placement",     "students seeking campus placements"),
        # Business
        ("founder",       "startup founders and entrepreneurs"),
        ("entrepreneur",  "entrepreneurs and early-stage founders"),
        ("freelancer",    "freelancers and independent professionals"),
        ("agency",        "agency owners and creative professionals"),
        ("marketer",      "marketers and growth professionals"),
        ("creator",       "content creators and influencers"),
        # Academic
        ("student",       "students and learners"),
        ("college",       "college students"),
        # Other
        ("fitness",       "fitness enthusiasts and gym-goers"),
        ("investor",      "investors and finance professionals"),
        ("designer",      "designers and creative professionals"),
    ]
    for kw, label in explicit:
        if kw in lower:
            return label

    # Mode-based inference
    if mode == "product":
        # Infer from niche
        niche_audience = {
            "career":    "job seekers and professionals",
            "ai":        "tech-savvy professionals and builders",
            "saas":      "startup founders and product teams",
            "startup":   "founders and early adopters",
            "fitness":   "fitness enthusiasts",
            "finance":   "people building financial independence",
            "education": "learners and skill builders",
            "tech":      "developers and tech professionals",
            "marketing": "marketers and growth teams",
        }
        return niche_audience.get(niche, "professionals and builders")

    if mode == "personal":   return "professionals and peers in your industry"
    if mode == "freelancer": return "potential clients and business owners"
    if mode == "career":     return "recruiters and hiring managers"
    if mode == "creator":    return "your target niche audience"
    return "professionals and curious learners"


# ── NICHE EXTRACTOR ───────────────────────────────────────────────────────────

def _extract_niche(lower: str) -> str:
    niche_map = [
        # Tech niches — more specific first
        ("devops",   "tech"), ("kubernetes", "tech"), ("docker", "tech"),
        ("aws",      "tech"), ("cloud",      "tech"), ("backend", "tech"),
        ("frontend", "tech"), ("developer",  "tech"), ("coding", "tech"),
        ("programming","tech"),("software",  "tech"),
        # AI
        ("machine learning","ai"),("deep learning","ai"),("llm","ai"),
        ("chatgpt","ai"),("openai","ai"),("ai ","ai"),
        # Career
        ("resume","career"),("job","career"),("interview","career"),
        ("hiring","career"),("career","career"),("placement","career"),
        ("fresher","career"),
        # Startup/SaaS
        ("saas","saas"),("startup","startup"),("founder","startup"),
        # Other
        ("fitness","fitness"),("gym","fitness"),("workout","fitness"),
        ("finance","finance"),("invest","finance"),("money","finance"),
        ("fashion","fashion"),("food","food"),("restaurant","food"),
        ("course","education"),("learn","education"),("skill","education"),
        ("marketing","marketing"),("freelanc","freelancer"),
    ]
    for kw, niche in niche_map:
        if kw in lower:
            return niche
    return "general"


# ── OTHER EXTRACTORS ──────────────────────────────────────────────────────────

def _extract_platforms(lower: str) -> list:
    out = []
    if "linkedin" in lower:          out.append("linkedin")
    if "instagram" in lower or " ig " in lower: out.append("instagram")
    if "twitter" in lower or "tweet" in lower:  out.append("twitter")
    if "facebook" in lower:          out.append("facebook")
    return out


def _extract_tone(lower: str) -> str:
    if any(w in lower for w in ["funny","humor","meme","sarcastic","witty","playful","lol"]):
        return "funny"
    if any(w in lower for w in ["controversial","bold","savage","hot take","unpopular",
                                  "direct","harsh","brutal","startup vibe","gets reach","get reach"]):
        return "bold"
    if any(w in lower for w in ["emotional","story","vulnerable","personal","honest","raw"]):
        return "emotional"
    if any(w in lower for w in ["educational","tips","how to","guide","teach","explain",
                                  "mistakes","lessons","breakdown","errors","avoid"]):
        return "educational"
    if any(w in lower for w in ["professional","formal","authoritative","corporate"]):
        return "professional"
    if any(w in lower for w in ["motivational","inspire","energetic","uplifting"]):
        return "inspirational"
    return "default"


def _extract_length(lower: str) -> str:
    # Thread wins over short — "short thread" means a brief thread, not a one-liner
    if any(w in lower for w in ["thread","series","numbered list"]):
        return "thread"
    if any(w in lower for w in ["short","quick","brief","one line","concise","single"]):
        return "short"
    if any(w in lower for w in ["long","detailed","deep","comprehensive","in depth"]):
        return "long"
    return "default"


def _extract_action(lower: str, subject: str, mode: str) -> str:
    if any(w in lower for w in ["launch","launching","just launched"]):
        return f"launch {subject}"
    if re.search(r'\d+\s*users?', lower):
        m = re.search(r'(\d+)\s*users?', lower)
        return f"get {m.group(1)} users"
    if any(w in lower for w in ["viral","go viral"]):
        return f"go viral with {subject}"
    if mode == "career":    return "get noticed by recruiters"
    if mode == "personal":  return "build authority and following"
    if mode == "freelancer":return "attract new clients"
    if mode == "creator":   return "grow the page"
    return f"grow with {subject}"


def _extract_duration(lower: str):
    m = re.search(r'(\d+)\s*(day|week|month|year)s?', lower)
    return f"{m.group(1)} {m.group(2)}s" if m else None