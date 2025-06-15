import os
import json
import shutil
import traceback
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from typing import Dict, List, Any, Optional

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

    # 确保我们处理的是字典
    if not isinstance(exif, dict):
        try:
            exif_dict = dict(exif)
        except (TypeError, ValueError):
            return None
    else:
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
