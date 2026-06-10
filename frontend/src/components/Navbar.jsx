import { Link, NavLink } from 'react-router-dom';
import { Home, MessageCircle, Search, LayoutDashboard } from 'lucide-react';

const defaultNavItems = [
  { label: 'Home', path: '/', icon: Home },
  { label: 'Properties', path: '/properties', icon: Search },
  { label: 'Chat', path: '/chat', icon: MessageCircle },
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard }
];

export default function Navbar({ navItems = defaultNavItems, showCompactNav = true }) {
  return (
    <header className="sticky top-0 z-40 border-b border-white/60 bg-white/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-primary text-white shadow-soft">
            <Home size={20} />
          </div>
          <div>
            <p className="font-display text-lg font-bold leading-none">GMR AI Homes</p>
            <p className="text-xs uppercase tracking-[0.24em] text-muted">Real estate platform</p>
          </div>
        </Link>

        {showCompactNav && (
          <nav className="hidden items-center gap-2 md:flex">
            {navItems.map((item) => (
              <NavLink
                key={item.label}
                to={item.path}
                className={({ isActive }) =>
                  `rounded-2xl px-4 py-2 text-sm font-medium transition ${
                    isActive
                      ? 'bg-secondary text-white shadow-soft'
                      : 'text-muted hover:bg-slate-100 hover:text-secondary'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        )}

        <Link
          to="/chat"
          className="rounded-2xl bg-primary px-4 py-2 text-sm font-semibold text-white shadow-soft transition hover:translate-y-[-1px] hover:bg-blue-700"
        >
          Ask AI
        </Link>
      </div>
    </header>
  );
}