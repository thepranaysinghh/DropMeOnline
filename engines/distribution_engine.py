# distribution_engine.py — Creates a smart day-wise posting distribution plan

def create_distribution_plan(days: int, platforms: list, pages_per_platform: int) -> list:
    """
    Input:
        days                — campaign duration (e.g. 30)
        platforms           — e.g. ["linkedin", "instagram", "twitter"]
        pages_per_platform  — number of pages/accounts per platform (e.g. 3)
    Output:
        List of scheduled posts — one entry per post slot
    Rules:
        - Rotate post types to avoid repetition
        - Spread platforms across days (no same platform on every slot)
        - Rotate pages so each page gets equal coverage
        - No two pages of the same platform post the same type on the same day
    """

    # Post types in rotation order
    post_types = ["authority", "educational", "story", "proof", "cta"]

    plan = []
    type_index = 0  # Global rotating index for post types

    for day in range(1, days + 1):

        # Rotate which platform leads each day to avoid repetition
        day_platforms = _rotate_platforms(platforms, day)

        for platform in day_platforms:
            for page in range(1, pages_per_platform + 1):

                # Each page on same platform gets a different post type that day
                post_type = post_types[(type_index + page - 1) % len(post_types)]

                plan.append({
                    "day":       day,
                    "platform":  platform,
                    "page":      page,
                    "post_type": post_type,
                })

            type_index += 1  # Advance type index after each platform group

    return plan


def _rotate_platforms(platforms: list, day: int) -> list:
    """
    Rotates platform order each day so no single platform always leads.
    Day 1: [linkedin, instagram, twitter]
    Day 2: [instagram, twitter, linkedin]
    Day 3: [twitter, linkedin, instagram]
    """
    offset = (day - 1) % len(platforms)
    return platforms[offset:] + platforms[:offset]