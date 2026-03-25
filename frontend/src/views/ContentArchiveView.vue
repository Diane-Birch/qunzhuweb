<template>
  <div class="archive-page section-space">
    <div class="page-shell">
      <div class="archive-head">
        <button class="archive-back" type="button" @click="goBackHome">&#x8FD4;&#x56DE;&#x9996;&#x9875;</button>
        <SectionHeading :title="currentConfig.title" :subtitle="currentConfig.subtitle" :description="currentConfig.rule" />
      </div>

      <div v-if="loading" class="surface-card archive-loading">
        <el-skeleton animated :rows="10" />
      </div>

      <template v-else>
        <div v-if="items.length" class="archive-grid">
          <SectionArchiveCard
            v-if="contentType === 'section'"
            v-for="item in items"
            :key="`section-${item.id}`"
            :item="item"
            :detail-query="detailQuery"
          />
          <ProductCard
            v-else-if="contentType === 'product'"
            v-for="item in items"
            :key="`product-${item.id}`"
            :item="item"
            :detail-query="detailQuery"
            :show-specs="false"
          />
          <NewsCard
            v-else
            v-for="item in items"
            :key="`news-${item.id}`"
            :item="item"
            :detail-query="detailQuery"
          />
        </div>

        <div v-else class="surface-card archive-empty">
          <el-empty description="&#x6682;&#x65E0;&#x5185;&#x5BB9;" />
        </div>

        <el-pagination
          v-if="total > pageSize"
          class="archive-pager"
          background
          layout="total, prev, pager, next"
          :total="total"
          :current-page="page"
          :page-size="pageSize"
          @current-change="loadPage"
        />
      </template>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { fetchPublicNews, fetchPublicProducts, fetchPublicSectionGroup } from "../api/content";
import NewsCard from "../components/NewsCard.vue";
import ProductCard from "../components/ProductCard.vue";
import SectionArchiveCard from "../components/SectionArchiveCard.vue";
import SectionHeading from "../components/SectionHeading.vue";
import { newsArchiveConfig, productArchiveConfig, sectionBoardMap } from "../utils/contentBoards";

const props = defineProps({
  contentType: {
    type: String,
    required: true,
  },
  groupKey: {
    type: String,
    default: "",
  },
});

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const items = ref([]);
const total = ref(0);
const page = ref(1);
const pageSize = 9;

const currentConfig = computed(() => {
  if (props.contentType === "section") {
    return sectionBoardMap[props.groupKey] || {
      title: "\u677f\u5757\u5185\u5bb9\u5217\u8868",
      subtitle: "\u5386\u53f2\u5185\u5bb9\u5f52\u6863",
      rule: "\u6309\u53d1\u5e03\u65f6\u95f4\u5012\u5e8f\u5c55\u793a\u5168\u90e8\u5185\u5bb9\u3002",
    };
  }
  if (props.contentType === "product") {
    return productArchiveConfig;
  }
  return newsArchiveConfig;
});

const detailQuery = computed(() => ({ back: route.fullPath }));

const goBackHome = async () => {
  const hash = props.contentType === "section" ? `#${props.groupKey}` : props.contentType === "product" ? "#products" : "#news";
  await router.push({ path: "/", hash });
};

const loadPage = async (targetPage = 1) => {
  loading.value = true;
  try {
    let data;
    if (props.contentType === "section") {
      data = await fetchPublicSectionGroup(props.groupKey, { page: targetPage, page_size: pageSize });
    } else if (props.contentType === "product") {
      data = await fetchPublicProducts({ page: targetPage, page_size: pageSize });
    } else {
      data = await fetchPublicNews({ page: targetPage, page_size: pageSize });
    }
    items.value = data.items || [];
    total.value = data.total || 0;
    page.value = targetPage;
  } catch (error) {
    items.value = [];
    total.value = 0;
    ElMessage.error(error.response?.data?.detail || "\u5217\u8868\u52a0\u8f7d\u5931\u8d25");
  } finally {
    loading.value = false;
  }
};

watch(
  () => [props.contentType, props.groupKey],
  () => {
    loadPage(1);
  },
  { immediate: true }
);
</script>

<style scoped>
.archive-page { min-height: 100vh; }
.archive-head { display: grid; gap: 18px; margin-bottom: 24px; }
.archive-back { width: fit-content; padding: 12px 20px; border: none; border-radius: 999px; background: rgba(141, 79, 42, 0.14); color: var(--color-primary-deep); cursor: pointer; transition: transform 0.24s ease, background-color 0.24s ease; }
.archive-back:hover { background: rgba(141, 79, 42, 0.2); transform: translateY(-1px); }
.archive-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; }
.archive-loading, .archive-empty { padding: 28px; }
.archive-pager { margin-top: 24px; justify-content: flex-end; }
@media (max-width: 1024px) { .archive-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 768px) { .archive-grid { grid-template-columns: 1fr; } .archive-loading, .archive-empty { padding: 20px; } }
</style>
