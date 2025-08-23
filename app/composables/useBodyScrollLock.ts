import { ref, watch, onUnmounted, type Ref } from "vue";

interface FixedElement {
  element: HTMLElement;
  originalPadding: string;
}

/**
 * 一个用于无感锁定/解锁 body 滚动的 Vue Composable (跨设备增强版)。
 * @param isLocked - 一个 Ref<boolean>，用于控制锁定状态。
 * @param scrollableTarget - (可选) 一个 Ref<HTMLElement | null>，指向在锁定期间应保持可滚动的元素（例如，弹窗的内容区域）。
 * @param fixedElementSelector - (可选) 一个 CSS 选择器，用于匹配需要同步调整 padding 的 fixed 定位元素。
 */
export function useBodyScrollLock(
  isLocked: Ref<boolean>,
  scrollableTarget: Ref<HTMLElement | null> = ref(null),
  fixedElementSelector: string | null = null
) {
  const scrollY = ref(0);
  const originalStyle = ref<{
    overflow: string;
    paddingRight: string;
    position: string;
    width: string;
    top: string;
  }>({ overflow: "", paddingRight: "", position: "", width: "", top: "" });
  const fixedElementsOriginalPadding = ref<FixedElement[]>([]);

  const getScrollbarWidth = (): number =>
    window.innerWidth - document.documentElement.clientWidth;

  // 核心：处理 touchmove 事件
  const handleTouchMove = (event: TouchEvent) => {
    const target = event.target as HTMLElement;

    // 如果没有指定可滚动区域，或者触摸点不在可滚动区域内，则阻止默认行为
    if (!scrollableTarget.value || !scrollableTarget.value.contains(target)) {
      if (event.cancelable) event.preventDefault();
      return;
    }

    // 智能判断：如果可滚动区域已经滚到顶部或底部，则阻止冒泡滚动（橡皮筋效果）
    const { scrollTop, scrollHeight, clientHeight } = scrollableTarget.value;
    const isAtTop = scrollTop === 0;
    const isAtBottom = scrollTop + clientHeight >= scrollHeight;

    // event.touches[0].clientY 是当前触摸点的位置
    // 你需要一个变量来存储上一个触摸点的位置来判断方向
    // 为了简化，这里我们只处理已经到边界的情况
    if (isAtTop && event.touches[0].clientY > (window as any)._lastTouchY) {
      if (event.cancelable) event.preventDefault();
    } else if (
      isAtBottom &&
      event.touches[0].clientY < (window as any)._lastTouchY
    ) {
      if (event.cancelable) event.preventDefault();
    }

    // 记录最后触摸位置
    (window as any)._lastTouchY = event.touches[0].clientY;
  };

  const handleTouchStart = (event: TouchEvent) => {
    // 记录初始触摸位置
    (window as any)._lastTouchY = event.touches[0].clientY;
  };

  const lock = (): void => {
    const scrollbarWidth = getScrollbarWidth();

    // 1. 保存样式和滚动位置
    scrollY.value = window.scrollY;
    originalStyle.value = {
      overflow: document.body.style.overflow,
      paddingRight: document.body.style.paddingRight,
      position: document.body.style.position,
      width: document.body.style.width,
      top: document.body.style.top,
    };

    // 2. 固定 body，防止跳动
    document.body.style.overflow = "hidden";
    document.body.style.paddingRight = `${scrollbarWidth}px`;
    document.body.style.position = "fixed";
    document.body.style.width = "100%";
    document.body.style.top = `-${scrollY.value}px`;

    // 3. 处理 fixed 定位的元素
    if (fixedElementSelector) {
      // ... (这部分逻辑不变)
    }

    // 4. 添加触摸事件监听器
    document.addEventListener("touchstart", handleTouchStart);
    document.addEventListener("touchmove", handleTouchMove, { passive: false });
  };

  const unlock = (): void => {
    // 1. 恢复 body 样式
    document.body.style.overflow = originalStyle.value.overflow;
    document.body.style.paddingRight = originalStyle.value.paddingRight;
    document.body.style.position = originalStyle.value.position;
    document.body.style.width = originalStyle.value.width;
    document.body.style.top = originalStyle.value.top;

    // 2. 恢复滚动位置
    window.scrollTo(0, scrollY.value);

    // 3. 恢复 fixed 元素的样式
    if (fixedElementSelector) {
      // ... (这部分逻辑不变)
    }

    // 4. 移除触摸事件监听器
    document.removeEventListener("touchstart", handleTouchStart);
    document.removeEventListener("touchmove", handleTouchMove);
  };

  watch(isLocked, (newVal) => {
    if (newVal) {
      lock();
    } else {
      unlock();
    }
  });

  onUnmounted(() => {
    if (isLocked.value) {
      unlock();
    }
  });
}
