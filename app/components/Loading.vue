<template>
  <div v-if="visible" :class="[
    'loading-container',
    overlay ? 'loading-overlay' : '',
    fullscreen ? 'loading-fullscreen' : ''
  ]" :style="containerStyle">
    <!-- 默认旋转圆圈动画 -->
    <div v-if="type === 'spinner'" class="loading-spinner">
      <div class="spinner-ring"></div>
    </div>

    <!-- 脉冲点动画 -->
    <div v-else-if="type === 'dots'" class="loading-dots">
      <div class="dot" v-for="i in 3" :key="i"></div>
    </div>

    <!-- 波浪动画 -->
    <div v-else-if="type === 'wave'" class="loading-wave">
      <div class="wave-bar" v-for="i in 5" :key="i"></div>
    </div>

    <!-- 渐变圆环动画 -->
    <div v-else-if="type === 'gradient'" class="loading-gradient">
      <div class="gradient-ring"></div>
    </div>

    <!-- 加载文本 -->
    <div v-if="text" class="loading-text">{{ text }}</div>
  </div>
</template>

<script>
export default {
  name: 'LoadingComponent',
  props: {
    // 是否显示加载动画
    visible: {
      type: Boolean,
      default: true
    },
    // 动画类型：spinner, dots, wave, gradient
    type: {
      type: String,
      default: 'spinner',
      validator: value => ['spinner', 'dots', 'wave', 'gradient'].includes(value)
    },
    // 是否显示遮罩层
    overlay: {
      type: Boolean,
      default: true
    },
    // 是否全屏显示
    fullscreen: {
      type: Boolean,
      default: false
    },
    // 加载文本
    text: {
      type: String,
      default: ''
    },
    // 主题色
    color: {
      type: String,
      default: '#409EFF'
    },
    // 大小
    size: {
      type: String,
      default: 'medium',
      validator: value => ['small', 'medium', 'large'].includes(value)
    }
  },
  computed: {
    containerStyle() {
      const sizeMap = {
        small: '24px',
        medium: '40px',
        large: '56px'
      };

      return {
        '--loading-color': this.color,
        '--loading-size': sizeMap[this.size]
      };
    }
  }
}
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 20px;
  box-sizing: border-box;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(2px);
  z-index: 1000;
}

.loading-fullscreen {
  width: 100vw;
  height: 100vh;
}

/* 旋转圆圈动画 */
.loading-spinner {
  width: var(--loading-size);
  height: var(--loading-size);
}

.spinner-ring {
  width: 100%;
  height: 100%;
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--loading-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* 脉冲点动画 */
.loading-dots {
  display: flex;
  gap: 8px;
  align-items: center;
}

.dot {
  width: calc(var(--loading-size) / 4);
  height: calc(var(--loading-size) / 4);
  background: var(--loading-color);
  border-radius: 50%;
  animation: pulse 1.4s ease-in-out infinite both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

.dot:nth-child(3) {
  animation-delay: 0s;
}

@keyframes pulse {

  0%,
  80%,
  100% {
    transform: scale(0.6);
    opacity: 0.5;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 波浪动画 */
.loading-wave {
  display: flex;
  gap: 4px;
  align-items: end;
  height: var(--loading-size);
}

.wave-bar {
  width: calc(var(--loading-size) / 8);
  height: 20%;
  background: var(--loading-color);
  border-radius: 2px;
  animation: wave 1.2s ease-in-out infinite;
}

.wave-bar:nth-child(1) {
  animation-delay: -0.4s;
}

.wave-bar:nth-child(2) {
  animation-delay: -0.3s;
}

.wave-bar:nth-child(3) {
  animation-delay: -0.2s;
}

.wave-bar:nth-child(4) {
  animation-delay: -0.1s;
}

.wave-bar:nth-child(5) {
  animation-delay: 0s;
}

@keyframes wave {

  0%,
  40%,
  100% {
    height: 20%;
  }

  20% {
    height: 100%;
  }
}

/* 渐变圆环动画 */
.loading-gradient {
  width: var(--loading-size);
  height: var(--loading-size);
}

.gradient-ring {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: conic-gradient(from 0deg,
      transparent 0deg,
      var(--loading-color) 60deg,
      transparent 120deg);
  animation: rotate 1s linear infinite;
  mask: radial-gradient(circle at center, transparent 60%, black 65%);
  -webkit-mask: radial-gradient(circle at center, transparent 60%, black 65%);
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* 加载文本 */
.loading-text {
  color: #666;
  font-size: 14px;
  font-weight: 500;
  text-align: center;
  margin-top: 8px;
  animation: fadeInOut 2s ease-in-out infinite;
}

@keyframes fadeInOut {

  0%,
  100% {
    opacity: 0.6;
  }

  50% {
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .loading-container {
    padding: 16px;
  }

  .loading-text {
    font-size: 12px;
  }
}

/* 深色主题支持 */
@media (prefers-color-scheme: dark) {
  .loading-overlay {
    background: rgba(0, 0, 0, 0.9);
  }

  .loading-text {
    color: #ccc;
  }

  .spinner-ring {
    border-color: #333;
    border-top-color: var(--loading-color);
  }
}
</style>