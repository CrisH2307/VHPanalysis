const LeftToolbar = () => {
  const buttonClass =
    'group relative flex h-12 w-12 items-center justify-center rounded-sm bg-slate-700 text-slate-300 transition-all hover:bg-slate-600 hover:text-white active:bg-slate-500';

  return (
    <aside className="flex w-16 flex-col items-center gap-2 border-r border-slate-300 bg-slate-800 p-2 shadow-lg">
      <button
        type="button"
        aria-label="Add scenario"
        className={buttonClass}
        title="Add scenario"
      >
        <svg
          className="h-6 w-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 4v16m8-8H4"
          />
        </svg>
      </button>

      <button
        type="button"
        aria-label="Remove scenario"
        className={buttonClass}
        title="Remove scenario"
      >
        <svg
          className="h-6 w-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M20 12H4"
          />
        </svg>
      </button>


      <button
        type="button"
        aria-label="Reset layout"
        className={buttonClass}
        title="Reset layout"
      >
        <svg
          className="h-6 w-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
          />
        </svg>
      </button>
    </aside>
  );
};

export default LeftToolbar;
