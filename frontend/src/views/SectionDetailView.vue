<template>
  <div class="section-detail-page section-space">
    <div class="page-shell">
      <div v-if="loading" class="surface-card detail-loading">
        <el-skeleton animated :rows="10" />
      </div>

      <div v-else-if="section" class="detail-layout">
        <button class="detail-back" type="button" @click="goBackHome">返回首页</button>

        <article class="surface-card detail-article">
          <SectionHeading :title="section.title" :subtitle="section.subtitle" :description="section.summary" />

          <div v-if="hasMedia" class="detail-media-wrap">
            <MediaAsset
              :media-type="section.media_type || 'image'"
              :image-url="section.image_url"
              :video-url="section.video_url"
              :alt="section.title"
              :controls="(section.media_type || 'image') === 'video'"
              wrapper-class="detail-media-shell"
              element-class="detail-media"
            />
          </div>

          <div v-if="meta.tags.length || meta.stats.length" class="detail-meta">
            <div v-if="meta.tags.length" class="detail-tags">
              <span v-for="tag in meta.tags" :key="tag">{{ tag }}</span>
            </div>
            <div v-if="meta.stats.length" class="detail-stats">
              <div v-for="stat in meta.stats" :key="stat.label">
                <strong>{{ stat.value }}</strong>
                <span>{{ stat.label }}</span>
              </div>
            </div>
          </div>

          <div class="rich-text-content" v-html="sanitizedBody" />
        </article>
      </div>

      <div v-else class="surface-card detail-empty">
        <el-empty description="未找到该板块内容" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { useRoute, useRouter } from "vue-router";

import { fetchSectionDetail } from "../api/content";
import MediaAsset from "../components/MediaAsset.vue";
import SectionHeading from "../components/SectionHeading.vue";
import { sanitizeRichText } from "../utils/richText";
import { normalizeSectionId } from "../utils/sectionNavigation";

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const section = ref(null);

const hasMedia = computed(() => Boolean(section.value?.image_url || section.value?.video_url));
const sanitizedBody = computed(() => sanitizeRichText(section.value?.body || ""));
const meta = computed(() => {
  try {
    const parsed = JSON.parse(section.value?.extra_json || "{}");
    return {
      tags: Array.isArray(parsed.tags) ? parsed.tags : [],
      stats: Array.isArray(parsed.stats) ? parsed.stats : [],
    };
  } catch (error) {
    return { tags: [], stats: [] };
  }
});

const loadSection = async (key) => {
  if (!key) {
    section.value = null;
    return;
  }

  loading.value = true;
  try {
    section.value = await fetchSectionDetail(key);
  } catch (error) {
    section.value = null;
    ElMessage.error(error.response?.data?.detail || "板块详情加载失败");
  } finally {
    loading.value = false;
  }
};

const goBackHome = async () => {
  const hash = section.value?.key ? `#${normalizeSectionId(section.value.key)}` : "";
  await router.push({ path: "/", hash });
};

watch(
  () => route.params.key,
  (value) => {
    loadSection(value);
  },
  { immediate: true }
);
</script>

<style scoped>
.section-detail-page {
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

.detail-meta {
  display: grid;
  gap: 18px;
  margin-bottom: 20px;
}

.detail-tags,
.detail-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.detail-tags span {
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(110, 134, 97, 0.12);
  color: var(--color-secondary);
}

.detail-stats div {
  min-width: 160px;
  padding: 18px 20px;
  border-radius: 18px;
  background: var(--color-surface-strong);
}

.detail-stats strong {
  display: block;
  font-size: 28px;
  font-family: var(--font-display);
}

.detail-stats span {
  color: var(--color-text-soft);
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
