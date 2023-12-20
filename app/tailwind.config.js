/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./node_modules/flowbite/**/*.js",
    "./config/**/*.py",
    "./connection/**/*.py",
    "./club/templates/**/*.html",
    "./connection/templates/**/*.html",
    "./event/templates/**/*.html",
    "./shop/templates/**/*.html",
    "./public/templates/**/*.html",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      backgroundImage:{
        'wall': "url('img/bg.png')"
      },
      // les couleurs personnaliser 
      colors:{
        redPrime : '#fe6973',
        redDark : '#E2505D',
        yallowPrime: '#fbeb95',
        yallowLight: '#fbf1ca',
        purpelPrime: '#612858',
        purpleLight: '#c5b3c2',
      }
    },
  },
  plugins: [require('flowbite/plugin')],
}
