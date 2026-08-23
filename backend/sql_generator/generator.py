"""
SQL Generation Module
Maps NLP intent + schema match → SQL query using templates.
"""
import re
from backend.utils.schema_meta import SCHEMA_META

class SQLGenerator:
    def generate(self, query: str, preprocessed: dict, schema_match: dict) -> dict:
        intent = preprocessed["intent"]
        numbers = preprocessed["numbers"]
        table = schema_match["matched_table"]
        columns = [col for col, _ in schema_match["matched_columns"]]
        query_lower = query.lower()

        sql = ""
        explanation = {}

        if intent == "COUNT":
            sql = f"SELECT COUNT(*) as total FROM {table}"
            explanation = {"intent": "COUNT", "table": table}

        elif intent == "AVERAGE":
            numeric_cols = self._get_numeric_columns(table)
            avg_col = self._keyword_match(query_lower, numeric_cols) or columns[0] if columns else numeric_cols[0]
            sql = f"SELECT AVG({avg_col}) as average_{avg_col} FROM {table}"
            explanation = {"intent": "AVERAGE", "table": table, "column": avg_col}

        elif intent == "TOP_N":
            n = int(numbers[0]) if numbers else 5
            order_col = self._keyword_match(query_lower, self._get_numeric_columns(table)) or self._get_numeric_columns(table)[0]
            sql = f"SELECT * FROM {table} ORDER BY {order_col} DESC LIMIT {n}"
            explanation = {"intent": "TOP_N", "table": table, "order_by": order_col, "limit": n}

        elif intent == "BOTTOM_N":
            n = int(numbers[0]) if numbers else 5
            order_col = self._keyword_match(query_lower, self._get_numeric_columns(table)) or self._get_numeric_columns(table)[0]
            sql = f"SELECT * FROM {table} ORDER BY {order_col} ASC LIMIT {n}"
            explanation = {"intent": "BOTTOM_N", "table": table, "order_by": order_col, "limit": n}

        elif intent == "FILTER_LT":
            filter_col, threshold = self._get_filter_params(query_lower, table, numbers)
            sql = f"SELECT * FROM {table} WHERE {filter_col} < {threshold}"
            explanation = {"intent": "FILTER_LT", "table": table, "condition": f"{filter_col} < {threshold}"}

        elif intent == "FILTER_GT":
            filter_col, threshold = self._get_filter_params(query_lower, table, numbers)
            sql = f"SELECT * FROM {table} WHERE {filter_col} > {threshold}"
            explanation = {"intent": "FILTER_GT", "table": table, "condition": f"{filter_col} > {threshold}"}

        else:  # SELECT
            dept_match = re.search(r'\b(cse|ece|me|civil|it|eee)\b', query_lower)
            if dept_match:
                dept = dept_match.group(1).upper()
                sql = f"SELECT * FROM {table} WHERE department = \'{dept}\'"
                explanation = {"intent": "SELECT_FILTER", "table": table, "condition": f"department = \'{dept}\'"}
            else:
                sql = f"SELECT * FROM {table} LIMIT 20"
                explanation = {"intent": "SELECT_ALL", "table": table}

        return {"sql": sql, "explanation": explanation}

    def _get_numeric_columns(self, table: str) -> list:
        numeric_map = {
            "students": ["cgpa", "attendance", "semester"],
            "marks": ["marks", "semester"],
            "courses": ["credits"]
        }
        return numeric_map.get(table, ["id"])

    def _keyword_match(self, query_lower: str, columns: list) -> str:
        """Directly check if column name appears in the query."""
        for col in columns:
            if col in query_lower:
                return col
        return None

    def _get_filter_params(self, query_lower: str, table: str, numbers: list) -> tuple:
        numeric = self._get_numeric_columns(table)
        filter_col = self._keyword_match(query_lower, numeric) or numeric[0]
        # Default thresholds per column
        defaults = {"attendance": 75, "cgpa": 8.0, "marks": 50, "semester": 4, "credits": 3}
        threshold = numbers[0] if numbers else defaults.get(filter_col, 50)
        return filter_col, threshold
