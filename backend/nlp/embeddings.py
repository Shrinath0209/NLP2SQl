"""
Embedding Generation Module
Uses SentenceTransformer (all-MiniLM-L6-v2) to generate semantic vector representations
for user queries and schema metadata, then computes cosine similarity for schema linking.
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from backend.utils.schema_meta import SCHEMA_META, SYNONYMS

MODEL_NAME = "all-MiniLM-L6-v2"

class EmbeddingMatcher:
    def __init__(self):
        print(f"Loading transformer model: {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)
        self._build_schema_embeddings()

    def _build_schema_embeddings(self):
        """Pre-compute embeddings for all schema components."""
        self.table_embeddings = {}
        self.column_embeddings = {}

        for table, meta in SCHEMA_META.items():
            self.table_embeddings[table] = self.model.encode([meta["description"]])[0]
            self.column_embeddings[table] = {}
            for col, desc in meta["columns"].items():
                self.column_embeddings[table][col] = self.model.encode([desc])[0]

    def apply_synonyms(self, text: str) -> str:
        for word, replacement in SYNONYMS.items():
            text = text.replace(word, replacement)
        return text

    def match_table(self, query: str) -> tuple:
        """Returns (best_table, confidence_score)"""
        query = self.apply_synonyms(query)
        query_emb = self.model.encode([query])[0]

        scores = {}
        for table, emb in self.table_embeddings.items():
            sim = cosine_similarity([query_emb], [emb])[0][0]
            scores[table] = float(sim)

        best_table = max(scores, key=scores.get)
        return best_table, scores[best_table], scores

    def match_columns(self, query: str, table: str) -> list:
        """Returns list of (column, confidence) sorted by relevance."""
        query = self.apply_synonyms(query)
        query_emb = self.model.encode([query])[0]

        if table not in self.column_embeddings:
            return []

        results = []
        for col, emb in self.column_embeddings[table].items():
            sim = cosine_similarity([query_emb], [emb])[0][0]
            results.append((col, float(sim)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_schema_match(self, query: str) -> dict:
        """Full schema matching: returns table + relevant columns with confidence scores."""
        table, table_conf, all_table_scores = self.match_table(query)
        columns = self.match_columns(query, table)

        return {
            "matched_table": table,
            "table_confidence": round(table_conf * 100, 1),
            "all_table_scores": {k: round(v * 100, 1) for k, v in all_table_scores.items()},
            "matched_columns": [(col, round(conf * 100, 1)) for col, conf in columns[:5]]
        }
