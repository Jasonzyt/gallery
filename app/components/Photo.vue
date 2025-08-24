<template>
  <div
    class="shadow-md hover:shadow-xl transition-shadow rounded-xl relative"
    @mouseenter="isHovering = true"
    @mouseleave="isHovering = false"
    @click="$emit('click')"
  >
    <img
      :src="formatUrlWithSize(photo.url ?? '', size)"
      :alt="photo.title"
      ref="img"
      class="size-full object-cover rounded-xl z-0"
    />
    <p
      v-if="description.length !== 0"
      class="absolute w-full mt-[-3rem] py-3 px-4 rounded-b-xl text-gray-100 transition-opacity duration-300 z-10"
      :class="isHovering || isTouchDevice ? 'opacity-100' : 'opacity-0'"
    >
      {{ description }}
    </p>
  </div>
</template>

<script lang="ts" setup>
defineProps({
  photo: {
    type: Object as PropType<Photo>,
    required: true,
  },
  size: {
    type: String,
    default: "sm",
  },
});

const emits = defineEmits(["click"]);

const isHovering = ref(false);
const description = ref("");

const isTouchDevice = "ontouchstart" in window || navigator.maxTouchPoints > 0;
</script>

<style scoped>
p {
  background: linear-gradient(0deg, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0));
}
</style>
