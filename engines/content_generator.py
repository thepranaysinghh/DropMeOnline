# content_generator.py — Generates platform-specific content based on user goal
 
def generate_content(goal: str) -> dict:
    """
    Input:  goal (string) — e.g. "Grow AI niche for 30 days"
    Output: dictionary with platform-specific posts
    Note:   Returns dummy data for now (AI logic added later)
    """
 
    content = {
        "linkedin": f"Professional post about: {goal}",
        "instagram": f"Short caption about: {goal}",
        "twitter": f"Bold opinion about: {goal}"
    }
 
    return content
 
