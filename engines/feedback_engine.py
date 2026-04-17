# feedback_engine.py — Analyzes qualitative feedback and decides next strategy
 
def analyze_feedback(platform: str, feedback: dict) -> dict:
    """
    Input:
        platform — "linkedin" | "instagram" | "twitter"
        feedback — {
            "reach":    "low" | "medium" | "high",
            "likes":    "low" | "medium" | "high",
            "comments": "low" | "medium" | "high",
            "time":     "morning" | "midday" | "evening",
            "overall":  "poor" | "average" | "good"
        }
    Output:
        dict with next_time, frequency, content_style, decision
    """
 
    reach    = feedback.get("reach", "low")
    likes    = feedback.get("likes", "low")
    comments = feedback.get("comments", "low")
    time     = feedback.get("time", "morning")
    overall  = feedback.get("overall", "average")
 
    platform = platform.lower()
 
    # --- Pattern matching ---
 
    # High everything — keep and repeat
    if reach == "high" and likes == "high" and comments == "high":
        return {
            "next_time":     time,
            "frequency":     "keep",
            "content_style": "Same as current — it's working",
            "decision":      "keep"
        }
 
    # Low everything — full strategy change
    if reach == "low" and likes == "low" and comments == "low":
        return {
            "next_time":     _shift_time(time),
            "frequency":     "reduce",
            "content_style": "Complete format change — try storytelling or bold opinion",
            "decision":      "change"
        }
 
    # Low reach + high comments — content good, timing weak
    if reach == "low" and comments == "high":
        return {
            "next_time":     _shift_time(time),
            "frequency":     "keep",
            "content_style": "Keep current content style — only fix posting time",
            "decision":      "change"
        }
 
    # High reach + low comments — hook good, value weak
    if reach == "high" and comments == "low":
        return {
            "next_time":     time,
            "frequency":     "keep",
            "content_style": "Improve post depth — add insights, questions, or takeaways",
            "decision":      "change"
        }
 
    # Average overall — small adjustments
    if overall == "average":
        return {
            "next_time":     time,
            "frequency":     "keep",
            "content_style": "Test a new hook style — try curiosity or controversy",
            "decision":      "change"
        }
 
    # Good overall — maintain
    if overall == "good":
        return {
            "next_time":     time,
            "frequency":     "keep",
            "content_style": "Maintain current approach — consider slight format variation",
            "decision":      "keep"
        }
 
    # Fallback
    return {
        "next_time":     "09:00",
        "frequency":     "keep",
        "content_style": "Reassess with more data",
        "decision":      "keep"
    }
 
 
def _shift_time(current_time: str) -> str:
    """Suggests next time slot to test based on current slot."""
    shifts = {
        "morning": "12:00",
        "midday":  "18:00",
        "evening": "09:00"
    }
    return shifts.get(current_time, "12:00")
 