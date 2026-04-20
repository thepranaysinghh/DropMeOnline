# visual_engine.py — Complete Visual Production Engine
# Generates platform-specific creative briefs, image prompts, captions, and style guides

def generate_visual_assets(goal: str, content: str) -> dict:
    """
    Input:
        goal    — e.g. "Promote AI resume tool"
        content — core message or topic for this post
    Output:
        Complete visual production package for LinkedIn, Instagram, Twitter
    """

    g = goal.strip()
    c = content.strip()

    return {

        # ── LinkedIn Carousel ─────────────────────────────────────────────────
        "linkedin_carousel": {
            "headline":     _linkedin_headline(g),
            "thumbnail":    f"Slide 0 — Thumbnail Hook: {_thumbnail_hook(g)}",
            "slides": [
                f"Slide 1 — Hook: Nobody talks about this problem with {c}.",
                f"Slide 2 — Problem: Most people fail here because they overlook {c}.",
                f"Slide 3 — Insight: Here's what top performers know about {c}.",
                f"Slide 4 — Solution: How {g} solves this in minutes.",
                f"Slide 5 — Proof: Real results. Real people. {g} delivers.",
                f"Slide 6 — CTA: Follow for more. Try {g} free today.",
            ],
            "caption": (
                f"{_linkedin_headline(g)}\n\n"
                f"Swipe to see the full breakdown 👉\n\n"
                f"Save this post — you'll want to come back to it.\n\n"
                f"#productivity #ai #growthmindset #linkedin #buildinpublic"
            ),
            "style":        "premium clean authority",
            "design_notes": (
                "White or deep navy background. "
                "Bold sans-serif font (e.g. Syne or DM Sans). "
                "One key insight per slide. "
                "Subtle gradient accent on corners. "
                "No clutter — lots of breathing room."
            ),
        },

        # ── Instagram Post ────────────────────────────────────────────────────
        "instagram_post": {
            "headline":     _instagram_headline(c),
            "caption_text": (
                f"POV: You finally found a tool that actually works 👀\n\n"
                f"{c} — and most people are still sleeping on it.\n\n"
                f"This is {g}. Built for people who are done wasting time.\n\n"
                f"Save this. Share this. You'll thank yourself later. 🔥\n\n"
                f"#ai #productivity #growthmindset #buildinpublic #viral"
            ),
            "meme_text": {
                "top":    f"Me before discovering {g}:",
                "bottom": f"Me after discovering {g}: 😎🔥",
            },
            "style":        "bold meme vibrant modern",
            "design_notes": (
                "High contrast colors — neon on dark OR bold on white. "
                "Big oversized text overlay. "
                "Meme format or split before/after comparison. "
                "Eye-catching thumbnail — face or bold graphic. "
                "Use gradients: purple-to-blue or orange-to-pink."
            ),
        },

        # ── Twitter Graphic ───────────────────────────────────────────────────
        "twitter_graphic": {
            "headline":     _twitter_headline(c),
            "caption": (
                f"{_twitter_headline(c)}\n\n"
                f"Thread below 🧵"
            ),
            "style":        "sharp minimal controversial",
            "design_notes": (
                "Plain dark card (#0f0f0f or #1a1a2e). "
                "One punchy line. White or purple text. "
                "No icons or clutter. "
                "Feels like a quote card that demands a retweet."
            ),
        },

        # ── AI Image Generation Prompts ───────────────────────────────────────
        "image_prompts": {
            "linkedin": (
                f"Professional dark navy presentation slide. "
                f"Bold white text: '{_linkedin_headline(g)}'. "
                f"Minimalist premium design. Subtle purple gradient accent. "
                f"Clean corporate aesthetic. High resolution. No people."
            ),
            "instagram": (
                f"Vibrant bold social media graphic. "
                f"Split screen comparison design. "
                f"Left side dark moody. Right side bright energetic. "
                f"Large text overlay: '{_instagram_headline(c)}'. "
                f"Neon purple and electric blue palette. Eye-catching. Viral aesthetic."
            ),
            "twitter": (
                f"Minimal dark quote card. Black background. "
                f"Single bold white sentence: '{_twitter_headline(c)}'. "
                f"No images. No icons. Sharp typography. "
                f"Feels like a controversial statement card."
            ),
        },

        # ── Color and Style Guide ─────────────────────────────────────────────
        "styles": {
            "linkedin": {
                "background":  "#0a0a1a or #ffffff",
                "accent":      "#7c3aed (purple) or #2563eb (blue)",
                "font":        "Syne Bold / DM Sans",
                "mood":        "Authority, trust, expertise",
                "avoid":       "Emojis, bright colors, casual language",
            },
            "instagram": {
                "background":  "#1a1a2e or high contrast gradient",
                "accent":      "#f59e0b (amber), #ec4899 (pink), #7c3aed (purple)",
                "font":        "Impact / Bebas Neue / Anton",
                "mood":        "Energy, relatability, virality",
                "avoid":       "Dense text, plain white, corporate feel",
            },
            "twitter": {
                "background":  "#0f0f0f or #111827",
                "accent":      "#ffffff or #a78bfa",
                "font":        "Inter Bold / Space Grotesk",
                "mood":        "Controversy, confidence, directness",
                "avoid":       "Long paragraphs, multiple colors, decorations",
            },
        },

    }


# ── Headline generators ────────────────────────────────────────────────────────

def _linkedin_headline(goal: str) -> str:
    hooks = [
        f"I spent 30 days testing {goal}. Here's what nobody tells you.",
        f"The uncomfortable truth about {goal} — and how to use it.",
        f"What top performers know about {goal} that most people don't.",
        f"Stop doing this. Start using {goal} instead.",
        f"This changed everything about how I approach {goal}.",
    ]
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


def _thumbnail_hook(goal: str) -> str:
    hooks = [
        f"🚨 {goal} — most people don't know this",
        f"The {goal} truth nobody shares (swipe)",
        f"I wish I knew this about {goal} earlier →",
        f"Why {goal} is changing everything in 2025",
        f"Read this before you ignore {goal} again",
    ]
    return hooks[len(goal) % len(hooks)]