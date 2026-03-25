<template>
  <button class="section-card surface-card" type="button" @click="openDetail">
    <div v-if="hasMedia" class="section-image">
      <MediaAsset
        :media-type="item.media_type || 'image'"
        :image-url="item.image_url"
        :video-url="item.video_url"
        :alt="item.title"
        :controls="false"
        wrapper-class="section-media-wrap"
        element-class="section-media"
      />
    </div>
    <div class="section-content">
      <p class="section-date">{{ formatDate(item.created_at) }}</p>
      <h3>{{ item.title }}</h3>
      <p v-if="summaryText" class="section-summary">{{ summaryText }}</p>
    </div>
  </button>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

import MediaAsset from "./MediaAsset.vue";
import { richTextToPlainText } from "../utils/richText";

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  detailQuery: {
    type: Object,
    default: () => ({}),
  },
});

const router = useRouter();
const hasMedia = computed(() => Boolean(props.item.video_url || props.item.image_url));
const summaryText = computed(() => props.item.summary || richTextToPlainText(props.item.body || ""));

const formatDate = (value) => {
  if (!value) {
    return "";
  }
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(value));
};

const openDetail = async () => {
  await router.push({ name: "section-detail", params: { key: props.item.key }, query: props.detailQuery });
};
</script>

<style scoped>
.section-card {
  width: 100%;
  overflow: hidden;
  padding: 0;
  text-align: left;
  border: 1px solid var(--color-border);
  cursor: pointer;
}

.section-image {
  aspect-ratio: 1.3 / 1;
  overflow: hidden;
}

.section-media-wrap,
.section-media {
  width: 100%;
  height: 100%;
}

.section-content {
  padding: 22px;
}

.section-date {
  margin: 0 0 10px;
  color: var(--color-secondary);
  font-size: 13px;
}

h3 {
  margin: 0;
  font-size: 24px;
  line-height: 1.4;
  font-family: var(--font-display);
}

.section-summary {
  margin: 16px 0 0;
  color: var(--color-text-soft);
  line-height: 1.8;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
