# brain_engine.py — Analyzes performance data and decides next posting strategy
 
def analyze_and_decide(platform: str, performance_data: dict) -> dict:
    """
    Input:
        platform         — "linkedin" | "instagram" | "twitter"
        performance_data — {
            "reach":     int,
            "likes":     int,
            "comments":  int,
            "post_time": "HH:MM",
            "frequency": "daily" | "3x/week" | etc.
        }
    Output:
        strategy dict with next post time, frequency change, content style, reason
    """
 
    platform   = platform.lower()
    reach      = performance_data.get("reach", 0)
    likes      = performance_data.get("likes", 0)
    comments   = performance_data.get("comments", 0)
    post_time  = performance_data.get("post_time", "09:00")
    frequency  = performance_data.get("frequency", "daily")
 
    # Parse post hour for time-based decisions
    try:
        post_hour = int(post_time.split(":")[0])
    except:
        post_hour = 9
 
    is_morning  = 6  <= post_hour < 12
    is_midday   = 12 <= post_hour < 16
    is_evening  = 16 <= post_hour < 22
 
    engagement_rate = (likes + comments) / max(reach, 1) * 100  # % engagement
 
    # ------------------------------------------------------------------ LinkedIn
    if platform == "linkedin":
 
        # Strong comments = educational/story content is working
        if comments >= 10:
            content_style = "Educational + Personal Story"
            reason = "Strong comment activity — educational and story content is resonating well."
        else:
            content_style = "Opinion + Bold Insight"
            reason = "Low comment activity — shift to opinion posts to spark discussion."
 
        # Frequency decision
        if engagement_rate < 2 and frequency == "daily":
            frequency_change = "decrease"
            reason += " Daily posting with low engagement — reduce to 3x/week and improve quality."
        elif engagement_rate >= 5:
            frequency_change = "keep"
            reason += " Engagement rate is healthy — maintain current frequency."
        else:
            frequency_change = "keep"
            reason += " Moderate engagement — keep frequency and test new hooks."
 
        # Best time decision
        if is_morning and engagement_rate >= 3:
            next_post_time = "09:00"
        elif is_morning and engagement_rate < 3:
            next_post_time = "12:00"
            reason += " Morning performance is weak — test midday next."
        else:
            next_post_time = "09:00"
            reason += " Defaulting to morning slot for LinkedIn."
 
    # ---------------------------------------------------------------- Instagram
    elif platform == "instagram":
 
        # High reach = reels are working
        if reach >= 1000:
            content_style = "Reels (reach priority)"
            reason = "High reach detected — reels are performing well, continue prioritizing them."
        else:
            content_style = "Carousel (engagement priority)"
            reason = "Reach is low — test carousels to boost saves and shares."
 
        # Frequency decision
        if engagement_rate >= 4:
            frequency_change = "keep"
            reason += " Engagement is strong — maintain current schedule."
        elif engagement_rate < 2:
            frequency_change = "increase"
            reason += " Low engagement — increase posting frequency to improve visibility."
        else:
            frequency_change = "keep"
            reason += " Average engagement — keep frequency and iterate on content style."
 
        # Best time decision
        if is_evening and engagement_rate >= 3:
            next_post_time = "19:00"
            reason += " Evening engagement is strong — keep evening slot."
        elif is_evening and engagement_rate < 3:
            next_post_time = "12:00"
            reason += " Evening underperforming — test midday slot."
        else:
            next_post_time = "18:00"
            reason += " Defaulting to early evening for Instagram."
 
    # ------------------------------------------------------------------ Twitter
    elif platform == "twitter":
 
        content_style = "Bold Opinion + Thread"
 
        # Low reach = need more volume + replies
        if reach < 300:
            frequency_change = "increase"
            reason = "Reach is low — increase posting volume and engage with replies on larger accounts."
            next_post_time = "12:00" if is_midday else "09:00"
        elif engagement_rate >= 3:
            frequency_change = "keep"
            reason = "Engagement is healthy — keep current volume and style."
            next_post_time = "12:00" if is_midday and engagement_rate >= 3 else "09:00"
        else:
            frequency_change = "increase"
            reason = "Average performance — increase frequency and test more controversial hooks."
            next_post_time = "10:00"
 
        if is_midday and engagement_rate >= 3:
            next_post_time = "12:00"
            reason += " Midday slot is performing well — keep it."
 
    # --------------------------------------------------------- Unknown platform
    else:
        return {
            "next_post_time":    "09:00",
            "frequency_change":  "keep",
            "content_style":     "Educational + Story",
            "reason":            f"Platform '{platform}' not recognized. Using default strategy."
        }
 
    return {
        "next_post_time":   next_post_time,
        "frequency_change": frequency_change,
        "content_style":    content_style,
        "reason":           reason.strip()
    }
 