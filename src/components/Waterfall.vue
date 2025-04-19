<template>
  <div class="relative">
    <div ref="masonryContainer" class="sm:hidden flex w-full" :style="`gap: ${gap}`">
      <!-- 动态生成多栏 -->
      <div v-for="colIndex in columns" :key="colIndex" class="flex flex-col"
        :style="`width: ${100 / columns}%; gap: ${gap}`">
        <Photo v-for="img in columnImages[colIndex - 1]" :key="img.src" :src="img.src" :alt="img.src"
          :style="img.maxHeight ? `max-height: ${img.maxHeight}` : ''"
          class="w-full transition-shadow hover:shadow-xl cursor-pointer"
          @click="$emit('click', img.src, img.originalIndex)" />
      </div>

      <!-- 用于触发加载更多的不可见标记元素 -->
      <div ref="loadMoreTrigger" class="w-full h-1 absolute bottom-0 opacity-0"></div>
    </div>

    <!-- 底部结束提示 -->
    <USeparator v-if="hasReachedEnd" class="w-full px-2 py-4 text-center" :ui="{ container: 'text-gray-500' }"
      :label="endText" />
  </div>
</template>

<script lang="ts" setup>
const props = defineProps({
  images: {
    type: Array<string>,
    required: true
  },
  columns: {
    type: Number,
    default: 2
  },
  gap: {
    type: String,
    default: "1rem"
  },
  maxHeight: {
    type: String,
    default: ""
  },
  // 触发加载更多的距离阈值，默认为400px
  loadMoreThreshold: {
    type: Number,
    default: 400
  },
  // 是否启用自动检测滚动加载
  enableAutoLoad: {
    type: Boolean,
    default: true
  },
  // 结束提示文本
  endText: {
    type: String,
    default: "到底了~"
  }
});

const emit = defineEmits(["click", "loadMore"]);

// 容器引用
const masonryContainer = useTemplateRef('masonryContainer');
const loadMoreTrigger = useTemplateRef('loadMoreTrigger');

// 是否已到达底部
const hasReachedEnd = ref(false);
const observer = ref<IntersectionObserver | null>(null);

// 存储所有图片的数据，包括高度信息
const imageData = reactive<{
  items: Array<{
    src: string;
    height: number;
    loaded: boolean;
    originalIndex: number;
    maxHeight?: string;
  }>;
}>({ items: [] });

// 每列图片
const columnImages = ref<Array<Array<{
  src: string;
  originalIndex: number;
  maxHeight?: string;
}>>>(Array.from({ length: props.columns }, () => []));

// 每列的累积高度
const columnHeights = ref<number[]>(Array(props.columns).fill(0));

// 标记是否正在加载
const isLoading = ref(false);

// 初始化列数据
const initializeColumns = () => {
  columnImages.value = Array.from({ length: props.columns }, () => []);
  columnHeights.value = Array(props.columns).fill(0);
};

// 加载图片并获取高度
const loadImages = async (images: string[]) => {
  // 防止重复加载
  if (isLoading.value) return;

  isLoading.value = true;

  try {
    // 重置图片数据
    imageData.items = [];

    // 创建新的图片项
    const newItems = images.map((src, index) => ({
      src,
      height: 0,
      loaded: false,
      originalIndex: index,
      maxHeight: props.maxHeight || undefined
    }));

    // 添加到现有数组
    imageData.items.push(...newItems);

    // 加载所有图片并获取高度
    await Promise.all(newItems.map(item => {
      return new Promise<void>((resolve) => {
        const img = new Image();
        img.onload = () => {
          item.height = img.height;
          item.loaded = true;
          resolve();
        };
        img.onerror = () => {
          item.height = 300; // 默认高度
          item.loaded = true;
          resolve();
        };
        img.src = item.src;
      });
    }));

    // 更新布局
    updateLayout();

    // 重置结束状态
    hasReachedEnd.value = false;
  } finally {
    isLoading.value = false;
  }
};

// 更新布局
const updateLayout = () => {
  // 重置列
  initializeColumns();

  // 按原始顺序排序图片
  const sortedItems = [...imageData.items].sort((a, b) => a.originalIndex - b.originalIndex);

  // 将图片分配到各列
  sortedItems.forEach(item => {
    // 找出当前高度最低的列
    const minHeightIndex = columnHeights.value.indexOf(Math.min(...columnHeights.value));

    // 将图片添加到该列
    columnImages.value[minHeightIndex].push({
      src: item.src,
      originalIndex: item.originalIndex,
      maxHeight: item.maxHeight
    });

    // 更新该列的高度
    columnHeights.value[minHeightIndex] += item.height + parseFloat(props.gap);
  });
};

// 添加新图片
const appendImages = async (newImages: string[]) => {
  if (!Array.isArray(newImages) || newImages.length === 0) {
    hasReachedEnd.value = true;
    return;
  }

  // 防止重复加载
  if (isLoading.value) return;

  isLoading.value = true;

  try {
    const startIndex = imageData.items.length;

    // 创建新的图片项
    const newItems = newImages.map((src, index) => ({
      src,
      height: 0,
      loaded: false,
      originalIndex: startIndex + index,
      maxHeight: props.maxHeight || undefined
    }));

    // 添加到现有数组
    imageData.items.push(...newItems);

    // 加载所有新图片
    await Promise.all(newItems.map(item => {
      return new Promise<void>((resolve) => {
        const img = new Image();
        img.onload = () => {
          item.height = img.height;
          item.loaded = true;
          resolve();
        };
        img.onerror = () => {
          item.height = 300; // 默认高度
          item.loaded = true;
          resolve();
        };
        img.src = item.src;
      });
    }));

    // 更新布局
    updateLayout();
  } finally {
    isLoading.value = false;
  }
};

// 重置图片
const resetImages = async (images: string[] = []) => {
  // 重置结束状态
  hasReachedEnd.value = false;
  await loadImages(images);
};

// 获取当前所有图片
const getCurrentImages = () => {
  return imageData.items.map(item => item.src);
};

// 设置交叉观察器
const setupObserver = () => {
  if (!loadMoreTrigger.value) return;

  // 创建Observer实例
  observer.value = new IntersectionObserver((entries) => {
    const entry = entries[0];
    // 当触发元素进入视口时
    if (entry.isIntersecting && !isLoading.value && !hasReachedEnd.value) {
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
  if (isLoading.value || hasReachedEnd.value) return;

  emit('loadMore');
};

// 监听初始props.images变化
watch(() => props.images, async (newImages) => {
  await loadImages([...newImages]);
}, { immediate: true });

// 监听列数变化
watch(() => props.columns, () => {
  updateLayout();
});

// 监听maxHeight变化
watch(() => props.maxHeight, () => {
  imageData.items.forEach(item => {
    item.maxHeight = props.maxHeight || undefined;
  });
  updateLayout();
});

// 监听enableAutoLoad变化
watch(() => props.enableAutoLoad, (newValue) => {
  if (newValue) {
    setupObserver();
  } else {
    cleanupObserver();
  }
});

// 组件挂载后初始化
onMounted(async () => {
  await nextTick();
  if (props.images.length > 0) {
    await loadImages([...props.images]);
  }
  setupObserver();
});

// 组件卸载前清理
onUnmounted(() => {
  cleanupObserver();
});

// 设置结束状态
const setEndReached = (isEnd: boolean = true) => {
  hasReachedEnd.value = isEnd;
};

// 暴露组件内部方法
defineExpose({
  appendImages,
  resetImages,
  getCurrentImages,
  setEndReached
});
</script>