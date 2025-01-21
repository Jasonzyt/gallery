// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  srcDir: "src/",
  css: ["~/assets/css/base.css"],
  modules: ["@nuxt/ui", "@nuxt/icon"],
  icon: {
    customCollections: [
      { prefix: "my", dir: "assets/icon/my" },
      {
        prefix: "album-icons",
        dir: "assets/icon/album-icons",
      },
    ],
  },
});
