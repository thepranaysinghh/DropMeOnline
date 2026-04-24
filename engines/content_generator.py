# content_generator.py — Mode-aware, platform-native content generator
# Uses intent_parser v2 — never dumps raw prompt text into posts

from engines.intent_parser import parse_intent
from datetime import datetime
import random


def _seed() -> int:
    return int(datetime.now().microsecond) % 8


# ══════════════════════════════════════════════════════════════════════════════
# MODE-AWARE DISPATCHER
# ══════════════════════════════════════════════════════════════════════════════

def generate_content(goal: str) -> dict:
    intent = parse_intent(goal)
    mode   = intent["mode"]

    li = _linkedin(intent)
    ig = _instagram(intent)
    tw = _twitter(intent)

    return {
        "linkedin":  li,
        "instagram": ig,
        "twitter":   tw,
        "_intent":   intent,
    }


# ══════════════════════════════════════════════════════════════════════════════
# LINKEDIN
# ══════════════════════════════════════════════════════════════════════════════

def _linkedin(i: dict) -> str:
    mode   = i["mode"]
    tone   = i["tone"]
    length = i["length"]
    p      = i["product"]
    ref    = i["product_ref"]
    aud    = i["audience"]
    subj   = i["subject"]
    niche  = i["niche"]
    s      = _seed()

    if length == "short":
        return _li_short(mode, p, ref, aud, subj, s)
    if length == "thread":
        return _li_thread(mode, p, ref, aud, subj, niche)

    # Mode-specific generators
    if mode == "product":
        return _li_product(p, ref, aud, tone, s)
    if mode == "personal":
        return _li_personal(subj, aud, niche, tone, s)
    if mode == "freelancer":
        return _li_freelancer(subj, ref, aud, tone, s)
    if mode == "career":
        return _li_career(aud, niche, tone, s)
    if mode == "creator":
        return _li_topic(subj, aud, tone, s)
    # topic / default
    return _li_topic(subj, aud, tone, s)


def _li_short(mode, p, ref, aud, subj, s):
    opts = {
        "product": [
            f"Most {aud} are doing this the hard way.\n\n{p} exists so they don't have to.",
            f"Built {p} for {aud}.\n\nThe feedback has been humbling.\n\nThank you.",
            f"The best tools disappear into your workflow.\n\nThat's what we built {p} to do.",
        ],
        "personal": [
            f"A year into this journey — things look completely different from where I started.",
            f"The most underrated move in any career: showing up consistently before anyone's watching.",
            f"You don't need a big audience to have a strong professional brand. You need a clear point of view.",
        ],
        "career": [
            f"Most {aud} optimise for the wrong thing at the start of their job search.\n\nFocus on visibility, not just applications.",
            f"The job market doesn't reward the most qualified. It rewards the most visible.\n\nStart building that now.",
        ],
        "topic": [
            f"The most common mistake with {subj}: treating it as a tactic instead of a strategy.",
            f"{subj} is not complicated. But it requires doing the uncomfortable thing consistently.",
        ],
    }
    choices = opts.get(mode, opts["topic"])
    return choices[s % len(choices)]


def _li_thread(mode, p, ref, aud, subj, niche):
    if mode == "product":
        return (
            f"Why we built {p} — and what we learned from it. Full thread 🧵\n\n"
            f"1/ The problem: {aud} had no tool built specifically for them. Generic ones kept failing.\n\n"
            f"2/ Most tools are built by people who heard about the problem secondhand. We lived it.\n\n"
            f"3/ First principle: if you have to explain why someone should use it, you haven't solved it yet.\n\n"
            f"4/ We shipped v1 ugly. Got feedback. Shipped again. The cycle is the product.\n\n"
            f"5/ The biggest lesson: distribution matters as much as the product. Maybe more.\n\n"
            f"6/ {p} is live. Built for {aud}. Free to start.\n\nRT if this thread helped."
        )
    if mode == "personal":
        return (
            f"Everything I've learned in the last 12 months — condensed. Save this 🧵\n\n"
            f"1/ Learning in public is uncomfortable at first. That discomfort is a signal, not a warning.\n\n"
            f"2/ The people who grow fastest aren't the most talented. They're the most consistent.\n\n"
            f"3/ Your audience doesn't need your highlights. They need your honest process.\n\n"
            f"4/ Every post you don't write is feedback someone else doesn't get.\n\n"
            f"5/ One year of consistent posting will compound into something you can't plan for.\n\n"
            f"Follow if this resonated."
        )
    if mode == "career":
        return (
            f"What I wish I knew before starting my job search — full breakdown 🧵\n\n"
            f"1/ Applying in bulk is not a strategy. It's a coping mechanism.\n\n"
            f"2/ The jobs that matter are filled before they're posted. Network accordingly.\n\n"
            f"3/ Your LinkedIn profile is read before your resume. Treat it that way.\n\n"
            f"4/ One strong referral beats 50 cold applications. Every single time.\n\n"
            f"5/ Recruiters spend 6 seconds on your profile. Give them a reason to stop.\n\n"
            f"Follow for more honest career content."
        )
    # topic / default
    return (
        f"Everything I know about {subj} — one thread 🧵\n\n"
        f"1/ Most people start with tactics. They should start with understanding.\n\n"
        f"2/ The fundamentals of {subj} haven't changed. The environment around them has.\n\n"
        f"3/ The people winning at {subj} right now: consistent, specific, patient.\n\n"
        f"4/ The people losing: chasing shortcuts that compound into nothing.\n\n"
        f"5/ Final: {subj} is not complicated. But it requires doing obvious things for longer than feels reasonable.\n\n"
        f"Follow for more."
    )


def _li_product(p, ref, aud, tone, s):
    opts = {
        "bold": (
            f"Unpopular opinion: most tools built for {aud} are designed by people who've never been {aud}.\n\n"
            f"That's why they fall short.\n\n"
            f"We built {p} differently:\n\n"
            f"→ Starting from the real problem, not the obvious one\n"
            f"→ Optimising for outcomes, not feature counts\n"
            f"→ Shipping fast and listening faster\n\n"
            f"The result: something {aud} actually use.\n\n"
            f"That's the only metric that matters to us."
        ),
        "emotional": (
            f"The reason we built {p}:\n\n"
            f"We watched talented {aud} get stuck.\n\n"
            f"Not because they weren't capable.\n\n"
            f"Because the tools available weren't built for them. They were built for someone else's version of the problem.\n\n"
            f"We got tired of that.\n\n"
            f"So we built {ref}. For {aud}. From the beginning.\n\n"
            f"If that's you — this is for you."
        ),
        "funny": (
            f"We built {p} because we were tired of watching {aud} overcomplicate something that should be simple.\n\n"
            f"The process before {ref}:\n"
            f"→ Hours of manual work\n"
            f"→ Generic advice that doesn't fit\n"
            f"→ Pretending everything is under control\n\n"
            f"The process with {ref}:\n"
            f"→ Actually just works\n\n"
            f"We're not going to apologise for making it this easy."
        ),
        "educational": (
            f"3 things most {aud} don't realise until it's too late:\n\n"
            f"1. The biggest bottleneck isn't effort — it's the right system\n"
            f"2. Manual processes don't scale, and they don't need to\n"
            f"3. The right tool removes friction before you even notice it\n\n"
            f"This is exactly what {p} is built to do.\n\n"
            f"Not another layer of complexity.\n"
            f"A simpler path to the outcome {aud} actually want."
        ),
    }
    defaults = [
        (
            f"We built {p} for one simple reason:\n\n"
            f"{aud.capitalize()} deserve a tool that actually understands their problem.\n\n"
            f"Not a generic solution. Not another feature nobody asked for.\n\n"
            f"Just the thing that moves the needle — simply, quickly, reliably.\n\n"
            f"That's {ref}."
        ),
        (
            f"Here's what building {p} taught us about {aud}:\n\n"
            f"They don't want more features.\n\n"
            f"They want less friction.\n\n"
            f"Every decision we made in {ref} was filtered through one question:\n"
            f"'Does this reduce friction or add it?'\n\n"
            f"The answer shaped everything."
        ),
    ]
    return opts.get(tone, defaults[s % len(defaults)])


def _li_personal(subj, aud, niche, tone, s):
    tech_niches = {"tech", "ai", "saas", "general"}
    is_tech = niche in tech_niches

    opts_bold = (
        f"Controversial take on being a {subj}:\n\n"
        f"Most advice you'll find is written by people who figured it out years ago.\n\n"
        f"The context has changed. The advice hasn't.\n\n"
        f"Here's what actually works right now:\n\n"
        f"→ Building in public > staying silent\n"
        f"→ One strong post > ten average ones\n"
        f"→ Showing your process > showing your highlights\n\n"
        f"The people growing fastest in this space aren't the most experienced.\n\n"
        f"They're the most honest."
    )
    opts_educational = (
        f"Things I've learned as a {subj} that I wish someone had told me earlier:\n\n"
        f"1. Your learning compounds faster when you document it publicly\n"
        f"2. The people you want to connect with are watching the ones who show up consistently\n"
        f"3. Done is infinitely better than perfect, especially at the start\n"
        f"4. Your niche will find you if you start before it's obvious\n\n"
        f"If you're just starting: start now, not when it feels ready."
    )
    opts_default = [
        (
            f"A year ago, I would not have believed where being a {subj} would take me.\n\n"
            f"Not because of luck.\n\n"
            f"Because of one shift: I started sharing the process, not just the outcome.\n\n"
            f"The audience doesn't want your polished results.\n\n"
            f"They want your honest, unfiltered journey.\n\n"
            f"That's what I'm sharing. Follow if you want to see it unfold."
        ),
        (
            f"The most underrated competitive advantage as a {subj}:\n\n"
            f"Showing up before you're 'ready'.\n\n"
            f"The people you'll learn the most from are watching the ones who started before they had all the answers.\n\n"
            f"Be that person."
        ),
    ]
    if tone == "bold":        return opts_bold
    if tone == "educational": return opts_educational
    return opts_default[s % len(opts_default)]


def _li_freelancer(subj, ref, aud, tone, s):
    opts = [
        (
            f"The hardest thing about running {ref}:\n\n"
            f"It's not the work. The work is the easy part.\n\n"
            f"It's convincing people that the work is worth paying for.\n\n"
            f"Here's what actually changed that for us:\n\n"
            f"→ Showing the process, not just the output\n"
            f"→ Being specific about who we help and how\n"
            f"→ Building trust before pitching anything\n\n"
            f"{aud.capitalize()} don't hire vendors. They hire people they trust."
        ),
        (
            f"Most {aud} don't know what they're looking for until they see it done right.\n\n"
            f"That's not a criticism. It's an opportunity.\n\n"
            f"For {ref}, it means:\n\n"
            f"→ Education first, pitch second\n"
            f"→ Examples over explanations\n"
            f"→ Trust over transactions\n\n"
            f"The clients we work with longest found us through content, not cold outreach."
        ),
    ]
    return opts[s % len(opts)]


def _li_career(aud, niche, tone, s):
    opts_bold = (
        f"Uncomfortable truth about the job market:\n\n"
        f"It doesn't reward the most qualified. It rewards the most visible.\n\n"
        f"Most {aud} spend 90% of their time on the resume.\n\n"
        f"The ones getting hired spend 90% of their time on visibility.\n\n"
        f"That's not fair. But it is the game.\n\n"
        f"Learn it, or keep losing to people who did."
    )
    opts_tech = (
        f"What nobody tells {aud} about breaking into tech:\n\n"
        f"The technical skills get your foot in the door.\n\n"
        f"Your online presence determines which door opens.\n\n"
        f"Here's what actually moves the needle:\n\n"
        f"→ A GitHub that shows you build things, not just follow tutorials\n"
        f"→ A LinkedIn that reads like an engineer, not a student\n"
        f"→ One consistent thing you share publicly in your niche\n\n"
        f"The interview is just confirmation. The decision is made before you walk in."
    )
    opts_default = [
        (
            f"The job search advice most {aud} get is well-intentioned and completely wrong for the current market.\n\n"
            f"'Apply to everything' → leads to burnout, not offers\n"
            f"'Perfect your resume' → most resumes aren't read by humans first\n"
            f"'Network more' → vague advice that ignores what networking actually is\n\n"
            f"What actually works:\n\n"
            f"Be specific. Be visible. Be consistent.\n\n"
            f"The market rewards the prepared and the patient."
        ),
        (
            f"I've watched hundreds of {aud} go through the same cycle:\n\n"
            f"Apply → wait → rejection → repeat\n\n"
            f"The ones who break the cycle do one thing differently:\n\n"
            f"They stop waiting to be found and start making themselves findable.\n\n"
            f"LinkedIn. GitHub. One area of genuine expertise made public.\n\n"
            f"That's the whole strategy."
        ),
    ]
    if tone == "bold":                         return opts_bold
    if niche == "tech" or niche == "career":   return opts_tech
    return opts_default[s % len(opts_default)]


def _li_topic(subj, aud, tone, s):
    opts = {
        "bold": (
            f"Unpopular opinion about {subj}:\n\n"
            f"90% of what you've read is optimised for engagement — not results.\n\n"
            f"Here's what actually works:\n\n"
            f"→ Specificity beats volume every time\n"
            f"→ One strong move outperforms ten average ones\n"
            f"→ {aud.capitalize()} don't want more content — they want the right insight\n\n"
            f"The people winning at {subj} right now aren't doing more.\n\n"
            f"They're thinking harder before they act.\n\n"
            f"That's the edge most people skip."
        ),
        "educational": (
            f"Most people approach {subj} wrong. Here's why:\n\n"
            f"They start with tactics. They should start with fundamentals.\n\n"
            f"The 3-part framework that actually works:\n\n"
            f"1. Understand what you're optimising for (output or outcome?)\n"
            f"2. Remove what's not working before adding more\n"
            f"3. Measure leading indicators, not just results\n\n"
            f"Once you have those three locked in, {subj} becomes execution — not guesswork.\n\n"
            f"The strategy is simple. The discipline to follow it is where most people fall off."
        ),
        "funny": (
            f"My relationship with {subj}, summarised:\n\n"
            f"Month 1: Completely confident\n"
            f"Month 2: Completely lost\n"
            f"Month 3: Uncomfortably aware of how much I don't know\n"
            f"Month 6: Still figuring it out, but now with better questions\n\n"
            f"If you're in months 2 or 3: that's not a setback. That's the curriculum."
        ),
    }
    default = (
        f"Here's what changes everything about {subj}:\n\n"
        f"Most {aud} are optimising for the wrong thing.\n\n"
        f"They want reach. They should want resonance.\n\n"
        f"Because reach without resonance is just noise.\n\n"
        f"The accounts growing fastest right now have one thing in common:\n"
        f"→ They say things their audience needed to hear\n"
        f"→ They show up before anyone's watching\n"
        f"→ They're specific when everyone else is vague\n\n"
        f"That's the whole playbook."
    )
    return opts.get(tone, default)


# ══════════════════════════════════════════════════════════════════════════════
# INSTAGRAM
# ══════════════════════════════════════════════════════════════════════════════

def _instagram(i: dict) -> str:
    mode   = i["mode"]
    tone   = i["tone"]
    length = i["length"]
    p      = i["product"]
    ref    = i["product_ref"]
    aud    = i["audience"]
    subj   = i["subject"]
    niche  = i["niche"]
    s      = _seed()

    if length == "short":
        return f"Built for {aud}. That's {p}. 🔥\n\n#buildinpublic #growth"

    hashtag_sets = {
        "career":    "#career #personalbrand #linkedin #jobsearch #growthmindset",
        "ai":        "#ai #aitools #futureofwork #buildinpublic #techstartup",
        "startup":   "#startup #founder #buildinpublic #entrepreneurship #indiehacker",
        "tech":      "#tech #developer #coding #buildinpublic #softwareengineering",
        "fitness":   "#fitness #healthylifestyle #workout #mindset #motivation",
        "finance":   "#personalfinance #investing #moneymindset #financialfreedom",
        "education": "#learning #selfimprovement #skills #growthmindset #education",
        "general":   "#growth #mindset #motivation #growthmindset #buildinpublic",
    }
    tags = hashtag_sets.get(niche, hashtag_sets["general"])

    if mode == "creator" or tone == "funny":
        posts = [
            f"POV: You're a {aud.split()[0]} who just found out this exists 👀\n\nBefore: doing everything manually and pretending it's fine 💀\nAfter: actually having a system that works 😤\n\nDrop a 🙋 if this is your arc.",
            f"Nobody talks about the actual reason most {aud} stay stuck.\n\nIt's not talent.\nIt's not connections.\n\nIt's using the wrong tools for the right problem. 🔥\n\nSave this if you needed to hear it. 📌",
            f"Things that are somehow easier than fixing your {subj} setup:\n\n- Scrolling for 2 hours\n- Reorganising your phone\n- Planning to start next Monday\n\n(been there) 💀",
        ]
        return posts[s % len(posts)] + f"\n\n{tags}"

    if mode == "career":
        posts = [
            f"To every {aud.split()[0]} who's been applying in silence —\n\nYour effort is real. The strategy just needs adjusting. 🌱\n\nThe ones who break through don't work harder. They work more visibly.\n\nSave this. Come back to it. 📌",
            f"Harsh truth: 80% of jobs are filled before they're posted.\n\nThe {aud.split()[0]}s who get those jobs aren't luckier.\n\nThey're more visible, more connected, more vocal about what they can do. 🔥\n\nStart building that now.",
        ]
        return posts[s % len(posts)] + f"\n\n{tags}"

    if mode == "product":
        posts = [
            f"Built {p} for {aud} who are tired of doing it the hard way. ✨\n\nSimple. Fast. Actually works.\n\nSave this if you've been looking for something like this. 📌",
            f"The thing about {ref}?\n\nIt doesn't try to do everything.\n\nIt does the one thing {aud} actually need — and does it well. 🎯\n\nLink in bio.",
        ]
        return posts[s % len(posts)] + f"\n\n{tags}"

    # personal / topic / default
    posts = [
        f"The version of you that figured out {subj.lower()}? 🚀\n\nThat version exists.\n\nYou're just one consistent month away from meeting them.\n\nDouble tap if you needed this. ✨",
        f"Reminder for {aud}: 🌱\n\nProgress doesn't always look like progress when you're in it.\n\nKeep going. The compounding is happening even when you can't see it.",
    ]
    return posts[s % len(posts)] + f"\n\n{tags}"


# ══════════════════════════════════════════════════════════════════════════════
# TWITTER
# ══════════════════════════════════════════════════════════════════════════════

def _twitter(i: dict) -> str:
    mode   = i["mode"]
    tone   = i["tone"]
    length = i["length"]
    p      = i["product"]
    ref    = i["product_ref"]
    aud    = i["audience"]
    subj   = i["subject"]
    niche  = i["niche"]
    s      = _seed()

    if length == "short":
        opts = {
            "product":   [f"Built {p} for {aud}. Shipped before it was perfect. Zero regrets.", f"{p} for {aud}. Free to start."],
            "personal":  [f"Best career move I made: sharing the process before I had the answers.", f"Consistency > intensity. Every single time."],
            "career":    [f"Most {aud}: optimise resume.\nThe ones getting hired: optimise visibility.", f"The job isn't posted yet. The decision is already forming."],
            "topic":     [f"{subj}: less complicated than people make it, harder than they expect.", f"The thing about {subj} nobody says out loud:"],
        }
        choices = opts.get(mode, opts["topic"])
        return choices[s % len(choices)]

    if length == "thread":
        return _tw_thread(mode, p, ref, aud, subj, niche, s)

    # Single punchy tweets
    opts = {
        "bold": {
            "product":   f"Most tools for {aud} are built by people who've never been {aud}.\n\nThat's why they fail.\n\nWe built {p} from the inside. There's a difference.",
            "personal":  f"Controversial: the advice you're following is probably outdated.\n\nThe context changed. The advice didn't.\n\nRun your own experiments.",
            "career":    f"Hot take: the {aud} who are struggling aren't the least qualified.\n\nThey're the least visible.\n\nFix visibility before fixing the resume.",
            "topic":     f"Unpopular opinion about {subj}:\n\nMost people are optimising for the wrong metric.\n\nChange the metric. Change the outcome.",
        },
        "funny": {
            "product":   f"{aud.capitalize()} after finding {p}:\n\n'Why didn't this exist before'\n\n(it kind of did, we just made it actually work)",
            "personal":  f"My journey as a {subj}:\n\nMonth 1: confident\nMonth 2: humbled\nMonth 6: dangerously self-aware\n\n(recommend)",
            "career":    f"Job application status: sent to void.\n\nVoid: 👁️\n\nMe: 👁️\n\n(I will not give up)",
            "topic":     f"The {subj} learning curve:\n\n'This is easy'\n'Wait'\n'Oh no'\n'Oh'\n'Oh wait I get it now'\n\n(every time)",
        },
        "educational": {
            "product":   f"The {p} principle:\n\n→ Less friction\n→ More outcome\n→ Built for {aud}\n\nSimple to say. Took years to get right.",
            "personal":  f"Things that compound in your career:\n\n→ Writing publicly\n→ Building in public\n→ Being consistently useful\n\nNone of these have shortcuts.",
            "career":    f"What gets {aud} hired in 2025:\n\n→ Visible work, not just applications\n→ Specific skills, not just 'eager to learn'\n→ Warm introductions, not cold resumes\n\nThe game has changed.",
            "topic":     f"The {subj} framework:\n\n→ Clarity before tactics\n→ Audience before algorithm\n→ Consistency before perfection\n\nIn that order. Always.",
        },
    }
    tone_map = opts.get(tone, opts.get("educational", {}))
    return tone_map.get(mode, tone_map.get("topic", f"The thing about {subj} that changes everything:\n\nDoing the obvious thing for longer than feels reasonable."))


def _tw_thread(mode, p, ref, aud, subj, niche, s):
    if mode == "product":
        return (
            f"Built {p} for {aud}. Here's what nobody tells you about shipping something real 🧵\n\n"
            f"1/ The problem we were solving wasn't the one we started with.\n\n"
            f"2/ First principle: if you have to explain why someone should use it, you haven't solved it yet.\n\n"
            f"3/ We shipped ugly. Got feedback. Shipped again. That cycle is the product.\n\n"
            f"4/ The biggest lesson: distribution > product quality in the early days.\n\n"
            f"5/ {p} is live. Built for {aud}. Learned the hard way.\n\nRT if this helped."
        )
    if mode == "career":
        return (
            f"What I wish I knew before my job search. Thread 🧵\n\n"
            f"1/ Applying in bulk is not a strategy. It's a coping mechanism.\n\n"
            f"2/ The jobs that matter are filled before they're posted.\n\n"
            f"3/ One strong referral beats 50 cold applications.\n\n"
            f"4/ Your LinkedIn profile is read before your resume. Make it count.\n\n"
            f"5/ The interview is confirmation. The decision is made before you walk in.\n\nRT if this helps someone."
        )
    if mode == "freelancer":
        return (
            f"Freelancing mistakes I made so you don't have to 🧵\n\n"
            f"1/ Competing on price = racing to the bottom. Stop.\n\n"
            f"2/ Not having a clear niche = attracting the wrong clients.\n\n"
            f"3/ Waiting for referrals > creating content that makes referrals inevitable.\n\n"
            f"4/ Charging for hours instead of outcomes. Big mistake.\n\n"
            f"5/ Not building an audience while doing client work. Do both.\n\nRT if this landed."
        )
    # topic / personal
    return (
        f"Everything I know about {subj} in one thread 🧵\n\n"
        f"1/ Most people start with tactics. Wrong. Start with fundamentals.\n\n"
        f"2/ The fundamentals of {subj}: clarity, consistency, patience.\n\n"
        f"3/ Tactics compound on top of fundamentals. Not the other way around.\n\n"
        f"4/ The people winning at {subj} aren't doing more. They're doing the right things for longer.\n\n"
        f"5/ Final: {subj} is not complicated. It requires doing obvious things consistently.\n\nRT if this helped."
    )