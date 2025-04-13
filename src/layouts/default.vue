<template>
  <div class="flex h-[100vh]">
    <div class="fixed z-20">
      <Nav />
    </div>
    <div class="sm:w-[15vw] flex-none"></div>
    <div class="grow p-2 sm:p-0">
      <slot />
    </div>
  </div>
</template>

<script lang="ts" setup>
</script>

<style></style>