# prompt_brain.py — Understands natural language product prompts and extracts key info

def understand_prompt(user_prompt: str) -> dict:
    """
    Input:  user_prompt (string) — natural language description
            e.g. "I have an AI resume tool for freshers. Need 100 users in 30 days. Zero budget."
    Output: structured dict with product, audience, goal, tone, budget, platforms
    Note:   Keyword-based extraction (AI-powered version in future phase)
    """

    text = user_prompt.lower()

    # --- Extract PRODUCT ---
    product = "Unknown Product"
    product_keywords = {
        "resume":     "AI Resume Tool",
        "portfolio":  "Portfolio Builder",
        "chatbot":    "AI Chatbot",
        "saas":       "SaaS Product",
        "app":        "Mobile App",
        "website":    "Website",
        "tool":       "Productivity Tool",
        "store":      "Online Store",
        "course":     "Online Course",
        "blog":       "Blog / Content Site",
        "agency":     "Agency Service",
    }
    for keyword, label in product_keywords.items():
        if keyword in text:
            product = label
            break

    # --- Extract AUDIENCE ---
    audience = "General audience"
    audience_keywords = {
        "fresher":      "College freshers / Entry-level job seekers",
        "student":      "Students",
        "developer":    "Developers / Programmers",
        "entrepreneur": "Entrepreneurs",
        "startup":      "Startup founders",
        "freelancer":   "Freelancers",
        "professional": "Working professionals",
        "business":     "Business owners",
        "creator":      "Content creators",
        "marketer":     "Marketers",
    }
    for keyword, label in audience_keywords.items():
        if keyword in text:
            audience = label
            break

    # --- Extract GOAL ---
    goal = "Grow brand awareness"
    import re
    user_match = re.search(r'(\d+)\s*users?', text)
    follower_match = re.search(r'(\d+)\s*followers?', text)
    sale_match = re.search(r'(\d+)\s*sales?', text)

    if user_match:
        goal = f"Get {user_match.group(1)} users"
    elif follower_match:
        goal = f"Gain {follower_match.group(1)} followers"
    elif sale_match:
        goal = f"Close {sale_match.group(1)} sales"
    elif "viral" in text:
        goal = "Go viral"
    elif "awareness" in text:
        goal = "Build brand awareness"
    elif "launch" in text:
        goal = "Product launch"

    # --- Extract TONE ---
    tone = "Professional + Engaging"
    tone_keywords = {
        "casual":        "Casual + Friendly",
        "fun":           "Fun + Energetic",
        "professional":  "Professional + Authoritative",
        "gen z":         "Gen Z + Trendy",
        "motivational":  "Motivational + Inspiring",
        "educational":   "Educational + Informative",
        "bold":          "Bold + Direct",
        "storytelling":  "Story-driven + Emotional",
    }
    for keyword, label in tone_keywords.items():
        if keyword in text:
            tone = label
            break

    # --- Extract BUDGET ---
    budget = "Unknown"
    if any(word in text for word in ["zero budget", "no budget", "free", "zero", "₹0", "$0"]):
        budget = "Zero / Free"
    elif any(word in text for word in ["low budget", "small budget", "limited"]):
        budget = "Low Budget"
    elif any(word in text for word in ["paid", "ads", "sponsored", "budget"]):
        budget = "Paid / Has Budget"

    # --- Extract PLATFORMS ---
    platforms = []
    platform_map = {
        "linkedin":  "linkedin",
        "instagram": "instagram",
        "twitter":   "twitter",
        "facebook":  "facebook",
        "youtube":   "youtube",
        "tiktok":    "tiktok",
        "reddit":    "reddit",
    }
    for keyword, platform in platform_map.items():
        if keyword in text:
            platforms.append(platform)

    # Default to top 3 if none detected
    if not platforms:
        platforms = ["linkedin", "instagram", "twitter"]

    return {
        "product":   product,
        "audience":  audience,
        "goal":      goal,
        "tone":      tone,
        "budget":    budget,
        "platforms": platforms
    }