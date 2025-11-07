import React from 'react';

const statusLegend = [
  { level: 'Must', detail: 'Needs attention, do more' },
  { level: 'High', detail: 'Looks good, keep going' },
  { level: 'Low', detail: 'Hot zone, not ok' },
];

const ScorePanel = () => {
  return (
    <section className="flex min-h-[280px] flex-col rounded-2xl border border-slate-200 bg-white p-5">
      <header className="mb-2">
        <h2 className="text-lg font-semibold text-slate-800">Score</h2>
        <span className="text-sm text-slate-500">Same date</span>
      </header>

      <div className="text-4xl font-bold text-blue-600">400</div>
      <div className="flex-1 text-sm leading-relaxed text-slate-600">
        <p className="text-slate-500">Explanation placeholder</p>
        <ul className="mt-3 list-disc pl-5 text-slate-600">
          <li>Key insight detail</li>
          <li>Why this matters</li>
          <li>Next consideration</li>
        </ul>
      </div>

      <div className="space-y-2 border-t border-dashed border-slate-200 pt-3 text-sm text-slate-600">
        {statusLegend.map((legend) => (
          <div key={legend.level}>
            <strong className="text-slate-900">{legend.level}</strong>
            <p className="m-0 text-slate-600">{legend.detail}</p>
          </div>
        ))}
      </div>

      <button
        type="button"
        className="mt-3 w-fit rounded-full bg-blue-600 px-5 py-2 text-sm font-semibold text-white transition hover:bg-blue-500"
      >
        Recommend Action
      </button>
    </section>
  );
};

export default ScorePanel;
