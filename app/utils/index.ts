import type { Collections } from "@nuxt/content";
import { findAlbums } from "./fs";

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

export function getAlbumIds() {
  return findAlbums();
}

export async function getAlbums() {
  const { data } = await useAsyncData("albumsMeta", () => {
    return queryCollection("albumsMeta").order("updated", "DESC").all();
  });
  console.log("getAlbums", data.value);
  return data.value as Album[];
}

export async function getAlbum(id: string) {
  const { data } = await useAsyncData(() => {
    return queryCollection("albumsMeta").where("id", "=", id).first();
  });
  console.log("getAlbum", data.value);
  return data.value as Album | undefined;
}

export async function getAlbumPhotos(albumid: string) {
  const { data } = await useAsyncData(() => {
    return queryCollection(albumid as keyof Collections).all();
  });
  console.log("getAlbumPhotos", data.value);
  return data.value as Photo[];
}

export async function getAlbumPhotosWithUrls(
  albumid: string,
  size: string = "{size}"
) {
  const { data } = await useAsyncData(() => {
    const album = queryCollection("albumsMeta").where("id", "=", albumid).first()
    const photos = queryCollection(albumid as keyof Collections).all()
    return Promise.all([album, photos]);
  });
  const photos = data.value?.[1] as Photo[];
  const album = data.value?.[0] as Album | undefined;
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

export async function getAllPhotosWithUrls(limit: number = 100, size: string = "{size}") {
  const allPhotos: Photo[] = [];
  const albums = await getAlbums();
  albums.forEach(async (album) => {
    const albumPhotos = await queryCollection(album.id as keyof Collections).all() as Photo[];
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
  });
  console.log("getAllPhotosWithUrls", allPhotos);
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
