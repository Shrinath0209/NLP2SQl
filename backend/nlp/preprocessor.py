"""
NLP Preprocessing Module
Handles: tokenization, normalization, punctuation removal, keyword/entity detection.

Intent Detection:
  If a trained neural model exists (models/intent_classifier.pt),
  uses the fine-tuned MiniLM + Linear head (neural).
  Falls back to rule-based detection if model not found.
"""
import re
import os
import torch

STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "of", "in", "on", "at", "to", "for", "with", "by", "from", "and", "or", "but", "not", "all", "me", "my", "i", "we", "you", "it", "this", "that", "those", "these", "who", "which", "where", "what", "how", "get", "give", "show", "list", "find", "display", "fetch"}

NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "intent_classifier.pt")


def _load_neural_model():
    """Load fine-tuned IntentClassifier if weights exist."""
    abs_path = os.path.abspath(MODEL_PATH)
    if not os.path.exists(abs_path):
        return None, None
    try:
        from backend.nlp.intent_model import IntentClassifier
        checkpoint = torch.load(abs_path, map_location="cpu", weights_only=False)
        model = IntentClassifier(
            num_classes=checkpoint["num_classes"],
            hidden_dim=checkpoint["hidden_dim"],
        )
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()
        id2label = checkpoint["id2label"]
        print("[NLPreprocessor] Neural intent model loaded ✓")
        return model, id2label
    except Exception as e:
        print(f"[NLPreprocessor] Neural model load failed: {e} — using rules")
        return None, None


# Load once at module import
_NEURAL_MODEL, _ID2LABEL = _load_neural_model()
_DEVICE = torch.device("cpu")


class NLPreprocessor:
    def preprocess(self, text: str) -> dict:
        """Full preprocessing pipeline. Returns structured info."""
        normalized = self.normalize(text)
        tokens     = self.tokenize(normalized)
        keywords   = self.extract_keywords(tokens)
        numbers    = self.extract_numbers(text)
        intent, intent_conf, intent_source = self.detect_intent(text)
        return {
            "original"      : text,
            "normalized"    : normalized,
            "tokens"        : tokens,
            "keywords"      : keywords,
            "numbers"       : numbers,
            "intent"        : intent,
            "intent_conf"   : round(intent_conf * 100, 1),
            "intent_source" : intent_source,   # "neural" | "rules"
        }

    def normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def tokenize(self, text: str) -> list:
        return text.split()

    def extract_keywords(self, tokens: list) -> list:
        return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

    def extract_numbers(self, text: str) -> list:
        nums   = re.findall(r'\b\d+\.?\d*\b', text)
        result = [float(n) if '.' in n else int(n) for n in nums]
        for word, val in NUMBER_WORDS.items():
            if word in text.lower():
                result.append(val)
        return result

    def detect_intent(self, text: str) -> tuple:
        """
        Returns (intent_label, confidence, source).
        Uses neural model if available, else rule-based fallback.
        """
        # ── Neural path ──
        if _NEURAL_MODEL is not None:
            label_id, confidence = _NEURAL_MODEL.predict(text, _DEVICE)
            intent = _ID2LABEL[label_id]
            return intent, confidence, "neural"

        # ── Rule-based fallback ──
        text_lower = text.lower()
        if any(w in text_lower for w in ["count", "how many", "total number"]):
            return "COUNT", 1.0, "rules"
        if any(w in text_lower for w in ["average", "avg", "mean"]):
            return "AVERAGE", 1.0, "rules"
        if any(w in text_lower for w in ["top", "highest", "best", "maximum", "max"]):
            return "TOP_N", 1.0, "rules"
        if any(w in text_lower for w in ["bottom", "lowest", "worst", "minimum", "min"]):
            return "BOTTOM_N", 1.0, "rules"
        if any(w in text_lower for w in ["below", "less than", "under", "low"]):
            return "FILTER_LT", 1.0, "rules"
        if any(w in text_lower for w in ["above", "greater than", "over", "high", "more than"]):
            return "FILTER_GT", 1.0, "rules"
        return "SELECT", 1.0, "rules"
