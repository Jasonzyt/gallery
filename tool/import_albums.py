import os
import json
import shutil
from pathlib import Path
from PIL import Image

CWD = Path.cwd()
METADATA_FILE = CWD / "src/utils/meta.json"
IMPORT_DIR = CWD / "src/public/assets/import-albums"
ALBUMS_DIR = CWD / "src/public/assets/albums"

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    METADATA = json.load(f)

SIZES = {
    "sm": {"max_width": 800, "quality": 80},
    "md": {"max_width": 2000, "quality": 80},
    "lg": {"max_width": 4000, "quality": 80},
    "xl": {"max_width": 6000, "quality": 80},
}


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
            "urlFormat": f"/assets/albums/{name}/{{photo}}-{{size}}.webp",
            "photos": photos,
        }
    )


def process_image(img_path, id, album_name):
    img = Image.open(img_path)
    for size, config in SIZES.items():
        max_width, quality = config["max_width"], config["quality"]
        filename = ALBUMS_DIR / album_name / f"{id}-{size}.webp"
        if filename.exists():
            print(f"Overwriting {filename} as it already exists")
            filename.unlink()
        img_resized = img.copy()
        img_resized.thumbnail((max_width, max_width))
        img_resized.save(filename, format="WEBP", quality=quality)

    # Square crop
    filename = ALBUMS_DIR / album_name / f"{id}-sq.webp"
    if filename.exists():
        print(f"Overwriting {filename} as it already exists")
        filename.unlink()
    img_square = img.copy()
    img_square = img_square.crop((0, 0, 400, 400))  # Simple center crop
    img_square.save(filename, format="WEBP", quality=80)
    img.close()


def import_album(dir_path):
    print(f"Importing photos from {dir_path}")
    count = 0
    photos = []
    album_name = Path(dir_path).name
    album_path = ALBUMS_DIR / album_name
    album_path.mkdir(parents=True, exist_ok=True)

    for img_file in Path(dir_path).iterdir():
        if img_file.is_file():
            try:
                id = img_file.stem
                process_image(img_file, id, album_name)
                photos.append(id)
                count += 1
                img_file.unlink()  # Remove original file after processing
            except Exception as e:
                print(f"Error when processing image {img_file.name}: {e}")

    album_exists = next((a for a in METADATA["albums"] if a["id"] == album_name), None)
    if album_exists:
        print("Album already exists, appending photos")
        album_exists["photos"].extend(
            p for p in photos if p not in album_exists["photos"]
        )
    else:
        create_new_album(album_name, photos)
        print(
            f"Created new album {album_name}. Please add a cover photo and description in meta.json"
        )

    write_metadata()
    print(f"Imported {count} photos")


count = 0
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
