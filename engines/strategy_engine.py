# strategy_engine.py — Generates dynamic content strategy based on user goal
 
def generate_strategy(goal: str) -> dict:
    """
    Input:  goal (string) — e.g. "Grow AI niche for 30 days"
    Output: strategy dictionary (dynamic, keyword-based)
    Note:   Rule-based for now (AI logic added later)
    """
 
    goal_lower = goal.lower()
 
    # --- Detect niche from goal ---
    if "ai" in goal_lower or "artificial intelligence" in goal_lower:
        niche = "AI"
        pillars = ["Education", "Opinion", "Future Trends"]
        tone = "Professional + Forward-thinking"
 
    elif "fitness" in goal_lower or "health" in goal_lower or "gym" in goal_lower:
        niche = "Fitness"
        pillars = ["Motivation", "Tips", "Transformation"]
        tone = "Energetic + Motivational"
 
    elif "business" in goal_lower or "startup" in goal_lower or "entrepreneur" in goal_lower:
        niche = "Business"
        pillars = ["Strategy", "Lessons", "Growth"]
        tone = "Bold + Professional"
 
    elif "coding" in goal_lower or "developer" in goal_lower or "programming" in goal_lower:
        niche = "Tech / Coding"
        pillars = ["Tutorials", "Tips", "Career"]
        tone = "Casual + Informative"
 
    elif "finance" in goal_lower or "money" in goal_lower or "investing" in goal_lower:
        niche = "Finance"
        pillars = ["Education", "Mindset", "Strategies"]
        tone = "Trustworthy + Clear"
 
    else:
        # Default fallback
        niche = "Personal Brand"
        pillars = ["Education", "Opinion", "Story"]
        tone = "Professional + Engaging"
 
    # --- Build strategy output ---
    strategy = {
        "goal": goal,
        "niche": niche,
        "content_pillars": pillars,
        "posting_frequency": "1 post per day",
        "tone": tone,
        "content_mix": {
            "education": 40,
            "opinion": 30,
            "story": 20,
            "viral": 10
        }
    }
 
    return strategy
 