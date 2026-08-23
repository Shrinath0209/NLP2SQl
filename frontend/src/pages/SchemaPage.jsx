export default function SchemaPage({ schemaInfo }) {
  if (!schemaInfo) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-400 text-sm">
        Loading schema…
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4">
      <div className="mb-4 text-[10px] tracking-widest text-gray-400 font-semibold">
        {Object.keys(schemaInfo).length} TABLES · academic.db
      </div>
      <div className="flex flex-col gap-4">
        {Object.entries(schemaInfo).map(([table, meta]) => (
          <div key={table} className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            {/* Table header */}
            <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-100 bg-gray-50">
              <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <rect x="3" y="3" width="18" height="18" rx="2" strokeWidth={2} />
                <path d="M3 9h18M9 9v12" strokeWidth={2} />
              </svg>
              <span className="text-sm font-bold text-gray-900 uppercase tracking-wide">{table}</span>
              <span className="text-[10px] text-gray-400 ml-auto">{Object.keys(meta.columns).length} columns</span>
            </div>
            {/* Description */}
            <div className="px-4 py-2 border-b border-gray-50 text-[11px] text-gray-500 italic">
              {meta.description}
            </div>
            {/* Columns */}
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="px-4 py-2 text-left text-[10px] tracking-widest font-semibold text-gray-400 w-1/3">COLUMN</th>
                  <th className="px-4 py-2 text-left text-[10px] tracking-widest font-semibold text-gray-400">DESCRIPTION</th>
                  <th className="px-4 py-2 text-left text-[10px] tracking-widest font-semibold text-gray-400 w-1/5">TYPE</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(meta.columns).map(([col, desc]) => {
                  const isId = col.includes("id");
                  const isNum = ["cgpa", "attendance", "marks", "credits", "semester"].includes(col);
                  const type = isId ? "INTEGER PK" : isNum ? "REAL" : "TEXT";
                  return (
                    <tr key={col} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-2.5 font-mono font-semibold text-gray-800">{col}</td>
                      <td className="px-4 py-2.5 text-gray-500">{desc}</td>
                      <td className="px-4 py-2.5">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                          isId ? "bg-amber-100 text-amber-700" :
                          isNum ? "bg-blue-100 text-blue-700" :
                          "bg-gray-100 text-gray-600"
                        }`}>{type}</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}
