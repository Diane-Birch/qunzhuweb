<template>
  <div>
    <header class="topbar">
      <div class="page-shell topbar-inner">
        <a class="brand" href="#top">哈尼梯田红米</a>
        <nav class="topbar-nav">
          <a href="#culture">文化亮点</a>
          <a href="#products">产品展示</a>
          <a href="#news">企业动态</a>
          <router-link to="/admin/login">后台管理</router-link>
        </nav>
      </div>
    </header>

    <main id="top">
      <HeroCarousel :items="homepage.banners" />

      <section id="culture" class="section-space">
        <div class="page-shell">
          <div v-if="loading" class="surface-card loading-card">
            <el-skeleton animated :rows="8" />
          </div>

          <div v-else class="story-grid">
            <article
              v-for="section in homepage.sections"
              :key="section.id"
              class="story-card surface-card"
            >
              <div class="story-copy">
                <SectionHeading
                  :title="section.title"
                  :subtitle="section.subtitle"
                  :description="section.body"
                />
                <div v-if="parseExtra(section.extra_json).tags.length" class="tag-list">
                  <span v-for="tag in parseExtra(section.extra_json).tags" :key="tag">{{ tag }}</span>
                </div>
                <div v-if="parseExtra(section.extra_json).stats.length" class="stats-grid">
                  <div v-for="stat in parseExtra(section.extra_json).stats" :key="stat.label">
                    <strong>{{ stat.value }}</strong>
                    <span>{{ stat.label }}</span>
                  </div>
                </div>
              </div>
              <div v-if="section.image_url" class="story-image">
                <img :src="section.image_url" :alt="section.title" />
              </div>
            </article>
          </div>
        </div>
      </section>

      <section id="products" class="section-space muted-section">
        <div class="page-shell">
          <SectionHeading
            v-if="homepage.product_intro"
            :title="homepage.product_intro.title"
            :subtitle="homepage.product_intro.subtitle"
            :description="homepage.product_intro.body"
          />
          <div class="product-grid">
            <ProductCard v-for="item in homepage.products" :key="item.id" :item="item" />
          </div>
          <div v-if="!homepage.products.length && !loading" class="surface-card empty-card">
            <el-empty description="后台暂未发布产品内容" />
          </div>
        </div>
      </section>

      <section id="news" class="section-space">
        <div class="page-shell">
          <SectionHeading
            v-if="homepage.news_intro"
            :title="homepage.news_intro.title"
            :subtitle="homepage.news_intro.subtitle"
            :description="homepage.news_intro.body"
          />
          <div class="news-grid">
            <NewsCard v-for="item in homepage.news" :key="item.id" :item="item" />
          </div>
          <div v-if="!homepage.news.length && !loading" class="surface-card empty-card">
            <el-empty description="后台暂未发布新闻动态" />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { ElMessage } from "element-plus";

import { fetchHomepage } from "../api/content";
import HeroCarousel from "../components/HeroCarousel.vue";
import NewsCard from "../components/NewsCard.vue";
import ProductCard from "../components/ProductCard.vue";
import SectionHeading from "../components/SectionHeading.vue";

const loading = ref(true);
const homepage = reactive({
  banners: [],
  sections: [],
  products: [],
  news: [],
  product_intro: null,
  news_intro: null,
});

const parseExtra = (value) => {
  try {
    const data = JSON.parse(value || "{}");
    return {
      tags: Array.isArray(data.tags) ? data.tags : [],
      stats: Array.isArray(data.stats) ? data.stats : [],
    };
  } catch (error) {
    return { tags: [], stats: [] };
  }
};

const loadHomepage = async () => {
  loading.value = true;
  try {
    const data = await fetchHomepage();
    Object.assign(homepage, data);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "首页数据加载失败");
  } finally {
    loading.value = false;
  }
};

onMounted(loadHomepage);
</script>

<style scoped>
.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(247, 240, 228, 0.88);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(99, 66, 42, 0.08);
}

.topbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 72px;
}

.brand {
  font-family: var(--font-display);
  font-size: 28px;
  color: var(--color-primary-deep);
}

.topbar-nav {
  display: flex;
  gap: 22px;
  color: var(--color-text-soft);
}

.story-grid,
.product-grid,
.news-grid {
  display: grid;
  gap: 24px;
}

.story-grid {
  grid-template-columns: 1fr;
}

.story-card {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
  gap: 24px;
  padding: 24px;
}

.story-copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.story-image {
  overflow: hidden;
  border-radius: 24px;
  min-height: 320px;
}

.story-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tag-list,
.stats-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag-list {
  margin-top: 4px;
}

.tag-list span {
  padding: 10px 14px;
  background: rgba(110, 134, 97, 0.12);
  border-radius: 999px;
  color: var(--color-secondary);
}

.stats-grid {
  margin-top: 22px;
}

.stats-grid div {
  min-width: 150px;
  padding: 18px 22px;
  background: var(--color-surface-strong);
  border-radius: 18px;
}

.stats-grid strong {
  display: block;
  font-size: 28px;
  font-family: var(--font-display);
}

.stats-grid span {
  color: var(--color-text-soft);
}

.product-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.news-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.muted-section {
  background: linear-gradient(180deg, rgba(222, 210, 189, 0.5), rgba(245, 238, 223, 0));
}

.empty-card,
.loading-card {
  padding: 32px;
}

@media (max-width: 1024px) {
  .story-card,
  .news-grid,
  .product-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .topbar-inner {
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    padding: 14px 0;
    gap: 10px;
  }

  .topbar-nav {
    flex-wrap: wrap;
    gap: 12px 18px;
  }

  .story-card {
    padding: 18px;
  }

  .story-image {
    min-height: 220px;
  }
}
</style>
