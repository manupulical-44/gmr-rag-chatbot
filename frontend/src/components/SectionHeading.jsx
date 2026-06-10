export default function SectionHeading({ eyebrow, title, description, align = 'center' }) {
  const alignment = align === 'left' ? 'text-left' : 'text-center';

  return (
    <div className={`${alignment} mx-auto max-w-3xl`}>
      <p className="text-sm font-semibold uppercase tracking-[0.24em] text-accent">{eyebrow}</p>
      <h2 className="mt-3 font-display text-3xl font-bold text-secondary sm:text-4xl">{title}</h2>
      {description && <p className="mt-4 text-base leading-7 text-slate-600">{description}</p>}
    </div>
  );
}