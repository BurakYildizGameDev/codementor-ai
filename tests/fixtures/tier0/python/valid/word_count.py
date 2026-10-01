from collections import Counter


def word_count(text: str) -> dict[str, int]:
    """Metindeki kelimeleri sayar."""
    words = [w.strip(".,!?").lower() for w in text.split()]
    return dict(Counter(w for w in words if w))


if __name__ == "__main__":
    print(word_count("Bir iki bir üç"))
