// tailwind.config.js
module.exports = {
  content: [
    './templates/**/*.html', // Include all HTML files in the templates folder
    './apps/**/templates/**/*.html', // Include HTML files in nested app templates
    './apps/**/*.py', // Include Python files (to capture classes in strings)
    './core/**/*.py', // Include core folder Python files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
