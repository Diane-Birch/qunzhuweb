<template>
  <div class="detail-page section-space">
    <div class="page-shell">
      <div v-if="loading" class="surface-card detail-loading">
        <el-skeleton animated :rows="10" />
      </div>

      <div v-else-if="product" class="detail-layout">
        <button class="detail-back" type="button" @click="goBackHome">返回产品区</button>

        <article class="surface-card detail-article">
          <SectionHeading :title="product.name" :subtitle="product.subtitle" :description="product.description" />

          <div v-if="hasMedia" class="detail-media-wrap">
            <MediaAsset
              :media-type="product.media_type || 'image'"
              :image-url="product.cover_image"
              :video-url="product.video_url"
              :alt="product.name"
              :controls="(product.media_type || 'image') === 'video'"
              wrapper-class="detail-media-shell"
              element-class="detail-media"
            />
          </div>

          <dl v-if="specList.length" class="detail-specs">
            <div v-for="spec in specList" :key="spec.label">
              <dt>{{ spec.label }}</dt>
              <dd>{{ spec.value }}</dd>
            </div>
          </dl>
        </article>
      </div>

      <div v-else class="surface-card detail-empty">
        <el-empty description="未找到该产品" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { useRoute, useRouter } from "vue-router";

import { fetchProductDetail } from "../api/content";
import MediaAsset from "../components/MediaAsset.vue";
import SectionHeading from "../components/SectionHeading.vue";

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const product = ref(null);

const hasMedia = computed(() => Boolean(product.value?.cover_image || product.value?.video_url));
const specList = computed(() => {
  try {
    const raw = JSON.parse(product.value?.specs_json || "{}");
    return Object.entries(raw).map(([label, value]) => ({ label, value }));
  } catch (error) {
    return [];
  }
});

const loadProduct = async (id) => {
  if (!id) {
    product.value = null;
    return;
  }

  loading.value = true;
  try {
    product.value = await fetchProductDetail(id);
  } catch (error) {
    product.value = null;
    ElMessage.error(error.response?.data?.detail || "产品详情加载失败");
  } finally {
    loading.value = false;
  }
};

const goBackHome = async () => {
  await router.push({ path: "/", hash: "#products" });
};

watch(
  () => route.params.id,
  (value) => {
    loadProduct(value);
  },
  { immediate: true }
);
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
}

.detail-layout {
  display: grid;
  gap: 18px;
}

.detail-back {
  width: fit-content;
  padding: 12px 20px;
  border: none;
  border-radius: 999px;
  background: rgba(141, 79, 42, 0.14);
  color: var(--color-primary-deep);
  cursor: pointer;
  transition: transform 0.24s ease, background-color 0.24s ease;
}

.detail-back:hover {
  background: rgba(141, 79, 42, 0.2);
  transform: translateY(-1px);
}

.detail-article,
.detail-loading,
.detail-empty {
  padding: 28px;
}

.detail-media-wrap {
  overflow: hidden;
  border-radius: 28px;
  margin-bottom: 28px;
}

.detail-media-shell,
.detail-media {
  width: 100%;
  min-height: 360px;
}

.detail-specs {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.detail-specs div {
  padding: 18px 20px;
  border-radius: 18px;
  background: var(--color-surface-strong);
}

.detail-specs dt {
  color: var(--color-text-soft);
  font-size: 13px;
}

.detail-specs dd {
  margin: 8px 0 0;
  font-weight: 600;
  color: var(--color-primary-deep);
}

@media (max-width: 768px) {
  .detail-article,
  .detail-loading,
  .detail-empty {
    padding: 20px;
  }

  .detail-media-shell,
  .detail-media {
    min-height: 220px;
  }

  .detail-specs {
    grid-template-columns: 1fr;
  }
}
</style>
