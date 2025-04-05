<template>
  <Transition name="fade">
    <div v-show="modelValue"
      class="fixed inset-0 z-50 bg-[rgba(0,0,0,0.8)] flex items-center justify-center select-none"
      @keydown="handleKeydown" tabindex="0" ref="viewerRef">
      <!-- 主图片容器 -->
      <div class="relative w-full h-full flex items-center justify-center">

        <!-- 主图片 -->
        <Transition name="slide" mode="out-in">
          <div :key="currentImageSrc" class="flex items-center justify-center">
            <NuxtImg v-if="currentImageSrc" :src="currentImageSrc" class="max-w-full max-h-screen object-contain"
              @load="isLoading = false" />

            <!-- 图片信息区域 - 现在居中显示且宽度有限制 -->
            <Transition name="slide-up">
              <div v-show="showInfo"
                class="absolute bottom-0 left-1/2 transform -translate-x-1/2 bg-[rgba(0,0,0,0.6)] text-[rgba(255,255,255,0.8)] transition-all duration-300 rounded-t-xl max-w-[600px] w-full mx-auto"
                :class="{ 'h-16': !fullInfo, 'h-32': fullInfo }">
                <UCard class="bg-transparent ring-0">
                  <div class="text-lg font-bold">
                    Info
                  </div>
                  <p>当前图片: {{ currentIndex + 1 }} / {{ totalImages }} </p>
                  <p v-if="fullInfo">更多详细信息可以在这里显示...
                  </p>
                </UCard>
              </div>
            </Transition>
          </div>
        </Transition>

        <!-- 左侧导航区域 - 现在整个左侧10%区域都是可点击的 -->
        <div v-show="hasPrevious && !isLoading"
          class="absolute left-0 top-0 bottom-0 w-1/10 cursor-pointer flex items-center justify-start pl-8 opacity-0 hover:opacity-100 transition-opacity duration-300 group"
          @click="prevImage">
          <Icon name="i-heroicons-arrow-left" class="text-2xl text-white" />
        </div>

        <!-- 右侧导航区域 - 现在整个右侧10%区域都是可点击的 -->
        <div v-show="hasNext && !isLoading"
          class="absolute right-0 top-0 bottom-0 w-1/10 cursor-pointer flex items-center justify-end pr-8 opacity-0 hover:opacity-100 transition-opacity duration-300 group"
          @click="nextImage">
          <Icon name="i-heroicons-arrow-right" class="text-2xl text-white" />
        </div>

        <!-- 顶部控制栏 -->
        <div class="absolute top-4 right-4 flex space-x-2">
          <Icon name="i-heroicons-x-mark" class="text-3xl text-white cursor-pointer" @click="closeViewer" />
        </div>

        <!-- 预加载下一张图片 -->
        <div class="hidden">
          <NuxtImg v-if="preloadSrc" :src="preloadSrc" @load="handlePreloadComplete" />
        </div>
      </div>
    </div>
  </Transition>
</template>
<script setup lang="ts">
import type { separator } from '#build/ui';
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue';

const props = defineProps({
  nextPhoto: {
    type: Function,
    required: true
  },
  previousPhoto: {
    type: Function,
    required: true
  },
  initialImageSrc: {
    type: String,
    default: ''
  },
  initialIndex: {
    type: Number,
    default: 0
  }
});

const show = defineModel<boolean>()

const emit = defineEmits(['update:modelValue']);

// 状态管理
const currentImageSrc = ref(props.initialImageSrc);
const preloadSrc = ref('');
const isLoading = ref(true);
const showInfo = ref(false);
const fullInfo = ref(false);
const mouseY = ref(0);
const viewerRef = useTemplateRef('viewerRef');
const currentIndex = ref(props.initialIndex);
const totalImages = ref(1);
const hasPrevious = ref(false);
const hasNext = ref(false);

// 鼠标移动处理
const handleMouseMove = (e: MouseEvent) => {
  if (!viewerRef.value) return;

  const rect = (viewerRef.value as HTMLElement).getBoundingClientRect();
  const height = rect.height;
  mouseY.value = e.clientY - rect.top;

  // 检查鼠标是否在底部10%的区域
  const infoTriggerZone = height * 0.9;
  showInfo.value = mouseY.value > infoTriggerZone;

  // 检查鼠标是否接近底部边缘
  const fullInfoTriggerZone = height * 0.95;
  fullInfo.value = mouseY.value > fullInfoTriggerZone;
};

// 键盘导航
const handleKeydown = (e: KeyboardEvent) => {
  if (!show.value) return;
  if (e.key === 'ArrowLeft') {
    e.preventDefault();
    prevImage();
  } else if (e.key === 'ArrowRight') {
    e.preventDefault();
    nextImage();
  } else if (e.key === 'Escape') {
    e.preventDefault();
    closeViewer();
  }
};

// 图片导航
const prevImage = () => {
  if (!hasPrevious.value) return;

  // isLoading.value = true;
  const prevSrc = props.previousPhoto(currentIndex.value);
  console.log('prevSrc', prevSrc);
  if (prevSrc) {
    currentImageSrc.value = prevSrc;
    currentIndex.value--;
    updateNavState();
    preloadNextImage();
    nextTick(refocusViewer);
  }
};

const nextImage = () => {
  if (!hasNext.value) return;

  isLoading.value = true;
  const nextSrc = props.nextPhoto(currentIndex.value);
  if (nextSrc) {
    currentImageSrc.value = nextSrc;
    currentIndex.value++;
    updateNavState();
    preloadNextImage();
    nextTick(refocusViewer);
  }
};

// 预加载下一张图片
const preloadNextImage = () => {
  // 尝试预加载下一张图片
  const nextSrc = props.nextPhoto(currentIndex.value);
  if (nextSrc) {
    preloadSrc.value = nextSrc;
  }
};

const handlePreloadComplete = () => {
  // 预加载完成，这里可以添加一些状态管理
  console.log('Next image preloaded');
};

const refocusViewer = () => {
  if (viewerRef.value) {
    (viewerRef.value as HTMLElement).focus();
  }
};

// 关闭查看器
const closeViewer = () => {
  show.value = false;
};

// 更新导航状态
const updateNavState = () => {
  const prevSrc = props.previousPhoto(currentIndex.value);
  const nextSrc = props.nextPhoto(currentIndex.value);

  hasPrevious.value = !!prevSrc;
  hasNext.value = !!nextSrc;

  // 调试输出
  console.log("Navigation state updated:", {
    hasPrevious: hasPrevious.value,
    hasNext: hasNext.value,
    prevSrc,
    currentIndex: currentIndex.value
  });
};

// 生命周期钩子
onMounted(() => {
  if (viewerRef.value) {
    refocusViewer();
    window.addEventListener('mousemove', handleMouseMove);
  }

  updateNavState();
  preloadNextImage();
});

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', handleMouseMove);
});

// 监听show变化
watch(() => show, (newVal) => {
  if (newVal) {
    // 当打开查看器时，重置状态
    isLoading.value = true;
    currentImageSrc.value = props.initialImageSrc;
    currentIndex.value = 0;
    updateNavState();

    // 确保DOM更新后获取焦点
    nextTick(refocusViewer);
  }
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-enter-from {
  transform: translateX(30px);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(-30px);
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-up-enter-from {
  transform: translateY(100%);
  opacity: 0;
}

.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>