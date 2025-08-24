<template>
  <div
    v-if="aspectRatio < 1"
    class="flex flex-row justify-center items-center p-2"
  >
    <img
      :src="photoUrl"
      alt="Photo Detail"
      class="w-fit h-[96.5vh] rounded-lg shadow-lg mb-4"
    />
    <div class="px-6 max-w-[500px]">
      <h2 class="text-2xl font-bold mb-2">{{ photo.title }}</h2>
      <p class="text-toned mb-4" v-html="photo.description"></p>
      <ExifCard :img="photoUrl" />
    </div>
  </div>
  <div
    v-if="aspectRatio >= 1"
    class="m-auto flex flex-col justify-center items-center p-2 max-w-[1000px]"
  >
    <img
      :src="photoUrl"
      alt="Photo Detail"
      class="w-fit rounded-lg shadow-lg mb-4"
    />
    <div class="px-6 max-w-[1000px] text-center">
      <h2 class="text-2xl font-bold mb-2">{{ photo.title }}</h2>
      <p class="text-toned mb-4" v-html="photo.description"></p>
      <ExifCard :img="photoUrl" />
    </div>
  </div>
</template>

<script lang="ts" setup>
const route = useRoute();
const albumid = route.params.album as string;
const photoid = route.params.photo as string;
const album = await getAlbum(albumid);
if (!album) {
  throw createError({
    statusCode: 404,
    statusMessage: "相册不存在",
  });
}
const photo = await getPhoto(album, photoid);
if (!photo) {
  throw createError({
    statusCode: 404,
    statusMessage: "照片不存在",
  });
}
const photoUrl =
  formatUrlWithSize(album.urlFormat.replace("{photo}", photoid), "md") || "";

const aspectRatio = ref(1);

onMounted(async () => {
  const img = await loadImage(photoUrl);
  aspectRatio.value = img ? img.width / img.height : 1;
});
</script>

<style></style>
