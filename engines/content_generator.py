# content_generator.py — Generates platform-specific content based on user goal
 
def generate_content(goal: str) -> dict:
    """
    Input:  goal (string) — e.g. "Grow AI niche for 30 days"
    Output: dictionary with platform-specific posts
    Note:   Rule-based for now (AI logic added later)
    """
 
    content = {
 
        # LinkedIn — professional tone, 3-4 lines
        "linkedin": (
            f"Here's what most people get wrong about: {goal}.\n\n"
            f"The ones who succeed don't wait for the perfect moment.\n"
            f"They start, learn, and adapt faster than anyone else.\n"
            f"If this is your goal too — the time to act is now."
        ),
 
        # Instagram — short and catchy, 1-2 lines
        "instagram": (
            f"Your next big move? {goal} 🚀\n"
            f"Start before you're ready."
        ),
 
        # Twitter — bold opinion, 1 line
        "twitter": (
            f"Unpopular opinion: {goal} is the only thing that actually matters right now."
        )
 
    }
 
    return content
 