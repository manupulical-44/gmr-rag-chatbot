export default function StatCard({ label, value, description }) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-soft">
      <p className="text-sm font-medium text-muted">{label}</p>
      <p className="mt-2 font-display text-3xl font-bold text-secondary">{value}</p>
      <p className="mt-2 text-sm text-slate-500">{description}</p>
    </div>
  );
}