import meta from "./meta.json";

export type Album = {
  id: string;
  name: string;
  desc: string;
  cover: string | null;
  urlFormat: string;
  photos: string[];
};

export function getAlbums(): Album[] {
  return meta.albums;
}

export function getAlbum(id: string): Album | undefined {
  return meta.albums.filter((it) => it.id === id).at(0);
}

export function formatUrlsWithSize(urls: string[], size: string): string[] {
  return urls.map((it) => formatUrlWithSize(it, size));
}

export function formatUrlWithSize(url: string, size: string): string {
  return url.replace("{size}", size);
}

export function getAlbumPhotoUrls(
  album: Album,
  size: string = "{size}"
): string[] {
  return album.photos.map((it) =>
    album.urlFormat.replace("{photo}", it).replace("{size}", size)
  );
}

export function getAllPhotoUrls(size: string = "{size}"): string[] {
  const result: string[] = [];
  meta.albums.forEach((album) =>
    result.push(...getAlbumPhotoUrls(album, size))
  );
  return result;
}

// TODO: find a better way to reverse-find the album name
export function findAlbumsByPhotoUrl(url: string): Album[] | undefined {
  const filename = url.replace("\\", "/").split("/").pop()?.split("?")[0];
  if (!filename) return undefined;
  const basename = filename.split(".").slice(0, -1).join(".");
  return meta.albums.filter((album) => {
    return album.photos.some((photo) => {
      return basename.indexOf(photo) !== -1;
    });
  });
}

export function shuffle<T>(array: T[]): T[] {
  const result = array.slice();
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

export async function loadImage(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = (err) => reject(err);
    img.src = url;
  });
}
