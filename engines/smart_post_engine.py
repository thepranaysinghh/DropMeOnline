# smart_post_engine.py — Decides posting frequency per platform based on goal
 
def decide_post_plan(goal: str) -> dict:
    """
    Input:  goal (string) — e.g. "Grow AI niche for 30 days"
    Output: posting frequency plan per platform with reasoning
    Note:   Rule-based logic (AI logic added later)
    """
 
    goal_lower = goal.lower()
 
    # --- Detect urgency from goal ---
    is_aggressive = any(word in goal_lower for word in ["fast", "quick", "rapid", "30 days", "viral"])
 
    if is_aggressive:
        linkedin_freq  = "5 times/week"
        instagram_freq = "2 times/day"
        twitter_freq   = "3 times/day"
        reasoning      = "Aggressive growth goal detected — higher frequency across all platforms."
    else:
        # Default: platform-native best practices
        linkedin_freq  = "3 times/week"   # LinkedIn rewards quality over quantity
        instagram_freq = "1 time/day"     # Instagram rewards consistency
        twitter_freq   = "2 times/day"    # Twitter rewards high volume
        reasoning      = "Standard growth plan — LinkedIn: quality, Instagram: consistency, Twitter: volume."
 
    return {
        "linkedin_frequency":  linkedin_freq,
        "instagram_frequency": instagram_freq,
        "twitter_frequency":   twitter_freq,
        "reasoning":           reasoning
    }
 