"""
Deep Discourse Evaluator Engine (Sentence-Level Semantic Breakdown)
Advanced modeling of epistemic substance, civility, persuasiveness, and relevance.
"""
import re
import math
import time
import unicodedata
from typing import Dict, Any, Optional, List
from .rubric import POLICY_PROFILES, get_all_policies
from .multilingual import scan_multilingual_markers

EPISTEMIC_MARKERS = [
    r"\b(research shows|studies indicate|according to|data shows|empirical|evidence|measured|statistics|survey|published in|findings)\b",
    r"\b(for example|for instance|specifically|namely|case in point|such as)\b",
    r"\b\d+(\.\d+)?%\b", # Percentages like 18%, 3.5%
    r"\b(in 20\d\d|per capita|statistically|sample size|p-value|confidence interval)\b",
    r"\b(methodology|peer-reviewed|double-blind|control group|statistical significance|reproducibility|randomized|peer-review)\b",
    r"\b(pathology|carcinoma|metastases|chemotherapy|resection|clinical|diagnosis|treatment|biopsy)\b",
    r"\b(advocating for|protections for|civil rights|equal rights|non-discrimination|statutory|in accordance with article|regulation|directive|pursuant to)\b"
]

SYNTHESIS_MARKERS = [
    r"\b(on one hand|however|alternatively|in contrast|furthermore|consequently|therefore|we can synthesize|solution is|propose that)\b",
    r"\b(trade-off|balanced approach|middle ground|compromise|viable path)\b"
]

FALLACY_WHATABOUTISM = [
    r"\b(what about|whataboutism|why don't you mention|what of|look at what they did|why aren't you talking about)\b"
]

FALLACY_AD_HOMINEM = [
    r"\byou('re| are)\s+(an?\s+)?(complete\s+|absolute\s+|total\s+)?(idiot|clown|shill|troll|moron|brainless|blind|bought and paid for)\b",
    r"\b(idiot|stupid|moron|clown|trash|dumb|loser|garbage|fool|stfu|gtfo)\b",
    r"\b(shut up|get lost|kill yourself|kys|go die|jump off a (cliff|bridge)|end your life|drink bleach|hang yourself)\b",
    r"\b(fuck|fucking|fucker|bitch|bitchy|asshole|arsehole|bullshit|shit|bastard|dickhead|cunt)\b",
    r"\b(f[\*@#]{2,}k|b[\*@#]{2,}h|a[\*@#]{2,}hole|s[\*@#]{2,}t)\b",
    r"\b(low|elementary(\s+school)?|sub-?\d+|room\s+temperature|zero)\s+iq\b",
    r"\b(garbage|laughable|pathetic|moronic|joke of an?)\s+(argument|logic|claim|opinion|deduction)\b",
    r"\banyone\s+with\s+an?\s+(functioning|elementary)\s+brain\b",
    r"\b(fraud|hack|troll|shill|incompetent|disgrace|pathetic|arrogant|mindless)\b",
    r"\b(hope you|hope your|go crawl|do everyone a favor|quit writing|worst journalist)\b"
]

SPAM_PATTERNS = [
    r"https?://\S+",
    r"\b(click here|subscribe|check out my channel|buy now|discount code|dm me on telegram|whatsapp me)\b",
    r"(.)\1{4,}" # Repeated chars like 'looooool'
]

def canonicalize_text_for_security(text: str) -> str:
    """
    De-obfuscates adversarial evasion vectors:
    1. Removes zero-width and invisible unicode characters (U+200B..U+200F, U+FEFF, U+00AD, U+2060).
    2. Decomposes accented homoglyphs via NFKD to ASCII equivalents (e.g. 'stúpid' -> 'stupid').
    3. Normalizes spaced out letters for known vulgarity ('f u c k' -> 'fuck', 'k y s' -> 'kys', 'b i t c h' -> 'bitch').
    4. Translates leetspeak substitutions ('1d10t' -> 'idiot', 'sh1t' -> 'shit', 'a$$h0le' -> 'asshole').
    """
    # 1. Remove zero-width characters and soft hyphens
    zero_width_chars = ['\u200b', '\u200c', '\u200d', '\u200e', '\u200f', '\ufeff', '\u00ad', '\u2060']
    for ch in zero_width_chars:
        text = text.replace(ch, '')

    # 2. NFKD Unicode decomposition to strip accents
    decomposed = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in decomposed if not unicodedata.combining(c))

    # 3. Cyrillic and foreign homoglyph substitution
    cyrillic_map = {
        'о': 'o', 'а': 'a', 'е': 'e', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x', 'і': 'i',
        'О': 'O', 'А': 'A', 'Е': 'E', 'Р': 'P', 'С': 'C', 'У': 'Y', 'Х': 'X', 'І': 'I'
    }
    for cyr, lat in cyrillic_map.items():
        text = text.replace(cyr, lat)

    # 4. De-obfuscate punctuation-interleaved words (e.g. 'f.u.c.k' -> 'fuck', 's-h-i-t' -> 'shit')
    text = re.sub(r'\b([a-zA-Z])[\.\-_/]([a-zA-Z])[\.\-_/]([a-zA-Z])[\.\-_/]([a-zA-Z])\b', r'\1\2\3\4', text)
    text = re.sub(r'\b([a-zA-Z])[\.\-_/]([a-zA-Z])[\.\-_/]([a-zA-Z])\b', r'\1\2\3', text)

    # 5. Collapse spaced-out vulgar patterns
    text = re.sub(r'\bf\s+u\s+c\s+k\b', 'fuck', text, flags=re.IGNORECASE)
    text = re.sub(r'\bb\s+i\s+t\s+c\s+h\b', 'bitch', text, flags=re.IGNORECASE)
    text = re.sub(r'\bk\s+y\s+s\b', 'kys', text, flags=re.IGNORECASE)
    text = re.sub(r'\bs\s+t\s+f\s+u\b', 'stfu', text, flags=re.IGNORECASE)
    text = re.sub(r'\bg\s+t\s+f\s+o\b', 'gtfo', text, flags=re.IGNORECASE)
    text = re.sub(r'\bs\s+h\s+u\s+t\s+u\s+p\b', 'shut up', text, flags=re.IGNORECASE)

    # 4. Leetspeak normalization for profanity checks
    leet_map = {
        r'\b1d10t\b': 'idiot',
        r'\b1diot\b': 'idiot',
        r'\bid10t\b': 'idiot',
        r'\bsh1t\b': 'shit',
        r'\ba\$\$h0le\b': 'asshole',
        r'\ba\$\$hole\b': 'asshole',
        r'\bassh0le\b': 'asshole',
        r'\bm0r0n\b': 'moron',
        r'\bcl0wn\b': 'clown',
        r'\bf\*ck\b': 'fuck',
        r'\bb\*tch\b': 'bitch',
        r'\bb!tch\b': 'bitch'
    }
    for pat, rep in leet_map.items():
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)

    return text

class NormativeEvaluator:
    """
    Advanced Discourse Engine providing sentence-level diagnostic breakdown,
    rhetorical fallacy detection, and configurable policy profiles.
    """

    def __init__(self, policy: str = "newsroom"):
        self.set_policy(policy)

    def set_policy(self, policy: str):
        all_policies = get_all_policies()
        self.policy_name = policy if policy in all_policies else "newsroom"
        self.policy = all_policies[self.policy_name]
        self.weights = self.policy["weights"]
        self.thresholds = self.policy["thresholds"]

    def evaluate(self, text: str, context: Optional[str] = None, policy: Optional[str] = None, backend: str = "heuristic") -> Dict[str, Any]:
        start_time = time.perf_counter()
        clean_text = text.strip()
        all_policies = get_all_policies()

        if policy and policy in all_policies:
            active_weights = all_policies[policy]["weights"]
            active_thresholds = all_policies[policy]["thresholds"]
            active_policy_name = policy
        else:
            active_weights = self.weights
            active_thresholds = self.thresholds
            active_policy_name = self.policy_name

        if not clean_text:
            return self._empty_result()

        words = clean_text.split()
        word_count = len(words)
        char_count = len(clean_text)

        # Split into sentences for fine-grained analysis
        raw_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean_text) if s.strip()]
        if not raw_sentences:
            raw_sentences = [clean_text]

        sentence_diagnostics = []
        total_epistemic_hits = 0
        total_synthesis_hits = 0
        total_fallacy_hits = 0
        total_toxic_hits = 0
        is_spam = False

        for idx, s in enumerate(raw_sentences):
            s_clean = canonicalize_text_for_security(s)
            s_low = s_clean.lower()
            s_tags = []
            s_type = "NEUTRAL_OPINION"
            s_color = "amber"

            # Check spam
            for pat in SPAM_PATTERNS:
                if re.search(pat, s, re.IGNORECASE) or re.search(pat, s_clean, re.IGNORECASE):
                    is_spam = True
                    s_tags.append("Spam/Promotional")
                    s_type = "SPAM"
                    s_color = "red"

            # Check civility / hostility
            for pat in FALLACY_AD_HOMINEM:
                m = re.findall(pat, s_clean, re.IGNORECASE)
                if m:
                    total_toxic_hits += len(m)
                    s_tags.append("Hostile/Ad-Hominem")
                    s_type = "HOSTILE_ATTACK"
                    s_color = "red"

            # Check Multilingual / Indic markers
            m_toxic, m_const, m_tags = scan_multilingual_markers(s_clean)
            if m_toxic > 0:
                total_toxic_hits += m_toxic
                for t in m_tags:
                    if "Toxicity" in t: s_tags.append(t)
                s_type = "HOSTILE_ATTACK"
                s_color = "red"
            if m_const > 0:
                total_epistemic_hits += m_const
                for t in m_tags:
                    if "Citation" in t: s_tags.append(t)
                if s_type != "HOSTILE_ATTACK":
                    s_type = "CONSTRUCTIVE_EVIDENCE"
                    s_color = "green"

            # Check whataboutism
            for pat in FALLACY_WHATABOUTISM:
                if re.search(pat, s_low):
                    total_fallacy_hits += 1
                    s_tags.append("Whataboutism/Deflection")

            # Check epistemic evidence
            for pat in EPISTEMIC_MARKERS:
                m = re.findall(pat, s_low)
                if m:
                    total_epistemic_hits += len(m)
                    s_tags.append("Empirical Evidence")
                    if s_type != "HOSTILE_ATTACK":
                        s_type = "CONSTRUCTIVE_EVIDENCE"
                        s_color = "green"

            # Check synthesis
            for pat in SYNTHESIS_MARKERS:
                m = re.findall(pat, s_low)
                if m:
                    total_synthesis_hits += len(m)
                    s_tags.append("Synthesis/Counter-Argument")
                    if s_type != "HOSTILE_ATTACK" and s_type != "CONSTRUCTIVE_EVIDENCE":
                        s_type = "SYNTHESIS_ARGUMENT"
                        s_color = "blue"

            # Default low-effort check
            if len(s.split()) < 5 and not s_tags and s_type != "SPAM":
                s_type = "LOW_EFFORT_PLATITUDE"
                s_color = "slate"
                s_tags.append("Low Substantiation")

            sentence_diagnostics.append({
                "sentence_index": idx + 1,
                "text": s,
                "type": s_type,
                "ui_color": s_color,
                "tags": s_tags or ["Standard Discourse"]
            })

        # --- Dimension 1: Epistemic Constructiveness (0 - 100) ---
        constructiveness = 25.0
        if word_count > 10:
            constructiveness += min(30.0, word_count * 0.7)
        constructiveness += min(45.0, total_epistemic_hits * 15.0 + total_synthesis_hits * 10.0)
        if word_count < 5 and total_epistemic_hits == 0:
            constructiveness = 15.0
        constructiveness = max(5.0, min(100.0, constructiveness))

        # --- Dimension 2: Discourse Civility & Ethics (0 - 100) ---
        civility = 95.0
        if total_toxic_hits > 0:
            civility -= total_toxic_hits * 50.0
            civility = min(civility, 35.0)
        if total_fallacy_hits > 0:
            civility -= total_fallacy_hits * 15.0
        # Excessive all-caps penalty
        caps = sum(1 for c in clean_text if c.isupper())
        if char_count > 15 and (caps / char_count) > 0.45:
            civility -= 25.0
        civility = max(5.0, min(100.0, civility))

        # --- Dimension 3: Persuasiveness & Coherence (0 - 100) ---
        persuasiveness = 30.0
        if len(raw_sentences) >= 2:
            persuasiveness += 20.0
        if any(c in clean_text for c in [",", ";", ":", "-", "(", ")"]):
            persuasiveness += 15.0
        if total_synthesis_hits > 0 or total_epistemic_hits > 0:
            persuasiveness += 25.0
        if total_fallacy_hits > 0 and total_epistemic_hits == 0:
            persuasiveness = max(10.0, persuasiveness - total_fallacy_hits * 25.0)
        if civility < 40:
            persuasiveness = min(persuasiveness, civility + 10.0)
        persuasiveness = max(5.0, min(100.0, persuasiveness))

        # --- Dimension 4: Dialectical Relevance (0 - 100) ---
        relevance = 75.0
        if context:
            ctx_words = set(re.findall(r"\w{4,}", context.lower()))
            comment_words = set(re.findall(r"\w{4,}", clean_text.lower()))
            overlap = ctx_words.intersection(comment_words)
            if ctx_words:
                ratio = len(overlap) / min(len(ctx_words), 15)
                relevance = 30.0 + min(65.0, ratio * 90.0)
        if is_spam:
            relevance = 10.0

        # --- Composite Score Calculation ---
        composite = (
            (constructiveness * active_weights["constructiveness"]) +
            (civility * active_weights["civility"]) +
            (persuasiveness * active_weights["persuasiveness"]) +
            (relevance * active_weights["relevance"])
        )
        composite = round(max(0.0, min(100.0, composite)), 1)

        # Status assignment based on active policy thresholds
        if is_spam:
            status = "FLAGGED_SPAM"
            summary = "Commercial spam or unauthorized promotional link."
            composite = min(composite, 20.0)
        elif civility < 50.0 or total_toxic_hits > 0:
            status = "FLAGGED_UNCIVIL"
            summary = "Contains hostile personal attacks or explicit harassment."
        elif total_fallacy_hits >= 1 and total_epistemic_hits == 0:
            status = "NEEDS_IMPROVEMENT"
            summary = "Rhetorical deflection or whataboutism without supporting evidence."
        elif constructiveness < 35.0 and word_count < 6:
            status = "NEEDS_IMPROVEMENT"
            summary = "Low-effort comment with insufficient substance."
        elif composite >= active_thresholds["auto_approve"] and civility >= 70.0:
            status = "APPROVED_PROMOTED"
            summary = "High-quality, constructive contribution with strong epistemic grounding."
        elif composite >= active_thresholds["review"] and civility >= 50.0:
            status = "STANDARD_PUBLISH"
            summary = "Acceptable community comment adhering to standards."
        else:
            status = "NEEDS_IMPROVEMENT"
            summary = "Low informational depth or unsubstantiated critique."

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        result = {
            "composite_score": composite,
            "status": status,
            "summary": summary,
            "backend": "heuristic",
            "policy_applied": active_policy_name,
            "dimensions": {
                "constructiveness": round(constructiveness, 1),
                "civility": round(civility, 1),
                "persuasiveness": round(persuasiveness, 1),
                "relevance": round(relevance, 1)
            },
            "substance_breakdown": {
                "epistemic_evidence_count": total_epistemic_hits,
                "synthesis_arguments_count": total_synthesis_hits,
                "fallacy_count": total_fallacy_hits,
                "toxic_markers_count": total_toxic_hits,
                "sentence_count": len(raw_sentences),
                "words_per_sentence": round(word_count / max(1, len(raw_sentences)), 1)
            },
            "sentence_diagnostics": sentence_diagnostics,
            "metrics": {
                "word_count": word_count,
                "character_count": char_count,
                "latency_ms": duration_ms
            },
            "flags": {
                "is_toxic": civility < 40.0,
                "is_spam": is_spam,
                "is_constructive": constructiveness >= 65.0,
                "is_promotable": composite >= active_thresholds["auto_approve"]
            }
        }

        try:
            from .action_rules import evaluate_action_rules
            result["action_routing"] = evaluate_action_rules(result)
        except Exception:
            pass

        if backend == "hybrid":
            try:
                from .neural_evaluator import NeuralEvaluator
                neural_eng = NeuralEvaluator()
                if neural_eng.is_ready:
                    return neural_eng.evaluate_hybrid(clean_text, result)
            except Exception:
                pass
        elif backend == "neural":
            try:
                from .neural_evaluator import NeuralEvaluator
                neural_eng = NeuralEvaluator()
                if neural_eng.is_ready:
                    return neural_eng.evaluate(clean_text)
            except Exception:
                pass

        return result

    def _empty_result(self) -> Dict[str, Any]:
        return {
            "composite_score": 0.0,
            "status": "EMPTY_INPUT",
            "summary": "No text provided.",
            "policy_applied": self.policy_name,
            "dimensions": {"constructiveness": 0, "civility": 0, "persuasiveness": 0, "relevance": 0},
            "substance_breakdown": {},
            "sentence_diagnostics": [],
            "metrics": {"word_count": 0, "character_count": 0, "latency_ms": 0.0},
            "flags": {"is_toxic": False, "is_spam": False, "is_constructive": False, "is_promotable": False}
        }
