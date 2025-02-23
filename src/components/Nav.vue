<template>
  <div class="w-48 min-h-full px-2 border-r-2 border-gray-200">
    <h2 class="px-4 pt-4 pb-2.5">Gallery</h2>
    <UNavigationMenu :items="links" orientation="vertical"
      :ui="{ root: 'size-full', item: 'text-xl', link: 'py-2.5 px-4', linkLeadingIcon: 'text-xl' }">
    </UNavigationMenu>
  </div>
</template>

<script setup lang="ts">
const links = ref([
  [],
  [
    {
      label: "Photo",
      icon: "i-lucide-image",
      to: "/photo"
    },
    {
      label: "Album",
      icon: "i-ic-baseline-burst-mode",
    },
    {
      label: "Timeline",
      icon: "i-material-symbols-timer-play-outline",
      disabled: true
    }
  ],
  [
    {
      label: "GitHub",
      icon: "i-uil-github",
      to: "https://github.com/Jasonzyt/gallery",
      target: '_blank'
    },
    {
      label: "Blog",
      icon: 'i-my-campu-icon',
      to: "https://jasonz.yt",
      target: "_blank"
    }
  ]
])
</script>