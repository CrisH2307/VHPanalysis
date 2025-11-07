import React, { ReactNode } from 'react';

type MapPanelProps = {
  title: string;
  subtitle: string;
  children?: ReactNode;
  description?: string;
  className?: string;
};

const baseClass =
  'flex min-h-[280px] flex-col rounded-2xl border border-slate-200 bg-white p-5';

const MapPanel = ({
  title,
  subtitle,
  children,
  description,
  className,
}: MapPanelProps) => {
  const content = children ?? description;
  const composedClass = className ? `${baseClass} ${className}` : baseClass;

  return (
    <section className={composedClass}>
      <header className="mb-4">
        <h2 className="text-lg font-semibold text-slate-800">{title}</h2>
        <span className="text-sm text-slate-500">{subtitle}</span>
      </header>
      <div className="flex-1 text-sm leading-relaxed text-slate-500">{content}</div>
    </section>
  );
};

export default MapPanel;
