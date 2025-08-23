<template>
  <div class="w-full flex flex-wrap gap-4">
    <Photo
      v-for="(img, index) in displayImages"
      :src="img"
      :alt="img"
      class="item hover:shadow-xl transition-shadow"
      @click="$emit('click', img, index)"
    />
    <Loading
      :visible="isLoading"
      class="w-full mt-8"
      type="wave"
      :overlay="false"
      :fullscreen="false"
    />
    <!-- 用于触发加载更多的不可见标记元素 -->
    <div ref="loadMoreTrigger" class="w-full h-1 bottom-0 opacity-0"></div>
  </div>

  <!-- 底部结束提示 -->
  <USeparator
    v-if="hasReachedEnd"
    class="w-full px-4 text-center"
    :ui="{ container: 'text-gray-500' }"
    :label="endText"
  />
</template>

<script lang="ts">
const calcHeight = (x: number = 0.15) => {
  let result = window.innerWidth * x;
  if (result < 150) {
    result = 150;
  }
  if (result > 275) {
    result = 275;
  }
  return `${result}px`;
};
</script>

<script lang="ts" setup>
const props = defineProps({
  height: {
    type: String,
  },
  maxWidth: {
    type: String,
    default: "50%",
  },
  list: {
    type: Array as PropType<string[]>,
    default: () => [],
  },
  loadMoreThreshold: {
    type: Number,
  },
  endText: {
    type: String,
    default: "到底了~",
  },
  // expose
  onLoadMore: {
    type: Function,
    default: null,
  },
});

const emit = defineEmits(["click", "loadMore"]);

const isLoading = ref(false);
const currentHeight = ref(props.height);
const loadMoreTrigger = ref<HTMLElement | null>(null);
const hasReachedEnd = ref(false);
const observer = ref<IntersectionObserver | null>(null);
const loadMoreThreshold = ref(props.loadMoreThreshold);

const displayImages = ref<string[]>([]);

// 添加新图片到现有的图片集合中
const appendImages = (newImages: string[] | undefined) => {
  if (!newImages || newImages.length === 0) {
    hasReachedEnd.value = true;
    return displayImages.value;
  }

  isLoading.value = true;
  let loadCount = 0;
  newImages.forEach(async (img) => {
    loadImage(img).finally(() => {
      loadCount++;
      if (loadCount === newImages.length) {
        displayImages.value.push(...newImages);
        isLoading.value = false;
      }
    });
  });

  // return displayImages.value;
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
};

// 设置交叉观察器
const setupObserver = () => {
  if (!loadMoreTrigger.value) return;

  // 创建Observer实例
  observer.value = new IntersectionObserver(
    (entries) => {
      const entry = entries[0];
      // console.log('entry', entry);
      if (entry?.isIntersecting) {
        triggerLoadMore();
      }
    },
    {
      // 设置根元素为视口
      root: null,
      // 提前触发的距离
      rootMargin: `0px 0px ${loadMoreThreshold.value ?? "200"}px 0px`,
      threshold: 0,
    }
  );

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
  if (props.onLoadMore) {
    emit("loadMore");
  } else if (props.list) {
    const startIndex = displayImages.value.length;
    let endIndex = startIndex + 20 - 1; // 每次加载20张图片
    if (startIndex >= props.list.length) {
      setEndReached(true);
      return;
    }
    if (endIndex >= props.list.length) {
      endIndex = props.list.length - 1;
    }
    const newImages = props.list.slice(startIndex, endIndex + 1);
    appendImages(newImages);
  } else {
    console.warn("No loadMore event handler provided.");
  }
};

// 组件挂载后初始化
onMounted(async () => {
  if (loadMoreThreshold.value === undefined) {
    loadMoreThreshold.value = window.innerHeight * 0.2; // 默认阈值
  }
  currentHeight.value = calcHeight();
  window.onresize = () => {
    currentHeight.value = calcHeight();
  };
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
  setEndReached,
});
</script>
<style scoped>
.item {
  flex-grow: 1;
  object-fit: cover;
  height: v-bind("currentHeight");
  max-width: v-bind("maxWidth");
}
</style>
