# campaign_engine.py — Generates a day-wise campaign plan based on goal, duration, platforms

def generate_campaign(goal: str, days: int, platforms: list) -> list:
    """
    Input:
        goal      — e.g. "Promote AI resume tool"
        days      — campaign duration (e.g. 30)
        platforms — e.g. ["linkedin", "instagram"]
    Output:
        List of day-wise campaign plans
    """

    campaign = []

    for day in range(1, days + 1):

        # --- Determine phase ---
        if day <= 5:
            phase  = "Awareness"
            theme  = _awareness_theme(day)
            hook   = _awareness_hook(goal, day)
            cta    = "Follow for more updates."

        elif day <= 15:
            phase  = "Education + Trust"
            theme  = _education_theme(day)
            hook   = _education_hook(goal, day)
            cta    = "Save this post — you'll need it later."

        elif day <= 25:
            phase  = "Proof + Results"
            theme  = _proof_theme(day)
            hook   = _proof_hook(goal, day)
            cta    = "Comment your thoughts below."

        else:
            phase  = "Conversion"
            theme  = _conversion_theme(day)
            hook   = _conversion_hook(goal, day)
            cta    = "Try it now — link in bio."

        # --- Build day plan ---
        day_plan = {
            "day":   day,
            "phase": phase,
            "theme": theme,
            "hook":  hook,
            "cta":   cta,
        }

        # Add platform-specific post for each requested platform
        for platform in platforms:
            day_plan[platform] = _generate_post(platform, hook, cta, goal)

        campaign.append(day_plan)

    return campaign


# ── Phase theme helpers ────────────────────────────────────────────────────────

def _awareness_theme(day):
    themes = ["Introduction", "Problem Statement", "Who Is This For", "Why It Matters", "Our Mission"]
    return themes[(day - 1) % len(themes)]

def _education_theme(day):
    themes = [
        "How It Works", "Key Feature 1", "Key Feature 2",
        "Common Mistake", "Pro Tip", "Comparison", "Behind The Scenes",
        "FAQ", "User Benefit", "Quick Win"
    ]
    return themes[(day - 6) % len(themes)]

def _proof_theme(day):
    themes = [
        "User Story", "Before vs After", "Result Showcase",
        "Testimonial", "Case Study", "Numbers & Stats",
        "Real Example", "Community Highlight", "Milestone", "Progress Update"
    ]
    return themes[(day - 16) % len(themes)]

def _conversion_theme(day):
    themes = ["Limited Offer", "Final Push", "Last Chance", "Join Now", "Take Action"]
    return themes[(day - 26) % len(themes)]


# ── Hook generators ────────────────────────────────────────────────────────────

def _awareness_hook(goal, day):
    hooks = [
        f"Most people struggle with this — that's why we built: {goal}.",
        f"What if you could solve this problem in minutes? Introducing: {goal}.",
        f"This is for anyone who has ever felt stuck. Here's our solution: {goal}.",
        f"We noticed a gap nobody was solving. So we built it ourselves: {goal}.",
        f"One problem. One solution. This is our mission: {goal}.",
    ]
    return hooks[(day - 1) % len(hooks)]

def _education_hook(goal, day):
    hooks = [
        f"Here's exactly how {goal} works — step by step.",
        f"3 things you didn't know {goal} could do.",
        f"Most people make this mistake. Here's how {goal} fixes it.",
        f"The real reason people love {goal} — it's not what you think.",
        f"A quick tip from the team behind {goal}.",
        f"We compared {goal} vs doing it manually. The results surprised us.",
        f"Behind the scenes: how we built {goal}.",
        f"Your top questions about {goal} — answered.",
        f"The #1 benefit people get from {goal} within the first week.",
        f"Here's a quick win you can get from {goal} today.",
    ]
    return hooks[(day - 6) % len(hooks)]

def _proof_hook(goal, day):
    hooks = [
        f"A user shared their experience with {goal} — and it blew us away.",
        f"Before {goal} vs after {goal}. The difference is real.",
        f"Real results from real users of {goal}.",
        f"What people are saying about {goal} — unfiltered.",
        f"We tracked the results of {goal} for 30 days. Here's what happened.",
        f"The numbers behind {goal} don't lie.",
        f"Here's a real-world example of {goal} in action.",
        f"Our community is growing — here's why they chose {goal}.",
        f"We hit a milestone with {goal} and we're sharing it with you.",
        f"Week {day - 15} update: here's how {goal} is performing.",
    ]
    return hooks[(day - 16) % len(hooks)]

def _conversion_hook(goal, day):
    hooks = [
        f"This might be the last time we talk about {goal} for a while.",
        f"If you've been waiting to try {goal} — this is your sign.",
        f"Last chance to be an early adopter of {goal}.",
        f"Join hundreds of people already using {goal}.",
        f"Don't wait. {goal} is ready for you right now.",
    ]
    return hooks[(day - 26) % len(hooks)]


# ── Platform post formatter ────────────────────────────────────────────────────

def _generate_post(platform: str, hook: str, cta: str, goal: str) -> str:
    """Formats post per platform style."""

    if platform == "linkedin":
        return (
            f"{hook}\n\n"
            f"Here's what makes this different:\n"
            f"→ Built for real problems\n"
            f"→ Designed for results\n"
            f"→ Free to get started\n\n"
            f"{cta}"
        )

    elif platform == "instagram":
        return (
            f"{hook} ✨\n\n"
            f"{cta}\n\n"
            f"#ai #productivity #growthmindset #startup #buildinpublic"
        )

    elif platform == "twitter":
        # Twitter: short + punchy
        short_hook = hook.split(".")[0]
        return f"{short_hook}. {cta}"

    elif platform == "facebook":
        return (
            f"{hook}\n\n"
            f"We'd love to hear your thoughts. {cta}"
        )

    else:
        return f"{hook} — {cta}"