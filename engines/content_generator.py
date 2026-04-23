# content_generator.py — Smart platform-specific content generator
# Uses intent_parser — never dumps raw prompt into post copy

from engines.intent_parser import parse_intent
from datetime import datetime


def _seed() -> int:
    return int(datetime.now().microsecond) % 7


# ── LINKEDIN ─────────────────────────────────────────────────────────────────

def _linkedin_post(intent: dict) -> str:
    p   = intent["product"]        # e.g. "AI Resume Tool"
    ref = intent["product_ref"]    # e.g. "the tool"
    aud = intent["audience"]       # e.g. "job seekers"
    tone   = intent["tone"]
    length = intent["length"]
    s      = _seed()

    if length == "short":
        shorts = [
            f"Most {aud} are doing this the hard way.\n\n{p} exists so they don't have to.\n\nStart where it's easier.",
            f"The best thing about {p}?\n\nIt does the heavy lifting so {aud} can focus on what actually matters.\n\nThat's the whole idea.",
            f"{p} isn't complicated.\n\nIt's just what happens when you stop building for yourself and start building for {aud}.",
        ]
        return shorts[s % len(shorts)]

    if length == "thread":
        return (
            f"Everything I learned building {p} for {aud} — save this 🧵\n\n"
            f"1/ Most people building in this space start with the wrong question. 'How do I make this?' instead of 'Why does this need to exist?'\n\n"
            f"2/ {p} started from a simple frustration. {aud.capitalize()} had a real problem. Nobody was solving it well.\n\n"
            f"3/ Once you nail the 'why', the what and how become obvious. The path clears.\n\n"
            f"4/ The first version was ugly. We shipped it anyway. Real feedback beats perfect planning every time.\n\n"
            f"5/ The lesson: the people winning aren't the most talented. They're the ones who started before they were ready.\n\n"
            f"6/ {p} is what we built when we stopped waiting. It's built specifically for {aud}.\n\n"
            f"Follow for more on building in public."
        )

    posts = {
        "funny": (
            f"We built {p} because we were tired of watching {aud} overcomplicate something that should be simple.\n\n"
            f"The process before {ref}:\n"
            f"→ Hours of manual work\n"
            f"→ Generic advice that doesn't fit\n"
            f"→ Pretending it's all under control\n\n"
            f"The process with {ref}:\n"
            f"→ Actually just works\n\n"
            f"(We're not going to apologise for making it this easy.)"
        ),
        "bold": (
            f"Unpopular opinion: most tools built for {aud} are designed by people who've never been {aud}.\n\n"
            f"That's why they fail.\n\n"
            f"We built {p} differently:\n\n"
            f"→ Starting from the real problem, not the obvious one\n"
            f"→ Optimising for outcomes, not features\n"
            f"→ Shipping fast and listening faster\n\n"
            f"The result: something {aud} actually use.\n\n"
            f"That's the only metric that matters."
        ),
        "emotional": (
            f"The reason we built {p}:\n\n"
            f"We watched talented {aud} get stuck. Not because they weren't capable.\n\n"
            f"Because the tools available weren't built for them.\n\n"
            f"They were built for someone else's version of the problem.\n\n"
            f"We got tired of that.\n\n"
            f"So we built {ref}. For {aud}. From the beginning.\n\n"
            f"If that's you — this is for you."
        ),
        "educational": (
            f"3 things most {aud} don't realise until it's too late:\n\n"
            f"1. The biggest bottleneck isn't effort — it's the right system\n"
            f"2. Manual processes don't scale, and they don't need to\n"
            f"3. The right tool removes friction before you even notice it\n\n"
            f"This is what we built {p} to do.\n\n"
            f"Not another layer of complexity.\n"
            f"A simpler path to the outcome {aud} actually want."
        ),
        "professional": (
            f"Building something that genuinely works for {aud} requires understanding two things:\n\n"
            f"What they say they need. And what they actually need.\n\n"
            f"Those are almost never the same thing.\n\n"
            f"{p} was built after listening to the second category.\n\n"
            f"The result is a product that fits into how {aud} actually work — not how we imagined they might."
        ),
        "inspirational": (
            f"A year from now, the {aud} who figured out how to work smarter will be unrecognisable.\n\n"
            f"Not because they're smarter.\n\n"
            f"Because they stopped doing manually what could be done better.\n\n"
            f"That's what {p} is built around.\n\n"
            f"The compounding starts the day you stop doing it the hard way."
        ),
    }

    default = (
        f"We built {p} for one simple reason:\n\n"
        f"{aud.capitalize()} deserve a tool that actually understands their problem.\n\n"
        f"Not a generic solution.\n"
        f"Not another feature nobody asked for.\n\n"
        f"Just the thing that moves the needle — simply, quickly, reliably.\n\n"
        f"That's {ref}."
    )
    return posts.get(tone, default)


# ── INSTAGRAM ────────────────────────────────────────────────────────────────

def _instagram_post(intent: dict) -> str:
    p   = intent["product"]
    ref = intent["product_ref"]
    aud = intent["audience"]
    tone   = intent["tone"]
    length = intent["length"]
    s      = _seed()
    niche  = intent["niche"]

    if length == "short":
        return f"Built for {aud}. Tested by {aud}. That's {p}. 🔥\n\n#buildinpublic #growth"

    posts = {
        "funny": (
            f"POV: You're {aud} and you just found {p} 👀\n\n"
            f"Before: doing everything manually and pretending it's fine 💀\n"
            f"After: actually having a system that works 😤\n\n"
            f"Drop a 🙋 if this is your arc.\n\n"
            f"#relatable #growthmindset #buildinpublic"
        ),
        "bold": (
            f"Hot take: most {aud} are using the wrong tools for the job. 🔥\n\n"
            f"Not their fault — the right ones are hard to find.\n\n"
            f"{p} was built to fix that.\n\n"
            f"Save this if you're finally ready to try the right one. 📌"
        ),
        "emotional": (
            f"To every {aud.split()[0]} who's been figuring this out alone —\n\n"
            f"We built {p} for you. 🌱\n\n"
            f"You don't have to do it the hard way anymore.\n\n"
            f"❤️ Save this when you need the reminder."
        ),
        "educational": (
            f"3 things {aud} get wrong — and how {p} fixes them 👇\n\n"
            f"1. Starting with tactics before strategy\n"
            f"2. Manual work that should be automated\n"
            f"3. Skipping the step that compounds everything\n\n"
            f"Save this. Come back to it. 📌"
        ),
        "inspirational": (
            f"The version of you that figured out {ref}? 🚀\n\n"
            f"That version exists.\n\n"
            f"Built for {aud} who are done waiting.\n\n"
            f"Double tap if you're ready. ✨"
        ),
    }

    hashtag_sets = {
        "career":    "#career #personalbrand #linkedin #jobsearch #growthmindset",
        "ai":        "#ai #aitools #futureofwork #buildinpublic #techstartup",
        "startup":   "#startup #founder #buildinpublic #entrepreneurship #indiehacker",
        "fitness":   "#fitness #healthylifestyle #workout #mindset #motivation",
        "finance":   "#personalfinance #investing #moneymindset #financialfreedom",
        "education": "#learning #selfimprovement #skills #growthmindset #education",
        "saas":      "#saas #productdesign #buildinpublic #startup #tech",
        "general":   "#growth #mindset #motivation #growthmindset #buildinpublic",
    }

    base = posts.get(tone, f"{p} — built specifically for {aud}. ✨\n\nThis is what it looks like when tools actually understand the problem.\n\nSave this if you're tired of the hard way. 📌")
    tags = hashtag_sets.get(niche, hashtag_sets["general"])

    if "#" not in base:
        base = base.rstrip() + f"\n\n{tags}"
    return base


# ── TWITTER ──────────────────────────────────────────────────────────────────

def _twitter_post(intent: dict) -> str:
    p    = intent["product"]
    ref  = intent["product_ref"]
    aud  = intent["audience"]
    tone = intent["tone"]
    length = intent["length"]
    s    = _seed()

    if length == "short":
        shorts = [
            f"Built {p} for {aud}. Shipped it before it was perfect. Zero regrets.",
            f"{aud.capitalize()} deserve better tools. That's why {p} exists.",
            f"The hard way was never the right way. {p} for {aud}.",
        ]
        return shorts[s % len(shorts)]

    if length == "thread":
        return (
            f"Why we built {p} for {aud} — and what we learned shipping it 🧵\n\n"
            f"1/ The problem: {aud} had no tool built specifically for them. Generic ones kept failing.\n\n"
            f"2/ Most tools are built by people who heard about the problem secondhand. We lived it.\n\n"
            f"3/ First principle: if you have to explain why someone should use it, you haven't solved it yet.\n\n"
            f"4/ We shipped ugly. Got feedback. Shipped again. The cycle is the product.\n\n"
            f"5/ Lesson: distribution matters as much as the product. Maybe more.\n\n"
            f"6/ {p} is live. Built for {aud}. Free to start.\n\n"
            f"RT if this thread helped."
        )

    posts = {
        "bold": (
            f"Controversial: most tools for {aud} are built by people who've never been {aud}.\n\n"
            f"That's why they're mediocre.\n\n"
            f"We built {p} from the inside. There's a difference."
        ),
        "funny": (
            f"{aud.capitalize()} after finding {p}:\n\n"
            f"'Why didn't this exist before'\n\n"
            f"(it kind of did, we just made it actually work)"
        ),
        "educational": (
            f"What nobody tells {aud}:\n\n"
            f"→ The bottleneck isn't effort\n"
            f"→ It's having the right system\n"
            f"→ {p} is that system\n\n"
            f"Thread on how 🧵"
        ),
        "emotional": (
            f"We built {p} because we watched great {aud} struggle with tools not built for them.\n\n"
            f"That felt wrong.\n\n"
            f"So we fixed it."
        ),
        "inspirational": (
            f"The {aud} who figure out {ref} early will look back and wonder why they waited.\n\n"
            f"Don't be that person."
        ),
    }

    default = (
        f"Built {p} for {aud}.\n\n"
        f"Simple problem. Took too long to solve properly.\n\n"
        f"We solved it."
    )
    return posts.get(tone, default)


# ── MAIN FUNCTION ─────────────────────────────────────────────────────────────

def generate_content(goal: str) -> dict:
    """
    Input:  raw user goal string
    Output: platform-specific content dict
    Never dumps raw goal into post copy.
    """
    intent = parse_intent(goal)

    return {
        "linkedin":  _linkedin_post(intent),
        "instagram": _instagram_post(intent),
        "twitter":   _twitter_post(intent),
        "_intent":   intent,
    }