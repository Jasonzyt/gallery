<template>
  <div class="masonry">
    <Photo v-for="img in images" :src="img" :alt="img" class="item hover:shadow-xl transition-shadow">
    </Photo>
  </div>
</template>

<script lang="ts" setup>
defineProps({
  height: {
    type: String,
    default: "300px"
  },
  maxWidth: {
    type: String,
    default: "100%"
  },
  images: {
    type: Array<string>
  }
})

</script>

<style scoped>
.masonry {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 1rem 2rem;
  /* width: 500px; */
}

.item {
  flex-grow: 1;
  object-fit: cover;
  height: v-bind("height");
  max-width: v-bind("maxWidth");
}
</style>