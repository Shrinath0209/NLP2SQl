export default function SchemaCard({ match }) {
  return (
    <div className="card">
      <h3>🔍 Detected Schema</h3>
      <div className="table-name">{match.matched_table}</div>
      <div className="confidence">Confidence: {match.table_confidence}%</div>
      <div className="score-bars">
        {Object.entries(match.all_table_scores).map(([table, score]) => (
          <div className="score-bar-row" key={table}>
            <span className="score-bar-label">{table}</span>
            <div className="score-bar-track">
              <div className="score-bar-fill" style={{ width: `${score}%` }} />
            </div>
            <span className="score-bar-pct">{score}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
