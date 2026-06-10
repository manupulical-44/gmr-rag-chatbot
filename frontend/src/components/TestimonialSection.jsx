import { motion } from 'framer-motion';
import { Star } from 'lucide-react';

export default function TestimonialSection({ testimonials }) {
  return (
    <section className="section-padding py-16">
      <div className="container-width">
        <div className="mb-10 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-accent">Testimonials</p>
          <h2 className="mt-3 font-display text-3xl font-bold text-secondary sm:text-4xl">What customers say</h2>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.08 }}
              viewport={{ once: true }}
              className="glass-panel rounded-3xl p-6 shadow-soft"
            >
              <div className="mb-4 flex items-center gap-1 text-amber-500">
                {Array.from({ length: testimonial.rating }).map((_, starIndex) => (
                  <Star key={starIndex} size={16} fill="currentColor" />
                ))}
              </div>
              <p className="text-slate-600">“{testimonial.quote}”</p>
              <div className="mt-5">
                <p className="font-semibold text-secondary">{testimonial.name}</p>
                <p className="text-sm text-muted">{testimonial.role}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}