import { Bell, ChevronDown, Search } from 'lucide-react';

export default function TopNavigation() {
  return (
    <div className="glass-panel flex items-center justify-between rounded-3xl px-5 py-4 shadow-soft">
      <div>
        <p className="text-sm text-muted">AI ready search and discovery</p>
        <h2 className="font-display text-2xl font-bold">Premium Real Estate Platform</h2>
      </div>

      <div className="flex items-center gap-3">
        <button className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-100 text-secondary transition hover:bg-slate-200">
          <Bell size={18} />
        </button>
        <button className="flex items-center gap-2 rounded-2xl bg-secondary px-4 py-2 text-sm font-semibold text-white">
          <Search size={16} />
          Explore
          <ChevronDown size={16} />
        </button>
      </div>
    </div>
  );
}