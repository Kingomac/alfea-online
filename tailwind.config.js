/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html"],
  theme: {
    extend: {
      gridTemplateColumns: {
        'auto-1fr': 'auto 1fr',
      },
    },
  },
  plugins: [],
}

