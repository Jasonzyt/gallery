<template>
  <div class="rounded-md bg-accented p-3 font-mono text-left">
    <p>
      <Icon
        name="ic:round-photo-camera"
        size="20px"
        class="align-middle"
      /><span class="ml-2 text-sm">{{ stringifyCameraInfo(data) }}</span>
    </p>
    <p>
      <Icon name="ri:camera-lens-fill" size="20px" class="align-middle" /><span
        class="ml-2 text-sm"
        >{{ data.FocalLengthIn35mmFormat }}mm &nbsp;{{
          stringifyShutterSpeed(data)
        }}
        &nbsp;f/{{ data.FNumber }} &nbsp;ISO {{ data.ISO }}</span
      >
    </p>
    <p v-if="hasGPS">
      <Icon
        name="ic:baseline-location-on"
        size="20px"
        class="align-middle"
      /><span class="ml-2 text-sm" v-html="stringifyGpsInfo(data)"></span>
    </p>
    <p>
      <Icon
        name="ic:baseline-calendar-month"
        size="20px"
        class="align-middle"
      /><span class="ml-2 text-sm">{{
        (data.CreateDate as Date).toLocaleDateString() +
        " " +
        (data.CreateDate as Date).toLocaleTimeString() +
        " UTC" +
        ((data.CreateDate as Date).getTimezoneOffset() < 0 ? "+" : "-") +
        (data.CreateDate as Date).getTimezoneOffset() / -60
      }}</span>
    </p>
  </div>
</template>

<script lang="ts" setup>
const props = defineProps({
  img: {
    type: String,
    required: true,
  },
});

const data = await parseExif(props.img);
const hasGPS = data.GPSLatitude && data.GPSLongitude;
const stringifyGpsInfo = (data: Record<string, any>) => {
  if (!data.GPSLatitude || !data.GPSLongitude) return "";
  return `${data.GPSLatitude[0]}°${data.GPSLatitude[1]}' ${data.GPSLatitudeRef} &nbsp; ${data.GPSLongitude[0]}°${data.GPSLongitude[1]}' ${data.GPSLongitudeRef}`;
};
</script>

<style></style>
