/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',

  safelist: [
        {
            pattern: /text-(red|green|blue)-(100|400)/,
            variants: ['group-hover']
        },
        {
            pattern: /bg-(red|green|blue)-(100|400)/,
            variants: ['group-hover']
        }
    ],

  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    screens: {
      xs: "614px",
      sm: "1002px",
      md: "1022px",
      lg: "1092px",
      xl: "1280px",
    },

    extend: {
      colors: {
         // Yeni mor paletimiz
        purple: {
          100: '#ede9fe',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
        },
        dim: {
          50: '#5F99F7', // Bu mavi kalabilir veya morun bir tonu yapılabilir
          100: '#5F99F7',
          200: '#38444d',
          300: '#202e3a',
          400: '#253341',
          500: '#5F99F7',
          600: '#5F99F7',
          700: '#192734',
          800: '#162d40',
          900: '#15202b',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

