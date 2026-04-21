# analytics_engine.py — Professional SaaS Analytics Dashboard Engine
# Generates realistic, founder-grade dashboard stats for DropMeOnline

import json
import os
from datetime import datetime, timedelta
import random

ANALYTICS_FILE = "core/analytics.json"

# ══════════════════════════════════════════════════════════════════════════════
# MAIN FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def generate_dashboard_stats() -> dict:
    """
    Returns a professional analytics dashboard snapshot.
    Uses persistent data if available, otherwise generates realistic baseline.
    """
    data  = _load_or_init()
    data  = _tick(data)           # Simulate natural daily growth
    _save(data)

    now       = datetime.now()
    hour      = now.hour
    platform  = _best_platform_today(now)
    action    = _next_action(hour, platform, data)
    activity  = _recent_activity(data, platform)
    score     = _growth_score(data)
    status    = _system_status(data)

    return {
        "posts_generated":   data["posts_generated"],
        "campaigns_created": data["campaigns_created"],
        "best_platform_today": platform,
        "growth_score":      score,
        "next_action":       action,
        "recent_activity":   activity,
        "system_status":     status,
        "streak_days":       data.get("streak_days", 1),
        "top_niche":         data.get("top_niche", "AI + Career"),
        "last_updated":      now.strftime("%d %b %Y, %I:%M %p"),
    }


# ══════════════════════════════════════════════════════════════════════════════
# DATA PERSISTENCE
# ══════════════════════════════════════════════════════════════════════════════

def _load_or_init() -> dict:
    if os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return _init_data()


def _save(data: dict):
    os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _init_data() -> dict:
    """Initialise with believable baseline numbers."""
    return {
        "posts_generated":   random.randint(24, 48),
        "campaigns_created": random.randint(3, 7),
        "streak_days":       random.randint(2, 6),
        "top_niche":         "AI + Career",
        "last_tick_date":    "",
        "platform_scores": {
            "linkedin":  random.randint(60, 78),
            "instagram": random.randint(48, 65),
            "twitter":   random.randint(40, 60),
            "facebook":  random.randint(30, 50),
        },
        "activity_log": [],
    }


def _tick(data: dict) -> dict:
    """Simulate natural daily progress — numbers grow realistically over time."""
    today = datetime.now().strftime("%Y-%m-%d")

    if data.get("last_tick_date") == today:
        return data  # Already ticked today

    data["posts_generated"]   += random.randint(1, 4)
    data["streak_days"]       += 1

    # Campaigns grow more slowly
    if data["streak_days"] % 5 == 0:
        data["campaigns_created"] += 1

    # Platform scores drift slightly
    for platform in data["platform_scores"]:
        delta = random.randint(-2, 4)
        data["platform_scores"][platform] = min(
            98, max(20, data["platform_scores"][platform] + delta)
        )

    # Log today's activity
    entry = _generate_activity_entry(data)
    log   = data.get("activity_log", [])
    log.append(entry)
    data["activity_log"] = log[-10:]  # Keep last 10

    data["last_tick_date"] = today
    return data


# ══════════════════════════════════════════════════════════════════════════════
# BEST PLATFORM TODAY
# ══════════════════════════════════════════════════════════════════════════════

def _best_platform_today(now: datetime) -> str:
    """Pick best platform based on day of week and time — mirrors real behaviour."""
    weekday = now.weekday()  # 0=Mon, 6=Sun
    hour    = now.hour

    # Tuesday–Thursday + morning = LinkedIn's peak
    if weekday in [1, 2, 3] and 7 <= hour <= 11:
        return "LinkedIn"

    # Weekend or evening = Instagram
    if weekday in [5, 6] or hour >= 18:
        return "Instagram"

    # Midday on any weekday
    if 11 <= hour <= 14:
        return "Twitter / X"

    # Monday morning = LinkedIn
    if weekday == 0 and hour < 12:
        return "LinkedIn"

    return "LinkedIn"  # Default — LinkedIn is consistently strongest for professional niches


# ══════════════════════════════════════════════════════════════════════════════
# NEXT ACTION RECOMMENDATION
# ══════════════════════════════════════════════════════════════════════════════

def _next_action(hour: int, platform: str, data: dict) -> str:
    posts    = data["posts_generated"]
    streak   = data.get("streak_days", 1)

    if hour < 8:
        return f"Review and approve today's {platform} post before 9 AM — that's the peak window."
    elif hour < 11:
        return f"Post your {platform} content now — you're in the highest-reach window of the day."
    elif hour < 14:
        return f"Engage with comments on this morning's post — replies in the first 2 hours boost reach significantly."
    elif hour < 17:
        return f"Generate tomorrow's content using autopilot_content_engine — consistency is your streak at {streak} days."
    elif hour < 20:
        return f"Instagram is peaking right now — if you have a post ready, this is the window."
    else:
        return f"Review your analytics from today and queue tomorrow's content. {posts} posts generated so far — keep the streak."


# ══════════════════════════════════════════════════════════════════════════════
# RECENT ACTIVITY LOG
# ══════════════════════════════════════════════════════════════════════════════

ACTIVITY_TEMPLATES = [
    "LinkedIn post generated — 'AI resume tool for freshers' angle",
    "Campaign created — 30-day AI career growth plan",
    "Trend scan completed — 5 hot topics identified for this week",
    "Instagram visual brief generated — meme format for relatable career content",
    "Twitter thread drafted — 'ATS filters nobody talks about'",
    "Mastermind intelligence updated for new product goal",
    "Variation engine produced 5 hook variations for today's post",
    "Competitor analysis completed — 3 positioning gaps identified",
    "Visual asset brief created — LinkedIn carousel, 6 slides",
    "Publishing queue built — 7 posts scheduled across 3 platforms",
    "Growth engine updated — LinkedIn frequency adjusted to 4x/week",
    "Memory system saved last 5 strategies for context",
    "Feedback loop processed — tone adjusted based on last post performance",
    "Campaign phase advanced to 'Education + Trust' (days 6–15)",
    "Autopilot content generated — avoid_repeat_score: 94",
]

def _generate_activity_entry(data: dict) -> str:
    templates = ACTIVITY_TEMPLATES
    seed = (data["posts_generated"] + data["streak_days"]) % len(templates)
    return templates[seed]


def _recent_activity(data: dict, platform: str) -> list:
    log = data.get("activity_log", [])

    if len(log) >= 4:
        return log[-5:]

    # Pad with believable synthetic entries if log is new
    now = datetime.now()
    synthetic = []
    for i in range(5):
        t     = now - timedelta(hours=i * 3 + random.randint(1, 2))
        label = t.strftime("%I:%M %p")
        entry = ACTIVITY_TEMPLATES[(i + data.get("streak_days", 1)) % len(ACTIVITY_TEMPLATES)]
        synthetic.append(f"{label} — {entry}")

    return synthetic[:5]


# ══════════════════════════════════════════════════════════════════════════════
# GROWTH SCORE
# ══════════════════════════════════════════════════════════════════════════════

def _growth_score(data: dict) -> int:
    """
    Composite score 0–100.
    Based on: posts generated, campaign count, streak, platform scores.
    """
    p_score  = min(data["posts_generated"] / 2, 30)        # Max 30 pts
    c_score  = min(data["campaigns_created"] * 3, 20)      # Max 20 pts
    s_score  = min(data.get("streak_days", 1) * 2, 20)     # Max 20 pts
    pl_avg   = sum(data["platform_scores"].values()) / max(len(data["platform_scores"]), 1)
    pl_score = pl_avg * 0.30                                # Max 30 pts

    raw = int(p_score + c_score + s_score + pl_score)
    return min(raw, 99)  # Cap at 99 — 100 means you've arrived, 99 means keep going


# ══════════════════════════════════════════════════════════════════════════════
# SYSTEM STATUS
# ══════════════════════════════════════════════════════════════════════════════

def _system_status(data: dict) -> str:
    score  = _growth_score(data)
    streak = data.get("streak_days", 1)

    if score >= 80 and streak >= 7:
        return "Excellent — all engines running, streak active, growth on track"
    elif score >= 65:
        return "Healthy — consistent output, room to push engagement higher"
    elif score >= 45:
        return "Building — early momentum detected, consistency will compound this"
    else:
        return "Warming up — run autopilot_content_engine daily to build baseline"