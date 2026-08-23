export default function HistoryPage({ history, onRerun, onClear }) {
  if (history.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-[#8a7a6a] gap-3 py-20">
        <svg className="w-10 h-10 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span className="text-sm">No queries yet. Run something from the Query tab.</span>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <span className="text-[10px] tracking-[0.15em] text-[#8a7a6a] font-semibold uppercase">{history.length} queries</span>
        <button
          onClick={onClear}
          className="text-[11px] text-red-400 hover:text-red-600 transition-colors px-2 py-1 border border-red-200 hover:bg-red-50"
        >Clear All</button>
      </div>

      {[...history].reverse().map((item, i) => (
        <div key={i} className="bg-white border border-[#e5ddd0] overflow-hidden">
          <div className="flex items-center justify-between px-4 py-2.5 border-b border-[#ede6d8] bg-[#fdfcfa]">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-[10px] text-[#8a7a6a]">{item.timestamp}</span>
              <span className={`px-2 py-0.5 text-[10px] font-semibold border ${
                item.success
                  ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                  : "bg-red-50 text-red-600 border-red-200"
              }`}>
                {item.success ? `${item.row_count} rows` : "Error"}
              </span>
              {/* Intent badge */}
              <span className="px-2 py-0.5 bg-[#c92a0e] text-white text-[10px] font-semibold">
                {item.intent}
              </span>
              {/* Neural/rules source badge */}
              {item.intent_src && (
                <span className={`px-2 py-0.5 text-[10px] font-semibold border ${
                  item.intent_src === "neural"
                    ? "bg-[#fff0ee] text-[#c92a0e] border-[#f5c4bc]"
                    : "bg-stone-100 text-stone-500 border-stone-200"
                }`}>
                  {item.intent_src === "neural" ? "⚡ neural" : "📋 rules"}
                </span>
              )}
              {/* Confidence */}
              {item.intent_conf > 0 && (
                <span className="text-[10px] text-[#8a7a6a]">{item.intent_conf}%</span>
              )}
            </div>
            <button
              onClick={() => onRerun(item.query)}
              className="text-[11px] text-[#8a7a6a] hover:text-[#1c1410] border border-[#e5ddd0] px-2 py-0.5 hover:bg-stone-50 transition-colors shrink-0"
            >↩ Rerun</button>
          </div>
          <div className="px-4 py-3">
            <div className="text-sm text-[#1c1410] font-medium mb-2">{item.query}</div>
            <div className="bg-[#1a0f08] px-3 py-2 font-mono text-[11px] text-orange-300 overflow-x-auto whitespace-pre">
              {item.sql}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
