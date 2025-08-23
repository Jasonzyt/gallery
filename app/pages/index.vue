<template>
  <div class="p-4 max-sm:hidden">
    <Masonry ref="masonry" :list="smPhotos" @click="handleClick" />
  </div>
  <div class="p-2.5 sm:hidden">
    <Waterfall ref="waterfall" :list="smPhotos" @click="handleClick" />
  </div>
  <ImageViewer ref="viewer" v-model="showViewer" :photo-list="lgPhotos" />
</template>

<script lang="ts" setup>
const showViewer = ref(false);
const allPhotos = getAllPhotoUrls()
const lgPhotos = ref(formatUrlsWithSize(allPhotos, 'lg'))
const smPhotos = ref(formatUrlsWithSize(allPhotos, 'sm'))

const viewerRef = useTemplateRef('viewer')

const handleClick = (_img: string, index: number) => {
  showViewer.value = true
  viewerRef.value!.setPhotoIndex(index)
}
</script>

<style></style>