export default function QueryInput({ value, onChange, onSubmit, loading, samples, onSample }) {
  return (
    <div className="input-section">
      <div className="input-row">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && onSubmit()}
          placeholder="Ask anything… e.g. show top 5 students by cgpa"
          autoComplete="off"
        />
        <button className="generate-btn" onClick={onSubmit} disabled={loading}>
          {loading ? "Loading…" : "Generate SQL"}
        </button>
      </div>
      <div className="chips">
        {samples.map((s) => (
          <span key={s} className="chip" onClick={() => onSample(s)}>
            {s}
          </span>
        ))}
      </div>
    </div>
  );
}
