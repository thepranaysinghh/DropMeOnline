# platform_adapter.py — Adapts content for each platform's style and rules
 
def adapt_platform(content: dict) -> dict:
    """
    Input:  content dict — {"linkedin": "...", "instagram": "...", "twitter": "..."}
    Output: adapted content dict with platform-specific improvements
    Note:   Rule-based for now (AI logic added later)
    """
 
    adapted = {}
 
    # LinkedIn — add professional closing line + line break
    adapted["linkedin"] = (
        content.get("linkedin", "") +
        "\n\n— Thoughts? Drop them below. Let's discuss."
    )
 
    # Instagram — add emojis + hashtags
    adapted["instagram"] = (
        "✨ " + content.get("instagram", "") +
        "\n\n#growthmindset #aitools"
    )
 
    # Twitter — shorten + make sharper
    twitter_text = content.get("twitter", "")
    adapted["twitter"] = twitter_text.split(".")[0] + ". Act on it."
 
    return adapted
 