# trend_radar_engine.py — Trend Radar Engine
# Simulates a smart strategist scanning what's hot right now
# Platform-aware, niche-specific, audience-matched

from datetime import datetime
import random

def scan_trends(goal: str, niche: str, audience: str, platform: str) -> dict:
    """
    Input:
        goal     — e.g. "Promote AI resume tool"
        niche    — e.g. "career + AI"
        audience — e.g. "freshers"
        platform — "linkedin" | "instagram" | "twitter" | "facebook"
    Output:
        Trend intelligence package with hot topics, opportunities, angles, avoids
    """

    text     = f"{goal} {niche} {audience}".lower()
    platform = platform.lower().strip()
    detected = _detect_niche(text)

    hot_topics    = _get_hot_topics(detected, platform)
    opportunities = _get_opportunities(detected, platform, audience, goal)
    angles        = _get_angles(detected, platform, audience)
    avoid         = _get_avoid(detected, platform)
    best_topic    = _pick_best_topic(hot_topics, detected, platform)
    why_now       = _build_why_now(best_topic, detected, platform)

    return {
        "hot_topics":           hot_topics,
        "content_opportunities": opportunities,
        "angles_to_use":        angles,
        "avoid_topics":         avoid,
        "best_topic_today":     best_topic,
        "why_now":              why_now,
    }


# ══════════════════════════════════════════════════════════════════════════════
# NICHE DETECTOR
# ══════════════════════════════════════════════════════════════════════════════

def _detect_niche(text: str) -> str:
    niches = {
        "ai_career":  ["resume", "job", "hiring", "career", "linkedin", "fresher", "placement"],
        "ai_tech":    ["ai", "chatgpt", "llm", "automation", "saas", "tool", "developer", "build"],
        "fitness":    ["fitness", "workout", "gym", "health", "nutrition", "weight"],
        "finance":    ["finance", "invest", "money", "income", "wealth", "trading", "stock"],
        "education":  ["course", "learn", "skill", "tutorial", "education", "study"],
        "creator":    ["creator", "content", "youtube", "followers", "brand", "influencer"],
        "startup":    ["startup", "founder", "entrepreneur", "product", "launch", "mvp"],
        "fashion":    ["fashion", "style", "clothing", "outfit", "trend", "aesthetic"],
    }
    scores = {n: 0 for n in niches}
    for n, keywords in niches.items():
        for kw in keywords:
            if kw in text:
                scores[n] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"


# ══════════════════════════════════════════════════════════════════════════════
# HOT TOPICS — niche + platform specific
# ══════════════════════════════════════════════════════════════════════════════

TOPIC_BANK = {

    "ai_career": {
        "linkedin": [
            "AI is changing what hiring managers look for — and most candidates don't know it yet",
            "LinkedIn profiles that use AI optimization are getting 3x more profile views",
            "The 'perfect resume' is dead — here's what's replacing it",
            "Freshers who show AI literacy are jumping the queue in hiring pipelines",
            "Remote jobs vs in-office: the real numbers in 2025",
            "Why your LinkedIn summary is the most important thing you've never optimized",
            "The hidden ATS filters that reject 75% of applications before a human sees them",
        ],
        "instagram": [
            "Job rejection era → career glow-up arc — people are obsessed with this narrative",
            "POV: you finally found the tool that fixes your entire job search",
            "The LinkedIn profile audit trend is blowing up — everyone wants to know their score",
            "Career anxiety content is getting record saves and DMs right now",
            "Side hustles from home are trending harder than ever among students",
        ],
        "twitter": [
            "The job market feels broken because it kind of is — and AI is making it weirder",
            "Hot take: the best candidates aren't applying on job boards anymore",
            "ATS systems are filtering out great candidates and nobody talks about it enough",
            "LinkedIn is becoming less about connections and more about content — shift accordingly",
            "Freshers who build in public are outpacing MBAs in hiring pipelines",
        ],
    },

    "ai_tech": {
        "linkedin": [
            "AI tool fatigue is real — the ones that survive are solving actual problems",
            "Founders who build in public are seeing 10x the organic reach of those who don't",
            "The SaaS graveyard is full of products that launched without an audience",
            "GPT-4o, Claude, Gemini — the real differentiator is now UX, not intelligence",
            "Developer-led marketing is outperforming traditional growth in 2025",
        ],
        "instagram": [
            "AI tools that went viral this week — and what made them different",
            "The 'I built this in a weekend' trend is dominating tech Instagram",
            "Showing your build process in real time is the new portfolio",
            "AI meme culture is at peak saturation — creators who go deeper are winning",
        ],
        "twitter": [
            "Every week a new AI tool launches. Almost none of them last. Here's the pattern.",
            "The best AI products aren't the smartest ones. They're the ones people actually use.",
            "Shipping fast > perfecting endlessly. The market has spoken.",
            "Build in public isn't a strategy anymore. It's table stakes.",
            "Hot take: most AI wrappers aren't products. But some are. And those some are making real money.",
        ],
    },

    "fitness": {
        "linkedin": [
            "High performers treating fitness as a career asset — not just health",
            "The productivity-fitness link: what the research actually says",
            "Why rest days are now the most underrated competitive advantage",
        ],
        "instagram": [
            "10-minute workout content is destroying 1-hour gym content in every metric",
            "The anti-grind fitness era — rest and recovery content exploding",
            "Realistic body content outperforming aspirational content in saves",
            "Home workout aesthetic is back and better than ever",
        ],
        "twitter": [
            "The gym culture wars continue — functional fitness vs aesthetics, who's winning",
            "Hot take: most fitness advice optimizes for looking fit, not being fit",
            "Walking is still underrated. There. I said it.",
        ],
    },

    "finance": {
        "linkedin": [
            "The financial literacy gap between generations is widening — and it matters professionally",
            "Salary transparency is shifting power — what employers don't want employees to know",
            "Side income as a career hedge — professionals are treating it seriously now",
        ],
        "instagram": [
            "Money diary content — 'I make X, here's how I spend it' — is going viral",
            "Frugal flex is the new rich flex — anti-consumerism content exploding",
            "The 'broke to first investment' journey is one of the highest engagement formats",
        ],
        "twitter": [
            "Every financial influencer has the same advice. The people actually building wealth don't post much.",
            "Hot take: most personal finance advice is written for people who already have money",
            "The best investment most people can make right now isn't in the market",
        ],
    },

    "education": {
        "linkedin": [
            "Micro-credentials are outperforming degrees in certain hiring pipelines — the data is clear",
            "The 'learn in public' movement is the most efficient way to build a professional reputation",
            "Skills gap is widening — the people upskilling now are pulling ahead faster than expected",
        ],
        "instagram": [
            "Free resource drop posts are getting 5x normal saves right now",
            "Study with me content is dominating — accountability and community in one",
            "The 'I taught myself X in 30 days' format never gets old and always performs",
        ],
        "twitter": [
            "You can learn almost any skill for free now. The barrier isn't access. It's direction.",
            "Hot take: university teaches you how to learn, not what to learn. That's still valuable.",
            "The best educators online are giving away knowledge that used to cost thousands.",
        ],
    },

    "startup": {
        "linkedin": [
            "Zero-budget marketing is producing some of the most compelling founder stories right now",
            "The founder brand is outperforming the company brand for early-stage startups",
            "Building without funding is a flex in 2025 — bootstrapped stories are dominating",
        ],
        "instagram": [
            "Day-in-the-life founder content is getting organic reach that paid ads can't buy",
            "The 'I built this alone' era — solo founder content is having a massive moment",
            "Revenue transparency posts from indie founders are exploding — real numbers win",
        ],
        "twitter": [
            "The best startups right now were built by people who were personally frustrated by the problem",
            "Seed rounds are down. Bootstrapped revenue is up. The market is self-correcting.",
            "Hot take: most startup advice is survivorship bias dressed up as wisdom",
        ],
    },

    "creator": {
        "linkedin": [
            "Creator economy professionalisation — the best creators are running businesses, not channels",
            "LinkedIn creators are growing faster than any other platform right now — the window won't last",
        ],
        "instagram": [
            "The authentic era — raw, unpolished content is beating high-production content across all metrics",
            "Engagement pods are dead — community-driven growth is what's working",
            "Niche down energy — 10K engaged followers beats 100K passive ones every time",
        ],
        "twitter": [
            "Hot take: the creator economy is actually just the economy now for under-35s",
            "Follower count is becoming a vanity metric. Email list and community are the real assets.",
        ],
    },

    "general": {
        "linkedin": [
            "Personal branding isn't optional anymore — it's infrastructure",
            "The professionals growing fastest right now have one thing in common: they show their thinking publicly",
            "Authenticity is outperforming polish across every professional platform",
        ],
        "instagram": [
            "The algorithm is rewarding consistency over perfection right now — just ship it",
            "Community over following — the accounts growing fastest are building real relationships",
            "Behind-the-scenes content is outperforming highlight reel content in saves and shares",
        ],
        "twitter": [
            "The people growing fastest on every platform have a clear, specific point of view",
            "Hot take: most social media advice is optimizing for the wrong metric",
            "Consistency beats virality. Still. Always.",
        ],
    },
}

def _get_hot_topics(niche: str, platform: str) -> list:
    bank   = TOPIC_BANK.get(niche, TOPIC_BANK["general"])
    topics = bank.get(platform, bank.get("linkedin", []))
    seed   = int(datetime.now().hour) % max(len(topics), 1)
    # Rotate selection so it feels fresh each session
    rotated = topics[seed:] + topics[:seed]
    return rotated[:5]


# ══════════════════════════════════════════════════════════════════════════════
# CONTENT OPPORTUNITIES
# ══════════════════════════════════════════════════════════════════════════════

def _get_opportunities(niche: str, platform: str, audience: str, goal: str) -> list:
    a = audience.lower()
    ops = {
        "ai_career": [
            f"Create a 'LinkedIn profile audit' post using {goal} — high search intent right now",
            f"Post a before/after profile comparison — visual proof drives saves",
            f"Write a '5 things ATS filters reject' educational post — fear + value combo",
            f"'I applied to 50 jobs with AI help' personal story — high engagement format",
            f"Debunk one common resume myth — controversy + education always performs",
        ],
        "ai_tech": [
            f"'I built {goal} in X days' — build-in-public moment is always high-reach",
            f"Compare {goal} vs doing it manually — time-saved hook works every time",
            f"'5 AI tools that actually save time' — include {goal}, list format gets shared",
            f"Post a product demo with real output — proof beats claims consistently",
            f"Founder frustration story — why you built {goal} — authenticity drives connection",
        ],
        "fitness": [
            "10-minute home workout post — search volume is massive right now",
            "Myth-bust one fitness belief — controversy + education = high engagement",
            "Share a realistic transformation story — not aspirational, real",
        ],
        "finance": [
            "Salary transparency post — share your income story with context",
            "'I was broke, here's what changed' — one of the highest-engagement formats",
            "Debunk one popular investing myth — positions you as trustworthy contrarian",
        ],
        "education": [
            "Drop a free resource in the post — massive saves guaranteed",
            "'I learned X in 30 days' — specific, believable, shareable",
            "Post a skill roadmap as a carousel — evergreen save-bait",
        ],
        "startup": [
            f"'Zero budget marketing for {goal}' — founders are obsessed with this content",
            "Share your real MRR or user count — transparency builds trust and reach",
            "Founder failure story with lesson — authentic vulnerability drives engagement",
        ],
        "general": [
            f"Behind-the-scenes of building {goal} — authenticity over polish right now",
            "Post a contrarian take on conventional wisdom in your niche",
            "Create a free resource drop — saves and follows in one",
        ],
    }
    return ops.get(niche, ops["general"])


# ══════════════════════════════════════════════════════════════════════════════
# ANGLES TO USE
# ══════════════════════════════════════════════════════════════════════════════

def _get_angles(niche: str, platform: str, audience: str) -> list:
    angles = {
        "linkedin": [
            "Contrarian professional angle — say what others in your industry won't",
            "Lesson-from-failure angle — vulnerability + wisdom outperforms wins right now",
            "Data-backed angle — lead with a stat that surprises, then explain it",
            "Systems over hustle angle — people are tired of grind content, they want leverage",
            "'Here's what I actually learned' angle — first-person experience beats theory",
        ],
        "instagram": [
            "Relatable fail → glow-up arc — universal emotional journey format",
            "Contrarian lifestyle angle — go against what everyone else in your niche is saying",
            "Real numbers angle — transparency of any kind performs well right now",
            "POV format — puts the viewer in the story immediately",
            "Before/after visual angle — works for almost any niche",
        ],
        "twitter": [
            "Hot take angle — take a clear, defensible position most won't say",
            "Pattern recognition angle — 'I studied X and here's what nobody mentions'",
            "Debunk angle — take a popular belief and show why it's incomplete",
            "Prediction angle — specific, not vague — 'this will happen because...'",
            "Quiet confidence angle — state the uncomfortable truth calmly",
        ],
    }
    return angles.get(platform, angles["linkedin"])


# ══════════════════════════════════════════════════════════════════════════════
# AVOID TOPICS
# ══════════════════════════════════════════════════════════════════════════════

def _get_avoid(niche: str, platform: str) -> list:
    universal = [
        "Engagement bait ('Comment YES if you agree')",
        "Reposting the same content across platforms without adapting it",
        "Generic motivational quotes with no original perspective",
        "Posting without a clear point of view — neutral content is invisible",
    ]
    platform_specific = {
        "linkedin": [
            "'Grateful and humbled' posts without substance",
            "Humble-brag disguised as a lesson",
            "Posting only about your product — ratio should be 80% value, 20% product",
            "Overlong paragraphs with no line breaks — people scan before they read",
        ],
        "instagram": [
            "Over-polished content that looks like an ad — authenticity is winning right now",
            "Caption that just repeats what's in the image",
            "Generic hashtags (#love, #life, #motivation) — too broad to drive discovery",
            "Posting without a visual hook — first frame decides everything",
        ],
        "twitter": [
            "Long threads with weak premise — earn the thread with the first tweet",
            "Hedging language ('this might be controversial but...')",
            "Vague takes that nobody can agree or disagree with",
            "Chasing trending topics that have nothing to do with your niche",
        ],
    }
    return universal + platform_specific.get(platform, [])


# ══════════════════════════════════════════════════════════════════════════════
# BEST TOPIC PICKER
# ══════════════════════════════════════════════════════════════════════════════

def _pick_best_topic(hot_topics: list, niche: str, platform: str) -> str:
    if not hot_topics:
        return "Your personal story of building and why it matters right now"
    # Use time-of-day seed so it feels fresh each session
    seed = int(datetime.now().minute) % len(hot_topics)
    return hot_topics[seed]


# ══════════════════════════════════════════════════════════════════════════════
# WHY NOW
# ══════════════════════════════════════════════════════════════════════════════

def _build_why_now(best_topic: str, niche: str, platform: str) -> str:
    platform_context = {
        "linkedin": (
            "LinkedIn's algorithm is currently favouring original thought leadership over reposts. "
            "Organic reach on text-based posts is higher than it's been in 18 months. "
            "The window for early movers in this conversation is open — it won't be forever."
        ),
        "instagram": (
            "Instagram Reels and carousels are both in algorithmic favour right now. "
            "Authentic content is outperforming polished content in saves and shares. "
            "The bar for what 'good' looks like is lower than most creators think — ship it."
        ),
        "twitter": (
            "Twitter/X engagement is concentrated in niche communities right now — "
            "owning a specific lane outperforms chasing broad appeal. "
            "Hot takes with a defensible position are getting disproportionate reach."
        ),
        "facebook": (
            "Facebook Groups and community content are seeing strong organic reach. "
            "Long-form personal stories are outperforming link posts significantly."
        ),
    }
    base = platform_context.get(platform, "Organic reach on this platform favours consistent, original creators right now.")
    topic_note = f" The specific topic '{best_topic[:60]}...' is relevant because it connects a current trend to a persistent audience problem — that combination always has high engagement potential."
    return base + topic_note