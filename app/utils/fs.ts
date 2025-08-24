import fs from "node:fs";
import path from "node:path";

const ALBUMS_CACHE: string[] = [];

function isDirectory(filePath: string): boolean {
  if (!fs.existsSync(filePath)) {
    return false;
  }
  return fs.statSync(filePath).isDirectory();
}

export function findAlbums(): string[] {
  if (ALBUMS_CACHE.length > 0) {
    return ALBUMS_CACHE;
  }
  const albumsDir = path.resolve("content");
  const albums = fs
    .readdirSync(albumsDir)
    .filter((file) => isDirectory(path.join(albumsDir, file)));
  ALBUMS_CACHE.push(...albums);
  return ALBUMS_CACHE;
}