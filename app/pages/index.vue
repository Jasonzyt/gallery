<template>
  <div class="p-4 max-sm:hidden">
    <Masonry ref="masonry" :list="photos" @click="handleClick" />
  </div>
  <div class="p-2.5 sm:hidden">
    <Waterfall ref="waterfall" :list="photos" @click="handleClick" />
  </div>
  <ImageViewer ref="viewer" v-model="showViewer" :photo-list="photos" />
</template>

<script lang="ts" setup>
const showViewer = ref(false);
const photos = await getAllPhotosWithUrls();
const viewerRef = useTemplateRef("viewer");
const handleClick = (_img: string, index: number) => {
  showViewer.value = true;
  viewerRef.value!.setPhotoIndex(index);
};
</script>

<style></style>
