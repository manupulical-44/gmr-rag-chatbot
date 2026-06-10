import { Search } from 'lucide-react';

export default function SearchBar({ value, onChange, onSubmit, placeholder = 'Search properties...' }) {
  return (
    <form
      onSubmit={onSubmit}
      className="glass-panel flex flex-col gap-3 rounded-3xl p-3 shadow-soft sm:flex-row sm:items-center"
    >
      <div className="flex flex-1 items-center gap-3 rounded-2xl bg-slate-50 px-4 py-3">
        <Search size={18} className="text-muted" />
        <input
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className="w-full bg-transparent text-sm outline-none placeholder:text-slate-400"
        />
      </div>
      <button
        type="submit"
        className="rounded-2xl bg-primary px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
      >
        Search
      </button>
    </form>
  );
}