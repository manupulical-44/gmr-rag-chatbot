import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { CalendarDays, MapPin, PhoneCall, Calculator, BedDouble, Bath, Maximize } from 'lucide-react';
import { propertyService } from '../services/propertyService';
import LoadingSkeleton from '../components/LoadingSkeleton';
import PropertyGrid from '../components/PropertyGrid';
import { formatArea, formatCurrency } from '../utils/formatters';

const galleryFallback = [
  'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80',
  'https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80',
  'https://images.unsplash.com/photo-1560185007-cde436f6a4d0?auto=format&fit=crop&w=1200&q=80',
  'https://images.unsplash.com/photo-1572120360610-d971b9d7767c?auto=format&fit=crop&w=1200&q=80'
];

export default function PropertyDetailsPage() {
  const { propertyId } = useParams();
  const [property, setProperty] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [selectedImage, setSelectedImage] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const currentProperty = await propertyService.getPropertyById(propertyId);
      setProperty(currentProperty);
      setSelectedImage(0);
      const related = await propertyService.getSimilarProperties(propertyId);
      setSimilar(related);
      setLoading(false);
    };

    load();
  }, [propertyId]);

  const gallery = useMemo(() => {
    if (!property) return [];
    const images = property.gallery?.length ? property.gallery : [property.image, ...galleryFallback];
    return [...new Set(images)].slice(0, 4);
  }, [property]);

  if (loading) {
    return <LoadingSkeleton count={3} />;
  }

  if (!property) {
    return (
      <div className="glass-panel rounded-3xl p-10 text-center shadow-soft">
        <h2 className="font-display text-2xl font-bold">Property not found</h2>
        <p className="mt-2 text-muted">The requested listing may no longer be available.</p>
        <Link to="/properties" className="mt-6 inline-flex rounded-2xl bg-primary px-5 py-3 text-white">
          Back to search
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <section className="grid gap-8 xl:grid-cols-[1.5fr_0.7fr]">
        <div className="space-y-6">
          <div className="overflow-hidden rounded-[2rem] bg-white shadow-soft">
            <img src={gallery[selectedImage]} alt={property.title} className="h-[420px] w-full object-cover" />
            <div className="grid grid-cols-4 gap-2 border-t border-slate-200 p-3">
              {gallery.map((image, index) => (
                <button key={image} onClick={() => setSelectedImage(index)} className={`overflow-hidden rounded-2xl ${selectedImage === index ? 'ring-2 ring-primary' : ''}`}>
                  <img src={image} alt={`${property.title} ${index + 1}`} className="h-24 w-full object-cover" />
                </button>
              ))}
            </div>
          </div>

          <div className="glass-panel rounded-3xl p-6 shadow-soft">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.24em] text-accent">Property Details</p>
                <h1 className="mt-2 font-display text-4xl font-bold text-secondary">{property.title}</h1>
                <div className="mt-3 flex items-center gap-2 text-sm text-muted">
                  <MapPin size={16} />
                  {property.address}
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm text-muted">Starting from</p>
                <p className="font-display text-3xl font-bold text-primary">{formatCurrency(property.price)}</p>
              </div>
            </div>

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
                <p className="mt-2 text-sm text-muted">Area</p>
                <p className="text-lg font-bold">{formatArea(property.area)}</p>
              </div>
            </div>

            <div className="mt-8 space-y-4">
              <div>
                <h2 className="font-display text-2xl font-bold">Description</h2>
                <p className="mt-3 leading-7 text-slate-600">{property.description}</p>
              </div>

              <div>
                <h2 className="font-display text-2xl font-bold">Amenities</h2>
                <div className="mt-4 flex flex-wrap gap-3">
                  {property.amenities.map((amenity) => (
                    <span key={amenity} className="rounded-full bg-primary/10 px-4 py-2 text-sm font-medium text-primary">
                      {amenity}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <aside className="space-y-6 xl:sticky xl:top-28 xl:self-start">
          <div className="glass-panel rounded-3xl p-6 shadow-soft">
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-accent">Contact Agent</p>
            <h3 className="mt-2 font-display text-2xl font-bold">Book a guided visit</h3>
            <div className="mt-5 space-y-3 text-sm text-slate-600">
              <button className="flex w-full items-center justify-center gap-2 rounded-2xl bg-primary px-4 py-3 font-semibold text-white transition hover:bg-blue-700">
                <PhoneCall size={16} />
                Contact Agent
              </button>
              <button className="flex w-full items-center justify-center gap-2 rounded-2xl bg-secondary px-4 py-3 font-semibold text-white transition hover:bg-slate-800">
                <CalendarDays size={16} />
                Schedule Visit
              </button>
              <button className="flex w-full items-center justify-center gap-2 rounded-2xl bg-slate-100 px-4 py-3 font-semibold text-secondary transition hover:bg-slate-200">
                <Calculator size={16} />
                EMI Calculator
              </button>
            </div>
          </div>

          <div className="glass-panel rounded-3xl p-6 shadow-soft">
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-accent">Location</p>
            <div className="mt-4 rounded-2xl bg-slate-100 p-4 text-sm text-muted">
              {property.city}, {property.state}
            </div>
          </div>
        </aside>
      </section>

      <section className="space-y-5">
        <h2 className="font-display text-3xl font-bold text-secondary">Similar Properties</h2>
        <PropertyGrid properties={similar} />
      </section>
    </div>
  );
}