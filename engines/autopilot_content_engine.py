# autopilot_content_engine.py — Autonomous Content Intelligence Engine
# Behaves like a senior human content strategist. No templates. No repetition. No cringe.

import random
import hashlib
from datetime import datetime

def generate_autopilot_content(
    goal:      str,
    platform:  str,
    niche:     str,
    audience:  str,
    history:   list = None
) -> dict:
    """
    Input:
        goal     — e.g. "Grow LinkedIn for AI resume tool"
        platform — "linkedin" | "instagram" | "twitter" | "facebook"
        niche    — e.g. "career + AI"
        audience — e.g. "freshers"
        history  — list of previously used hooks/styles (for repeat protection)
    Output:
        Full content package: angle, tone, style, hook, post, cta, image_idea,
        why_this_will_work, avoid_repeat_score
    """

    history   = history or []
    platform  = platform.lower().strip()
    text      = f"{goal} {niche} {audience}".lower()

    # --- Intelligence layers ---
    mood         = _pick_mood(history)
    trigger      = _pick_trigger(audience, text)
    trend_angle  = _pick_trend(niche, text)
    angle        = _build_angle(goal, audience, mood, trend_angle, trigger)
    tone         = _build_tone(platform, mood, audience)
    style        = _build_style(platform, mood)
    hook         = _build_hook(goal, audience, niche, platform, mood, trigger, history)
    post         = _build_post(hook, goal, audience, platform, mood, niche, trigger)
    cta          = _build_cta(platform, trigger, goal)
    image_idea   = _build_image_idea(platform, mood, niche)
    why          = _build_why(hook, mood, trigger, platform)
    repeat_score = _repeat_score(hook, history)

    return {
        "angle":              angle,
        "tone":               tone,
        "style":              style,
        "hook":               hook,
        "post":               post,
        "cta":                cta,
        "image_idea":         image_idea,
        "why_this_will_work": why,
        "avoid_repeat_score": repeat_score,
    }


# ══════════════════════════════════════════════════════════════════════════════
# MOOD ENGINE — rotates so every post feels different
# ══════════════════════════════════════════════════════════════════════════════

MOODS = [
    "funny", "savage", "emotional", "inspirational",
    "educational", "controversial", "storytelling", "curiosity"
]

def _pick_mood(history: list) -> str:
    # Avoid last used mood if possible
    used = [h.get("mood") for h in history if isinstance(h, dict) and "mood" in h]
    available = [m for m in MOODS if m not in used[-2:]]
    pool = available if available else MOODS
    # Use time-seeded randomness so every call is different
    seed = int(datetime.now().timestamp() * 1000) % len(pool)
    return pool[seed % len(pool)]


# ══════════════════════════════════════════════════════════════════════════════
# PSYCHOLOGY TRIGGER ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def _pick_trigger(audience: str, text: str) -> str:
    a = audience.lower()
    triggers = {
        "fear":      ["fresher", "student", "unemployed", "struggling"],
        "speed":     ["busy", "founder", "entrepreneur", "startup", "time"],
        "status":    ["professional", "expert", "leader", "brand", "authority"],
        "greed":     ["income", "money", "earn", "freelancer", "client", "revenue"],
        "relief":    ["tired", "easy", "simple", "finally", "just works", "tool"],
        "curiosity": ["secret", "nobody", "truth", "hidden", "actually", "real"],
        "belonging": ["community", "together", "join", "everyone", "we"],
        "ambition":  ["grow", "build", "scale", "launch", "future", "dream"],
    }
    scores = {t: 0 for t in triggers}
    for trigger, keywords in triggers.items():
        for kw in keywords:
            if kw in a or kw in text:
                scores[trigger] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else random.choice(list(triggers.keys()))


# ══════════════════════════════════════════════════════════════════════════════
# TREND RADAR — simulates awareness of current social/niche shifts
# ══════════════════════════════════════════════════════════════════════════════

TREND_BANK = {
    "career":    ["AI is changing hiring faster than anyone admits",
                  "LinkedIn is full of noise — authentic beats polished right now",
                  "Freshers who build in public are getting hired faster",
                  "The resume is becoming secondary — portfolio and presence matter more"],
    "ai":        ["Everyone's talking about AI but few show real use cases",
                  "AI fatigue is real — practical tools beat hype right now",
                  "The 'I use AI' flex is tired — the 'here's what I built' flex wins",
                  "AI tools that save actual time are going viral organically"],
    "fitness":   ["Mental health + fitness crossover content is exploding",
                  "Short (10-min) workout content is massively outperforming long videos",
                  "Rest days and recovery content is trending — anti-grind energy"],
    "finance":   ["Gen Z is rejecting traditional finance advice",
                  "Side income transparency content is getting enormous engagement",
                  "Debt-free journey content is one of the fastest growing niches"],
    "saas":      ["Founder-led content is outperforming paid ads across the board",
                  "Free tool launches are getting 10x organic reach of paid promotions",
                  "Build in public is shifting from trend to expectation"],
    "fashion":   ["Sustainable fashion content is growing fast",
                  "Anti-fast fashion takes are going viral across platforms",
                  "Outfit repeating is becoming a positive flex — not a flaw"],
    "education": ["Micro-learning (under 60 sec) is dominating all platforms",
                  "Free resource drops are the highest-converting content right now",
                  "Skill stacking content outperforms single-skill tutorials"],
    "general":   ["Authenticity is outperforming production quality right now",
                  "Creators who take clear positions are growing faster than neutral ones",
                  "Story-first content is seeing the highest saves and shares"],
}

def _pick_trend(niche: str, text: str) -> str:
    niche = niche.lower()
    matched = []
    for key, trends in TREND_BANK.items():
        if key in niche or key in text:
            matched.extend(trends)
    if not matched:
        matched = TREND_BANK["general"]
    seed = int(datetime.now().microsecond) % len(matched)
    return matched[seed]


# ══════════════════════════════════════════════════════════════════════════════
# ANGLE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def _build_angle(goal: str, audience: str, mood: str, trend: str, trigger: str) -> str:
    angles = {
        "funny":         f"Use comedy to disarm {audience} — make them laugh, then make them think about {goal}.",
        "savage":        f"Call out the comfortable lie that {audience} believe about their situation. {goal} is the honest alternative.",
        "emotional":     f"Lead with a moment of vulnerability that {audience} will deeply recognise. Then connect to {goal}.",
        "inspirational": f"Show the version of {audience} that{goal} makes possible — aspirational but believable.",
        "educational":   f"Break down something {audience} thinks they understand about {goal} but actually don't.",
        "controversial":  f"Take a position {audience} hasn't heard before about {goal}. Polarise to attract the right people.",
        "storytelling":  f"Tell a real-feeling story from the perspective of {audience} — journey, struggle, discovery of {goal}.",
        "curiosity":     f"Dangle one genuinely surprising insight about {goal} that {audience} can't scroll past.",
    }
    base = angles.get(mood, angles["curiosity"])
    return f"{base} Trend context: {trend}"


# ══════════════════════════════════════════════════════════════════════════════
# TONE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def _build_tone(platform: str, mood: str, audience: str) -> str:
    platform_base = {
        "linkedin":  "Warm authority — like a smart senior who actually cares",
        "instagram": "Punchy and relatable — feels like a smart friend texting you",
        "twitter":   "Sharp and confident — no hedging, no qualifiers",
        "facebook":  "Conversational and community-driven — inclusive energy",
    }
    mood_modifier = {
        "funny":         "with dry wit and self-awareness",
        "savage":        "with quiet confidence and zero apology",
        "emotional":     "with genuine vulnerability — earned, not performed",
        "inspirational": "with grounded optimism — realistic not toxic positive",
        "educational":   "with clarity and respect for the reader's intelligence",
        "controversial":  "with conviction — takes a side and owns it",
        "storytelling":  "with narrative pull — every sentence earns the next",
        "curiosity":     "with intrigue — gives enough to pull, holds back to hook",
    }
    base    = platform_base.get(platform, platform_base["linkedin"])
    mod     = mood_modifier.get(mood, "")
    return f"{base} — {mod}"


# ══════════════════════════════════════════════════════════════════════════════
# STYLE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def _build_style(platform: str, mood: str) -> str:
    styles = {
        ("linkedin",  "funny"):         "Short punchy paragraphs, self-aware joke, then pivot to insight",
        ("linkedin",  "emotional"):     "One-line opener, personal story, universal lesson",
        ("linkedin",  "educational"):   "Problem → insight → framework → takeaway",
        ("linkedin",  "controversial"):  "Bold statement → defend it calmly → invite pushback",
        ("linkedin",  "storytelling"):  "Scene-setting first line → tension → resolution",
        ("instagram", "funny"):         "Meme format — relatable top text, savage bottom text",
        ("instagram", "emotional"):     "Carousel — each slide one emotional beat",
        ("instagram", "curiosity"):     "Strong visual hook + 'swipe to see' energy",
        ("twitter",   "controversial"):  "Hot take → one line → mic drop",
        ("twitter",   "educational"):   "Thread format — promise big in tweet 1",
        ("twitter",   "funny"):         "One-liner with punchline timing",
    }
    key = (platform, mood)
    if key in styles:
        return styles[key]
    # Fallback combinations
    defaults = {
        "linkedin":  "Short punchy paragraphs. Line breaks for breathing room. One idea per block.",
        "instagram": "Visual-first thinking. Bold text overlay. Caption adds context not repetition.",
        "twitter":   "One punch per tweet. No throat-clearing. First word earns the second.",
        "facebook":  "Conversational. Question at end. Invites comment.",
    }
    return defaults.get(platform, "Clean, direct, one idea at a time.")


# ══════════════════════════════════════════════════════════════════════════════
# HOOK ENGINE — the most important part
# ══════════════════════════════════════════════════════════════════════════════

HOOK_POOL = {
    "linkedin": {
        "funny": [
            "My rejection email collection could fill a novel. Then I changed one thing.",
            "Spent 3 years doing this wrong. 3 weeks doing it right changed everything.",
            "My LinkedIn used to be a ghost town. Now I get messages I actually want.",
        ],
        "savage": [
            "Most people optimise their resume. Winners optimise their reputation.",
            "Job searching is broken. The people fixing it aren't the ones hiring you.",
            "Stop applying harder. Start becoming unforgettable.",
        ],
        "emotional": [
            "The day I got my 47th rejection, I stopped asking what's wrong with me.",
            "Nobody tells you how heavy silence feels after hitting send on 200 applications.",
            "I used to think I wasn't good enough. Turns out I was just invisible.",
        ],
        "educational": [
            "The LinkedIn algorithm rewards one behaviour above everything else. It's not posting.",
            "There are 3 types of professionals on LinkedIn. Only one actually grows.",
            "Your summary is the most underused asset on your entire profile. Here's why.",
        ],
        "controversial": [
            "Unpopular opinion: a good resume is the least important part of job searching.",
            "LinkedIn 'experts' are giving advice that actively hurts your chances.",
            "The people hiring you have already decided before they read your CV.",
        ],
        "storytelling": [
            "6 months unemployed. 1 tool changed the output. Here's the full story.",
            "I watched a fresher get hired over 5 experienced candidates. This is what they did.",
            "Two people. Same skills. Same experience. Completely different LinkedIn results.",
        ],
        "curiosity": [
            "The one section on your LinkedIn profile that almost nobody fills correctly.",
            "There's a pattern in every profile that gets callbacks. Most people skip it.",
            "I analysed 100 LinkedIn profiles that got hired fast. One thing stood out.",
        ],
        "inspirational": [
            "You're not behind. You're just about to find the thing that actually works.",
            "The right tool in the right moment doesn't just save time. It changes outcomes.",
            "Some people spend years stuck. Others find the shortcut. Both are choices.",
        ],
    },
    "instagram": {
        "funny": [
            "POV: You sent 100 applications and got 0 replies 💀",
            "Me explaining my gap year to every interviewer ever 😭",
            "When the job says 'entry level' but requires 5 years experience 🙃",
        ],
        "savage": [
            "Your competition isn't sleeping. And they found better tools than you.",
            "Talent without visibility is just a hobby.",
            "Nobody is coming to save your career. That's actually good news.",
        ],
        "emotional": [
            "To everyone who's been rejected more times than they want to count —",
            "The version of you that gets hired is closer than it feels right now.",
            "You're not failing. You're just not being seen yet.",
        ],
        "curiosity": [
            "What if the reason you're not getting interviews has nothing to do with your skills?",
            "The one thing top candidates do that others never find out about 👀",
            "Nobody talks about this part of job searching. Until now.",
        ],
        "controversial": [
            "Hot take: working hard is not enough and it never was.",
            "The resume advice you've been following is actively hurting you.",
            "Stop following career advice from people who've never hired anyone.",
        ],
    },
    "twitter": {
        "controversial": [
            "Most career advice is written by people who haven't applied for a job in 10 years.",
            "Applying to 200 jobs isn't hustle. It's avoiding the harder problem.",
            "Your resume isn't the problem. Your strategy is.",
        ],
        "funny": [
            "Recruiter: we'll be in touch. Also recruiter: *vanishes into the void*",
            "Entry level job requiring 5 years experience is just hazing for adults.",
            "Job searching in 2025 is just optimised rejection at scale.",
        ],
        "educational": [
            "The LinkedIn algorithm gives organic reach to exactly 3 post types. Thread 🧵",
            "Spent 30 days studying what gets callbacks. Here's what nobody says out loud:",
            "Freshers who get hired fast have one thing in common. It's not their degree.",
        ],
        "savage": [
            "Most people are optimising the wrong thing and wondering why nothing works.",
            "The job market isn't broken. Your approach to it is.",
            "Visibility beats qualification. Every single time.",
        ],
    },
}

def _build_hook(goal: str, audience: str, niche: str, platform: str,
                mood: str, trigger: str, history: list) -> str:
    # Get used hooks from history
    used_hooks = [h.get("hook", "") for h in history if isinstance(h, dict)] if history else []

    pool = HOOK_POOL.get(platform, HOOK_POOL["linkedin"])
    mood_pool = pool.get(mood, pool.get("curiosity", []))

    # Filter out previously used hooks
    fresh = [h for h in mood_pool if h not in used_hooks]
    candidates = fresh if fresh else mood_pool

    # Pick using microsecond seed for variety
    seed = int(datetime.now().microsecond) % len(candidates)
    return candidates[seed]


# ══════════════════════════════════════════════════════════════════════════════
# POST BUILDER — platform-native format
# ══════════════════════════════════════════════════════════════════════════════

def _build_post(hook: str, goal: str, audience: str, platform: str,
                mood: str, niche: str, trigger: str) -> str:

    g = goal.strip()
    a = audience.strip()

    if platform == "linkedin":
        return _linkedin_post(hook, g, a, mood, trigger)
    elif platform == "instagram":
        return _instagram_post(hook, g, a, mood)
    elif platform == "twitter":
        return _twitter_post(hook, g, mood)
    else:
        return _linkedin_post(hook, g, a, mood, trigger)


def _linkedin_post(hook: str, goal: str, audience: str, mood: str, trigger: str) -> str:
    bodies = {
        "funny": (
            f"{hook}\n\n"
            f"Here's the thing nobody tells {audience}:\n\n"
            f"The system isn't designed for you to figure it out alone.\n\n"
            f"That's not a motivational line. It's just true.\n\n"
            f"{goal} exists because we got tired of watching capable people stay invisible.\n\n"
            f"You don't need to work harder.\n"
            f"You need to work on the right thing."
        ),
        "emotional": (
            f"{hook}\n\n"
            f"I know what that feels like.\n\n"
            f"The silence after hitting send.\n"
            f"The wondering if something is wrong with you.\n"
            f"The slowly shrinking confidence.\n\n"
            f"Nothing was wrong with you.\n\n"
            f"The problem was visibility, not value.\n\n"
            f"That's the whole reason {goal} exists."
        ),
        "educational": (
            f"{hook}\n\n"
            f"Most {audience} skip this entirely.\n\n"
            f"Here's what the data actually shows:\n\n"
            f"→ First impression is formed in under 7 seconds\n"
            f"→ Most profiles are optimised for the wrong reader\n"
            f"→ The highest-performing profiles all share one structure\n\n"
            f"This is exactly what {goal} is built around.\n\n"
            f"Not theory. Actual pattern recognition from real results."
        ),
        "controversial": (
            f"{hook}\n\n"
            f"I'll defend this.\n\n"
            f"Every {audience} is told the same things:\n"
            f"→ Tailor your resume\n"
            f"→ Network more\n"
            f"→ Apply consistently\n\n"
            f"All correct. None sufficient.\n\n"
            f"The missing piece is positioning — and nobody teaches it.\n\n"
            f"That gap is exactly what {goal} fills."
        ),
        "storytelling": (
            f"{hook}\n\n"
            f"The difference wasn't talent.\n"
            f"It wasn't connections.\n"
            f"It wasn't even experience.\n\n"
            f"It was how they showed up before the interview existed.\n\n"
            f"Digital presence. Strategic visibility. Consistent signal.\n\n"
            f"{goal} makes that the default — not the exception."
        ),
    }
    default = (
        f"{hook}\n\n"
        f"The {audience} who grow fastest aren't working harder.\n\n"
        f"They found leverage.\n\n"
        f"{goal} is that leverage.\n\n"
        f"Built specifically for people who are done doing this the hard way."
    )
    return bodies.get(mood, default)


def _instagram_post(hook: str, goal: str, audience: str, mood: str) -> str:
    captions = {
        "funny":     f"{hook}\n\nSave this. You'll need it when it hits different at 2am.\n\n#reallife #careerlife #ai #relatable",
        "emotional": f"{hook}\n\nYou're closer than it feels. Promise.\n\n#motivation #growth #career #forreal",
        "savage":    f"{hook}\n\nSorry not sorry.\n\n#truth #growth #nofluff #career",
        "curiosity": f"{hook}\n\nSwipe → if you actually want to know. 👀\n\n#career #ai #hidden #growthmindset",
    }
    default = f"{hook} ✨\n\nThis is {goal} — built for people who are tired of waiting.\n\n#ai #productivity #career #growth"
    return captions.get(mood, default)


def _twitter_post(hook: str, goal: str, mood: str) -> str:
    posts = {
        "controversial": f"{hook}\n\nChange my mind.",
        "funny":         f"{hook}\n\n(I will not elaborate further.)",
        "educational":   f"{hook}\n\nThread below 🧵",
        "savage":        f"{hook}\n\nThe truth has always been free.",
    }
    default = f"{hook}\n\n{goal} fixes this."
    return posts.get(mood, default)


# ══════════════════════════════════════════════════════════════════════════════
# CTA ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def _build_cta(platform: str, trigger: str, goal: str) -> str:
    ctas = {
        "linkedin": {
            "fear":      "Don't let this be the thing you wish you'd found sooner. Try it free.",
            "speed":     f"Set up {goal} in under 5 minutes. Link in bio.",
            "status":    f"This is what people who take their career seriously use. Link below.",
            "curiosity": f"See why {goal} keeps showing up in conversations like this. Link in bio.",
            "relief":    f"Finally something that just works. Try {goal} free today.",
            "ambition":  f"If you're serious about this — {goal} is waiting. Link in bio.",
        },
        "instagram": {
            "fear":      "Don't sleep on this. Link in bio. 🔗",
            "speed":     "5 minutes to set up. Results in 7 days. Link in bio. ⚡",
            "curiosity": "Find out why everyone's been asking about this. Link in bio. 👀",
            "relief":    "Free. Simple. Actually works. Link in bio. ✨",
        },
        "twitter": {
            "fear":      f"Try {goal} before you need it. Free.",
            "speed":     f"{goal}. 5 min setup. Actual results. Link in bio.",
            "curiosity": f"Curious? {goal} — link in bio.",
            "status":    f"The ones winning already found {goal}.",
        },
    }
    platform_ctas = ctas.get(platform, ctas["linkedin"])
    return platform_ctas.get(trigger, f"Try {goal} free today — link in bio.")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE BRAIN
# ══════════════════════════════════════════════════════════════════════════════

def _build_image_idea(platform: str, mood: str, niche: str) -> str:
    ideas = {
        ("linkedin",  "educational"):   "Premium carousel — dark navy, one stat per slide, white bold font, subtle purple accent",
        ("linkedin",  "storytelling"):  "Single image — quote card with one powerful line, minimal design, no clutter",
        ("linkedin",  "controversial"):  "Text-only post (no image) — the words should be enough to stop the scroll",
        ("instagram", "funny"):         "Classic meme format — top text sets up, bottom text delivers. High contrast. Bold font.",
        ("instagram", "emotional"):     "Soft gradient background. Single line of text. No clutter. Feels like a note to self.",
        ("instagram", "curiosity"):     "Carousel — cover slide asks the question, swipe to reveal. Bold typography.",
        ("twitter",   "controversial"):  "Black card. White text. One sentence. Zero decoration. Retweet-designed.",
        ("twitter",   "funny"):         "No image needed — the copy is the creative",
        ("twitter",   "educational"):   "Simple infographic or text thread — data speaks louder than design here",
    }
    key = (platform, mood)
    if key in ideas:
        return ideas[key]
    defaults = {
        "linkedin":  "Clean authority visual — minimal, premium, text-led",
        "instagram": "Bold scroll-stopping graphic — high contrast, big typography",
        "twitter":   "Quote card or no image — let the words do the work",
        "facebook":  "Relatable scene image with text overlay — community energy",
    }
    return defaults.get(platform, "Bold visual matching the hook energy — text-first, minimal decoration")


# ══════════════════════════════════════════════════════════════════════════════
# SELF-EVALUATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def _build_why(hook: str, mood: str, trigger: str, platform: str) -> str:
    reasons = {
        "funny":         "Comedy disarms the scroll reflex — people pause, share, then engage with the message underneath.",
        "savage":        "Direct takes with zero hedging attract the audience that's tired of soft advice. High conviction = high trust.",
        "emotional":     "Vulnerability in the first line creates an immediate sense of 'this person gets it' — the hardest thing to fake.",
        "educational":   "Specific, non-obvious insights build credibility fast. People save and return to useful content.",
        "controversial":  "Taking a clear position polarises but also magnetises. The right readers will defend you — that's engagement.",
        "storytelling":  "Story structure triggers the brain to keep reading to find out what happened. Completion = connection.",
        "curiosity":     "Opening a loop the brain wants closed is the oldest hook in writing. Still works. Always will.",
        "inspirational": "Aspirational content gets shared by people who want to project the version of themselves it describes.",
    }
    base   = reasons.get(mood, "Post is designed to create a pause in the scroll and earn the read.")
    p_note = {
        "linkedin":  " LinkedIn rewards dwell time — this post is structured to earn it.",
        "instagram": " Instagram's algorithm prioritises saves and shares — this creative is designed for both.",
        "twitter":   " Twitter rewards replies and retweets — this take is designed to invite both.",
        "facebook":  " Facebook surfaces posts with comments — the CTA and tone invite response.",
    }
    return base + p_note.get(platform, "")


# ══════════════════════════════════════════════════════════════════════════════
# REPEAT PROTECTION SCORE
# ══════════════════════════════════════════════════════════════════════════════

def _repeat_score(hook: str, history: list) -> int:
    """
    Returns 0-100. Higher = fresher.
    Compares new hook against history using character-level similarity.
    """
    if not history:
        return 100

    used_hooks = [h.get("hook", "") for h in history if isinstance(h, dict)]
    if not used_hooks:
        return 100

    hook_sig = hashlib.md5(hook.lower().encode()).hexdigest()

    # Check for exact or near-exact matches
    for old in used_hooks:
        old_sig = hashlib.md5(old.lower().encode()).hexdigest()
        if hook_sig == old_sig:
            return 10  # Exact repeat

        # Check opening words
        new_words = hook.lower().split()[:5]
        old_words = old.lower().split()[:5]
        overlap = len(set(new_words) & set(old_words))
        if overlap >= 4:
            return 40  # Very similar opening

    # Score based on total history depth
    base_score = max(60, 100 - (len(used_hooks) * 3))
    return min(base_score, 98)