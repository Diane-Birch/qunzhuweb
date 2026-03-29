<template>
  <div v-if="hasRenderableMedia" class="media-asset" :class="[{ 'is-hoverable': hoverable && resolvedMediaType === 'image' }, wrapperClass]">
    <video
      v-if="resolvedMediaType === 'video' && videoUrl"
      class="media-element"
      :class="elementClass"
      :src="videoUrl"
      :autoplay="autoplay"
      :muted="muted"
      :loop="loop"
      :controls="controls"
      playsinline
      preload="metadata"
    />
    <img v-else-if="imageUrl" class="media-element" :class="elementClass" :src="imageUrl" :alt="alt" />
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  mediaType: {
    type: String,
    default: "image",
  },
  imageUrl: {
    type: String,
    default: "",
  },
  videoUrl: {
    type: String,
    default: "",
  },
  alt: {
    type: String,
    default: "",
  },
  autoplay: {
    type: Boolean,
    default: false,
  },
  muted: {
    type: Boolean,
    default: false,
  },
  loop: {
    type: Boolean,
    default: false,
  },
  controls: {
    type: Boolean,
    default: true,
  },
  hoverable: {
    type: Boolean,
    default: true,
  },
  wrapperClass: {
    type: [String, Array, Object],
    default: "",
  },
  elementClass: {
    type: [String, Array, Object],
    default: "",
  },
});

const resolvedMediaType = computed(() => (props.mediaType === "video" && props.videoUrl ? "video" : "image"));
const hasRenderableMedia = computed(() => Boolean((resolvedMediaType.value === "video" && props.videoUrl) || props.imageUrl));
</script>

<style scoped>
.media-asset {
  width: 100%;
  height: 100%;
}

.media-element {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.38s ease, filter 0.38s ease;
  transform-origin: center center;
}

.is-hoverable:hover .media-element {
  transform: scale(1.08);
  filter: saturate(1.02);
}
</style>
