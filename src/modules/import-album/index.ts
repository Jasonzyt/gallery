import { defineNuxtModule } from "nuxt/kit";
import { getAlbum } from "~/utils";
import process from "node:process";
import path from "node:path";
import fs from "node:fs";
import sharp from "sharp";

const CWD = process.cwd();
const METADATA_FILE = path.join(CWD, "src/utils/meta.json");
const IMPORT_DIR = path.join(CWD, "import-albums");
const ALBUMS_DIR = path.join(CWD, "src/public/assets/albums");
const METADATA = JSON.parse(fs.readFileSync(METADATA_FILE, "utf-8"));
const SIZES: Record<string, { maxWidth: number; quality: number }> = {
  sm: {
    maxWidth: 800,
    quality: 80,
  },
  md: {
    maxWidth: 2000,
    quality: 80,
  },
  lg: {
    maxWidth: 4000,
    quality: 80,
  },
  xl: {
    maxWidth: 6000,
    quality: 80,
  },
};

function writeMetadata() {
  fs.writeFileSync(METADATA_FILE, JSON.stringify(METADATA, null, 2));
}

function createNewAlbum(name: string, photos: string[]) {
  METADATA.albums.push({
    id: name,
    name: name,
    desc: "",
    cover: null,
    urlFormat: `/assets/albums/${name}/{photo}-{size}.webp`,
    photos: photos,
  });
}

async function processImage(img: sharp.Sharp, id: string, albumName: string) {
  for (const size in SIZES) {
    const { maxWidth, quality } = SIZES[size];
    const filename = path.join(ALBUMS_DIR, albumName, `${id}-${size}.webp`);
    if (fs.existsSync(filename)) {
      console.info("Overwritting", filename, "as it already exists");
      fs.rmSync(filename);
    }
    await img.resize({ width: maxWidth }).webp({ quality }).toFile(filename);
  }
  // square
  const filename = path.join(ALBUMS_DIR, albumName, `${id}-sq.webp`);
  if (fs.existsSync(filename)) {
    console.info("Overwritting", filename, "as it already exists");
    fs.rmSync(filename);
  }
  await img
    .resize({ width: 400, height: 400, fit: "cover", position: "center" })
    .webp({ quality: 80 })
    .toFile(filename);
  img.destroy();
}

async function importAlbum(dirPath: string) {
  console.info("Importing photos from", dirPath);
  let count = 0;
  let photos: string[] = [];
  const albumName = path.basename(dirPath);
  if (!fs.existsSync(path.join(ALBUMS_DIR, albumName))) {
    fs.mkdirSync(path.join(ALBUMS_DIR, albumName), { recursive: true });
  }
  const dir = fs.opendirSync(dirPath);
  for await (const dirent of dir) {
    try {
      if (dirent.isFile()) {
        {
          const img = sharp(path.join(dirPath, dirent.name));
          const id = path.basename(dirent.name, path.extname(dirent.name));
          await processImage(img, id, albumName);
          photos.push(id);
          count++;
        }
        fs.rmSync(path.join(dirPath, dirent.name));
      }
    } catch (e) {
      console.error(`Error when processing image ${dirent.name}:`, e);
    }
  }
  if (getAlbum(albumName)) {
    console.log("Album already exists, appending photos");
    for (const photo of photos) {
      if (METADATA.albums[albumName].photos.includes(photo)) {
        continue;
      }
      METADATA.albums[albumName].photos.push(photo);
    }
  } else {
    createNewAlbum(albumName, photos);
    console.log(
      "Created new album",
      albumName,
      "Please add a cover photo and description in meta.json"
    );
  }
  writeMetadata();
  console.info("Imported", count, "photos");
}

export default defineNuxtModule({
  setup(options, nuxt) {
    // const resolve = createResolver(import.meta.url).resolve;
    nuxt.hook("build:before", async () => {
      try {
        const dir = fs.opendirSync(IMPORT_DIR);
        let count = 0;
        for await (const dirent of dir) {
          if (dirent.isDirectory()) {
            await importAlbum(path.join(IMPORT_DIR, dirent.name));
            fs.rmSync(path.join(IMPORT_DIR, dirent.name), { recursive: true });
            writeMetadata();
            count++;
          }
        }
      } catch (e) {
        console.error(e);
      }
      console.info("Found and imported", METADATA.albums.length, "albums");
    });
  },
});
