# growth_engine.py — Decides growth strategy per platform based on performance data
 
def decide_growth_strategy(goal: str, platform: str, performance_data: dict) -> dict:
    """
    Input:
        goal             — e.g. "Grow AI niche for 30 days"
        platform         — "linkedin" | "instagram" | "twitter"
        performance_data — { "engagement": "high" | "low", "last_posts": int }
    Output:
        strategy dict with frequency, content type, hook style, notes
    """
 
    engagement  = performance_data.get("engagement", "low")
    last_posts  = performance_data.get("last_posts", 0)
    platform    = platform.lower()
 
    # --- LinkedIn ---
    if platform == "linkedin":
        if engagement == "high":
            return {
                "posting_frequency": "3-4 times/week",
                "content_type":      "Educational + Personal Story",
                "hook_style":        "Emotional opener + lesson",
                "notes":             "Engagement is strong. Maintain current mix and double down on best-performing formats."
            }
        else:
            return {
                "posting_frequency": "2 times/week",
                "content_type":      "Deep Educational + Opinion",
                "hook_style":        "Bold statement + insight",
                "notes":             "Engagement is low. Reduce frequency, increase post quality. Focus on value-heavy content."
            }
 
    # --- Instagram ---
    elif platform == "instagram":
        if engagement == "high":
            return {
                "posting_frequency": "1 time/day",
                "content_type":      "Mix of Reels + Carousels",
                "hook_style":        "Curiosity + visual hook",
                "notes":             "Engagement is strong. Maintain reel + carousel mix. Keep consistency."
            }
        else:
            return {
                "posting_frequency": "1-2 Reels/day",
                "content_type":      "Reels only (reach focus)",
                "hook_style":        "Pattern interrupt + trending audio",
                "notes":             "Growth is low. Shift to Reels for reach. Carousels later once audience grows."
            }
 
    # --- Twitter ---
    elif platform == "twitter":
        if engagement == "high":
            return {
                "posting_frequency": "3-5 times/day",
                "content_type":      "Bold opinions + Threads",
                "hook_style":        "Controversial + direct",
                "notes":             "Engagement is strong. Keep volume high. Add threads for deeper reach."
            }
        else:
            return {
                "posting_frequency": "5+ times/day",
                "content_type":      "Short bold takes + Replies",
                "hook_style":        "Provocative + contrarian",
                "notes":             "Engagement is low. Increase volume. Reply to bigger accounts to gain visibility."
            }
 
    # --- Unknown platform fallback ---
    else:
        return {
            "posting_frequency": "1 time/day",
            "content_type":      "Educational + Story",
            "hook_style":        "Curiosity-based",
            "notes":             f"Platform '{platform}' not recognized. Using default strategy."
        }
 