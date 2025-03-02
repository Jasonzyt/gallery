import { defineNuxtModule } from "nuxt/kit";
import child_process from "node:child_process";

export default defineNuxtModule({
  setup(options, nuxt) {
    // const resolve = createResolver(import.meta.url).resolve;
    nuxt.hook("build:before", async () => {
      try {
        child_process.execSync("python tool/import_albums.py");
      } catch (e) {
        console.error(e);
      }
    });
  },
});
