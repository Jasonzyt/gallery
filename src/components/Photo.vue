<template>
  <div class="shadow-md hover:shadow-xl transition-shadow rounded-xl relative" @mouseenter="isHovering = true"
    @mouseleave="isHovering = false" @click="$emit('click')">
    <NuxtImg :src="src" :alt="alt" ref="img" class="size-full object-cover rounded-xl z-0" />
    <p v-if="description.length !== 0"
      class="absolute w-full mt-[-3rem] py-3 px-4 rounded-b-xl text-gray-100 transition-opacity duration-300 z-10"
      :class="isHovering ? 'opacity-100' : 'opacity-0'">
      {{ description }}
    </p>
  </div>
</template>

<script lang="ts" setup>
import exifr from 'exifr';

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  alt: {
    type: String,
    default: ""
  }
})

const emits = defineEmits(['click'])

const isHovering = ref(false)
const description = ref("")

onMounted(async () => {
  const exif = await exifr.parse(props.src)
  console.log(exif)
  description.value = exif?.ImageDescription || ""
})

</script>

<style scoped>
p {
  background: linear-gradient(0deg, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0));
}
</style>