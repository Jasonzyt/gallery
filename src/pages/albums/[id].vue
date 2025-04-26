<template>
  <div class="w-full p-4">
    <NuxtImg :src="coverImage" alt="Album Cover" class="w-full h-[250px] object-cover rounded-lg mb-8" />
    <div class="flex flex-col items-center justify-center mb-8">
      <h1 class="text-2xl font-bold mb-2">{{ album.name }}</h1>
      <p class="text-gray-600">{{ album.desc }} - {{ photoCount }} photos</p>
    </div>
    <Masonry ref="masonry" :images="smPhotos" height="250px" @click="handleClick" />
  </div>
</template>

<script lang="ts" setup>
const route = useRoute()
const id = ref("")
if (Array.isArray(route.params.id)) {
  id.value = route.params.id.join("")
} else {
  id.value = route.params.id
}
const album = getAlbum(id.value)
if (!album) {
  throw createError({
    statusCode: 404,
    statusMessage: "Album not found",
  })
}
const photos = getAlbumPhotoUrls(album)
const smPhotos = formatUrlsWithSize(photos, 'sm')
const photoCount = ref(photos.length)
const coverImage = ref('')
if (!album.cover) {
  coverImage.value = formatUrlWithSize(photos[Math.floor(Math.random() * photos.length)], 'lg')
} else {
  coverImage.value = album.cover
}

const showViewer = ref(false)

const handleClick = (img: string, index: number) => {
  showViewer.value = true
}
</script>

<style>

</style>