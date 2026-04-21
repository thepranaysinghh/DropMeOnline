# orchestrator_engine.py — Central Coordination Layer
# Acts as Product Manager + Strategist across all DropMeOnline engines
# Decides which engines matter, locks tone, prevents conflicts, gives execution direction

def orchestrate(goal: str, prompt_data: dict) -> dict:
    """
    Input:
        goal        — e.g. "Grow LinkedIn for AI resume tool targeting freshers"
        prompt_data — output from prompt_brain.understand_prompt()
    Output:
        Full orchestration plan with engine priorities, strategy, tone lock, actions
    """

    text      = goal.lower()
    product   = prompt_data.get("product", "Unknown Product")
    audience  = prompt_data.get("audience", "general audience")
    platforms = prompt_data.get("platforms") or prompt_data.get("suggested_platforms", ["linkedin"])
    budget    = prompt_data.get("budget", "Unknown")
    goal_type = prompt_data.get("goal", "Grow brand awareness")

    # --- Intelligence layers ---
    phase             = _detect_phase(text, goal_type)
    priority_engine   = _pick_priority_engine(phase, text, budget)
    recommended_plat  = _recommend_platform(platforms, text, audience)
    tone_lock         = _lock_tone(audience, platforms, text)
    content_strategy  = _build_strategy(phase, product, audience, goal_type, tone_lock)
    final_focus       = _build_focus(phase, product, recommended_plat, goal_type)
    quality_checks    = _build_quality_checks(tone_lock, platforms, product, audience)
    next_actions      = _build_next_actions(phase, platforms, product, budget, priority_engine)

    return {
        "priority_engine":      priority_engine,
        "content_strategy":     content_strategy,
        "recommended_platform": recommended_plat,
        "tone_lock":            tone_lock,
        "final_focus":          final_focus,
        "quality_checks":       quality_checks,
        "next_actions":         next_actions,
    }


# ══════════════════════════════════════════════════════════════════════════════
# PHASE DETECTOR — where is this product in its lifecycle?
# ══════════════════════════════════════════════════════════════════════════════

def _detect_phase(text: str, goal_type: str) -> str:
    g = goal_type.lower()

    if any(w in text for w in ["launch", "new", "just built", "starting", "day 1"]):
        return "launch"
    if any(w in text for w in ["grow", "followers", "users", "reach", "audience"]):
        return "growth"
    if any(w in text for w in ["convert", "sale", "revenue", "customer", "buy", "signup"]):
        return "conversion"
    if any(w in text for w in ["brand", "authority", "awareness", "visibility", "known"]):
        return "awareness"
    if any(w in g for w in ["get", "gain", "close", "viral"]):
        return "growth"

    return "awareness"  # Safe default


# ══════════════════════════════════════════════════════════════════════════════
# PRIORITY ENGINE SELECTOR
# ══════════════════════════════════════════════════════════════════════════════

def _pick_priority_engine(phase: str, text: str, budget: str) -> str:
    is_zero_budget = "zero" in budget.lower() or "free" in budget.lower()

    priority_map = {
        "launch":     "mastermind_engine → autopilot_content_engine → campaign_engine",
        "growth":     "autopilot_content_engine → competitor_engine → distribution_engine",
        "conversion": "conversion_engine → mastermind_engine → publishing_engine",
        "awareness":  "competitor_engine → autopilot_content_engine → visual_engine",
    }

    base = priority_map.get(phase, priority_map["awareness"])

    if is_zero_budget:
        return f"{base} [Zero budget mode: organic-first, no paid amplification]"

    return base


# ══════════════════════════════════════════════════════════════════════════════
# PLATFORM RECOMMENDER
# ══════════════════════════════════════════════════════════════════════════════

def _recommend_platform(platforms: list, text: str, audience: str) -> str:
    a = audience.lower()

    # If user specified platforms, pick the best one to lead
    if platforms:
        # Score each platform by fit
        scores = {}
        for p in platforms:
            scores[p] = 0
            if p == "linkedin" and any(w in a for w in ["professional", "fresher", "developer", "founder"]):
                scores[p] += 3
            if p == "instagram" and any(w in a for w in ["student", "creator", "fashion", "fitness"]):
                scores[p] += 3
            if p == "twitter" and any(w in text for w in ["ai", "tech", "startup", "saas"]):
                scores[p] += 2
            if p == "facebook" and any(w in a for w in ["business", "local", "community"]):
                scores[p] += 2

        best = max(scores, key=scores.get)
        others = [p for p in platforms if p != best]
        support = f" (supporting: {', '.join(others)})" if others else ""
        return f"{best}{support}"

    # Fallback suggestion by audience
    if any(w in a for w in ["fresher", "student", "professional", "developer"]):
        return "linkedin (primary) + instagram (secondary)"
    if any(w in a for w in ["creator", "fashion", "fitness"]):
        return "instagram (primary) + twitter (secondary)"
    if any(w in text for w in ["ai", "tech", "saas", "startup"]):
        return "linkedin (primary) + twitter (secondary)"

    return "linkedin (primary) + instagram (secondary)"


# ══════════════════════════════════════════════════════════════════════════════
# TONE LOCK — one consistent voice across all engines
# ══════════════════════════════════════════════════════════════════════════════

def _lock_tone(audience: str, platforms: list, text: str) -> str:
    a = audience.lower()
    p = [pl.lower() for pl in platforms]

    # Audience-first tone decision
    if any(w in a for w in ["fresher", "student"]):
        base = "Honest + peer-level — no corporate speak, no toxic positivity"
    elif any(w in a for w in ["founder", "entrepreneur"]):
        base = "Builder-to-builder — direct, experienced, zero fluff"
    elif any(w in a for w in ["professional", "executive"]):
        base = "Quietly authoritative — intelligent without being arrogant"
    elif any(w in a for w in ["developer", "programmer"]):
        base = "Technically credible + dry wit — earns trust through specificity"
    elif any(w in a for w in ["creator", "gen z"]):
        base = "Relatable + sharp — meme-aware but substance-first"
    else:
        base = "Clear + human — smart without showing off"

    # Platform modifier
    if "twitter" in p and len(p) == 1:
        base += " | Twitter mode: sharper, bolder, shorter"
    elif "instagram" in p and "linkedin" not in p:
        base += " | Instagram mode: more visual, more casual, more energy"

    return base


# ══════════════════════════════════════════════════════════════════════════════
# CONTENT STRATEGY BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def _build_strategy(phase: str, product: str, audience: str, goal_type: str, tone: str) -> str:
    strategies = {
        "launch": (
            f"Phase: Launch. "
            f"Lead with founder story + problem framing for {product}. "
            f"First 7 days = introduce the problem that {audience} faces, not the product. "
            f"Let {audience} say 'this is me' before you show the solution. "
            f"Tone anchored at: {tone}."
        ),
        "growth": (
            f"Phase: Growth. "
            f"Content mix for {product}: 40% educational (builds trust), "
            f"30% story/proof (builds belief), 20% opinion (builds following), 10% direct CTA. "
            f"Consistency beats virality at this stage. "
            f"Post daily on primary platform. Every post optimised for saves + shares. "
            f"Tone anchored at: {tone}."
        ),
        "conversion": (
            f"Phase: Conversion. "
            f"Shift from building audience to activating it. "
            f"{product} content should lead with outcomes, not features. "
            f"Use urgency sparingly — earned urgency only (results, limits, timing). "
            f"Every post should have one clear action. "
            f"Tone anchored at: {tone}."
        ),
        "awareness": (
            f"Phase: Awareness. "
            f"Goal is for {audience} to encounter {product} repeatedly across contexts. "
            f"Prioritise reach over depth. "
            f"Hook quality matters more than post length at this stage. "
            f"Trend-riding + niche positioning = fastest awareness growth. "
            f"Tone anchored at: {tone}."
        ),
    }
    return strategies.get(phase, strategies["awareness"])


# ══════════════════════════════════════════════════════════════════════════════
# FINAL FOCUS
# ══════════════════════════════════════════════════════════════════════════════

def _build_focus(phase: str, product: str, platform: str, goal_type: str) -> str:
    focus_map = {
        "launch":     f"Make {audience_placeholder(product)} feel understood before they feel sold to. Story first, product second.",
        "growth":     f"Daily presence on {platform}. Volume + quality. Every post earns the follow.",
        "conversion": f"One CTA per post. Zero friction to try {product}. Remove every reason to hesitate.",
        "awareness":  f"Be unavoidable in your niche. Show up in conversations, trends, and searches around {product}.",
    }
    return focus_map.get(phase, f"Stay consistent. Build trust. Let {product} speak through results.")

def audience_placeholder(product: str) -> str:
    return f"your target audience for {product}"


# ══════════════════════════════════════════════════════════════════════════════
# QUALITY CHECKS
# ══════════════════════════════════════════════════════════════════════════════

def _build_quality_checks(tone: str, platforms: list, product: str, audience: str) -> list:
    checks = [
        f"Tone consistency: every post must feel like it was written by the same person — anchored at '{tone}'",
        f"No duplicate hooks: autopilot_content_engine history list must be passed on every call",
        f"Platform-native check: LinkedIn posts must not sound like Instagram captions and vice versa",
        f"CTA sanity: one action per post maximum — never stack multiple CTAs",
        f"Audience mirror: before publishing, confirm the post speaks to {audience} specifically — not 'everyone'",
        f"Product mention rule: {product} should be referenced naturally, not forced into every post",
        f"Hook freshness: run avoid_repeat_score check — never publish below 50",
        f"Length check: LinkedIn max 1500 chars, Instagram caption max 2200, Twitter max 280",
    ]
    if "instagram" in [p.lower() for p in platforms]:
        checks.append("Instagram visual check: every post needs a matching image brief from visual_engine")
    if "twitter" in [p.lower() for p in platforms]:
        checks.append("Twitter sharpness check: if it needs more than 3 seconds to understand, rewrite it")
    return checks


# ══════════════════════════════════════════════════════════════════════════════
# NEXT ACTIONS
# ══════════════════════════════════════════════════════════════════════════════

def _build_next_actions(phase: str, platforms: list, product: str,
                         budget: str, priority_engine: str) -> list:
    actions = []

    # Phase-specific first action
    phase_actions = {
        "launch":     f"Run mastermind_engine.build_mastermind() with full prompt_data for {product} — set the strategic foundation first",
        "growth":     f"Run autopilot_content_engine.generate_autopilot_content() for today's post on primary platform",
        "conversion": f"Run conversion_engine.generate_conversion_assets('{product}') — extract best CTA and urgency lines",
        "awareness":  f"Run competitor_engine.analyze_market() to find positioning gaps before creating any content",
    }
    actions.append(phase_actions.get(phase, f"Define core angle for {product} using mastermind_engine"))

    # Platform-specific actions
    for p in platforms[:2]:  # Max 2 platforms to keep it focused
        p = p.lower()
        if p == "linkedin":
            actions.append("LinkedIn: Generate 7-day content calendar using campaign_engine — mix educational, story, opinion")
        elif p == "instagram":
            actions.append("Instagram: Generate visual brief using visual_engine — lead with Reels for reach")
        elif p == "twitter":
            actions.append("Twitter: Prepare 3 hot takes using autopilot_content_engine — controversial mood, sharp style")
        elif p == "facebook":
            actions.append("Facebook: Build community post using campaign_engine — question format, high comment intent")

    # Budget-aware action
    is_zero = "zero" in budget.lower() or "free" in budget.lower()
    if is_zero:
        actions.append("Zero budget mode: prioritise organic reach tactics — commenting on viral posts, SEO hooks, share-bait content")
    else:
        actions.append("Budget available: consider amplifying top-performing organic post with minimal paid boost after day 3")

    # Universal final action
    actions.append(f"After first 7 days: run feedback_engine.analyze_feedback() to let the AI adapt strategy based on real results")

    return actions