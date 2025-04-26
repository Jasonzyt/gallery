<template>
  <!-- Main navigation container with responsive behavior -->
  <div class="relative h-full">
    <!-- Mobile menu toggle button - only visible on small screens -->
    <button @click="toggleMenu" v-show="!isMenuOpen"
      class="fixed top-4 left-4 z-30 bg-white rounded-md p-2 shadow-md hidden max-sm:flex items-center justify-center"
      aria-label="Toggle navigation menu">
      <Icon name="i-lucide-menu" size="1.4em" />
    </button>

    <!-- Backdrop overlay - only visible when menu is open on small screens -->
    <div v-show="isMenuOpen"
      class="fixed inset-0 bg-[rgba(0,0,0,0.3)] z-20 hidden max-sm:block transition-opacity duration-300 ease-in-out"
      :class="{ 'opacity-0': !isMenuOpen, 'opacity-100': isMenuOpen }" @click="closeMenuFromRightSide"
      @touchstart="handleTouchStart" @touchmove="handleTouchMove" @touchend="handleTouchEnd">
    </div>

    <!-- Navigation drawer - responsive for both desktop and mobile -->
    <div
      class="w-[15vw] min-h-full pt-2 pb-6 pl-2 pr-2 sm:pl-4 sm:border-r-2 border-gray-200 flex flex-col bg-white max-sm:fixed max-sm:left-0 max-sm:top-0 max-sm:bottom-0 max-sm:w-[80%] max-sm:z-20 max-sm:transform max-sm:transition-transform max-sm:duration-300 max-sm:ease-in-out"
      :class="isMenuOpen ? 'max-sm:translate-x-0' : 'max-sm:-translate-x-full'">
      <h2 class="px-4 pt-4 pb-2.5 text-2xl">
        <Icon name="my:gallery" size="1.4em" class="align-text-bottom mr-2" />Gallery
      </h2>
      <USeparator class="my-2" />
      <UNavigationMenu :items="links" orientation="vertical"
        :ui="{ root: 'w-full', link: 'py-2.5 px-[8%] text-[1.1rem]', linkLeadingIcon: 'text-xl mr-1' }">
      </UNavigationMenu>
      <div class="grow"></div>
      <USeparator class="my-2" />
      <UNavigationMenu :items="linksBottom" orientation="vertical"
        :ui="{ root: 'w-full', link: 'py-2.5 px-[8%] text-[1.1rem]', linkLeadingIcon: 'text-xl mr-1' }">
      </UNavigationMenu>
    </div>
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
    to: "/albums"
  },
  {
    label: "Timeline",
    icon: "i-material-symbols-timer-play-outline",
    // to: "/timeline",
    disabled: true
  }
]);

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
]);

// State management for responsive menu
const isMenuOpen = ref(false);
const touchStartX = ref(0);
const touchEndX = ref(0);

// Toggle menu state
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

// Close the menu if clicking on the right 10% of the screen when opened
const closeMenuFromRightSide = (event: MouseEvent) => {
  const screenWidth = window.innerWidth;
  const clickX = event.clientX;

  // If clicked in the right 10% of screen, close the menu
  if (clickX > screenWidth * 0.9) {
    isMenuOpen.value = false;
  }
};

// Touch gesture handlers for swipe to close
const handleTouchStart = (event: TouchEvent) => {
  touchStartX.value = event.touches[0].clientX;
};

const handleTouchMove = (event: TouchEvent) => {
  touchEndX.value = event.touches[0].clientX;
};

const handleTouchEnd = () => {
  // Calculate swipe distance
  const swipeDistance = touchStartX.value - touchEndX.value;
  const minSwipeDistance = 50; // Minimum distance for swipe to register

  // If swiped left with enough distance, close the menu
  if (swipeDistance > minSwipeDistance) {
    isMenuOpen.value = false;
  }

  // Reset values
  touchStartX.value = 0;
  touchEndX.value = 0;
};

watch(
  () => useRoute().path,
  (newPath, oldPath) => {
    // Close the menu when navigating to a new route
    if (isMenuOpen.value) {
      isMenuOpen.value = false;
    }
  },
  { immediate: true, deep: true }
)

</script>