/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'nepal-blue': '#1e3a8a',
        'nepal-red': '#dc2626',
        'nepal-green': '#16a34a',
      }
    },
  },
  plugins: [],
  darkMode: 'class'
}
