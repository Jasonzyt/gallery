import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  ssr: false,
  css: ["~/assets/css/main.css"],
  modules: ["@nuxt/ui", "@nuxt/icon", "@nuxt/image"],
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
  // nitro: {
  //   routeRules: {
  //     "/oss/**": { proxy: "https://gallery-oss.jasonz.yt/**", cors: true },
  //   },
  // },
});
