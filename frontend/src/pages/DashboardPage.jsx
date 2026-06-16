import { useEffect, useState } from 'react';
import { Building2, MessageCircle, Sparkles, TrendingUp } from 'lucide-react';
import StatCard from '../components/StatCard';
import PropertyGrid from '../components/PropertyGrid';
import { propertyService } from '../services/propertyService';

const stats = [
  { label: 'Active Listings',  value: '1.3M+', description: 'Properties across the US.' },
  { label: 'AI Queries',       value: '1.2k',  description: 'Natural language searches handled this month.' },
  { label: 'Lead Quality',     value: '94%',   description: 'Intent-qualified users ready for discovery.' },
  { label: 'Growth',           value: '+27%',  description: 'Month-over-month increase in high-intent visits.' },
];

const actions = [
  { icon: Building2,     label: 'Review Listings' },
  { icon: MessageCircle, label: 'Open AI Chat' },
  { icon: Sparkles,      label: 'Generate Insights' },
  { icon: TrendingUp,    label: 'Track Performance' },
];

export default function DashboardPage() {
  const [featured, setFeatured] = useState([]);

  useEffect(() => {
    propertyService.getFeaturedProperties(3)
      .then((res) => setFeatured(res.data || []))
      .catch(() => setFeatured([]));
  }, []);

  return (
    <div className="space-y-8">
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <StatCard key={stat.label} {...stat} />
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-[0.75fr_1.25fr]">
        <div className="glass-panel rounded-3xl p-6 shadow-soft">
          <h2 className="font-display text-2xl font-bold">Quick Actions</h2>
          <div className="mt-5 space-y-3">
            {actions.map((action) => (
              <button
                key={action.label}
                className="flex w-full items-center gap-3 rounded-2xl bg-slate-50 px-4 py-3 text-left font-medium text-secondary transition hover:bg-slate-100"
              >
                <action.icon size={18} className="text-primary" />
                {action.label}
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-5">
          <h2 className="font-display text-2xl font-bold">Recommended Homes</h2>
          <PropertyGrid properties={featured} />
        </div>
      </div>
    </div>
  );
}
