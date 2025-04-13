<template>
  <div class="flex flex-wrap gap-4 py-4 px-8 max-sm:hidden">
    <Photo v-for="(img, index) in displayImages" :src="img" :alt="img" class="item hover:shadow-xl transition-shadow"
      @click="$emit('click', img, index)" />
  </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue';

const props = defineProps({
  height: {
    type: String,
    default: "300px"
  },
  maxWidth: {
    type: String,
    default: "50%"
  },
  images: {
    type: Array<string>,
    default: () => []
  }
});

defineEmits(["click"]);

// 使用ref来管理图片，允许我们修改显示的图片
const displayImages = ref<string[]>([...props.images]);

// 添加新图片到现有的图片集合中
const appendImages = (newImages: string[]) => {
  displayImages.value = [...displayImages.value, ...newImages];
  return displayImages.value;
};

// 重置图片集合为新的图片数组
const resetImages = (newImages: string[]) => {
  displayImages.value = [...newImages];
  return displayImages.value;
};

// 获取当前显示的所有图片
const getCurrentImages = (): string[] => {
  return [...displayImages.value];
};

// 暴露组件方法，使父组件可以访问这些方法
defineExpose({
  appendImages,
  resetImages,
  getCurrentImages
});
</script>
<style scoped>
.item {
  flex-grow: 1;
  object-fit: cover;
  height: v-bind("height");
  max-width: v-bind("maxWidth");
}
</style>