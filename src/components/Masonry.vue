<template>
  <div class="hfall">
    <NuxtImg v-for="img in images" :src="img" :alt="img" class="item hover:shadow-xl transition-shadow"></NuxtImg>
  </div>
</template>

<script lang="ts" setup>
defineProps({
  images: {
    type: Array<string>
  }
})

</script>

<style scoped>
.hfall {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 1rem 2rem;
  /* width: 500px; */
}

.item {
  flex-grow: 1;
  object-fit: cover;
  height: 300px;
  max-width: 100%;
  border-radius: 12px;
  border: 1px rgb(var(--color-gray-500));
}
</style>