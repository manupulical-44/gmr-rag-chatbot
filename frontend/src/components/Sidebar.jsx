import { NavLink } from 'react-router-dom';

const items = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Properties', path: '/properties' },
  { label: 'AI Chat', path: '/chat' }
];

export default function Sidebar() {
  return (
    <aside className="glass-panel rounded-3xl p-5 shadow-soft">
      <p className="font-display text-xl font-bold">Navigation</p>
      <div className="mt-4 space-y-2">
        {items.map((item) => (
          <NavLink
            key={item.label}
            to={item.path}
            className={({ isActive }) =>
              `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                isActive ? 'bg-primary text-white' : 'bg-slate-50 text-muted hover:bg-slate-100 hover:text-secondary'
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </div>
    </aside>
  );
}