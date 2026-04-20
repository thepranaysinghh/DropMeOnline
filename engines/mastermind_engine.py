# mastermind_engine.py — Central Intelligence Layer
# Builds the strategic marketing brain for any product + audience combination

def build_mastermind(goal: str, prompt_data: dict) -> dict:
    """
    Input:
        goal        — e.g. "Promote AI resume tool on LinkedIn for freshers"
        prompt_data — { "product": "...", "platforms": [...], "audience": "..." }
    Output:
        Full strategic intelligence package for content and marketing
    """

    product   = prompt_data.get("product", goal)
    platforms = prompt_data.get("platforms", ["linkedin"])
    audience  = prompt_data.get("audience", "general")

    text = f"{goal} {product} {audience}".lower()

    # --- Core intelligence layers ---
    pain_point         = _detect_pain(text, audience)
    psychology_trigger = _detect_trigger(text, audience)
    hook_style         = _detect_hook_style(platforms)
    tone               = _detect_tone(platforms, audience)
    humour_style       = _detect_humour(audience, text)
    cta_style          = _detect_cta(psychology_trigger)
    core_angle         = _build_angle(product, audience, pain_point)
    content_direction  = _build_content_direction(platforms, psychology_trigger)
    offer_positioning  = _build_positioning(product, psychology_trigger)
    trust_builder      = _build_trust(product, audience)
    top_hooks          = _generate_hooks(product, audience, pain_point, psychology_trigger, platforms)

    return {
        "core_angle":          core_angle,
        "psychology_trigger":  psychology_trigger,
        "hook_style":          hook_style,
        "top_hooks":           top_hooks,
        "tone":                tone,
        "humour_style":        humour_style,
        "cta_style":           cta_style,
        "content_direction":   content_direction,
        "offer_positioning":   offer_positioning,
        "trust_builder":       trust_builder,
    }


# ── Pain point detector ────────────────────────────────────────────────────────

def _detect_pain(text: str, audience: str) -> str:
    audience = audience.lower()

    if any(w in audience for w in ["fresher", "student", "graduate"]):
        return "No experience, no callbacks, rejection loop"
    if any(w in audience for w in ["developer", "programmer", "engineer"]):
        return "Too busy to market themselves, undervalued despite skills"
    if any(w in audience for w in ["entrepreneur", "founder", "startup"]):
        return "No time, no budget, no marketing team"
    if any(w in audience for w in ["freelancer", "creator"]):
        return "Inconsistent income, hard to stand out in a crowded market"
    if any(w in audience for w in ["professional", "working"]):
        return "Stuck in a role, invisible on LinkedIn, no personal brand"
    if any(w in text for w in ["fitness", "health", "gym"]):
        return "Started strong but lost motivation, no visible results"
    if any(w in text for w in ["finance", "money", "invest"]):
        return "Earning but not growing wealth, confused by options"
    if any(w in text for w in ["fashion", "style"]):
        return "Want to look good but don't know how or can't afford it"
    if any(w in text for w in ["food", "restaurant"]):
        return "No time to cook, eating out is expensive and unhealthy"

    return "Wasting time on manual, inefficient approaches"


# ── Psychology trigger detector ────────────────────────────────────────────────

def _detect_trigger(text: str, audience: str) -> str:
    audience = audience.lower()

    if any(w in audience for w in ["fresher", "student"]):
        return "fear"           # Fear of unemployment, rejection
    if any(w in audience for w in ["entrepreneur", "founder"]):
        return "speed"          # Fast results with limited resources
    if any(w in audience for w in ["professional"]):
        return "status"         # Be seen as an expert, grow influence
    if any(w in audience for w in ["freelancer", "creator"]):
        return "greed"          # More clients, more income
    if any(w in text for w in ["free", "easy", "simple", "quick"]):
        return "relief"         # Finally, something that just works
    if any(w in text for w in ["secret", "nobody", "hidden", "truth"]):
        return "curiosity"
    if any(w in text for w in ["community", "together", "join"]):
        return "belonging"

    return "curiosity"          # Default: curiosity always works


# ── Hook style by platform ─────────────────────────────────────────────────────

def _detect_hook_style(platforms: list) -> str:
    styles = []
    for p in platforms:
        p = p.lower()
        if p == "linkedin":
            styles.append("LinkedIn: authority opener + personal story")
        elif p == "instagram":
            styles.append("Instagram: pattern interrupt + meme energy")
        elif p == "twitter":
            styles.append("Twitter: hot take + one-liner controversy")
        elif p == "facebook":
            styles.append("Facebook: emotional story + community angle")
    return " | ".join(styles) if styles else "Curiosity-driven hook across platforms"


# ── Tone detector ──────────────────────────────────────────────────────────────

def _detect_tone(platforms: list, audience: str) -> str:
    audience = audience.lower()
    platforms = [p.lower() for p in platforms]

    if "linkedin" in platforms and any(w in audience for w in ["professional", "founder", "executive"]):
        return "Authoritative, thoughtful, quietly confident"
    if "instagram" in platforms and any(w in audience for w in ["student", "fresher", "creator"]):
        return "Casual, relatable, energetic, Gen Z-aware"
    if "twitter" in platforms:
        return "Sharp, direct, opinionated, zero fluff"
    if any(w in audience for w in ["fresher", "student"]):
        return "Supportive, honest, peer-like — not corporate"

    return "Professional but human — intelligent without being boring"


# ── Humour style ───────────────────────────────────────────────────────────────

def _detect_humour(audience: str, text: str) -> str:
    audience = audience.lower()

    if any(w in audience for w in ["student", "fresher", "gen z", "creator"]):
        return "Meme-aware, self-deprecating, relatable fail humour"
    if any(w in audience for w in ["developer", "programmer"]):
        return "Dry wit, tech in-jokes, mild sarcasm"
    if any(w in audience for w in ["founder", "entrepreneur"]):
        return "Startup struggle humour — 'we've all been there' energy"
    if any(w in text for w in ["finance", "money"]):
        return "Dark humour about broke life, aspirational twist"

    return "Light, self-aware — never try-hard or forced"


# ── CTA style by trigger ───────────────────────────────────────────────────────

def _detect_cta(trigger: str) -> str:
    cta_map = {
        "fear":       "Soft urgency CTA — 'Don't let this be you. Try it free today.'",
        "greed":      "Value-first CTA — 'Start free. Upgrade when you're ready.'",
        "status":     "Aspiration CTA — 'Join people who take their brand seriously.'",
        "speed":      "Fast result CTA — 'Set it up in 5 minutes. Results in 7 days.'",
        "relief":     "Ease CTA — 'Finally, something that just works. Try it now.'",
        "curiosity":  "Tease CTA — 'See what everyone's been asking about. Link in bio.'",
        "belonging":  "Community CTA — 'Join 500+ people already using this. You're next.'",
    }
    return cta_map.get(trigger, "Try it free — no credit card needed.")


# ── Core angle builder ─────────────────────────────────────────────────────────

def _build_angle(product: str, audience: str, pain: str) -> str:
    return (
        f"{product} exists because {audience} are tired of: {pain}. "
        f"The angle is empathy-first — acknowledge the struggle, then present the solution "
        f"as obvious and accessible. Position it as the thing they should have found sooner."
    )


# ── Content direction ──────────────────────────────────────────────────────────

def _build_content_direction(platforms: list, trigger: str) -> str:
    directions = []
    for p in platforms:
        p = p.lower()
        if p == "linkedin":
            directions.append("LinkedIn: Mix of personal stories (40%), insights (40%), product posts (20%)")
        elif p == "instagram":
            directions.append("Instagram: Reels for reach, carousels for saves, memes for shares")
        elif p == "twitter":
            directions.append("Twitter: Hot takes + threads + replies to larger accounts")
        elif p == "facebook":
            directions.append("Facebook: Community posts + emotional stories + group engagement")

    base = " | ".join(directions) if directions else "Educational + Story mix"
    return f"{base}. Core trigger throughout: {trigger}."


# ── Offer positioning ──────────────────────────────────────────────────────────

def _build_positioning(product: str, trigger: str) -> str:
    positioning_map = {
        "fear":      f"{product} = the safety net they didn't know they needed. Lead with risk of NOT using it.",
        "greed":     f"{product} = more results, less effort. Show the ROI clearly and early.",
        "status":    f"{product} = what serious people use. Position as elite, not average.",
        "speed":     f"{product} = fastest path from problem to result. Time saved is the hero.",
        "relief":    f"{product} = finally, something that makes sense. Simplicity is the USP.",
        "curiosity": f"{product} = the thing everyone's been asking about. Mystery drives clicks.",
        "belonging": f"{product} = what the smart community already uses. FOMO is the hook.",
    }
    return positioning_map.get(trigger, f"{product} = the obvious solution to an obvious problem.")


# ── Trust builder ──────────────────────────────────────────────────────────────

def _build_trust(product: str, audience: str) -> str:
    return (
        f"Build trust with {audience} by: "
        f"(1) Showing real use cases, not just features. "
        f"(2) Using their exact language and frustrations in copy. "
        f"(3) Sharing the story of why {product} was built — founder authenticity. "
        f"(4) Giving real value for free before asking for anything. "
        f"(5) Social proof — early users, results, testimonials."
    )


# ── Top hook generator ─────────────────────────────────────────────────────────

def _generate_hooks(product: str, audience: str, pain: str, trigger: str, platforms: list) -> list:
    hooks = [
        # Fear-based
        f"Most {audience} will never fix '{pain}'. Here's the 1% that did.",
        f"If you're still dealing with {pain}, you haven't found {product} yet.",

        # Curiosity-based
        f"Nobody talks about why {pain} keeps happening to {audience}. Until now.",
        f"I found the reason {audience} struggle with {pain}. It's not what you think.",

        # Story-based
        f"6 months ago I was stuck in {pain}. Then I built {product}. Here's what changed.",
        f"I was tired of {pain}. So I stopped complaining and built {product}.",

        # Authority / Status
        f"The top-performing {audience} don't fight {pain}. They use tools like {product}.",
        f"Here's what {audience} who actually succeed have in common. Hint: it's not talent.",

        # Speed / Relief
        f"{product} does in 5 minutes what used to take {audience} hours.",
        f"Stop doing {pain} the hard way. {product} exists now.",
    ]
    return hooks