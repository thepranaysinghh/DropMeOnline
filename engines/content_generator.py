# content_generator.py — Smart platform-specific content generator
# Detects intent, length preference, style from user goal
# Produces human-quality, platform-native posts every time

from datetime import datetime
import random

# ── INTENT PARSER ─────────────────────────────────────────────────────────────

def _parse_intent(goal: str) -> dict:
    """
    Reads the user's goal and extracts platform, length, tone, style hints.
    Returns a dict that shapes how content is generated.
    """
    text = goal.lower()

    # Length intent
    if any(w in text for w in ["short", "quick", "brief", "one line", "1 line", "tiny"]):
        length = "short"
    elif any(w in text for w in ["long", "detailed", "deep", "in depth", "comprehensive", "full"]):
        length = "long"
    elif any(w in text for w in ["thread", "series", "multi"]):
        length = "thread"
    else:
        length = "default"

    # Tone intent
    if any(w in text for w in ["funny", "humor", "meme", "sarcastic", "witty"]):
        tone = "funny"
    elif any(w in text for w in ["bold", "savage", "controversial", "hot take", "unpopular"]):
        tone = "bold"
    elif any(w in text for w in ["emotional", "story", "vulnerable", "personal", "honest"]):
        tone = "emotional"
    elif any(w in text for w in ["educational", "tips", "how to", "guide", "learn", "explain"]):
        tone = "educational"
    elif any(w in text for w in ["professional", "corporate", "formal", "authority"]):
        tone = "professional"
    elif any(w in text for w in ["motivational", "inspire", "energetic", "pumped"]):
        tone = "inspirational"
    else:
        tone = "default"

    # Platform hint from goal itself
    platform_hints = []
    if "linkedin" in text:
        platform_hints.append("linkedin")
    if "instagram" in text or "ig" in text or "reels" in text:
        platform_hints.append("instagram")
    if "twitter" in text or "tweet" in text or "x " in text:
        platform_hints.append("twitter")

    # Niche
    niche = "general"
    for kw, n in [
        ("ai","ai"), ("resume","career"), ("job","career"), ("startup","startup"),
        ("saas","saas"), ("fitness","fitness"), ("food","food"),
        ("finance","finance"), ("fashion","fashion"), ("course","education"),
        ("developer","tech"), ("coding","tech"), ("marketing","marketing")
    ]:
        if kw in text:
            niche = n
            break

    return {
        "length":          length,
        "tone":            tone,
        "platform_hints":  platform_hints,
        "niche":           niche,
    }


# ── SEED FOR VARIETY ──────────────────────────────────────────────────────────

def _seed() -> int:
    return int(datetime.now().microsecond) % 7


# ── LINKEDIN GENERATOR ────────────────────────────────────────────────────────

def _linkedin_post(goal: str, intent: dict) -> str:
    tone   = intent["tone"]
    length = intent["length"]
    niche  = intent["niche"]
    s      = _seed()

    # Short mode
    if length == "short":
        shorts = [
            f"Most people overthink {goal}.\n\nHere's the thing — the ones who win just start.\n\nStop waiting. Start doing.",
            f"The fastest way to grow with {goal}?\n\nShow up consistently when nobody's watching.\n\nThe algorithm rewards the relentless.",
            f"{goal} isn't about being the smartest in the room.\n\nIt's about being the most useful.\n\nFocus on that.",
        ]
        return shorts[s % len(shorts)]

    # Thread mode
    if length == "thread":
        return (
            f"I've been studying {goal} for months. Here's everything I learned:\n\n"
            f"1/ Most people start wrong. They focus on tactics before they understand the foundation.\n\n"
            f"2/ The foundation is always the same — know your audience better than they know themselves.\n\n"
            f"3/ Once you have that, {goal} becomes a system. Not a guessing game.\n\n"
            f"4/ The creators growing fastest aren't the most talented. They're the most consistent.\n\n"
            f"5/ And they do one thing everyone else skips: they study what's NOT working as much as what is.\n\n"
            f"6/ Final thought: {goal} is not a sprint. The people who win treat it like infrastructure.\n\n"
            f"Save this. It'll make sense more the longer you're at it."
        )

    # Tone variations — default length (8-10 lines)
    posts = {
        "funny": (
            f"I used to think {goal} was complicated.\n\n"
            f"Spoiler: I was just doing it wrong for 6 months straight.\n\n"
            f"Here's what nobody tells you:\n\n"
            f"→ Everyone looks like they have it figured out. They don't.\n"
            f"→ The messy middle is where all the actual learning happens.\n"
            f"→ The people you admire? They failed louder than you. They just kept going.\n\n"
            f"Stop watching. Start building. Embarrass yourself publicly.\n\n"
            f"That's the whole secret.\n\n"
            f"(You're welcome.)"
        ),
        "bold": (
            f"Unpopular opinion about {goal}:\n\n"
            f"90% of the advice you've read is optimised for engagement — not results.\n\n"
            f"Here's what actually works:\n\n"
            f"→ Specificity beats volume every time\n"
            f"→ One strong post outperforms ten average ones\n"
            f"→ Your audience doesn't want more content — they want the right content\n\n"
            f"The people winning at {goal} right now aren't posting more.\n\n"
            f"They're thinking harder before they post.\n\n"
            f"That's the edge most people skip."
        ),
        "emotional": (
            f"6 months into {goal}, I almost gave up.\n\n"
            f"Not because it was hard. Because I couldn't see the progress.\n\n"
            f"Then someone told me: growth doesn't look like growth when you're in it.\n\n"
            f"It looks like confusion. Like starting over. Like questioning everything.\n\n"
            f"But one day you look back and realise —\n\n"
            f"You're not the same person who started.\n\n"
            f"That's the whole point of {goal}.\n\n"
            f"If you're in the hard part right now: keep going."
        ),
        "educational": (
            f"Most people approach {goal} wrong. Here's why:\n\n"
            f"They start with tactics. They should start with positioning.\n\n"
            f"The 3-part framework that actually works:\n\n"
            f"1. Who is this for? (Specific beats general, always)\n"
            f"2. What do they already believe? (Meet them there, not where you want them)\n"
            f"3. What's the one thing that changes their mind? (Lead with that)\n\n"
            f"Once you have those three locked in, {goal} becomes execution — not guesswork.\n\n"
            f"The strategy is simple. The discipline to follow it is where most people fall off."
        ),
        "professional": (
            f"After working on {goal} across multiple contexts, one pattern emerges clearly:\n\n"
            f"The organisations — and individuals — that sustain growth treat it as a system, not a campaign.\n\n"
            f"What separates them:\n\n"
            f"→ Consistent positioning over time\n"
            f"→ Audience intelligence before content creation\n"
            f"→ Measurement tied to outcomes, not vanity metrics\n\n"
            f"The fundamentals haven't changed. What's changed is how unforgiving the environment is when you ignore them.\n\n"
            f"Execution advantage compounds. So does the gap between those who have it and those who don't."
        ),
        "inspirational": (
            f"A year from now, you'll wish you had started {goal} today.\n\n"
            f"Not because it's easy.\n\n"
            f"Because the version of you that's consistent for 12 months is unrecognisable from the version that's still thinking about starting.\n\n"
            f"The secret the top 1% know:\n\n"
            f"→ They didn't have a perfect plan\n"
            f"→ They had a working one\n"
            f"→ And they showed up when the motivation wasn't there\n\n"
            f"That's the whole game.\n\n"
            f"Start before you're ready. You'll never be more ready than right now."
        ),
    }

    default = (
        f"Here's what changes everything about {goal}:\n\n"
        f"Most people are optimising for the wrong thing.\n\n"
        f"They want reach. They should want resonance.\n\n"
        f"Because reach without resonance is just noise.\n\n"
        f"The accounts growing fastest right now have one thing in common:\n\n"
        f"→ They know exactly who they're talking to\n"
        f"→ They say things that person needed to hear\n"
        f"→ They show up before anyone's watching\n\n"
        f"That's it. That's the whole playbook.\n\n"
        f"Now go build."
    )

    return posts.get(tone, default)


# ── INSTAGRAM GENERATOR ───────────────────────────────────────────────────────

def _instagram_post(goal: str, intent: dict) -> str:
    tone   = intent["tone"]
    length = intent["length"]
    s      = _seed()

    if length == "short":
        shorts = [
            f"This changed how I think about {goal} 👇\n\n#growth #mindset",
            f"Nobody talks about this side of {goal} 👀\n\n#realtalk #growthmindset",
            f"Start with {goal}. Figure the rest out as you go. 🚀\n\n#startbefore #momentum",
        ]
        return shorts[s % len(shorts)]

    posts = {
        "funny": (
            f"POV: You've been avoiding {goal} for 3 months 💀\n\n"
            f"Also you: 'I'll start Monday'\n\n"
            f"Monday: exists\n\n"
            f"You: 🦗\n\n"
            f"Okay but real talk — the hardest part isn't starting. It's starting badly and continuing anyway.\n\n"
            f"Drop a 🙋 if you've been here.\n\n"
            f"#relatable #growthmindset #realtalk #startanyway"
        ),
        "bold": (
            f"Hot take: most people will never figure out {goal} 🔥\n\n"
            f"Not because they're not smart enough.\n\n"
            f"Because they're waiting to be ready.\n\n"
            f"Readiness is a myth.\n\n"
            f"The people winning started uncomfortable and got comfortable through action.\n\n"
            f"Save this for when you're overthinking. 📌\n\n"
            f"#truth #boldmoves #startbefore #noexcuses"
        ),
        "emotional": (
            f"To everyone working on {goal} quietly —\n\n"
            f"The progress you can't see yet is still progress. 🌱\n\n"
            f"Keep going.\n\n"
            f"The version of you that didn't give up is going to be proud.\n\n"
            f"❤️ Save this when you need it.\n\n"
            f"#youvegotthis #growthmindset #keepgoing #motivation"
        ),
        "educational": (
            f"3 things nobody tells you about {goal} 👇\n\n"
            f"1. The beginning is the hardest — and the most important\n"
            f"2. The results come in waves, not straight lines\n"
            f"3. Consistency over a month beats intensity over a week\n\n"
            f"Save this and come back to it when you're doubting yourself. 📌\n\n"
            f"#tips #learn #growthhacks #mindset"
        ),
        "inspirational": (
            f"You're closer than you think with {goal}. ✨\n\n"
            f"The compounding is invisible until suddenly — it isn't.\n\n"
            f"Show up today like the version of you that figured it out already.\n\n"
            f"That energy is everything.\n\n"
            f"🚀 Double tap if you needed this.\n\n"
            f"#motivation #growthmindset #inspiration #believe"
        ),
    }

    default = (
        f"The thing about {goal} that changed everything for me 👇\n\n"
        f"It's not about being the best.\n\n"
        f"It's about being consistent when it's uncomfortable.\n\n"
        f"That's the actual edge. 🔥\n\n"
        f"Save this if you needed the reminder. 📌\n\n"
        f"#growth #mindset #realtalk #motivation #growthmindset"
    )

    return posts.get(tone, default)


# ── TWITTER GENERATOR ─────────────────────────────────────────────────────────

def _twitter_post(goal: str, intent: dict) -> str:
    tone   = intent["tone"]
    length = intent["length"]
    s      = _seed()

    if length == "thread":
        return (
            f"Everything I know about {goal} in one thread. Bookmark this 🧵\n\n"
            f"1/ Most people start with tactics. Wrong move. Start with clarity.\n\n"
            f"2/ Clarity = who you're for + what you uniquely offer + why now.\n\n"
            f"3/ Once that's locked: {goal} becomes execution, not strategy.\n\n"
            f"4/ Execution principle: do less, better. One strong move beats five weak ones.\n\n"
            f"5/ Measurement: track leading indicators, not lagging ones.\n\n"
            f"6/ The uncomfortable truth: 90% of people fail at {goal} because of inconsistency, not capability.\n\n"
            f"7/ Fix: build systems that work when motivation doesn't.\n\n"
            f"Final thought: {goal} is not a sprint. It's infrastructure. Build accordingly.\n\n"
            f"RT if this hit."
        )

    if length == "short":
        shorts = [
            f"{goal} > excuses.",
            f"Still not starting {goal}? Cool. Your competition is.",
            f"The best time to start {goal} was last year. Second best: now.",
        ]
        return shorts[s % len(shorts)]

    posts = {
        "funny": (
            f"Things that are easier than starting {goal}:\n\n"
            f"- Scrolling for 3 hours\n"
            f"- Reorganising your desktop\n"
            f"- Watching a 47-part series about productivity\n\n"
            f"Things that actually work: starting {goal} badly and improving."
        ),
        "bold": (
            f"Controversial opinion:\n\n"
            f"Most {goal} advice is written by people who haven't done it recently.\n\n"
            f"The market has changed. The tactics have changed.\n\n"
            f"Stop following blueprints. Start running experiments."
        ),
        "educational": (
            f"The {goal} framework nobody teaches:\n\n"
            f"→ Clarity before content\n"
            f"→ Audience before algorithm\n"
            f"→ Consistency before perfection\n\n"
            f"In that order. Every time.\n\n"
            f"Thread on why 🧵"
        ),
        "emotional": (
            f"Nobody talks about the quiet phase of {goal}.\n\n"
            f"Where you're doing the work.\n"
            f"Getting zero feedback.\n"
            f"Wondering if it's working.\n\n"
            f"It is.\n\n"
            f"Keep going."
        ),
        "inspirational": (
            f"The version of you that committed to {goal} 6 months ago would be unrecognisable.\n\n"
            f"That version still exists.\n\n"
            f"Start today."
        ),
    }

    default = (
        f"Hot take: {goal} isn't the hard part.\n\n"
        f"Starting is.\n"
        f"Continuing when it's quiet is.\n"
        f"Trusting the process when you can't see the results is.\n\n"
        f"The doing is actually the easy part."
    )

    return posts.get(tone, default)


# ── MAIN FUNCTION ─────────────────────────────────────────────────────────────

def generate_content(goal: str) -> dict:
    """
    Input:  goal (string) — user's natural language prompt
    Output: dict with platform-specific smart content
    """
    intent = _parse_intent(goal)

    return {
        "linkedin":  _linkedin_post(goal, intent),
        "instagram": _instagram_post(goal, intent),
        "twitter":   _twitter_post(goal, intent),
        "_intent":   intent,  # Pass intent downstream if needed
    }