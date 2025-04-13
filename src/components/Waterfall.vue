<template>
  <div ref="masonryContainer" class="flex w-full sm:hidden" :style="`gap: ${gap}`">
    <!-- 动态生成多栏 -->
    <div v-for="colIndex in columns" :key="colIndex" class="flex flex-col"
      :style="`width: ${100 / columns}%; gap: ${gap}`">
      <Photo v-for="img in columnImages[colIndex - 1]" :key="img.src" :src="img.src" :alt="img.src"
        :style="img.maxHeight ? `max-height: ${img.maxHeight}` : ''"
        class="w-full transition-shadow hover:shadow-xl cursor-pointer"
        @click="$emit('click', img.src, img.originalIndex)" />
    </div>
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
  }
});

defineEmits(["click"]);

// 容器引用
const masonryContainer = ref(null);

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

// 初始化列数据
const initializeColumns = () => {
  columnImages.value = Array.from({ length: props.columns }, () => []);
  columnHeights.value = Array(props.columns).fill(0);
};

// 加载图片并获取高度
const loadImages = async (images: string[]) => {
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
  if (!Array.isArray(newImages) || newImages.length === 0) return;

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
};

// 重置图片
const resetImages = async (images: string[] = []) => {
  await loadImages(images);
};

// 获取当前所有图片
const getCurrentImages = () => {
  return imageData.items.map(item => item.src);
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

// 组件挂载后初始化
onMounted(async () => {
  await nextTick();
  if (props.images.length > 0) {
    await loadImages([...props.images]);
  }
});

// 暴露组件内部方法
defineExpose({
  appendImages,
  resetImages,
  getCurrentImages
});
</script>