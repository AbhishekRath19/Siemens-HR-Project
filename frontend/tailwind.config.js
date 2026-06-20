/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#050816",
        surface: "#0F172A",
        card: "#111827",
        primary: "#4F8CFF",
        accent: "#60A5FA",
        success: "#22C55E",
        warning: "#F59E0B",
        danger: "#EF4444",
        muted: "#94A3B8",
      },
      fontFamily: {
        inter: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
}