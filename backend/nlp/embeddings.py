"""Lightweight schema matching for the production deployment.

TF-IDF keeps the Render free instance well below its memory limit. The
transformer implementation can still be used locally by replacing this
matcher when more memory is available.
"""
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from backend.utils.schema_meta import SCHEMA_META, SYNONYMS

class EmbeddingMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
        self._build_schema_vectors()

    def _build_schema_vectors(self):
        """Pre-compute sparse vectors for all schema components."""
        self.table_vectors = {}
        self.column_vectors = {}
        descriptions = []

        for table, meta in SCHEMA_META.items():
            descriptions.append(meta["description"])
            for col, desc in meta["columns"].items():
                descriptions.append(desc)

        self.vectorizer.fit(descriptions)
        for table, meta in SCHEMA_META.items():
            table_text = " ".join([meta["description"], *meta["columns"].values()])
            self.table_vectors[table] = self.vectorizer.transform([table_text])
            self.column_vectors[table] = {
                col: self.vectorizer.transform([desc])
                for col, desc in meta["columns"].items()
            }

    def apply_synonyms(self, text: str) -> str:
        for word, replacement in SYNONYMS.items():
            text = text.replace(word, replacement)
        return text

    def match_table(self, query: str) -> tuple:
        """Returns (best_table, confidence_score)"""
        query = self.apply_synonyms(query)
        query_vector = self.vectorizer.transform([query])

        scores = {}
        for table, vector in self.table_vectors.items():
            sim = cosine_similarity(query_vector, vector)[0][0]
            query_words = set(query.lower().split())
            if table in query_words:
                sim += 0.75
            if query_words.intersection(SCHEMA_META[table]["columns"]):
                sim += 0.5
            scores[table] = float(sim)

        best_table = max(scores, key=scores.get)
        return best_table, scores[best_table], scores

    def match_columns(self, query: str, table: str) -> list:
        """Returns list of (column, confidence) sorted by relevance."""
        query = self.apply_synonyms(query)
        query_vector = self.vectorizer.transform([query])

        if table not in self.column_vectors:
            return []

        results = []
        for col, vector in self.column_vectors[table].items():
            sim = cosine_similarity(query_vector, vector)[0][0]
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
