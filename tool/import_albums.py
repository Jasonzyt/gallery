import os
import json
import csv
import shutil
import traceback
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from typing import Dict, List, Any, Optional

CWD = Path.cwd()
# METADATA_FILE = CWD / "app/utils/meta.json"
IMPORT_DIR = CWD / "public/assets/import-albums"
ALBUMS_DIR = CWD / "public/assets/albums"

CONTENT_DIR = CWD / "content"
CONTENT_META_FILE = CONTENT_DIR / "albums-meta.csv"

ALBUMS_META: List[Dict[str, Any]] = []
ALBUM_PHOTOS: Dict[str, List[Dict[str, Any]]] = {}

SIZES = {
    "sm": {"max_width": 800, "quality": 80},
    "md": {"max_width": 2000, "quality": 80},
    "lg": {"max_width": 4000, "quality": 80},
    "xl": {"max_width": 6000, "quality": 80},
}


def filter_exif(
    exif: Optional[Dict[str, Any]], keep_tags: List[str]
) -> Optional[Dict[str, Any]]:
    """
    过滤EXIF数据，只保留指定的标签

    Args:
        exif: PIL的Image.Exif对象或Python字典
        keep_tags: 要保留的EXIF标签列表

    Returns:
        过滤后的EXIF字典，如果输入为None则返回None
    """
    if exif is None:
        return None

    exif_dict = exif

    # 创建标签ID和名称的映射
    tag_id_to_name = {v: k for k, v in TAGS.items()}
    gps_tag_id_to_name = {v: k for k, v in GPSTAGS.items()}

    # 创建新的EXIF字典，只包含需要保留的标签
    filtered_exif = {}

    # 处理普通EXIF标签
    for tag_id, value in exif_dict.items():
        # 跳过GPS信息块，我们会单独处理
        if tag_id == 34853:  # GPSInfo标签ID
            continue

        tag_name = TAGS.get(tag_id)
        if tag_name in keep_tags:
            filtered_exif[tag_id] = value

    # 处理GPS信息
    if 34853 in exif_dict:  # GPSInfo标签
        gps_info = exif_dict[34853]
        if isinstance(gps_info, dict):
            gps_filtered = {}
            for gps_tag_id, gps_value in gps_info.items():
                gps_tag_name = GPSTAGS.get(gps_tag_id)
                if f"GPS{gps_tag_name}" in keep_tags:
                    gps_filtered[gps_tag_id] = gps_value

            if gps_filtered:
                filtered_exif[34853] = gps_filtered

    return filtered_exif


def filter_exif_by_categories(
    exif: Optional[Dict[str, Any]], categories: Dict[str, List[str]]
) -> Optional[Dict[str, Any]]:
    """
    根据分类标签列表过滤EXIF数据

    Args:
        exif: PIL的Image.Exif对象或Python字典
        categories: 按类别分组的要保留的EXIF标签字典

    Returns:
        过滤后的EXIF字典，如果输入为None则返回None
    """
    # 合并所有类别的标签到一个列表
    all_keep_tags = []
    for category, tags in categories.items():
        all_keep_tags.extend(tags)

    # 使用主过滤函数
    return filter_exif(exif, all_keep_tags)


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


# def load_metadata():
#     if METADATA_FILE.exists():
#         with open(METADATA_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     else:
#         print(
#             f"[METADATA] Metadata file {METADATA_FILE} does not exist. Creating new metadata file."
#         )
#         write_metadata()
#     return METADATA


# def write_metadata():
#     with open(METADATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(METADATA, f, indent=2, ensure_ascii=False)


def load_metadata():
    """
    从 content/albums-meta.csv 和每个相册的 index.csv 加载元数据
    """
    global ALBUMS_META, ALBUM_PHOTOS
    if CONTENT_META_FILE.exists():
        with open(CONTENT_META_FILE, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            ALBUMS_META = [row for row in reader]

    for album_data in ALBUMS_META:
        album_id = album_data["id"]
        photos_meta = []
        photos_meta_file = CONTENT_DIR / album_id / "index.csv"
        if photos_meta_file.exists():
            with open(photos_meta_file, "r", encoding="utf-8", newline="") as pf:
                photo_reader = csv.DictReader(pf, delimiter=";")
                for photo_data in photo_reader:
                    if "extra" in photo_data and photo_data["extra"]:
                        try:
                            photo_data["extra"] = json.loads(photo_data["extra"])
                        except json.JSONDecodeError:
                            photo_data["extra"] = {}
                    else:
                        photo_data["extra"] = {}
                    photos_meta.append(photo_data)
        ALBUM_PHOTOS[album_id] = photos_meta


def write_metadata():
    """
    将元数据写回 content/albums-meta.csv 和每个相册的 index.csv
    """
    # 写回相册元数据
    if ALBUMS_META:
        with open(CONTENT_META_FILE, "w", encoding="utf-8", newline="") as f:
            album_headers = ALBUMS_META[0].keys()
            writer = csv.DictWriter(f, fieldnames=album_headers, delimiter=";")
            writer.writeheader()
            writer.writerows(ALBUMS_META)

    # 写回照片元数据
    photo_headers = ["photo", "title", "description", "tags", "extra"]
    for album_id, photos in ALBUM_PHOTOS.items():
        album_dir = CONTENT_DIR / album_id
        album_dir.mkdir(exist_ok=True)
        photos_meta_file = album_dir / "index.csv"
        with open(photos_meta_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=photo_headers, delimiter=";")
            writer.writeheader()
            for photo in photos:
                photo_to_write = photo.copy()
                photo_to_write["extra"] = json.dumps(
                    photo_to_write.get("extra", {}), ensure_ascii=False
                )
                # Ensure all headers are present
                for header in photo_headers:
                    if header not in photo_to_write:
                        photo_to_write[header] = ""
                writer.writerow(photo_to_write)


def create_new_album(name, photos):
    ALBUMS_META.append(
        {
            "id": name,
            "name": name,
            "description": "",
            "cover": "",
            "updated": "",
            "urlFormat": f"/assets/albums/{name}/{{photo}}-{{size}}.jpg",
        }
    )
    ALBUM_PHOTOS[name] = [
        {
            "photo": p,
            "title": "",
            "description": "",
            "tags": "",
            "extra": {},
        }
        for p in photos
    ]


def process_image(img_path, id, album_name):
    img = Image.open(img_path)
    exif = img.info.get("exif")
    if exif is None:
        exif = Image.Exif()
        print("! No exif data found, leaving it as is")
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

    album_exists = next((a for a in ALBUMS_META if a["id"] == album_name), None)
    if album_exists:
        print("[METADATA] Album already exists, appending photos")
        existing_photo_ids = {p["photo"] for p in ALBUM_PHOTOS.get(album_name, [])}
        for p_id in photos:
            if p_id not in existing_photo_ids:
                ALBUM_PHOTOS[album_name].append(
                    {
                        "photo": p_id,
                        "title": "",
                        "description": "",
                        "tags": "",
                        "extra": {},
                    }
                )
    else:
        create_new_album(album_name, photos)
        print(
            f"[METADATA] Created new album {album_name}. Please add a cover photo and description in {CONTENT_META_FILE}"
        )

    write_metadata()
    print(f"Imported {count} photos")


def main():
    count = 0
    check_dirs()
    load_metadata()
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
