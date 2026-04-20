# visual_engine.py — Viral Creative Asset Engine
# Generates platform-specific visual content briefs and copy

def generate_visual_assets(goal: str, content: str) -> dict:
    """
    Input:
        goal    — e.g. "Promote AI resume tool"
        content — core message or topic for this post
    Output:
        dict with visual asset specs for LinkedIn, Instagram, Twitter
    """

    g = goal.strip()
    c = content.strip()

    return {

        # ── LinkedIn Carousel ─────────────────────────────────────────────────
        "linkedin_carousel": {
            "headline": _linkedin_headline(g),
            "slides": [
                f"Slide 1 — Hook: Nobody talks about this problem with {c}.",
                f"Slide 2 — Problem: Most people fail at this because they don't know {c}.",
                f"Slide 3 — Insight: Here's what the top 1% do differently with {c}.",
                f"Slide 4 — Solution: How {g} solves this in minutes.",
                f"Slide 5 — Proof: Real results. Real people. {g} works.",
                f"Slide 6 — CTA: Follow for more. Try {g} free today.",
            ],
            "style": "premium clean authority",
            "design_notes": "White or dark background. Bold sans-serif font. One key point per slide. No clutter.",
        },

        # ── Instagram Post ────────────────────────────────────────────────────
        "instagram_post": {
            "headline": _instagram_headline(c),
            "caption_text": (
                f"POV: You finally found a tool that actually works 👀\n\n"
                f"{c} — and most people are sleeping on it.\n\n"
                f"This is {g}. Built for people who are done wasting time.\n\n"
                f"Save this. Share this. You'll thank yourself later. 🔥\n\n"
                f"#ai #productivity #growthmindset #buildinpublic #viral"
            ),
            "style": "bold meme vibrant modern",
            "design_notes": "High contrast colors. Big bold text overlay. Meme format or split comparison. Eye-catching thumbnail.",
        },

        # ── Twitter Graphic ───────────────────────────────────────────────────
        "twitter_graphic": {
            "headline": _twitter_headline(c),
            "style": "sharp minimal controversial",
            "design_notes": "Plain dark card. One punchy line. White text. No icons. Feels like a quote card that demands a retweet.",
        },

    }


# ── Headline generators ────────────────────────────────────────────────────────

def _linkedin_headline(goal: str) -> str:
    hooks = [
        f"I spent 30 days testing {goal}. Here's what nobody tells you.",
        f"The uncomfortable truth about {goal} — and how to use it.",
        f"What top performers know about {goal} that you don't.",
        f"Stop doing this. Start using {goal} instead.",
        f"This changed everything about how I approach {goal}.",
    ]
    # Rotate based on goal length as a simple deterministic selector
    return hooks[len(goal) % len(hooks)]


def _instagram_headline(content: str) -> str:
    hooks = [
        f"They said {content} was hard. They were wrong 💀",
        f"POV: You just discovered {content} exists 👀",
        f"This {content} hack is going viral for a reason 🔥",
        f"Nobody is talking about {content} and it's actually insane",
        f"The {content} glow-up nobody asked for but everyone needed ✨",
    ]
    return hooks[len(content) % len(hooks)]


def _twitter_headline(content: str) -> str:
    hooks = [
        f"Unpopular opinion: {content} is the only thing that matters.",
        f"Everyone is overthinking {content}. Here's the truth.",
        f"{content} will separate winners from everyone else in 2025.",
        f"You're doing {content} wrong. Here's the fix.",
        f"Hot take: {content} is still massively underrated.",
    ]
    return hooks[len(content) % len(hooks)]