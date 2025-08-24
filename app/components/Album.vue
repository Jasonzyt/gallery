<template>
  <UCard class="w-full">
    <div class="flex flex-col gap-2">
      <!-- 相册标题 -->
      <h3 class="text-lg font-medium">{{ album.name }}</h3>

      <!-- 相册描述 -->
      <p class="text-sm text-toned mb-2">{{ album.description }}</p>

      <!-- 相册预览图片 -->
      <div class="relative w-full overflow-hidden">
        <div class="flex overflow-x-auto pb-2 scrollbar-hide">
          <div
            v-for="(photo, index) in photos"
            :key="index"
            class="shrink-0 mr-2 cursor-pointer"
            @click="handlePhotoClick(photo, index)"
          >
            <img
              :src="photo.url"
              alt="Preview Photos"
              class="h-24 w-24 object-cover rounded"
            />
          </div>
        </div>
        <!-- 渐变遮罩 -->
        <div
          class="absolute right-0 top-0 h-full w-16 bg-gradient-to-l from-white to-transparent dark:from-[#0f172b] pointer-events-none"
        ></div>
      </div>
    </div>
  </UCard>
</template>

<script setup>
const props = defineProps({
  album: {
    type: Object,
    required: true,
  },
  size: {
    type: Number,
    default: 24, // 默认尺寸为 96px (24 * 4)
  },
});

const photos = ref(await getAlbumPhotosWithUrls(props.album, "sq"));
console.log("Album photos:", photos.value);

const emit = defineEmits(["photo-click"]);

const handlePhotoClick = (photo, index) => {
  emit("photo-click", { photo, index });
};
</script>

<style scoped>
/* 隐藏滚动条但保留滚动功能 */
.scrollbar-hide {
  -ms-overflow-style: none;
  /* IE and Edge */
  scrollbar-width: none;
  /* Firefox */
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
  /* Chrome, Safari and Opera */
}
</style>
