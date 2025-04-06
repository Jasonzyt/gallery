<template>
  <Masonry :images="smPhotos" height="250px" @click="handleClick" />
  <ImageViewer v-model="showViewer" :next-photo="nextPhoto" :previous-photo="previousPhoto"
    :initial-image-src="lgPhotos[initialIndex]" :initial-index="initialIndex" />
</template>

<script lang="ts" setup>
const showViewer = ref(false);
const photos = getAllPhotoUrls()
const lgPhotos = formatUrlsWithSize(photos, 'lg')
const smPhotos = formatUrlsWithSize(photos, 'sm')
const initialIndex = ref(0)
const nextPhoto = (currentIndex: number) => {
  if (currentIndex === photos.length - 1) {
    return undefined
  } else {
    currentIndex++
  }
  return lgPhotos[currentIndex]
}
const previousPhoto = (currentIndex: number) => {
  if (currentIndex === 0) {
    return undefined
  } else {
    currentIndex--
  }
  return lgPhotos[currentIndex]
}

const handleClick = (img: string, index: number) => {
  initialIndex.value = index
  showViewer.value = true
}
</script>

<style></style>