# competitor_engine.py — Market Intelligence Engine
# Infers competitors, trends, gaps, and positioning from product goal

def analyze_market(goal: str) -> dict:
    """
    Input:  goal (string) — e.g. "Promote AI resume tool"
    Output: market intelligence dict with competitors, trends, gaps, hooks, positioning
    Note:   Rule-based inference (real-time data via API in future phase)
    """

    g    = goal.strip()
    text = goal.lower()

    niche = _detect_niche(text)

    return {
        "competitors":       _get_competitors(niche),
        "trends":            _get_trends(niche),
        "saturated_topics":  _get_saturated(niche),
        "opportunities":     _get_opportunities(niche, g),
        "viral_hooks":       _get_viral_hooks(niche, g),
        "positioning":       _get_positioning(niche, g),
    }


# ── Niche detector ─────────────────────────────────────────────────────────────

def _detect_niche(text: str) -> str:
    niches = {
        "resume":      "career_tools",
        "job":         "career_tools",
        "linkedin":    "career_tools",
        "fitness":     "fitness",
        "workout":     "fitness",
        "health":      "fitness",
        "saas":        "saas",
        "tool":        "saas",
        "software":    "saas",
        "ai":          "ai_tech",
        "chatbot":     "ai_tech",
        "automation":  "ai_tech",
        "fashion":     "fashion",
        "clothing":    "fashion",
        "style":       "fashion",
        "food":        "food",
        "restaurant":  "food",
        "recipe":      "food",
        "course":      "education",
        "learn":       "education",
        "tutorial":    "education",
        "agency":      "agency",
        "marketing":   "agency",
        "freelance":   "agency",
        "finance":     "finance",
        "invest":      "finance",
        "money":       "finance",
    }
    for keyword, niche in niches.items():
        if keyword in text:
            return niche
    return "general"


# ── Data banks per niche ───────────────────────────────────────────────────────

def _get_competitors(niche: str) -> list:
    data = {
        "career_tools": ["LinkedIn Premium", "Resume.io", "Novoresume", "Career coaches on Instagram", "Job board content pages"],
        "fitness":       ["MyFitnessPal", "Nike Training Club", "Gym influencers", "YouTube fitness channels", "Whoop / Fitbit content"],
        "saas":          ["Product Hunt listings", "Indie hackers community", "SaaS review blogs", "G2 / Capterra competitors", "Bootstrapped founder pages"],
        "ai_tech":       ["ChatGPT content creators", "AI tool directories", "Tech YouTube channels", "AI newsletter writers", "Product Hunt AI launches"],
        "fashion":       ["SHEIN social pages", "Fashion influencers", "Zara / H&M Instagram", "Style bloggers", "Pinterest fashion boards"],
        "food":          ["Food bloggers", "Recipe Instagram accounts", "MasterChef pages", "Zomato / Swiggy content", "YouTube cooking channels"],
        "education":     ["Coursera / Udemy pages", "YouTube educators", "Newsletter teachers", "LinkedIn Learning", "Notion template sellers"],
        "agency":        ["Fiverr service pages", "Marketing agency LinkedIn pages", "Freelancer portfolio sites", "Cold outreach coaches", "Growth hacking blogs"],
        "finance":       ["Personal finance influencers", "Zerodha / Groww content", "Money YouTube channels", "Financial newsletter writers", "FIRE community pages"],
        "general":       ["Niche content creators", "Industry blogs", "YouTube educators", "Podcast pages", "Community newsletters"],
    }
    return data.get(niche, data["general"])


def _get_trends(niche: str) -> list:
    data = {
        "career_tools": ["AI-powered resume optimization going viral", "Video resumes gaining traction", "LinkedIn audio events growing", "Personal brand > job applications trend"],
        "fitness":       ["Short workout content (under 5 min) outperforming long videos", "Mobility and recovery content rising", "Aesthetic gym aesthetics driving Instagram reach"],
        "saas":          ["Build in public content trending", "Founder-led marketing outperforming ads", "Free tool launches getting massive organic reach", "SaaS roast / comparison videos viral"],
        "ai_tech":       ["AI tool comparison content going viral", "'I tried X AI tools' format performing well", "AI productivity hacks getting massive shares", "Anti-AI takes also getting huge engagement"],
        "fashion":       ["Outfit-of-the-day Reels dominating", "Sustainable fashion content rising", "Thrift flip content viral on Instagram and TikTok"],
        "food":          ["10-minute meal videos trending", "High protein recipe content surging", "Restaurant review Reels getting millions of views"],
        "education":     ["Micro-learning content (under 60 sec) outperforming", "Notion templates viral on Twitter", "Free resource drops getting massive saves on Instagram"],
        "agency":        ["Case study content outperforming ads", "Results-first content (before/after) going viral", "Cold email teardown content trending on LinkedIn"],
        "finance":       ["Personal finance for Gen Z trending", "Stock market reaction content viral", "Side hustle income report content exploding"],
        "general":       ["Short-form video dominating all platforms", "Authentic behind-the-scenes content trending", "Community-driven content outperforming polished ads"],
    }
    return data.get(niche, data["general"])


def _get_saturated(niche: str) -> list:
    data = {
        "career_tools": ["'Update your resume' generic posts", "'Top 5 LinkedIn tips' listicles", "'How to get a job in 2024' articles"],
        "fitness":       ["Generic 'stay consistent' motivation posts", "'Drink more water' health tips", "'Before and after' transformation posts (overused)"],
        "saas":          ["'We just launched on Product Hunt!' posts", "'Check out our new feature' updates", "Generic '10 productivity tools' listicles"],
        "ai_tech":       ["'AI will replace jobs' takes", "'Top 10 AI tools of 2024' lists", "'ChatGPT prompt hacks' (extremely oversaturated)"],
        "fashion":       ["Basic OOTD posts without personality", "'Shop my look' posts without story", "Generic style tips everyone posts"],
        "food":          ["'Easy 3 ingredient recipe' (overdone)", "Generic plating photos without story", "'What I eat in a day' without unique angle"],
        "education":     ["'Here are 5 tips to learn faster'", "Generic motivational study content", "'Stop wasting time' productivity posts"],
        "agency":        ["'We help businesses grow' generic pitches", "'Top marketing strategies' listicles", "Cold DM screenshots as proof"],
        "finance":       ["'Start investing early' basic advice", "'Compound interest explained' (10000th time)", "Generic 'rich vs poor mindset' posts"],
        "general":       ["Generic motivational quotes", "'Work hard and success will come' posts", "Engagement bait ('Comment YES if you agree')"],
    }
    return data.get(niche, data["general"])


def _get_opportunities(niche: str, goal: str) -> list:
    data = {
        "career_tools": [
            f"Share real user success stories from {goal} — social proof beats features",
            "Create 'resume mistakes' content — high fear-based engagement",
            "Post salary negotiation tips — extremely high LinkedIn engagement",
            "Build in public — show the journey of building the tool",
        ],
        "fitness": [
            "Focus on mental health + fitness angle — underserved",
            "Target busy professionals — '10 min workout' positioning",
            f"Use {goal} as a daily habit tracker angle — very shareable",
        ],
        "saas": [
            f"Founder story content for {goal} — people invest in people",
            "Show actual user dashboard / results — proof over promises",
            "Compare to doing it manually — time saved is a strong hook",
            "Free tool or template launch — organic reach multiplier",
        ],
        "ai_tech": [
            f"Show {goal} solving a specific real problem — not general AI hype",
            "Create 'AI saved me X hours' format — extremely shareable",
            "Contrast old way vs AI way — visual comparison content",
            "Target skeptics — 'I was wrong about AI' angle gets high engagement",
        ],
        "fashion": [
            "Outfit repeating / sustainable styling — trending and underserved",
            f"Budget fashion angle for {goal} — mass market appeal",
            "Cultural fashion fusion content — unique differentiation",
        ],
        "food": [
            "High protein + quick meals — massive search demand",
            f"Ingredient substitution content for {goal} — very practical",
            "Budget meals with restaurant-quality results — viral formula",
        ],
        "education": [
            f"Free resource drops using {goal} — drives massive saves and follows",
            "Teach one micro-skill per post — highly shareable",
            "Myth-busting content in your niche — strong engagement",
        ],
        "agency": [
            f"Case study breakdowns from {goal} — specificity builds trust",
            "Show client results with numbers — cuts through the noise",
            "Behind-the-scenes client work — builds authority fast",
        ],
        "finance": [
            "India-specific financial advice — massive underserved audience",
            f"'{goal} for beginners' angle — always high demand",
            "Real portfolio screenshots (with context) — authenticity wins",
        ],
        "general": [
            f"Document your journey building {goal} — authentic beats polished",
            "Create a controversy around a common belief in your niche",
            "Give away something free — builds audience fast",
        ],
    }
    return data.get(niche, data["general"])


def _get_viral_hooks(niche: str, goal: str) -> list:
    return [
        f"I used {goal} for 30 days. Here's what actually happened.",
        f"Nobody talks about this problem that {goal} solves.",
        f"Stop doing it the hard way. {goal} exists for a reason.",
        f"The real reason people fail at this — and how {goal} fixes it.",
        f"Hot take: {goal} is the most underrated tool in this space right now.",
        f"I wish someone told me about {goal} earlier. Here's why.",
        f"This is what separates people who succeed with {goal} from those who don't.",
    ]


def _get_positioning(niche: str, goal: str) -> list:
    return [
        f"Position {goal} as the 'anti-complexity' solution — simple wins.",
        f"Lead with results, not features — show outcomes first.",
        f"Own the 'for beginners' angle if competitors feel intimidating.",
        f"Be the brand that teaches, not just sells — education builds trust.",
        f"Use 'built by someone who had this problem' — founder story is powerful.",
        f"Make {goal} the obvious choice by making alternatives look painful.",
        f"Niche down — be the best for one specific audience, not average for all.",
    ]