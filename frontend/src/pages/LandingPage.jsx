import { motion } from 'framer-motion';
import { BrainCircuit, ShieldCheck, Sparkles, TrendingUp } from 'lucide-react';
import HeroSection from '../components/HeroSection';
import PropertyGrid from '../components/PropertyGrid';
import SectionHeading from '../components/SectionHeading';
import FeatureCard from '../components/FeatureCard';
import TestimonialSection from '../components/TestimonialSection';
import { mockProperties } from '../data/mockProperties';
import { mockTestimonials } from '../data/mockTestimonials';

const features = [
  {
    icon: ShieldCheck,
    title: 'Verified Listings',
    description: 'Curated property cards with key details, transparent pricing, and clean visual hierarchy.'
  },
  {
    icon: BrainCircuit,
    title: 'AI Property Assistant',
    description: 'Chat with an AI assistant to narrow down budgets, city preferences, and property types.'
  },
  {
    icon: TrendingUp,
    title: 'Premium Discovery',
    description: 'A polished home-search experience inspired by top real-estate marketplaces.'
  }
];

export default function LandingPage() {
  const featured = mockProperties.slice(0, 6);

  return (
    <div>
      <HeroSection />

      <section className="section-padding py-16">
        <div className="container-width space-y-10">
          <SectionHeading
            eyebrow="Featured Properties"
            title="Hand-picked homes for modern buyers"
            description="A curated set of premium homes designed to highlight the visual style, search structure, and interaction flow of the future product."
          />
          <PropertyGrid properties={featured} />
        </div>
      </section>

      <section className="section-padding bg-white py-16">
        <div className="container-width">
          <SectionHeading
            eyebrow="Why Choose Us"
            title="A polished search experience built for trust"
            description="The interface combines modern visuals, responsive layouts, and AI-assisted property discovery to feel production-ready from day one."
          />
          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {features.map((feature) => (
              <FeatureCard key={feature.title} {...feature} />
            ))}
          </div>
        </div>
      </section>

      <section className="section-padding py-16">
        <div className="container-width grid gap-8 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
          <motion.div
            initial={{ opacity: 0, x: -24 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="glass-panel rounded-[2rem] p-8 shadow-soft"
          >
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-accent">AI Property Assistant</p>
            <h3 className="mt-3 font-display text-3xl font-bold text-secondary">Ask natural language questions and find homes faster.</h3>
            <p className="mt-4 text-slate-600">
              The frontend is structured so a Python API can be connected later without changing the page architecture.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 24 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="grid gap-4 sm:grid-cols-2"
          >
            <div className="rounded-3xl bg-primary p-6 text-white shadow-soft">
              <Sparkles size={26} />
              <p className="mt-5 text-xl font-semibold">Natural language search</p>
              <p className="mt-2 text-sm text-blue-100">Search by budget, city, BHK, or property type.</p>
            </div>
            <div className="rounded-3xl bg-secondary p-6 text-white shadow-soft sm:mt-10">
              <Sparkles size={26} />
              <p className="mt-5 text-xl font-semibold">API-ready design</p>
              <p className="mt-2 text-sm text-slate-300">All data access lives in services for easy backend integration.</p>
            </div>
          </motion.div>
        </div>
      </section>

      <TestimonialSection testimonials={mockTestimonials} />
    </div>
  );
}