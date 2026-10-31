"""
Multilingual & Transliterated Discourse Markers
Expands Beyond Likes prosocial evaluation across Hinglish (Hindi-English transliteration),
Spanish, and French global community exchanges.
"""
import re
from typing import List, Tuple

# Hinglish & Indic colloquial hostile markers
INDIC_TOXIC_PATTERNS: List[str] = [
    r"\b(bakwaas|bakwas|chutiya|chutiye|madarchod|behenchod|bhenchod|harami|kamine|kamina|gandu|bevakoof|bewakoof|pagal|dimag kharab|chirkut|saale|saala)\b",
    r"\b(chup kar|nikal yahan se|bhag yahan se|mar ja|kuch nahi aata|andhe ho kya)\b",
    r"\byou('re| are) (an padh|anpadh|kachra|jahil)\b"
]

# Indic constructive / epistemic reasoning markers
INDIC_CONSTRUCTIVE_PATTERNS: List[str] = [
    r"\b(shodh ke anusaar|data ke mutabiq|tathya yeh hai|aankde batate hain|udaharan ke roop mein|mukhya mudda yeh hai)\b",
    r"\b(mere vichar se|dono pehluon ko dekhkar|santulit drishtikon|vikalp yeh hai)\b"
]

# Global Spanish / French hostility markers
GLOBAL_TOXIC_PATTERNS: List[str] = [
    r"\b(idiota|estupido|estupida|mierda|hijo de puta|callate|cabron|pendejo)\b",
    r"\b(imbecile|connard|salope|ferme ta gueule|va te faire foutre|putain)\b"
]

def scan_multilingual_markers(text: str) -> Tuple[int, int, List[str]]:
    """
    Scans text for multilingual toxic and constructive markers.
    Returns (toxic_count, constructive_count, detected_tags).
    """
    text_low = text.lower()
    toxic_hits = 0
    constructive_hits = 0
    tags = []

    # Check Indic / Global Toxic
    for pat in INDIC_TOXIC_PATTERNS + GLOBAL_TOXIC_PATTERNS:
        matches = re.findall(pat, text_low)
        if matches:
            toxic_hits += len(matches)
            tags.append("Multilingual/Indic Toxicity")

    # Check Indic Constructive
    for pat in INDIC_CONSTRUCTIVE_PATTERNS:
        matches = re.findall(pat, text_low)
        if matches:
            constructive_hits += len(matches)
            tags.append("Indic Epistemic Citation")

    return toxic_hits, constructive_hits, list(set(tags))
