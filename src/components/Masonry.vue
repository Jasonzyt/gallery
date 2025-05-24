<template>
  <div class="w-full flex flex-wrap gap-4">
    <Photo v-for="(img, index) in displayImages" :src="img" :alt="img" class="item hover:shadow-xl transition-shadow"
      @click="$emit('click', img, index)" />
    <!-- 用于触发加载更多的不可见标记元素 -->
    <div ref="loadMoreTrigger" class="w-full h-1 bottom-0 opacity-0"></div>
  </div>

  <!-- 底部结束提示 -->
  <USeparator v-if="hasReachedEnd" class="w-full px-4 pb-4 text-center" :ui="{ container: 'text-gray-500' }"
    :label="endText" />
</template>
<script lang="ts" setup>
const props = defineProps({
  height: {
    type: String,
    default: "300px"
  },
  maxWidth: {
    type: String,
    default: "50%"
  },
  loadMoreThreshold: {
    type: Number,
    default: window.innerHeight * 0.2
  },
  endText: {
    type: String,
    default: "到底了~"
  }
});

const emit = defineEmits(["click", "loadMore"]);

const loadMoreTrigger = ref<HTMLElement | null>(null);
const hasReachedEnd = ref(false);
const observer = ref<IntersectionObserver | null>(null);

// 使用ref来管理图片，允许我们修改显示的图片
const displayImages = ref<string[]>([]);

// 添加新图片到现有的图片集合中
const appendImages = (newImages: string[] | undefined) => {
  if (!newImages || newImages.length === 0) {
    hasReachedEnd.value = true;
    return displayImages.value;
  }
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

const setEndReached = (value: boolean) => {
  hasReachedEnd.value = value;
}

// 设置交叉观察器
const setupObserver = () => {
  if (!loadMoreTrigger.value) return;

  // 创建Observer实例
  observer.value = new IntersectionObserver((entries) => {
    const entry = entries[0];
    console.log('entry', entry);
    if (entry.isIntersecting) {
      triggerLoadMore();
    }
  }, {
    // 设置根元素为视口
    root: null,
    // 提前触发的距离
    rootMargin: `0px 0px ${props.loadMoreThreshold}px 0px`,
    threshold: 0
  });

  // 开始观察元素
  observer.value.observe(loadMoreTrigger.value);
};

// 清理Observer
const cleanupObserver = () => {
  if (observer.value) {
    observer.value.disconnect();
    observer.value = null;
  }
};

// 触发加载更多事件
const triggerLoadMore = () => {
  emit('loadMore');
};

// 组件挂载后初始化
onMounted(async () => {
  setupObserver();
});

// 组件卸载前清理
onUnmounted(() => {
  cleanupObserver();
});

// 暴露组件方法，使父组件可以访问这些方法
defineExpose({
  appendImages,
  resetImages,
  getCurrentImages,
  setEndReached
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