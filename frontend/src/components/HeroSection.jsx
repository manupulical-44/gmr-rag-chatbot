import { motion } from 'framer-motion';
import { Search, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-hero-gradient px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(20,184,166,0.15),transparent_40%),radial-gradient(circle_at_bottom_left,rgba(37,99,235,0.18),transparent_35%)]" />
      <div className="relative mx-auto grid max-w-7xl gap-12 lg:grid-cols-[1.15fr_0.85fr] lg:items-center">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-8"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-white/60 bg-white/70 px-4 py-2 text-sm font-medium text-secondary shadow-glass">
            <Sparkles size={16} className="text-accent" />
            AI-powered property discovery
          </div>

          <div className="max-w-2xl space-y-5">
            <h1 className="font-display text-5xl font-bold leading-tight text-secondary sm:text-6xl">
              Find Your Dream Home with AI
            </h1>
            <p className="text-lg leading-8 text-slate-600 sm:text-xl">
              Discover premium homes, compare listings, and chat with an intelligent assistant built for modern real estate journeys.
            </p>
          </div>

          <div className="glass-panel flex flex-col gap-3 rounded-3xl p-3 shadow-soft sm:flex-row sm:items-center">
            <div className="flex-1 rounded-2xl bg-white px-4 py-3">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted">Search</p>
              <p className="text-sm text-slate-500">BHK, city, budget, or neighborhood</p>
            </div>
            <Link
              to="/properties"
              className="inline-flex items-center justify-center gap-2 rounded-2xl bg-primary px-5 py-4 font-semibold text-white transition hover:bg-blue-700"
            >
              <Search size={18} />
              Explore Properties
            </Link>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="relative"
        >
          <div className="glass-panel relative overflow-hidden rounded-[2rem] p-4 shadow-soft">
            <img
              src="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80"
              alt="Modern luxury home"
              className="h-[420px] w-full rounded-[1.5rem] object-cover"
            />
            <div className="absolute bottom-6 left-6 right-6 rounded-3xl bg-white/90 p-5 shadow-soft backdrop-blur-xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.24em] text-muted">Featured home</p>
                  <p className="font-display text-xl font-bold">Skyline Residences</p>
                </div>
                <div className="rounded-2xl bg-accent px-3 py-2 text-sm font-semibold text-white">
                  3 BHK
                </div>
              </div>
              <p className="mt-2 text-sm text-slate-600">Premium city living with smart amenities and a guided AI experience.</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}