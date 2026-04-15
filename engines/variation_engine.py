# variation_engine.py — Generates 5 style-based variations of a given post
 
def generate_variations(text: str) -> list:
    """
    Input:  text (string) — original post or topic
    Output: list of 5 variations in different styles
    Note:   Rule-based for now (AI logic added later)
    """
 
    variations = [
        f"{text} — are you ready?",                          # motivational
        f"Stop ignoring this. {text}.",                      # bold
        f"{text}. Simple.",                                   # short
        f"Why are most people still sleeping on: {text}?",   # question
        f"{text} — and most people will never accept it.",   # controversial
    ]
 
    return variations
 