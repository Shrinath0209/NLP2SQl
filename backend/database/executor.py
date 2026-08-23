"""Safe SQL execution with validation."""
import re
import pandas as pd
from backend.database.schema import engine

BLOCKED_KEYWORDS = ["DROP", "DELETE", "INSERT", "UPDATE", "TRUNCATE", "ALTER", "CREATE", "EXEC"]

class SQLExecutor:
    def validate(self, sql: str) -> tuple:
        sql_upper = sql.upper()
        for kw in BLOCKED_KEYWORDS:
            if re.search(r'\b' + kw + r'\b', sql_upper):
                return False, f"Blocked keyword: {kw}"
        if not sql_upper.strip().startswith("SELECT"):
            return False, "Only SELECT queries allowed"
        return True, "OK"

    def execute(self, sql: str) -> dict:
        valid, msg = self.validate(sql)
        if not valid:
            return {"success": False, "error": msg, "rows": [], "columns": []}
        try:
            df = pd.read_sql(sql, engine)
            return {
                "success": True,
                "rows": df.values.tolist(),
                "columns": df.columns.tolist(),
                "row_count": len(df)
            }
        except Exception as e:
            return {"success": False, "error": str(e), "rows": [], "columns": []}
