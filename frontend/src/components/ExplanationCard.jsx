export default function ExplanationCard({ explanation }) {
  return (
    <div className="card" style={{ marginBottom: "1rem" }}>
      <h3>📋 Explanation</h3>
      <div className="explanation-items">
        {Object.entries(explanation).map(([k, v]) => (
          <div className="explanation-item" key={k}>
            <span className="key">{k}:</span>
            <span className="val">{String(v)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
