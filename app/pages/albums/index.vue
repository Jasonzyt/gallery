<template>
  <div class="w-full p-4 sm:p-8 grid grid-cols-1 gap-4 lg:grid-cols-2">
    <NuxtLink
      v-for="(album, index) in albums"
      :key="index"
      :to="`/albums/${album.id}`"
    >
      <Album
        :album="album"
        class="shadow-md hover:shadow-xl transition-shadow"
      />
    </NuxtLink>
  </div>
</template>

<script lang="ts" setup>
const albums = await getAlbums();
</script>

<style></style>
