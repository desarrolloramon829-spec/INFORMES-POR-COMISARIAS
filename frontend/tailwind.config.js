/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'policia-rojo': '#8B0000',
        'policia-rojo-claro': '#B22222',
        'policia-azul': '#1a237e',
        'policia-azul-claro': '#283593',
        'policia-dorado': '#DAA520',
        'policia-gris': '#F5F5F5',
      },
    },
  },
  plugins: [],
};
