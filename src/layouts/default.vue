<template>
  <div class="flex flex-col sm:flex-row min-h-screen">
    <!-- 导航菜单 - 在大于sm屏幕时固定在左侧15%宽度 -->
    <div class="sm:w-[15vw] fixed top-0 left-0 h-screen z-20">
      <Nav />
    </div>

    <!-- 内容区域 - 在sm以上屏幕宽度时占85%并右移 -->
    <div class="sm:ml-[15vw] p-2 sm:p-0 min-h-screen">
      <slot />
    </div>
  </div>
</template>

<script lang="ts" setup>
</script>

<style>
#__nuxt,
#__layout {
  width: 100%;
  overflow-x: hidden;
}
</style>
