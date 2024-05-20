/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        'winx': ['Winx Script', 'cursive'],
      },
      gridTemplateColumns: {
        'middle-3': '2fr 3fr 2fr',
        'middle-2/5': '2fr 5fr 2fr',
        'middle-1/5': '1fr 5fr 1fr'
      },
      gridTemplateRows: {
        '1fr-auto': '1fr auto'
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

      },
      backgroundImage: {
        'gradient-winx1': 'linear-gradient(135deg, rgba(78,86,170,1) 0%, rgba(197,126,254,1) 16%, rgba(222,128,255,1) 33%, rgba(229,214,254,1) 50%, rgba(207,255,255,1) 66%, rgba(160,205,255,1) 83%, rgba(66,144,200,1) 100%)',
      },
    },
  },
  plugins: [],
}

