# publish_engine.py — Generates safe, user-triggered publish links per platform
 
from urllib.parse import quote
 
def generate_publish_links(content: dict) -> dict:
    """
    Input:  content dict — {"linkedin": "...", "twitter": "...", "instagram": "..."}
    Output: dict with share URLs for LinkedIn/Twitter, copy action for Instagram
 
    IMPORTANT: No automation. No bots. No login handling.
    User clicks link → platform opens with content pre-filled.
    """
 
    linkedin_text  = content.get("linkedin", "")
    twitter_text   = content.get("twitter", "")
 
    # LinkedIn — share intent URL (text encoded)
    linkedin_url = (
        "https://www.linkedin.com/feed/?shareActive=true&text=" +
        quote(linkedin_text)
    )
 
    # Twitter — tweet intent URL (text encoded)
    twitter_url = (
        "https://twitter.com/intent/tweet?text=" +
        quote(twitter_text)
    )
 
    # Instagram — no API available for direct post, user must copy + open manually
    instagram_action = "copy_and_open"
 
    return {
        "linkedin_url":       linkedin_url,
        "twitter_url":        twitter_url,
        "instagram_action":   instagram_action
    }
 