import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { BrainCircuit, ShieldCheck, Sparkles, TrendingUp } from 'lucide-react';
import HeroSection from '../components/HeroSection';
import PropertyGrid from '../components/PropertyGrid';
import SectionHeading from '../components/SectionHeading';
import FeatureCard from '../components/FeatureCard';
import TestimonialSection from '../components/TestimonialSection';
import { propertyService } from '../services/propertyService';

const features = [
  {
    icon: ShieldCheck,
    title: 'Real Listings',
    description: 'Over 1.3 million properties sourced from real market data across the United States.',
  },
  {
    icon: BrainCircuit,
    title: 'AI Property Assistant',
    description: 'Chat with an AI assistant to narrow down budgets, city preferences, and property types.',
  },
  {
    icon: TrendingUp,
    title: 'Smart Discovery',
    description: 'Semantic search finds relevant properties even when your query doesn\'t match exact keywords.',
  },
];

const testimonials = [
  {
    id: 1,
    name: 'Sarah M.',
    role: 'First-time Buyer',
    quote: 'Found my dream home in under 10 minutes. The AI understood exactly what I was looking for.',
    rating: 5,
  },
  {
    id: 2,
    name: 'James T.',
    role: 'Real Estate Investor',
    quote: 'The natural language search saves me hours of filtering. I can just describe what I need.',
    rating: 5,
  },
  {
    id: 3,
    name: 'Priya K.',
    role: 'Property Buyer',
    quote: 'Incredible database. Found options in my budget across three states in one search.',
    rating: 5,
  },
];

export default function LandingPage() {
  const [featured, setFeatured] = useState([]);

  useEffect(() => {
    propertyService.getFeaturedProperties(6)
      .then((res) => setFeatured(res.data || []))
      .catch(() => setFeatured([]));
  }, []);

  return (
    <div>
      <HeroSection />

      <section className="section-padding py-16">
        <div className="container-width space-y-10">
          <SectionHeading
            eyebrow="Featured Properties"
            title="Premium homes across the United States"
            description="Sourced from real market data. Search by city, state, bedrooms, price, or just describe what you want."
          />
          <PropertyGrid properties={featured} />
        </div>
      </section>

      <section className="section-padding bg-white py-16">
        <div className="container-width">
          <SectionHeading
            eyebrow="Why Choose Us"
            title="Real data. Real AI. Real results."
            description="Semantic search powered by FAISS and Groq finds the right properties even from vague descriptions."
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
            <h3 className="mt-3 font-display text-3xl font-bold text-secondary">
              Ask natural language questions and find homes faster.
            </h3>
            <p className="mt-4 text-slate-600">
              Powered by FAISS semantic search and Groq LLM. Just describe what you need — the AI handles the rest.
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
              <p className="mt-2 text-sm text-blue-100">Search by budget, city, bedrooms, or describe your ideal home.</p>
            </div>
            <div className="rounded-3xl bg-secondary p-6 text-white shadow-soft sm:mt-10">
              <Sparkles size={26} />
              <p className="mt-5 text-xl font-semibold">1.3M+ real properties</p>
              <p className="mt-2 text-sm text-slate-300">Full US market data indexed and searchable in real time.</p>
            </div>
          </motion.div>
        </div>
      </section>

      <TestimonialSection testimonials={testimonials} />
    </div>
  );
}
