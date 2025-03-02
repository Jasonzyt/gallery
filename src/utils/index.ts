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

export function getAlbumPhotoUrls(album: Album, size: string): string[] {
  return album.photos.map((it) =>
    album.urlFormat.replace("{photo}", it).replace("{size}", size)
  );
}

export function getAllPhotoUrls(size: string): string[] {
  const result: string[] = [];
  meta.albums.forEach((album) =>
    result.push(...getAlbumPhotoUrls(album, size))
  );
  return result;
}
