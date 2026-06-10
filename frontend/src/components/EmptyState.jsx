import { SearchX } from 'lucide-react';

export default function EmptyState({ title = 'No properties found', description = 'Try changing your filters and search again.' }) {
  return (
    <div className="glass-panel flex flex-col items-center justify-center rounded-3xl px-6 py-16 text-center shadow-soft">
      <div className="mb-4 rounded-3xl bg-primary/10 p-4 text-primary">
        <SearchX size={28} />
      </div>
      <h3 className="font-display text-2xl font-bold text-secondary">{title}</h3>
      <p className="mt-3 max-w-md text-sm leading-6 text-slate-600">{description}</p>
    </div>
  );
}