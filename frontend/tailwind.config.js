module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      height: {
        main: "calc(100% - 4rem)",
      },
      maxHeight: {
        "screen-2/3": "66vh",
      },
    },
  },
  plugins: [],
};
