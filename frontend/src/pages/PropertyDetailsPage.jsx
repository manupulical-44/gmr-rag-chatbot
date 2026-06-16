import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { MapPin, BedDouble, Bath, Maximize, CalendarDays } from 'lucide-react';
import { propertyService } from '../services/propertyService';
import LoadingSkeleton from '../components/LoadingSkeleton';
import PropertyGrid from '../components/PropertyGrid';
import { formatArea, formatCurrency, formatRelativeDate } from '../utils/formatters';

const PLACEHOLDER_IMAGE =
  'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80';

export default function PropertyDetailsPage() {
  const { propertyId } = useParams();
  const [property, setProperty]   = useState(null);
  const [similar, setSimilar]     = useState([]);
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const prop    = await propertyService.getPropertyById(propertyId);
        setProperty(prop);
        const related = await propertyService.getSimilarProperties(propertyId);
        setSimilar(related.data || []);
      } catch {
        setProperty(null);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [propertyId]);

  if (loading) return <LoadingSkeleton count={3} />;

  if (!property) {
    return (
      <div className="glass-panel rounded-3xl p-10 text-center shadow-soft">
        <h2 className="font-display text-2xl font-bold">Property not found</h2>
        <p className="mt-2 text-muted">This listing may no longer be available.</p>
        <Link to="/properties" className="mt-6 inline-flex rounded-2xl bg-primary px-5 py-3 text-white">
          Back to search
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <section className="grid gap-8 xl:grid-cols-[1.5fr_0.7fr]">
        {/* Main image */}
        <div className="space-y-6">
          <div className="overflow-hidden rounded-[2rem] bg-white shadow-soft">
            <img
              src={property.image || PLACEHOLDER_IMAGE}
              alt={property.title}
              className="h-[420px] w-full object-cover"
            />
          </div>

          {/* Details card */}
          <div className="glass-panel rounded-3xl p-6 shadow-soft">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.24em] text-accent">
                  {property.status?.replace('_', ' ')}
                </p>
                <h1 className="mt-2 font-display text-4xl font-bold text-secondary">
                  {property.title}
                </h1>
                <div className="mt-3 flex items-center gap-2 text-sm text-muted">
                  <MapPin size={16} />
                  {property.city}, {property.state} {property.zip_code}
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm text-muted">Listed at</p>
                <p className="font-display text-3xl font-bold text-primary">
                  {formatCurrency(property.price)}
                </p>
              </div>
            </div>

            {/* Stats row */}
            <div className="mt-6 grid gap-4 sm:grid-cols-3">
              <div className="rounded-2xl bg-slate-50 p-4">
                <BedDouble className="text-primary" />
                <p className="mt-2 text-sm text-muted">Bedrooms</p>
                <p className="text-lg font-bold">{property.bedrooms}</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-4">
                <Bath className="text-primary" />
                <p className="mt-2 text-sm text-muted">Bathrooms</p>
                <p className="text-lg font-bold">{property.bathrooms}</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-4">
                <Maximize className="text-primary" />
                <p className="mt-2 text-sm text-muted">House Size</p>
                <p className="text-lg font-bold">{formatArea(property.area)}</p>
              </div>
            </div>

            {/* Description */}
            <div className="mt-8 space-y-4">
              <div>
                <h2 className="font-display text-2xl font-bold">Description</h2>
                <p className="mt-3 leading-7 text-slate-600">{property.description}</p>
              </div>

              {/* Extra details */}
              <div className="rounded-2xl bg-slate-50 p-4 text-sm text-slate-600 space-y-1">
                <p><span className="font-semibold">Lot Size:</span> {property.acre_lot} acres</p>
                {property.prev_sold_date && (
                  <p>
                    <span className="font-semibold">Previously Sold:</span>{' '}
                    {formatRelativeDate(property.prev_sold_date)}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <aside className="space-y-6 xl:sticky xl:top-28 xl:self-start">
          <div className="glass-panel rounded-3xl p-6 shadow-soft">
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-accent">Location</p>
            <div className="mt-4 rounded-2xl bg-slate-100 p-4 text-sm text-muted flex items-start gap-2">
              <MapPin size={16} className="mt-0.5 shrink-0 text-primary" />
              <span>{property.city}, {property.state} {property.zip_code}</span>
            </div>
          </div>

          <div className="glass-panel rounded-3xl p-6 shadow-soft">
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-accent">Listing Info</p>
            <div className="mt-4 space-y-2 text-sm text-slate-600">
              <p><span className="font-semibold">Status:</span> {property.status?.replace('_', ' ')}</p>
              <p><span className="font-semibold">Price:</span> {formatCurrency(property.price)}</p>
              <p><span className="font-semibold">Lot:</span> {property.acre_lot} acres</p>
              {property.prev_sold_date && (
                <p className="flex items-center gap-1">
                  <CalendarDays size={14} />
                  Last sold: {formatRelativeDate(property.prev_sold_date)}
                </p>
              )}
            </div>
          </div>
        </aside>
      </section>

      {similar.length > 0 && (
        <section className="space-y-5">
          <h2 className="font-display text-3xl font-bold text-secondary">Similar Properties</h2>
          <PropertyGrid properties={similar} />
        </section>
      )}
    </div>
  );
}
