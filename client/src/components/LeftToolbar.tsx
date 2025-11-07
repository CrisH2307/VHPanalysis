import React from 'react';

const buttonClass =
  'flex h-10 w-10 items-center justify-center rounded-lg bg-white/10 text-lg transition hover:bg-white/20';

const LeftToolbar = () => {
  return (
    <aside className="flex w-16 flex-col items-center gap-3 bg-slate-900 px-2 py-4 text-slate-100">
      <button type="button" aria-label="Add scenario" className={buttonClass}>
        +
      </button>
      <button type="button" aria-label="Remove scenario" className={buttonClass}>
        –
      </button>
      <button type="button" aria-label="Reset layout" className={buttonClass}>
        ↺
      </button>
    </aside>
  );
};

export default LeftToolbar;
