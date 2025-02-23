<template>
  <div class="flex h-[100vh]">
    <div class="">
      <Nav />
    </div>
    <div class="grow overflow-y-scroll overflow-x-hidden">
      <slot />
    </div>
  </div>
</template>

<script lang="ts" setup>
</script>

<style></style>