<template>
  <article class="product-card surface-card">
    <div v-if="hasMedia" class="product-image">
      <MediaAsset
        :media-type="item.media_type || 'image'"
        :image-url="item.cover_image"
        :video-url="item.video_url"
        :alt="item.name"
        :controls="(item.media_type || 'image') === 'video'"
        wrapper-class="product-media-wrap"
        element-class="product-media"
      />
    </div>
    <div class="product-content">
      <p v-if="item.subtitle" class="product-subtitle">{{ item.subtitle }}</p>
      <h3>{{ item.name }}</h3>
      <p v-if="item.description" class="product-description">{{ item.description }}</p>
      <dl v-if="specList.length" class="product-specs">
        <div v-for="spec in specList" :key="spec.label">
          <dt>{{ spec.label }}</dt>
          <dd>{{ spec.value }}</dd>
        </div>
      </dl>
    </div>
  </article>
</template>

<script setup>
import { computed } from "vue";

import MediaAsset from "./MediaAsset.vue";

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const hasMedia = computed(() => Boolean(props.item.video_url || props.item.cover_image));

const specList = computed(() => {
  try {
    const raw = JSON.parse(props.item.specs_json || "{}");
    return Object.entries(raw).map(([label, value]) => ({ label, value }));
  } catch (error) {
    return [];
  }
});
</script>

<style scoped>
.product-card {
  overflow: hidden;
}

.product-image {
  aspect-ratio: 1.25 / 1;
  overflow: hidden;
}

.product-media-wrap,
.product-media {
  width: 100%;
  height: 100%;
}

.product-content {
  padding: 24px;
}

.product-subtitle {
  margin: 0 0 10px;
  color: var(--color-secondary);
}

h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 28px;
}

.product-description {
  margin: 16px 0 0;
  color: var(--color-text-soft);
  line-height: 1.85;
}

.product-specs {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin: 24px 0 0;
}

.product-specs div {
  padding: 14px 16px;
  background: var(--color-surface-strong);
  border-radius: 16px;
}

.product-specs dt {
  color: var(--color-text-soft);
  font-size: 13px;
}

.product-specs dd {
  margin: 8px 0 0;
  font-weight: 600;
}

@media (max-width: 768px) {
  .product-specs {
    grid-template-columns: 1fr;
  }
}
</style>