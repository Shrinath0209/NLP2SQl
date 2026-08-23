"""
prepare_dataset.py
Downloads b-mc2/sql-create-context, labels by HYBRID (SQL + question keywords),
saves to dataset/labeled_dataset.json
"""

import re
import json
import os
from collections import Counter
from datasets import load_dataset

SAVE_PATH     = "dataset/labeled_dataset.json"
MAX_PER_CLASS = 600

INTENT_LABELS = ["COUNT", "AVERAGE", "TOP_N", "BOTTOM_N", "FILTER_LT", "FILTER_GT", "SELECT"]


def label_hybrid(question: str, sql: str) -> str:
    """Label using BOTH SQL structure AND question keywords (more accurate)."""
    s = sql.upper().strip()
    q = question.lower().strip()

    # ── COUNT ──
    if re.search(r'\bCOUNT\s*\(', s):
        return "COUNT"
    if any(w in q for w in ["how many", "count", "total number", "number of"]):
        return "COUNT"

    # ── AVERAGE ──
    if re.search(r'\b(AVG|AVERAGE)\s*\(', s):
        return "AVERAGE"
    if any(w in q for w in ["average", "avg", "mean"]):
        return "AVERAGE"

    # ── TOP_N ──
    if re.search(r'ORDER\s+BY\s+\S[\s\S]*?\bDESC\b.*?\bLIMIT\b', s):
        return "TOP_N"
    if any(w in q for w in ["top ", "highest", "best", "most", "maximum", "largest", "greatest"]):
        return "TOP_N"

    # ── BOTTOM_N ──
    if re.search(r'ORDER\s+BY\s+\S[\s\S]*?\bASC\b.*?\bLIMIT\b', s):
        return "BOTTOM_N"
    if any(w in q for w in ["bottom", "lowest", "worst", "least", "minimum", "smallest", "fewest"]):
        return "BOTTOM_N"

    # ── FILTER_LT ──
    if re.search(r'WHERE[\s\S]*?\s*<\s*[\d\'"]', s):
        return "FILTER_LT"
    if any(w in q for w in ["below", "less than", "under", "fewer than", "not more than"]):
        return "FILTER_LT"

    # ── FILTER_GT ──
    if re.search(r'WHERE[\s\S]*?\s*>\s*[\d\'"]', s):
        return "FILTER_GT"
    if any(w in q for w in ["above", "greater than", "more than", "over", "exceeds", "at least"]):
        return "FILTER_GT"

    return "SELECT"


def main():
    print("Loading dataset from HuggingFace (b-mc2/sql-create-context)...")
    ds = load_dataset("b-mc2/sql-create-context", split="train")
    print(f"Total rows: {len(ds)}")

    labeled = []
    for row in ds:
        question = row["question"].strip()
        sql      = row["answer"].strip()
        intent   = label_hybrid(question, sql)
        labeled.append({"text": question, "label": intent, "sql": sql})

    dist = Counter(item["label"] for item in labeled)
    print("\nRaw distribution:")
    for k, v in sorted(dist.items()):
        print(f"  {k:12s}: {v:>6}")

    # Balance
    balanced = []
    counts   = Counter()
    for item in labeled:
        if counts[item["label"]] < MAX_PER_CLASS:
            balanced.append(item)
            counts[item["label"]] += 1

    print(f"\nBalanced: {len(balanced)} examples")
    for k, v in sorted(counts.items()):
        print(f"  {k:12s}: {v}")

    # Mix in hand-crafted domain examples x10 so model learns academic query patterns
    import sys, random
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from dataset.intent_dataset import DATASET as HANDCRAFTED
    domain_examples = [{"text": text, "label": label} for text, label in HANDCRAFTED] * 10
    balanced = domain_examples + balanced
    random.shuffle(balanced)
    print(f"\nAfter domain boost: {len(balanced)} total examples ({len(domain_examples)} domain x10)")

    os.makedirs("dataset", exist_ok=True)
    with open(SAVE_PATH, "w") as f:
        json.dump(balanced, f, indent=2)
    print(f"\nSaved → {SAVE_PATH}")


if __name__ == "__main__":
    main()
