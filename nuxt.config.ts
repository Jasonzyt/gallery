import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  css: ["~/assets/css/main.css"],
  modules: ["@nuxt/ui", "@nuxt/icon", "@nuxt/image", "@nuxt/content"],
  ui: {
    theme: {
      colors: ["primary", "neutral"],
    },
  },
  icon: {
    customCollections: [
      {
        prefix: "my",
        dir: "./app/assets/icon/my",
      },
    ],
  },
  vite: {
    plugins: [tailwindcss()],
  },
  content: {
    build: {
      csv: {
        delimiter: ";", // Use semicolon as delimiter
        json: true,
      },
    },
  },
  // nitro: {
  //   routeRules: {
  //     "/oss/**": { proxy: "https://gallery-oss.jasonz.yt/**", cors: true },
  //   },
  // },
});
