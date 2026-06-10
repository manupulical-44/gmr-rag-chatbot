/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#2563EB',
        secondary: '#0F172A',
        accent: '#14B8A6',
        background: '#F8FAFC',
        surface: '#FFFFFF',
        muted: '#64748B'
      },
      boxShadow: {
        soft: '0 20px 60px rgba(15, 23, 42, 0.12)',
        glass: '0 8px 32px rgba(15, 23, 42, 0.08)'
      },
      borderRadius: {
        xl: '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem'
      },
      fontFamily: {
        sans: ['Manrope', 'ui-sans-serif', 'system-ui'],
        display: ['Space Grotesk', 'ui-sans-serif', 'system-ui']
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(20, 184, 166, 0.12))'
      }
    }
  },
  plugins: []
};