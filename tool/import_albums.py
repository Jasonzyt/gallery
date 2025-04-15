import os
import json
import shutil
import traceback
from pathlib import Path
from PIL import Image

CWD = Path.cwd()
METADATA_FILE = CWD / "src/utils/meta.json"
IMPORT_DIR = CWD / "src/public/assets/import-albums"
ALBUMS_DIR = CWD / "src/public/assets/albums"

METADATA = {"albums": []}

SIZES = {
    "sm": {"max_width": 800, "quality": 80},
    "md": {"max_width": 2000, "quality": 80},
    "lg": {"max_width": 4000, "quality": 80},
    "xl": {"max_width": 6000, "quality": 80},
}

# TODO: filter EXIF


def log_error(msg: str, e: Exception, enable_traceback: bool = True):
    print(f"! {msg}")
    print(f"! Error: {e}")
    if enable_traceback:
        tb = traceback.format_exc().splitlines()
        for line in tb:
            print(f"  {line}")


def check_dirs():
    if not IMPORT_DIR.exists():
        print(f"Directory {IMPORT_DIR} does not exist. Do you want to create it?")
        input("Press Enter to continue...")
        IMPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_metadata():
    if METADATA_FILE.exists():
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print(
            f"[METADATA] Metadata file {METADATA_FILE} does not exist. Creating new metadata file."
        )
        write_metadata()
    return METADATA


def write_metadata():
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(METADATA, f, indent=2, ensure_ascii=False)


def create_new_album(name, photos):
    METADATA["albums"].append(
        {
            "id": name,
            "name": name,
            "desc": "",
            "cover": None,
            "urlFormat": f"/assets/albums/{name}/{{photo}}-{{size}}.jpg",
            "photos": photos,
        }
    )


def process_image(img_path, id, album_name):
    img = Image.open(img_path)
    exif = img.info.get("exif")
    for size, config in SIZES.items():
        max_width, quality = config["max_width"], config["quality"]
        filename = ALBUMS_DIR / album_name / f"{id}-{size}.jpg"
        if filename.exists():
            print(f"- Overwriting {filename} as it already exists")
            filename.unlink()
        img_resized = img.copy()
        img_resized.thumbnail((max_width, max_width))
        img_resized.save(
            filename, format="JPEG", quality=quality, exif=exif, optimize=True
        )

    # Square crop
    filename = ALBUMS_DIR / album_name / f"{id}-sq.jpg"
    if filename.exists():
        print(f"- Overwriting {filename} as it already exists")
        filename.unlink()
    img_square = img.copy()
    w, h = img_square.size
    if w > h:
        img_square = img.crop(((w - h) / 2, 0, (w + h) / 2, h)).resize((640, 640))
    else:
        img_square = img.crop((0, (h - w) / 2, w, (h + w) / 2)).resize((640, 640))
    img_square.save(filename, format="JPEG", quality=80, exif=exif, optimize=True)
    img.close()
    print(f"- {img_path.name} processed")


def import_album(dir_path):
    print(f"Importing photos from {dir_path}")
    count = 0
    photos = []
    album_name = Path(dir_path).name
    album_path = ALBUMS_DIR / album_name
    album_path.mkdir(parents=True, exist_ok=True)

    if ALBUMS_DIR.exists():
        ALBUMS_DIR.mkdir(parents=True, exist_ok=True)

    for img_file in Path(dir_path).iterdir():
        if img_file.is_file():
            try:
                id = img_file.stem
                process_image(img_file, id, album_name)
                photos.append(id)
                count += 1
                img_file.unlink()  # Remove original file after processing
            except Exception as e:
                log_error("Error when processing image", e)

    album_exists = next((a for a in METADATA["albums"] if a["id"] == album_name), None)
    if album_exists:
        print("[METADATA] Album already exists, appending photos")
        album_exists["photos"].extend(
            p for p in photos if p not in album_exists["photos"]
        )
    else:
        create_new_album(album_name, photos)
        print(
            f"[METADATA] Created new album {album_name}. Please add a cover photo and description in meta.json"
        )

    write_metadata()
    print(f"Imported {count} photos")


def main():
    global METADATA
    count = 0
    check_dirs()
    METADATA = load_metadata()
    with os.scandir(IMPORT_DIR) as entries:
        for entry in entries:
            if entry.is_dir():
                album_path = IMPORT_DIR / entry.name
                import_album(album_path)
                if not any(album_path.iterdir()):
                    print(f"Album directory {album_path} is empty, deleting it.")
                    shutil.rmtree(album_path)
                write_metadata()
                count += 1
        print(f"Imported {count} albums")


if __name__ == "__main__":
    main()
