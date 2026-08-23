const INTENT_DESC = {
  COUNT: "Counting total records",
  AVERAGE: "Computing average of a numeric column",
  TOP_N: "Fetching top N records ordered by a metric",
  BOTTOM_N: "Fetching bottom N records ordered by a metric",
  FILTER_LT: "Filtering rows where a value is less than a threshold",
  FILTER_GT: "Filtering rows where a value is greater than a threshold",
  SELECT: "Selecting records with optional filters",
  SELECT_ALL: "Selecting all records",
  SELECT_FILTER: "Filtering by department or category",
};

export default function IntentCard({ intent }) {
  return (
    <div className="card">
      <h3>🧠 Intent</h3>
      <div className="intent-value">{intent}</div>
      <div className="intent-desc">{INTENT_DESC[intent] ?? "—"}</div>
    </div>
  );
}
