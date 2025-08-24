import "exifr";
import exifr from "exifr";

const EXIF_CATEGORIES: Record<string, string[]> = {
  camera: ["Make", "Model", "LensInfo", "LensModel"],
  shooting: [
    "FocalLength",
    "FocalLengthIn35mmFormat",
    "ExposureMode",
    "ExposureProgram",
    "ExposureTime",
    "ExposureCompensation",
    "FNumber",
    "ISO",
    "MeteringMode",
    "ApertureValue",
    "ShutterSpeedValue",
    "DigitalZoomRatio",
    "WhiteBalance",
  ],
  customized: ["Artist", "Copyright", "ImageDescription"],
  flash: ["Flash", "LightSource"],
  image: [
    "Orientation",
    "XResolution",
    "YResolution",
    "ResolutionUnit",
    "ColorSpace",
  ],
  time: [
    "DateTimeOriginal",
    "CreateDate",
    "ModifyDate",
    "OffsetTime",
    "OffsetTimeOriginal",
    "OffsetTimeDigitized",
  ],
  gps: [
    "GPSDateStamp",
    "GPSDifferential",
    "GPSLatitude",
    "GPSLatitudeRef",
    "GPSLongitude",
    "GPSLongitudeRef",
    "GPSAltitude",
    "GPSAltitudeRef",
    "GPSMapDatum",
    "GPSMeasureMode",
    "GPSStatus",
    "GPSTimeStamp",
    "GPSVersionID",
  ],
};

export async function parseExif(url: string) {
  return exifr.parse(url);
}

export async function parseExifCategories(
  url: string,
  categories: string[] = Object.keys(EXIF_CATEGORIES)
) {
  const exif = await parseExif(url);
  const result: Record<string, any> = {};

  for (const category of categories) {
    result[category] = {};
    for (const key of EXIF_CATEGORIES[category] || []) {
      if (exif[key]) {
        result[category][key] = exif[key];
      }
    }
    if (Object.keys(result[category]).length === 0) {
      delete result[category];
    }
  }

  return result;
}

export function stringifyCameraInfo(exifData: any) {
  return `${exifData.Make} ${exifData.Model} with ${exifData.LensModel}`;
}

export function stringifyShootingInfo(exifData: any) {
  let shutterSpeed = "";
  if (exifData.ExposureTime > 1) {
    shutterSpeed = `${exifData.ExposureTime}"`;
  } else {
    shutterSpeed = `1/${Math.round(1 / exifData.ExposureTime)}`;
  }
  return `${exifData.FocalLengthIn35mmFormat}mm ${shutterSpeed} f/${exifData.FNumber} ISO${exifData.ISO}`;
}

export function stringifyShutterSpeed(exifData: any) {
  if (exifData.ExposureTime > 1) {
    return `${exifData.ExposureTime}"`;
  } else {
    return `1/${Math.round(1 / exifData.ExposureTime)}`;
  }
}