<template>
  <div class="w-full p-4 sm:p-8 grid grid-cols-1 gap-4 lg:grid-cols-2">
    <Album v-for="(album, index) in albums" :key="index" :title="album.name" :description="album.desc"
      :preview-photos="getAlbumPhotoUrls(album, 'sq').slice(0, 20)" />
  </div>
</template>

<script lang="ts" setup>
const albums = getAlbums()
</script>

<style></style>