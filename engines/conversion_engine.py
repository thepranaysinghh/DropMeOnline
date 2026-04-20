# conversion_engine.py — Generates conversion-focused marketing assets based on goal

def generate_conversion_assets(goal: str) -> dict:
    """
    Input:  goal (string) — e.g. "Promote AI resume tool"
    Output: dict with cta, urgency, trust, and offer lines
    Note:   Rule-based template system (AI upgrade in future phase)
    """

    g = goal.strip()

    cta = [
        f"Try {g} for free — no credit card needed.",
        f"Start using {g} today and see results in 7 days.",
        f"Join the waitlist for {g} before spots run out.",
        f"Get early access to {g} — limited slots available.",
        f"Click the link and get started with {g} right now.",
    ]

    urgency = [
        f"Only a few early access spots left for {g}.",
        f"This offer for {g} ends soon — don't miss it.",
        f"We're closing the beta for {g} this week.",
        f"100 people signed up for {g} in the last 24 hours.",
        f"Don't wait — others are already getting results with {g}.",
    ]

    trust = [
        f"{g} is already helping real people solve real problems.",
        f"Built by people who faced this problem themselves — that's {g}.",
        f"No fluff. No hype. Just results. That's what {g} delivers.",
        f"Hundreds of early users trust {g} to get the job done.",
        f"{g} is free to start — because we want you to see value first.",
    ]

    offers = [
        f"Free plan available — start with {g} at zero cost.",
        f"First 100 users get lifetime free access to {g}.",
        f"Use {g} free for 14 days — no commitment needed.",
        f"Refer a friend to {g} and unlock premium features.",
        f"Early adopters of {g} get exclusive perks — join now.",
    ]

    return {
        "cta":     cta,
        "urgency": urgency,
        "trust":   trust,
        "offers":  offers,
    }