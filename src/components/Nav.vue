<template>
  <div class="w-[15vw] min-h-full pt-2 pb-4 pl-4 pr-2 border-r-2 border-gray-200 max-sm:hidden flex flex-col">
    <h2 class="px-4 pt-4 pb-2.5 text-[2xl]">
      <Icon name="my:gallery" size="1.4em" class="align-text-bottom mr-2" />Gallery
    </h2>
    <USeparator class="my-2" />
    <UNavigationMenu :items="links" orientation="vertical"
      :ui="{ root: 'size-full', link: 'py-2.5 px-[8%] text-[1.1rem]', linkLeadingIcon: 'text-xl mr-1' }">
    </UNavigationMenu>
    <div class="grow"></div>
    <USeparator class="my-2" />
    <UNavigationMenu :items="linksBottom" orientation="vertical"
      :ui="{ root: 'size-full', link: 'py-2.5 px-[8%] text-[1.1rem]', linkLeadingIcon: 'text-xl mr-1' }">
    </UNavigationMenu>
  </div>
</template>

<script setup lang="ts">
const links = ref([
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
])

const linksBottom = ref([
  {
    label: "GitHub",
    icon: "i-uil-github",
    to: "https://github.com/Jasonzyt/gallery",
    target: '_blank'
  },
  {
    label: "Blog",
    icon: "i-my-campu-icon",
    to: "https://jasonz.yt",
    target: "_blank",
  }
])

</script>