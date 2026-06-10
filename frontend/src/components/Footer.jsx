import { Facebook, Instagram, Linkedin, Twitter } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-secondary text-white">
      <div className="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 lg:grid-cols-3 lg:px-8">
        <div>
          <p className="font-display text-2xl font-bold">GMR AI Homes</p>
          <p className="mt-3 max-w-md text-sm text-slate-300">
            Premium real estate discovery with modern design, AI assistance, and a future-ready API layer.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-6 text-sm text-slate-300">
          <div>
            <p className="mb-3 font-semibold text-white">Explore</p>
            <ul className="space-y-2">
              <li>Featured Properties</li>
              <li>AI Assistant</li>
              <li>Mortgage Support</li>
            </ul>
          </div>
          <div>
            <p className="mb-3 font-semibold text-white">Company</p>
            <ul className="space-y-2">
              <li>About</li>
              <li>Careers</li>
              <li>Support</li>
            </ul>
          </div>
        </div>

        <div>
          <p className="mb-3 font-semibold text-white">Connect</p>
          <div className="flex gap-3">
            {[Facebook, Instagram, Linkedin, Twitter].map((Icon, index) => (
              <button
                key={index}
                className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white/10 transition hover:bg-white/20"
              >
                <Icon size={18} />
              </button>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}