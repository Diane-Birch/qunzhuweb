<template>
  <article class="news-card surface-card">
    <div v-if="item.cover_image" class="news-image">
      <img :src="item.cover_image" :alt="item.title" />
    </div>
    <div class="news-content">
      <p class="news-date">{{ formatDate(item.published_at) }}</p>
      <h3>{{ item.title }}</h3>
      <p v-if="item.summary" class="news-summary">{{ item.summary }}</p>
    </div>
  </article>
</template>

<script setup>
const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const formatDate = (value) => {
  if (!value) return "";
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(value));
};
</script>

<style scoped>
.news-card {
  overflow: hidden;
}

.news-image {
  aspect-ratio: 1.4 / 1;
  overflow: hidden;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
