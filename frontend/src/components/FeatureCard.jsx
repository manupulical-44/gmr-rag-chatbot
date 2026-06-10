export default function FeatureCard({ icon: Icon, title, description }) {
  return (
    <div className="glass-panel rounded-3xl p-6 shadow-soft transition hover:-translate-y-1">
      <div className="mb-4 inline-flex rounded-2xl bg-primary/10 p-3 text-primary">
        <Icon size={22} />
      </div>
      <h3 className="font-display text-xl font-bold text-secondary">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-slate-600">{description}</p>
    </div>
  );
}