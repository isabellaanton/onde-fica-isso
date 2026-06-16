import unicodedata

def normalize_text(text: str) -> str:
    text = unicodedata.normalize('NFKD', text.lower())
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text.strip()

def check_guess(guess: str, correct: str) -> bool:
    if not guess or not correct:
        return False
    g = normalize_text(guess)
    c = normalize_text(correct)
    return (g in c) or (c in g) or (len(g) > 4 and g.replace(" ", "") in c.replace(" ", ""))