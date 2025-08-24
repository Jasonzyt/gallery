import type { Collections } from "@nuxt/content";

export type Album = {
  id: string;
  name: string;
  description: string;
  cover: string | undefined;
  updated: string;
  urlFormat: string;
  // photos: string[];
};

export type Photo = {
  photo: string;
  title?: string;
  description?: string;
  tags?: string;
  extra?: string;

  url?: string; // Optional, can be used to store the formatted URL
};

export async function getAlbums() {
  const { data } = await useAsyncData("albumsMeta", () => {
    return queryCollection("albumsMeta").order("updated", "DESC").all();
  });
  console.log("getAlbums", data.value);
  return data.value as Album[];
}

export async function getAlbum(id: string) {
  const { data } = await useAsyncData(id, () => {
    return queryCollection("albumsMeta").where("id", "=", id).first();
  });
  console.log("getAlbum", data.value);
  return data.value as Album | undefined;
}

export async function getAlbumPhotos(albumid: string) {
  const { data } = await useAsyncData(albumid, () => {
    return queryCollection(albumid as keyof Collections).all() as Promise<Photo[]>;
  });
  return data.value as Photo[];
}

export async function getAlbumPhotosWithUrls(
  album: Album,
  size: string = "{size}"
) {
  const photos = await getAlbumPhotos(album.id);
  return photos.map((photo) => {
    return {
      ...photo,
      url: formatUrlWithSize(
        album?.urlFormat.replace("{photo}", photo.photo),
        size
      ),
    };
  });
}

export function formatUrlsWithSizeSafe(urls: string[], size: string): string[] {
  return urls.map((it) => formatUrlWithSizeSafe(it, size));
}

export function formatUrlWithSizeSafe(url: string, size: string): string {
  return url.replace("{size}", size);
}

export function formatUrlWithSize(
  url: string | undefined,
  size: string
): string | undefined {
  return url?.replace("{size}", size);
}

export async function getAllPhotosWithUrls(albums: Album[], limit: number = 100, size: string = "{size}") {
  const allPhotos: Photo[] = [];
  const { data } = await useAsyncData(async () => {
    const queries: Promise<Photo[]>[] = [];
    for (const album of albums) {
      queries.push(queryCollection(album.id as keyof Collections).all() as Promise<Photo[]>);
    }
    return Promise.all(queries);
  });
  const photos = data.value as Photo[][];
  for (let i = 0; i < photos.length && allPhotos.length < limit; i++) {
    const albumPhotos = photos[i] || [];
    const album = albums[i];
    if (!album) { continue; }
    albumPhotos.forEach((photo) => {
      photo.url = formatUrlWithSize(album.urlFormat.replace("{photo}", photo.photo), size);
    });
    if (limit - allPhotos.length < 0) {
      allPhotos.push(...albumPhotos.slice(0, limit - allPhotos.length));
    }
    else {
      allPhotos.push(...albumPhotos);
      limit -= albumPhotos.length;
    }
  }
  return allPhotos;
}

export async function loadImage(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = (err) => reject(err);
    img.src = url;
  });
}
