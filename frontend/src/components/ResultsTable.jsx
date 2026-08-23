export default function ResultsTable({ execution }) {
  if (!execution.success) {
    return <div className="error-box">SQL Error: {execution.error}</div>;
  }

  return (
    <div className="results-full-card">
      <h3>📊 Query Results</h3>
      <div className="row-count">{execution.row_count} row{execution.row_count !== 1 ? "s" : ""} returned</div>
      {execution.row_count === 0 ? (
        <p style={{ color: "#4b5563", fontSize: "0.88rem" }}>No results found.</p>
      ) : (
        <table className="results-table">
          <thead>
            <tr>{execution.columns.map((c) => <th key={c}>{c}</th>)}</tr>
          </thead>
          <tbody>
            {execution.rows.map((row, i) => (
              <tr key={i}>
                {row.map((cell, j) => <td key={j}>{cell ?? "—"}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
