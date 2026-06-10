export default function FilterPanel({ filters, onChange }) {
  const handleFieldChange = (field, value) => {
    onChange({ ...filters, [field]: value });
  };

  return (
    <div className="glass-panel rounded-3xl p-5 shadow-soft">
      <h3 className="font-display text-xl font-bold">Filters</h3>
      <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <label className="space-y-2 text-sm font-medium text-muted">
          BHK
          <select
            value={filters.bhk}
            onChange={(event) => handleFieldChange('bhk', event.target.value)}
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-secondary outline-none"
          >
            <option value="">Any</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4+</option>
          </select>
        </label>

        <label className="space-y-2 text-sm font-medium text-muted">
          Price Range
          <input
            value={filters.priceRange}
            onChange={(event) => handleFieldChange('priceRange', event.target.value)}
            placeholder="e.g. 5000000-10000000"
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-secondary outline-none"
          />
        </label>

        <label className="space-y-2 text-sm font-medium text-muted">
          City
          <input
            value={filters.city}
            onChange={(event) => handleFieldChange('city', event.target.value)}
            placeholder="Bengaluru"
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-secondary outline-none"
          />
        </label>

        <label className="space-y-2 text-sm font-medium text-muted">
          State
          <input
            value={filters.state}
            onChange={(event) => handleFieldChange('state', event.target.value)}
            placeholder="Karnataka"
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-secondary outline-none"
          />
        </label>

        <label className="space-y-2 text-sm font-medium text-muted">
          Bedrooms
          <input
            type="number"
            value={filters.bedrooms}
            onChange={(event) => handleFieldChange('bedrooms', event.target.value)}
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-secondary outline-none"
          />
        </label>

        <label className="space-y-2 text-sm font-medium text-muted">
          Bathrooms
          <input
            type="number"
            value={filters.bathrooms}
            onChange={(event) => handleFieldChange('bathrooms', event.target.value)}
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-secondary outline-none"
          />
        </label>
      </div>
    </div>
  );
}