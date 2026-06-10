import { Link, Outlet } from 'react-router-dom';
import { Bell, Menu, UserCircle2 } from 'lucide-react';
import Navbar from '../components/Navbar';

const navItems = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Properties', path: '/properties' },
  { label: 'AI Chat', path: '/chat' }
];

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-background text-secondary">
      <Navbar navItems={navItems} showCompactNav={false} />
      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:px-8">
        <aside className="glass-panel hidden w-64 shrink-0 rounded-3xl p-5 lg:block">
          <div className="mb-6 flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary text-white shadow-soft">
              <Menu size={20} />
            </div>
            <div>
              <p className="font-display text-lg font-bold">GMR AI</p>
              <p className="text-sm text-muted">Real estate workspace</p>
            </div>
          </div>

          <nav className="space-y-2 text-sm font-medium">
            {navItems.map((item) => (
              <Link
                key={item.label}
                to={item.path}
                className="block rounded-2xl px-4 py-3 text-muted transition hover:bg-slate-100 hover:text-secondary"
              >
                {item.label}
              </Link>
            ))}
          </nav>

          <div className="mt-8 rounded-2xl bg-slate-50 p-4">
            <p className="text-sm font-semibold text-secondary">Search summary</p>
            <p className="mt-1 text-sm text-muted">Property discovery, chat support, and future API integration.</p>
          </div>
        </aside>

        <section className="min-w-0 flex-1">
          <div className="mb-6 flex items-center justify-between rounded-3xl bg-white px-5 py-4 shadow-soft">
            <div>
              <p className="text-sm text-muted">Welcome back</p>
              <h1 className="font-display text-2xl font-bold">GMR Real Estate AI Assistant</h1>
            </div>
            <div className="flex items-center gap-3">
              <button className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-100 text-secondary transition hover:bg-slate-200">
                <Bell size={18} />
              </button>
              <button className="flex items-center gap-2 rounded-2xl bg-secondary px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800">
                <UserCircle2 size={18} />
                Profile
              </button>
            </div>
          </div>
          <Outlet />
        </section>
      </div>
    </div>
  );
}