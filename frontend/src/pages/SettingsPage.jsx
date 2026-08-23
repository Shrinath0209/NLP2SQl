export default function SettingsPage({ modelInfo }) {
  return (
    <div className="flex flex-col gap-4 max-w-xl">

      {/* Neural Model Info */}
      <div className="bg-white border border-[#e5ddd0] overflow-hidden">
        <div className="px-4 py-2.5 border-b border-[#ede6d8] bg-[#fdfcfa] text-[10px] tracking-[0.15em] font-semibold text-[#8a7a6a] uppercase">
          Neural Intent Classifier
        </div>
        <div className="p-4 space-y-2.5">
          {/* Architecture visual */}
          <div className="bg-[#1a0f08] p-3 font-mono text-[11px] leading-6 text-stone-300">
            <span className="text-[#8a7a6a]">Input text</span>{"\n"}
            {"    "}↓{"\n"}
            <span className="text-yellow-300">MiniLM</span>{" "}
            <span className="text-[#8a7a6a]">(frozen · 22.7M params)</span>{"\n"}
            {"    "}↓ <span className="text-emerald-400">384-dim</span>{"\n"}
            <span className="text-orange-300">Linear</span>
            <span className="text-stone-400">(384→128)</span>{" → "}
            <span className="text-orange-300">ReLU</span>{" → "}
            <span className="text-orange-300">Linear</span>
            <span className="text-stone-400">(128→7)</span>{"\n"}
            {"    "}↓ <span className="text-[#8a7a6a]">50,183 trainable params</span>{"\n"}
            <span className="text-[#c92a0e]">CrossEntropyLoss</span>
            {" · "}
            <span className="text-emerald-400">Adam</span>
          </div>

          {[
            ["Encoder",          modelInfo?.encoder          || "all-MiniLM-L6-v2"],
            ["Embedding Dim",    modelInfo?.encoder_dim      || 384],
            ["Trainable Params", modelInfo?.trainable_params || "50,183"],
            ["Frozen Params",    modelInfo?.frozen_params    || "22,713,216"],
            ["Loss Function",    modelInfo?.loss             || "CrossEntropyLoss"],
            ["Optimizer",        modelInfo?.optimizer        || "Adam (lr=2e-4)"],
            ["Epochs",           modelInfo?.epochs           || 40],
            ["Batch Size",       modelInfo?.batch_size       || 32],
            ["Val Accuracy",     modelInfo?.val_accuracy     || "90%"],
            ["Trained On",       "Google Colab T4 GPU"],
          ].map(([k, v]) => (
            <div key={k} className="flex items-center justify-between gap-2 border-b border-[#f5ede0] pb-2 last:border-0 last:pb-0">
              <span className="text-[11px] text-[#8a7a6a]">{k}</span>
              <span className="text-[11px] font-semibold text-[#1c1410] font-mono">{v}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Intent Classes */}
      <div className="bg-white border border-[#e5ddd0] overflow-hidden">
        <div className="px-4 py-2.5 border-b border-[#ede6d8] bg-[#fdfcfa] text-[10px] tracking-[0.15em] font-semibold text-[#8a7a6a] uppercase">
          Intent Classes (7)
        </div>
        <div className="p-4 flex flex-wrap gap-2">
          {(modelInfo?.intent_classes || ["COUNT","AVERAGE","TOP_N","BOTTOM_N","FILTER_LT","FILTER_GT","SELECT"]).map(c => (
            <span key={c} className="px-3 py-1 text-[11px] font-semibold bg-[#c92a0e] text-white">{c}</span>
          ))}
        </div>
      </div>

      {/* Training Dataset */}
      <div className="bg-white border border-[#e5ddd0] overflow-hidden">
        <div className="px-4 py-2.5 border-b border-[#ede6d8] bg-[#fdfcfa] text-[10px] tracking-[0.15em] font-semibold text-[#8a7a6a] uppercase">
          Training Data
        </div>
        <div className="p-4 space-y-2">
          {[
            ["Source",        "b-mc2/sql-create-context"],
            ["Size",          "78K NL→SQL pairs (HuggingFace)"],
            ["Labeling",      "Hybrid SQL pattern + question keywords"],
            ["Balanced",      "600 per class (4,200 total)"],
            ["Domain Boost",  "56 academic examples × 10"],
            ["Model Weights", "Ipsita /nl2sql-intent (HF)"],
          ].map(([k, v]) => (
            <div key={k} className="flex items-start justify-between gap-4 border-b border-[#f5ede0] pb-2 last:border-0 last:pb-0">
              <span className="text-[11px] text-[#8a7a6a] shrink-0">{k}</span>
              <span className="text-[11px] font-semibold text-[#1c1410] text-right">{v}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Backend */}
      <div className="bg-white border border-[#e5ddd0] overflow-hidden">
        <div className="px-4 py-2.5 border-b border-[#ede6d8] bg-[#fdfcfa] text-[10px] tracking-[0.15em] font-semibold text-[#8a7a6a] uppercase">
          Stack
        </div>
        <div className="p-4 space-y-2">
          {[
            ["Backend",    "FastAPI + Uvicorn"],
            ["Database",   "SQLite · academic.db"],
            ["Frontend",   "React + Vite + Tailwind"],
            ["NLP",        "sentence-transformers"],
            ["Author",     "Ipsita S · LPU"],
            ["Version",    "v2.0"],
          ].map(([k, v]) => (
            <div key={k} className="flex justify-between border-b border-[#f5ede0] pb-2 last:border-0 last:pb-0">
              <span className="text-[11px] text-[#8a7a6a]">{k}</span>
              <span className="text-[11px] font-semibold text-[#1c1410]">{v}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
