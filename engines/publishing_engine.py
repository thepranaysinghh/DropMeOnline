# publishing_engine.py — Builds a structured publish queue from campaign data

def build_publish_queue(campaign: list, platforms: list) -> dict:
    """
    Input:
        campaign  — list of day-wise campaign plans (from campaign_engine)
        platforms — list of active platforms e.g. ["linkedin", "instagram", "twitter"]
    Output:
        dict with today's posts, upcoming schedule, and action items
    """

    today    = []
    upcoming = []
    actions  = []

    for entry in campaign:
        day   = entry.get("day", 1)
        theme = entry.get("theme", "Content")
        hook  = entry.get("hook", "")

        # Short title from hook (first sentence, max 60 chars)
        title = hook.split(".")[0][:60] if hook else theme

        for platform in platforms:
            if platform not in entry:
                continue

            post_item = {
                "platform": platform,
                "day":      day,
                "title":    title,
                "preview":  entry[platform][:80] + "..." if len(entry.get(platform, "")) > 80 else entry.get(platform, ""),
                "status":   "ready" if day == 1 else "scheduled",
            }

            if day == 1:
                today.append(post_item)
            else:
                upcoming.append(post_item)

    # --- Generate action items ---

    # Actions for today's posts
    for post in today:
        platform_label = post["platform"].capitalize()
        actions.append(f"Publish {platform_label} post now: \"{post['title']}\"")

    # Actions for next 3 upcoming days
    seen_days = []
    for post in upcoming:
        if post["day"] not in seen_days and len(seen_days) < 3:
            seen_days.append(post["day"])
            actions.append(f"Review Day {post['day']} content before it goes live")

    # General action reminders
    if "instagram" in platforms:
        actions.append("Prepare Instagram visual / creative for today's post")
    if "linkedin" in platforms:
        actions.append("Check LinkedIn post engagement after 2 hours")
    if "twitter" in platforms:
        actions.append("Reply to Twitter comments to boost reach")

    return {
        "today":    today,
        "upcoming": upcoming[:20],  # Show next 20 upcoming items max
        "actions":  actions,
    }