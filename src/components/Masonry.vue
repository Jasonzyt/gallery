<template>
  <div class="masonry">
    <Photo v-for="(img, index) in images" :src="img" :alt="img" class="item hover:shadow-xl transition-shadow"
      @click="$emit('click', img, index)" />
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
    default: "50%"
  },
  images: {
    type: Array<string>
  }
})

defineEmits(["click"])

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