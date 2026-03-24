<template>
  <button class="news-card surface-card" type="button" @click="openDetail">
    <div v-if="hasMedia" class="news-image">
      <MediaAsset
        :media-type="item.media_type || 'image'"
        :image-url="item.cover_image"
        :video-url="item.video_url"
        :alt="item.title"
        :controls="false"
        wrapper-class="news-media-wrap"
        element-class="news-media"
      />
    </div>
    <div class="news-content">
      <p class="news-date">{{ formatDate(item.published_at) }}</p>
      <h3>{{ item.title }}</h3>
      <p v-if="item.summary" class="news-summary">{{ item.summary }}</p>
    </div>
  </button>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

import MediaAsset from "./MediaAsset.vue";

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const router = useRouter();
const hasMedia = computed(() => Boolean(props.item.video_url || props.item.cover_image));

const formatDate = (value) => {
  if (!value) return "";
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(value));
};

const openDetail = async () => {
  await router.push({ name: "news-detail", params: { id: props.item.id } });
};
</script>

<style scoped>
.news-card {
  width: 100%;
  overflow: hidden;
  padding: 0;
  text-align: left;
  border: 1px solid var(--color-border);
  cursor: pointer;
}

.news-image {
  aspect-ratio: 1.4 / 1;
  overflow: hidden;
}

.news-media-wrap,
.news-media {
  width: 100%;
  height: 100%;
}

.news-content {
  padding: 22px;
}

.news-date {
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

.news-summary {
  margin: 16px 0 0;
  color: var(--color-text-soft);
  line-height: 1.8;
}
</style>
