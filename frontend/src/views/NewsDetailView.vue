<template>
  <div class="detail-page section-space">
    <div class="page-shell">
      <div v-if="loading" class="surface-card detail-loading">
        <el-skeleton animated :rows="10" />
      </div>

      <div v-else-if="article" class="detail-layout">
        <button class="detail-back" type="button" @click="goBackHome">返回动态区</button>

        <article class="surface-card detail-article">
          <SectionHeading :title="article.title" :subtitle="formatDate(article.published_at)" :description="article.summary" />

          <div v-if="hasMedia" class="detail-media-wrap">
            <MediaAsset
              :media-type="article.media_type || 'image'"
              :image-url="article.cover_image"
              :video-url="article.video_url"
              :alt="article.title"
              :controls="(article.media_type || 'image') === 'video'"
              wrapper-class="detail-media-shell"
              element-class="detail-media"
            />
          </div>

          <div class="detail-content">{{ article.content || article.summary }}</div>
        </article>
      </div>

      <div v-else class="surface-card detail-empty">
        <el-empty description="未找到该动态" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { useRoute, useRouter } from "vue-router";

import { fetchNewsDetail } from "../api/content";
import MediaAsset from "../components/MediaAsset.vue";
import SectionHeading from "../components/SectionHeading.vue";

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const article = ref(null);

const hasMedia = computed(() => Boolean(article.value?.cover_image || article.value?.video_url));

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

const loadArticle = async (id) => {
  if (!id) {
    article.value = null;
    return;
  }

  loading.value = true;
  try {
    article.value = await fetchNewsDetail(id);
  } catch (error) {
    article.value = null;
    ElMessage.error(error.response?.data?.detail || "动态详情加载失败");
  } finally {
    loading.value = false;
  }
};

const goBackHome = async () => {
  await router.push({ path: "/", hash: "#news" });
};

watch(
  () => route.params.id,
  (value) => {
    loadArticle(value);
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

.detail-content {
  color: var(--color-text-soft);
  line-height: 1.9;
  white-space: pre-line;
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
}
</style>
