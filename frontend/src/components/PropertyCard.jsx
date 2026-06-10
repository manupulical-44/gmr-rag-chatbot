import { BedDouble, Bath, Maximize, MapPin } from 'lucide-react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { formatArea, formatCurrency } from '../utils/formatters';

export default function PropertyCard({ property }) {
  return (
    <motion.article
      whileHover={{ y: -6 }}
      transition={{ duration: 0.2 }}
      className="group overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft"
    >
      <div className="relative h-56 overflow-hidden">
        <img
          src={property.image}
          alt={property.title}
          className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
        />
        <div className="absolute left-4 top-4 rounded-full bg-white/90 px-3 py-1 text-xs font-semibold text-secondary shadow-glass backdrop-blur-xl">
          {property.status}
        </div>
      </div>

      <div className="space-y-4 p-5">
        <div>
          <div className="flex items-start justify-between gap-4">
            <div>
              <h3 className="font-display text-xl font-bold text-secondary">{property.title}</h3>
              <div className="mt-2 flex items-center gap-2 text-sm text-muted">
                <MapPin size={14} />
                {property.address}
              </div>
            </div>
            <p className="text-right text-lg font-bold text-primary">{formatCurrency(property.price)}</p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3 text-sm text-muted">
          <div className="rounded-2xl bg-slate-50 px-3 py-3 text-center">
            <BedDouble size={16} className="mx-auto mb-1 text-secondary" />
            {property.bedrooms} Beds
          </div>
          <div className="rounded-2xl bg-slate-50 px-3 py-3 text-center">
            <Bath size={16} className="mx-auto mb-1 text-secondary" />
            {property.bathrooms} Baths
          </div>
          <div className="rounded-2xl bg-slate-50 px-3 py-3 text-center">
            <Maximize size={16} className="mx-auto mb-1 text-secondary" />
            {formatArea(property.area)}
          </div>
        </div>

        <div className="flex items-center justify-between gap-3">
          <p className="text-sm text-muted">{property.propertyType}</p>
          <Link
            to={`/properties/${property.id}`}
            className="rounded-2xl bg-secondary px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            View Details
          </Link>
        </div>
      </div>
    </motion.article>
  );
}