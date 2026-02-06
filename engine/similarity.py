from difflib import SequenceMatcher

def similarity_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def is_too_similar(source: str, generated: str, threshold: float = 0.7) -> bool:
    return similarity_ratio(source, generated) >= threshold
