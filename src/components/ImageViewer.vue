<template>
  <Transition name="fade">
    <div v-show="show" class="fixed inset-0 z-50 bg-[rgba(0,0,0,0.8)] flex items-center justify-center select-none"
      @keydown="handleKeydown" tabindex="0" ref="viewerRef">
      <div class="relative w-full h-full flex items-center justify-center" @click="handleClick"
        @touchstart.passive="handleTouchStart" @touchmove.passive="handleTouchMove" @touchend="handleTouchEnd">
        <Transition name="slide" mode="out-in">
          <div :key="currentImageSrc" class="flex items-center justify-center w-full h-full">
            <NuxtImg v-if="currentImageSrc" :src="currentImageSrc" class="max-w-full max-h-screen object-contain"
              @load="isLoading = false" />
            <Transition name="fade">
              <div v-show="!isTouchDevice && showInfoTrigger && !showInfo"
                class="absolute bottom-0 left-0 right-0 h-1/10 bg-gradient-to-t from-black/70 to-transparent transition-opacity duration-300">
              </div>
            </Transition>

            <Transition name="fade-scale">
              <div v-show="(isTouchDevice || (!isTouchDevice && showInfoTrigger)) && !showInfo"
                class="absolute bottom-6 left-1/2 transform -translate-x-1/2 cursor-pointer flex items-center bg-black/50 px-4 py-2 rounded-full"
                @click="handleInfoToggleClick" ref="infoToggleRef">
                <Icon name="i-heroicons-information-circle" class="text-2xl text-white mr-2" />
                <span class="text-white">Info</span>
              </div>
            </Transition>

            <Transition name="slide-up">
              <div v-show="showInfo"
                class="absolute bottom-0 left-1/2 transform -translate-x-1/2 bg-[rgba(0,0,0,0.6)] text-[rgba(255,255,255,0.8)] transition-all duration-300 rounded-t-xl max-w-[600px] w-full mx-auto"
                :class="{ 'h-auto': showInfo }" ref="infoRef">
                <UCard class="bg-transparent ring-0 px-4 pt-4 sm:px-6 sm:pt-6 z-[100]" :ui="{ body: 'p-0 sm:p-0' }">
                  <div class="flex justify-between items-center mb-2">
                    <div class="text-xl font-bold">Info</div>
                    <Icon name="i-heroicons-x-mark" class="text-xl text-white cursor-pointer" @click="toggleInfo" />
                  </div>
                  <div class="overflow-y-scroll max-h-[65vh] sm:max-h-[90vh] info-scroll-bar">
                    <div v-for="(obj, category) in exifData" :key="category" class=" mb-2">
                      <div class="text-md font-bold uppercase">{{ category }}</div>
                      <div v-for="(v, k) in obj" :key="k">
                        <div class="text-sm text-gray-300">
                          <span class="font-bold">{{ k }}:</span> {{ v }}
                        </div>
                      </div>
                    </div>
                  </div>
                </UCard>
              </div>
            </Transition>
          </div>
        </Transition>

        <div v-show="hasPrevious && !isLoading && !showInfo"
          class="absolute left-0 top-0 bottom-0 w-1/5 sm:w-1/10 cursor-pointer flex items-center justify-start pl-4 sm:pl-8 opacity-50 hover:opacity-100 transition-opacity duration-300 group z-10"
          @click.stop="prevImage">
          <Icon name="i-heroicons-arrow-left" class="text-3xl sm:text-2xl text-white" />
        </div>

        <div v-show="hasNext && !isLoading && !showInfo"
          class="absolute right-0 top-0 bottom-0 w-1/5 sm:w-1/10 cursor-pointer flex items-center justify-end pr-4 sm:pr-8 opacity-50 hover:opacity-100 transition-opacity duration-300 group z-10"
          @click.stop="nextImage">
          <Icon name="i-heroicons-arrow-right" class="text-3xl sm:text-2xl text-white" />
        </div>

        <div class="absolute top-4 right-4 flex space-x-2 z-10">
          <Icon name="i-heroicons-x-mark" class="text-3xl text-white cursor-pointer" @click="closeViewer" />
        </div>

        <div class="hidden">
          <NuxtImg v-if="preloadSrc" :src="preloadSrc" @load="handlePreloadComplete" />
        </div>
      </div>
    </div>
  </Transition>
</template>
<script setup lang="ts">
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

const show = defineModel<boolean>();

const emit = defineEmits(['update:modelValue']);

// 状态管理
const currentImageSrc = ref(props.initialImageSrc);
const preloadSrc = ref('');
const isLoading = ref(true);
const showInfoTrigger = ref(false); // 控制Info图标显示 (非触屏)
const showInfo = ref(false); // 控制信息面板显示
const mouseY = ref(0);
const currentIndex = ref(props.initialIndex);
const hasPrevious = ref(false);
const hasNext = ref(false);
const exifData = ref({});
const viewerRef = useTemplateRef('viewerRef');
const infoRef = useTemplateRef('infoRef');
const infoToggleRef = useTemplateRef('infoToggleRef');

// --- 触屏相关状态 ---
const isTouchDevice = ref(false); // 是否为触屏设备
const touchStartX = ref(0);       // 触摸起始 X 坐标
const touchStartY = ref(0);       // 触摸起始 Y 坐标
const touchMoveX = ref(0);        // 触摸移动 X 坐标 (实时更新，用于结束时判断)
const touchMoveY = ref(0);        // 触摸移动 Y 坐标 (实时更新)
const swipeThresholdY = 50;       // 触发 *垂直* 滑动的最小距离 (像素) - 用于显示 Info
const swipeThresholdX = 75;       // 触发 *水平* 滑动的最小距离 (像素) - 用于切换图片
const isSwiping = ref(false);     // 标记是否正在进行滑动操作

// 鼠标移动处理 (仅非触屏设备)
const handleMouseMove = (e: MouseEvent) => {
  if (isTouchDevice.value || !viewerRef.value) return;

  const rect = (viewerRef.value as HTMLElement).getBoundingClientRect();
  const height = rect.height;
  mouseY.value = e.clientY - rect.top;
  const infoTriggerZone = height * 0.9;
  showInfoTrigger.value = mouseY.value > infoTriggerZone;
};

// 切换信息面板显示
const toggleInfo = () => {
  showInfo.value = !showInfo.value;
};

// Info 按钮点击处理 (仅非触屏)
const handleInfoToggleClick = (e: MouseEvent) => {
  if (isTouchDevice.value) return;
  e.stopPropagation();
  toggleInfo();
};

// --- 触屏事件处理 ---
const handleTouchStart = (e: TouchEvent) => {
  if (e.touches.length === 1) {
    touchStartX.value = e.touches[0].clientX;
    touchStartY.value = e.touches[0].clientY;
    touchMoveX.value = touchStartX.value; // 初始化 Move 坐标
    touchMoveY.value = touchStartY.value; // 初始化 Move 坐标
    isSwiping.value = false; // 重置滑动状态
  }
};

const handleTouchMove = (e: TouchEvent) => {
  if (e.touches.length === 1) {
    const currentX = e.touches[0].clientX;
    const currentY = e.touches[0].clientY;
    const deltaX = Math.abs(currentX - touchStartX.value);
    const deltaY = Math.abs(currentY - touchStartY.value);

    // 标记正在滑动，这样可以阻止 touchend 中的 tap 行为（如果需要）
    // 只有当移动超过一定小距离才判定为滑动开始，避免误触
    if (deltaX > 10 || deltaY > 10) {
      isSwiping.value = true;
    }

    touchMoveX.value = currentX;
    touchMoveY.value = currentY;
  }
};

const handleTouchEnd = () => {
  if (!isSwiping.value) { // 如果不是滑动（可能是点击），则不处理滑动逻辑
    // 如果需要处理点击逻辑，可以在这里添加，但目前 handleClick 已经处理
    return;
  }

  const deltaX = touchStartX.value - touchMoveX.value; // 正值表示向左滑 (Previous)
  const deltaY = touchStartY.value - touchMoveY.value; // 正值表示向上滑 (Show Info)
  const absDeltaX = Math.abs(deltaX);
  const absDeltaY = Math.abs(deltaY);

  // --- 判断滑动方向和意图 ---
  // 优先判断水平滑动 (切换图片)，且 Info 面板未显示
  if (absDeltaX > absDeltaY && absDeltaX > swipeThresholdX && !showInfo.value) {
    if (deltaX < 0) {
      // 向左滑动超过阈值 -> 上一张
      prevImage();
    } else {
      // 向右滑动超过阈值 -> 下一张
      nextImage();
    }
  }
  // 其次判断垂直向上滑动 (显示 Info)，且 Info 面板未显示
  else if (absDeltaY > absDeltaX && deltaY > swipeThresholdY && !showInfo.value) {
    // 向上滑动超过阈值 -> 显示 Info
    showInfo.value = true;
  }
  // 如果是向下滑动，可以考虑用于关闭 Info (可选)
  else if (absDeltaY > absDeltaX && deltaY < -swipeThresholdY && showInfo.value) {
    showInfo.value = false;
  }

  // 重置状态
  isSwiping.value = false;
  touchStartX.value = 0;
  touchStartY.value = 0;
  touchMoveX.value = 0;
  touchMoveY.value = 0;
};
// --- 结束新增触屏事件处理 ---

// 点击空白区域或图片本身的处理
const handleClick = (e: MouseEvent) => {
  // 如果正在滑动，则忽略点击事件
  if (isSwiping.value) return;

  const target = e.target as HTMLElement;
  const infoPanel = infoRef.value as HTMLElement | null;
  const isClickInsideInfo = infoPanel && infoPanel.contains(target);
  const isClickOnNav = target.closest('.absolute.left-0') || target.closest('.absolute.right-0');
  const isClickOnClose = target.closest('.absolute.top-4.right-4');

  // 如果 Info 面板是打开的，并且点击发生在 Info 面板、导航按钮、关闭按钮之外，则关闭 Info 面板
  if (showInfo.value && !isClickInsideInfo && !isClickOnNav && !isClickOnClose) {
    showInfo.value = false;
  }
};


// 键盘导航 (保持不变)
const handleKeydown = (e: KeyboardEvent) => {
  if (!show.value) return;
  // Info 显示时，只允许 Esc 和 i (非触屏)
  if (showInfo.value) {
    if (e.key === 'Escape') {
      e.preventDefault();
      showInfo.value = false; // Esc 关闭 Info 面板优先
    } else if (e.key === 'i' && !isTouchDevice.value) {
      e.preventDefault();
      toggleInfo();
    }
    return; // 阻止其他键盘事件如左右箭头
  }

  // Info 未显示时的键盘导航
  if (e.key === 'ArrowLeft') {
    e.preventDefault();
    prevImage();
  } else if (e.key === 'ArrowRight') {
    e.preventDefault();
    nextImage();
  } else if (e.key === 'Escape') {
    e.preventDefault();
    closeViewer();
  } else if (e.key === 'i' && !isTouchDevice.value) {
    e.preventDefault();
    toggleInfo();
  }
};

// 图片导航
const prevImage = () => {
  if (!hasPrevious.value || showInfo.value) return; // Info 显示时不允许切换

  isLoading.value = true; // 切换时显示加载状态
  const prevSrc = props.previousPhoto(currentIndex.value);
  if (prevSrc) {
    currentImageSrc.value = prevSrc;
    currentIndex.value--;
    updateNavState();
    preloadNextImage();
    nextTick(refocusViewer);
  } else {
    isLoading.value = false; // 如果没有上一张，取消加载状态
  }
};

const nextImage = () => {
  if (!hasNext.value || showInfo.value) return; // Info 显示时不允许切换

  isLoading.value = true; // 切换时显示加载状态
  const nextSrc = props.nextPhoto(currentIndex.value);
  if (nextSrc) {
    currentImageSrc.value = nextSrc;
    currentIndex.value++;
    updateNavState();
    preloadNextImage();
    nextTick(refocusViewer);
  } else {
    isLoading.value = false; // 如果没有下一张，取消加载状态
  }
};

// 预加载下一张图片 (保持不变)
const preloadNextImage = () => {
  const nextSrc = props.nextPhoto(currentIndex.value);
  if (nextSrc) {
    preloadSrc.value = nextSrc;
  } else {
    preloadSrc.value = ''; // 如果没有下一张，清空预加载
  }
};

const handlePreloadComplete = () => {
  // console.log('Next image preloaded');
};

// 重新聚焦 (保持不变)
const refocusViewer = () => {
  if (viewerRef.value) {
    (viewerRef.value as HTMLElement).focus();
  }
};

// 关闭查看器 (保持不变)
const closeViewer = () => {
  show.value = false;
};

// 更新导航状态
const updateNavState = async () => {
  try {
    exifData.value = await parseExifCategories(currentImageSrc.value);
  } catch (error) {
    console.error("Error parsing EXIF data:", error);
    exifData.value = { '错误': { '信息': '无法加载图片数据' } };
  }

  const prevSrc = props.previousPhoto(currentIndex.value);
  const nextSrc = props.nextPhoto(currentIndex.value);

  hasPrevious.value = !!prevSrc;
  hasNext.value = !!nextSrc;
};

// 生命周期钩子
onMounted(() => {
  isTouchDevice.value = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  if (viewerRef.value) {
    refocusViewer();
    if (!isTouchDevice.value) {
      window.addEventListener('mousemove', handleMouseMove);
    }
    // 注意：触摸事件已绑定在模板中的目标元素上，无需在此处通过 window 添加
  }

  // 初始加载时获取状态
  if (show.value) {
    isLoading.value = true;
    currentImageSrc.value = props.initialImageSrc;
    currentIndex.value = props.initialIndex;
    updateNavState().then(() => {
      // 可以在 EXIF 加载后或图片加载后设置 isLoading 为 false
      // isLoading.value = false; // 移到 NuxtImg 的 @load 事件处理
    });
    preloadNextImage();
    nextTick(refocusViewer);
  }
});

onBeforeUnmount(() => {
  if (!isTouchDevice.value) {
    window.removeEventListener('mousemove', handleMouseMove);
  }
  // 触摸事件监听器会随组件卸载自动移除
});

// 监听 show 变化
watch(() => show.value, (newVal, oldVal) => {
  if (newVal && !oldVal) { // 仅在从 false 变为 true 时执行初始化逻辑
    isLoading.value = true; // 打开时总是显示加载，直到图片加载完成
    currentImageSrc.value = props.initialImageSrc;
    currentIndex.value = props.initialIndex;
    showInfo.value = false; // 每次打开都确保 info 是关闭的
    updateNavState(); // 更新导航和 EXIF
    preloadNextImage(); // 预加载
    nextTick(refocusViewer); // 获取焦点
  } else if (!newVal) {
    // 可选：关闭时重置一些状态
    preloadSrc.value = ''; // 清空预加载
  }
});

// 监听图片源变化，确保加载状态正确并关闭Info
watch(currentImageSrc, (newSrc, oldSrc) => {
  if (newSrc !== oldSrc && show.value) { // 只有在 viewer 显示时才响应图片切换
    isLoading.value = true; // 图片源变化时，设置加载中
    showInfo.value = false; // 切换图片时自动隐藏 Info
    // updateNavState 和 preloadNextImage 已在 prevImage/nextImage 中调用
  }
});

// NuxtImg 的 @load 事件会设置 isLoading = false
</script>

<style scoped>
/* 样式保持不变 */
.info-scroll-bar::-webkit-scrollbar {
  width: 6px;
}

.info-scroll-bar::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
}

.info-scroll-bar::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0);
  border-radius: 4px;
}


.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  transform: translateY(10px) scale(0.95);
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

/* 确保 slide-up 动画从底部完全隐藏开始 */
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0.8;
  /* 可以调整离开时的透明度 */
}

.slide-up-enter-to,
.slide-up-leave-from {
  transform: translateY(0);
  opacity: 1;
}
</style>