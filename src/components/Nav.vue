<template>
  <div class="w-[15vw] min-h-full py-2 pl-4 pr-2 border-r-2 border-gray-200 max-sm:hidden">
    <h2 class="px-6 pt-4 pb-2.5 text-2xl">Gallery</h2>
    <UNavigationMenu :items="links" orientation="vertical"
      :ui="{ root: 'size-full', link: 'py-2.5 px-[8%] text-[1.1rem]', linkLeadingIcon: 'text-xl mr-1', separator: 'my-2' }">
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
      to: "/"
    },
    {
      label: "Album",
      icon: "i-ic-baseline-burst-mode",
    },
    {
      label: "Timeline",
      icon: "i-material-symbols-timer-play-outline",
      to: "/timeline",
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