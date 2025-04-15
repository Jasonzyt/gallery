<template>
  <Masonry ref="masonry" :images="smPhotos" height="250px" @click="handleClick" @load-more="handleLoadMore" />
  <Waterfall ref="waterfall" :images="smPhotos" @click="handleClick" @load-more="handleLoadMore" />
  <ImageViewer v-model="showViewer" :next-photo="nextPhoto" :previous-photo="previousPhoto"
    :initial-image-src="lgPhotos[initialIndex]" :initial-index="initialIndex" />
</template>

<script lang="ts" setup>
const showViewer = ref(false);
const allPhotos = getAllPhotoUrls()
const photos = allPhotos.slice(0, 19) // 只取前20张图片
const lgPhotos = formatUrlsWithSize(photos, 'lg')
const smPhotos = formatUrlsWithSize(photos, 'sm')
const pageCount = ref(0)
const initialIndex = ref(0)

const masonry = useTemplateRef('masonry')
const waterfall = useTemplateRef('waterfall')
const appendImages = (images: string[]) => {
  return document.body.clientWidth > 640
    ? masonry.value!.appendImages(images)
    : waterfall.value!.appendImages(images)
}
const setEndReached = (value: boolean) => {
  return document.body.clientWidth > 640
    ? masonry.value!.setEndReached(value)
    : waterfall.value!.setEndReached(value)
}

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

const handleLoadMore = () => {
  pageCount.value++
  const startIndex = pageCount.value * 20
  let endIndex = (pageCount.value + 1) * 20 - 1
  if (startIndex >= allPhotos.length) {

  }
  if (endIndex >= allPhotos.length) {
    endIndex = allPhotos.length - 1
  }
  const newPhotos = allPhotos.slice(startIndex, endIndex)
  const newLgPhotos = formatUrlsWithSize(newPhotos, 'lg')
  const newSmPhotos = formatUrlsWithSize(newPhotos, 'sm')
  lgPhotos.push(...newLgPhotos)
  smPhotos.push(...newSmPhotos)
  // 这里需要调用Waterfall组件的appendImages方法
  appendImages(newSmPhotos)
}

const handleClick = (img: string, index: number) => {
  initialIndex.value = index
  showViewer.value = true
}
</script>

<style></style>