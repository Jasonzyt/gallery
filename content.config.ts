import {
  DefinedCollection,
  defineCollection,
  defineContentConfig,
  z,
} from "@nuxt/content";
import fs from "node:fs";
import path from "node:path";

function isDirectory(filePath: string): boolean {
  if (!fs.existsSync(filePath)) {
    return false;
  }
  return fs.statSync(filePath).isDirectory();
}

function findAlbums(): string[] {
  const albumsDir = path.resolve("content");
  return fs
    .readdirSync(albumsDir)
    .filter((file) => isDirectory(path.join(albumsDir, file)));
}

function defineAlbumCollections(): Record<string, DefinedCollection> {
  const albums = findAlbums();
  const result: Record<string, DefinedCollection> = {};
  console.log("Found albums:", albums);
  albums.forEach((album) => {
    result[album] = defineCollection({
      type: "data",
      source: `${album}/**.csv`,
      schema: z.object({
        photo: z.string(),
        title: z.string().optional(),
        description: z.string().optional(),
        tags: z.string().optional(),
        extra: z.string().optional(),
      }),
    });
  });
  return result;
}

export default defineContentConfig({
  collections: {
    albumsMeta: defineCollection({
      type: "data",
      source: "albums-meta.csv",
      schema: z.object({
        id: z.string(),
        name: z.string(),
        description: z.string(),
        cover: z.string(),
        updated: z.string(),
        urlFormat: z.string(),
      }),
    }),
    ...defineAlbumCollections(),
  },
});
