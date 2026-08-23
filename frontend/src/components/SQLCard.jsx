export default function SQLCard({ sql }) {
  return (
    <div className="card full-width">
      <h3>⚙️ Generated SQL</h3>
      <div className="sql-block">{sql}</div>
    </div>
  );
}
