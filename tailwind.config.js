/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        'winx': ['Winx Script', 'cursive'],
      },
      gridTemplateColumns: {
        'auto-1fr': 'auto 1fr',
      },
      colors: {
        'wpink': {
          500: '#d42e5d',
          100: 'ff7aac'
        },
        'wblue': {
          500: '#6cb6fd',
          100: '#affeff'
        },

      }
    },
  },
  plugins: [],
}

