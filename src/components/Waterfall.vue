<template>
  <div class="relative">
    <div ref="masonryContainer" class="sm:hidden flex w-full" :style="`gap: ${gap}`">
      <!-- 动态生成多栏 -->
      <div v-for="colIndex in columns" :key="colIndex" class="flex flex-col"
        :style="`width: ${100 / columns}%; gap: ${gap}`" ref="columnsRef">
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
  list: {
    type: Array as PropType<string[]>,
    default: () => []
  },
  // 触发加载更多的距离阈值，默认为400px
  loadMoreThreshold: {
    type: Number,
    default: 400
  },
  // 结束提示文本
  endText: {
    type: String,
    default: "到底了~"
  },
  // expose
  onLoadMore: {
    type: Function,
    default: null
  }
});

const emit = defineEmits(["click", "loadMore"]);

// 容器引用
const masonryContainer = useTemplateRef('masonryContainer');
const loadMoreTrigger = useTemplateRef('loadMoreTrigger');
const columnsRef = useTemplateRef('columnsRef');

// 是否已到达底部
const hasReachedEnd = ref(false);
const observer = ref<IntersectionObserver | null>(null);

// 存储所有图片的数据，包括高度信息
const imageData = reactive<{
  items: Array<{
    src: string;
    width: number;
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

const columnWidth = ref(400)
const columnGap = ref(16);
// 每列的累积高度
const columnHeights = ref<number[]>(Array(props.columns).fill(0));

// 标记是否正在加载
const isLoading = ref(false);

// 初始化列数据
const initializeColumns = () => {
  columnImages.value = Array.from({ length: props.columns }, () => []);
  columnHeights.value = Array(props.columns).fill(0);
  columnWidth.value = columnsRef.value?.at(0)?.clientWidth || 200;
  columnGap.value = (columnsRef.value?.at(0)?.computedStyleMap()?.get("column-gap") as CSSUnitValue).value || 16;
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

    const actualHeight = item.height * (columnWidth.value / item.width);

    // 更新该列的高度
    columnHeights.value[minHeightIndex] += actualHeight + columnGap.value;

    // console.log(`Adding image ${item.src} ${actualHeight} to column ${minHeightIndex}, new height: ${columnHeights.value[minHeightIndex]}`);
  });

  // console.log("Column heights: ", columnHeights.value);
};

// 添加新图片
const appendImages = async (newImages: string[]) => {
  if (!Array.isArray(newImages) || newImages.length === 0) {
    hasReachedEnd.value = true;
    return;
  }

  // 如果正在加载，则等待加载完成
  if (isLoading.value) {
    await new Promise<void>(resolve => {
      const interval = setInterval(() => {
        if (!isLoading.value) {
          clearInterval(interval);
          resolve();
        }
      }, 100);
    });
  }

  isLoading.value = true;

  try {
    const startIndex = imageData.items.length;

    // 创建新的图片项
    const newItems = newImages.map((src, index) => ({
      src,
      width: 0,
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
          item.width = img.width;
          item.height = img.height;
          item.loaded = true;
          resolve();
        };
        img.onerror = () => {
          // item.height = 300; // 默认高度
          item.loaded = true;
          resolve();
        };
        img.src = item.src;
      });
    }));

    // 更新布局
    updateLayout();
  } catch (e) {
    console.error("Error loading images: ", e);
  } finally {
    isLoading.value = false;
  }
};

// 重置图片
const resetImages = async (images: string[] = []) => {
  // 重置结束状态
  hasReachedEnd.value = false;
  imageData.items = [];
  initializeColumns();
  await appendImages(images);
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

  if (props.onLoadMore) {
    emit('loadMore');
  } else if (props.list) {
    const startIndex = imageData.items.length;
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

// 组件挂载后初始化
onMounted(async () => {
  await nextTick();
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