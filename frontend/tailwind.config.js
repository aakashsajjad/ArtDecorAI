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
        primary: '#5A67D8', /* A deep, calming blue */
        secondary: '#667EEA', /* A slightly lighter, vibrant blue */
        accent: '#D53F8C', /* A rich, inviting pink */
        neutral: '#F7FAFC', /* A very light, almost white gray */
        'base-100': '#FFFFFF', /* Pure white for backgrounds */
        'dark-gray': '#2D3748', /* For text and darker elements */
        'light-gray': '#EDF2F7', /* For borders and subtle backgrounds */
        red: {
          500: '#EF4444',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        serif: ['Merriweather', 'serif'],
      },
      boxShadow: {
        '3xl': '0 35px 60px -15px rgba(0, 0, 0, 0.3)',
      },
    },
  },
  plugins: [],
  // Ensure JIT mode is enabled for faster compilation and to avoid issues with unused styles

  darkMode: 'class',
};