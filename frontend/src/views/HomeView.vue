<template>
  <div>
    <header class="topbar">
      <div class="page-shell topbar-inner">
        <div class="brand-group">
          <button class="brand-logo-button" type="button" :aria-label="siteTitle" @click="goHome">
            <img :src="logoImage" :alt="`${siteTitle} logo`" class="brand-logo" />
          </button>
          <button class="brand-title" type="button" @click="goHome">{{ siteTitle }}</button>
        </div>

        <div class="topbar-menu">
          <el-dropdown
            trigger="click"
            placement="bottom-end"
            popper-class="nav-dropdown-popover"
            @command="handleNavCommand"
          >
            <button class="nav-trigger" type="button">
              <span>{{ navMenuLabel }}</span>
              <el-icon><ArrowDown /></el-icon>
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item v-for="item in menuItems" :key="item.command" :command="item.command">
                  {{ item.label }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
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
              <div v-if="hasSectionMedia(section)" class="story-image">
                <MediaAsset
                  :media-type="section.media_type || 'image'"
                  :image-url="section.image_url"
                  :video-url="section.video_url"
                  :alt="section.title"
                  :controls="(section.media_type || 'image') === 'video'"
                  wrapper-class="story-media-wrap"
                  element-class="story-media"
                />
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
            <el-empty :description="emptyProductText" />
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
            <el-empty :description="emptyNewsText" />
          </div>
        </div>
      </section>
    </main>

    <footer v-if="hasFooterContent" class="site-footer">
      <section class="footer-transition" aria-hidden="true">
        <div class="page-shell footer-transition-shell">
          <div class="transition-ridge">
            <span v-for="index in 5" :key="`terrace-${index}`" class="terrace-line" />
            <div class="grain-orbs">
              <span v-for="index in 8" :key="`grain-${index}`" class="grain-orb" />
            </div>
            <div class="loom-pattern">
              <span v-for="index in 6" :key="`pattern-${index}`" class="loom-unit" />
            </div>
          </div>
        </div>
      </section>

      <div class="page-shell footer-shell">
        <section class="footer-panel surface-card" aria-label="Footer information">
          <div v-if="showQrImage" class="footer-qr-stage">
            <div class="footer-qr-frame">
              <img
                :src="homepage.footer_qr.image_url"
                :alt="homepage.footer_qr.name || qrFallbackLabel"
                class="footer-qr-image"
              />
            </div>
          </div>

          <div class="footer-copy">
            <p v-if="homepage.footer_qr?.name" class="footer-eyebrow">{{ homepage.footer_qr.name }}</p>
            <p v-if="showQrDescription" class="footer-description">{{ homepage.footer_qr.description }}</p>

            <div v-if="showFilingInfo" class="footer-filing-block">
              <span class="footer-filing-label">{{ homepage.footer_filing.name || filingFallbackLabel }}</span>
              <p class="footer-filing-copy">{{ homepage.footer_filing.description }}</p>
            </div>
          </div>
        </section>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ArrowDown } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { fetchHomepage } from "../api/content";
import HeroCarousel from "../components/HeroCarousel.vue";
import MediaAsset from "../components/MediaAsset.vue";
import NewsCard from "../components/NewsCard.vue";
import ProductCard from "../components/ProductCard.vue";
import SectionHeading from "../components/SectionHeading.vue";
import logoImage from "../../logo/logo.png";

const router = useRouter();
const loading = ref(true);
const siteTitle = "\u7ea2\u6cb3\u6587\u5316\u7ad9";
const navMenuLabel = "\u5bfc\u822a\u83dc\u5355";
const emptyProductText = "\u6682\u65e0\u4ea7\u54c1\u5185\u5bb9";
const emptyNewsText = "\u6682\u65e0\u65b0\u95fb\u5185\u5bb9";
const qrFallbackLabel = "\u626b\u7801\u5173\u6ce8";
const filingFallbackLabel = "\u5907\u6848\u4fe1\u606f";
const homepage = reactive({
  banners: [],
  sections: [],
  products: [],
  news: [],
  product_intro: null,
  news_intro: null,
  footer_qr: null,
  footer_filing: null,
});

const menuItems = [
  { label: "\u6587\u5316\u4eae\u70b9", command: "#culture" },
  { label: "\u4ea7\u54c1\u5c55\u793a", command: "#products" },
  { label: "\u4f01\u4e1a\u52a8\u6001", command: "#news" },
  { label: "\u540e\u53f0\u7ba1\u7406", command: "/admin/login" },
];

const showQrImage = computed(() => Boolean(homepage.footer_qr?.is_active && homepage.footer_qr?.image_url));
const showQrDescription = computed(() => Boolean(homepage.footer_qr?.is_active && homepage.footer_qr?.description));
const showFilingInfo = computed(() => Boolean(homepage.footer_filing?.is_active && homepage.footer_filing?.description));
const hasFooterContent = computed(() => showQrImage.value || showQrDescription.value || showFilingInfo.value);

const hasSectionMedia = (section) => Boolean(section?.video_url || section?.image_url);

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

const scrollToSection = (hash) => {
  const target = document.querySelector(hash);
  if (target) {
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

const goHome = async () => {
  try {
    if (router.currentRoute.value.path !== "/") {
      await router.push({ path: "/" });
    } else if (router.currentRoute.value.hash) {
      await router.replace({ path: "/" });
    }
  } catch (error) {
    // Ignore duplicate navigation errors.
  }
  window.scrollTo({ top: 0, behavior: "smooth" });
};

const handleNavCommand = async (command) => {
  if (command.startsWith("#")) {
    try {
      if (router.currentRoute.value.path !== "/" || router.currentRoute.value.hash !== command) {
        await router.push({ path: "/", hash: command });
        requestAnimationFrame(() => scrollToSection(command));
      } else {
        scrollToSection(command);
      }
    } catch (error) {
      scrollToSection(command);
    }
    return;
  }

  if (router.currentRoute.value.path !== command) {
    await router.push(command);
  }
};

const loadHomepage = async () => {
  loading.value = true;
  try {
    const data = await fetchHomepage();
    Object.assign(homepage, data);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "\u9996\u9875\u6570\u636e\u52a0\u8f7d\u5931\u8d25");
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
  background: rgba(247, 240, 228, 0.9);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(99, 66, 42, 0.08);
}

.topbar-inner {
  width: 100%;
  max-width: none;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  min-height: 76px;
  padding: 12px clamp(18px, 3vw, 42px);
}

.brand-group {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  margin-right: auto;
}

.topbar-menu {
  margin-left: auto;
  flex-shrink: 0;
}

.brand-logo-button,
.brand-title,
.nav-trigger {
  border: none;
  background: transparent;
  padding: 0;
  cursor: pointer;
}

.brand-logo-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.brand-logo {
  width: min(78px, 18vw);
  max-width: 80px;
  height: min(56px, 12vw);
  max-height: 60px;
  object-fit: contain;
}

.brand-title {
  font-family: var(--font-display);
  font-size: clamp(24px, 3vw, 30px);
  color: var(--color-primary-deep);
  white-space: nowrap;
  transition: color 0.24s ease;
}

.brand-logo-button:hover + .brand-title,
.brand-title:hover {
  color: var(--color-primary);
}

.nav-trigger {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  border-radius: 999px;
  background: rgba(141, 79, 42, 0.12);
  color: var(--color-primary-deep);
  font-weight: 600;
  transition: background-color 0.24s ease, transform 0.24s ease, box-shadow 0.24s ease;
}

.nav-trigger:hover {
  background: rgba(141, 79, 42, 0.2);
  box-shadow: 0 12px 24px rgba(99, 66, 42, 0.12);
  transform: translateY(-1px);
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

.story-media-wrap,
.story-media {
  width: 100%;
  height: 100%;
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

.site-footer {
  padding: 0 0 56px;
}

.footer-transition {
  padding: 28px 0 18px;
}

.footer-transition-shell {
  position: relative;
}

.transition-ridge {
  position: relative;
  min-height: 170px;
  overflow: hidden;
  border-radius: 40px 40px 24px 24px;
  background:
    radial-gradient(circle at 14% 20%, rgba(183, 112, 59, 0.18), transparent 20%),
    radial-gradient(circle at 82% 22%, rgba(110, 134, 97, 0.16), transparent 18%),
    linear-gradient(180deg, rgba(247, 240, 228, 0.88), rgba(230, 213, 184, 0.78));
  box-shadow: inset 0 -14px 32px rgba(138, 93, 56, 0.08);
}

.terrace-line {
  position: absolute;
  left: 50%;
  border: 1.5px solid rgba(141, 79, 42, 0.22);
  border-radius: 999px;
  transform: translateX(-50%);
}

.terrace-line:nth-child(1) {
  top: 28px;
  width: calc(100% - 120px);
  height: 74px;
}

.terrace-line:nth-child(2) {
  top: 52px;
  width: calc(100% - 200px);
  height: 86px;
}

.terrace-line:nth-child(3) {
  top: 78px;
  width: calc(100% - 280px);
  height: 92px;
}

.terrace-line:nth-child(4) {
  top: 104px;
  width: calc(100% - 360px);
  height: 88px;
}

.terrace-line:nth-child(5) {
  top: 126px;
  width: calc(100% - 460px);
  height: 78px;
}

.grain-orbs {
  position: absolute;
  left: 30px;
  bottom: 20px;
  display: grid;
  grid-template-columns: repeat(4, 12px);
  gap: 10px 12px;
}

.grain-orb {
  width: 12px;
  height: 22px;
  border-radius: 999px;
  background: linear-gradient(180deg, rgba(174, 76, 36, 0.92), rgba(114, 39, 18, 0.9));
  transform: rotate(24deg);
  box-shadow: 0 4px 10px rgba(118, 49, 23, 0.18);
}

.loom-pattern {
  position: absolute;
  right: 28px;
  bottom: 22px;
  display: grid;
  grid-template-columns: repeat(3, 12px);
  gap: 10px;
}

.loom-unit {
  width: 12px;
  height: 12px;
  border: 2px solid rgba(96, 58, 27, 0.38);
  transform: rotate(45deg);
}

.footer-shell {
  margin-top: -38px;
}

.footer-panel {
  display: grid;
  grid-template-columns: minmax(180px, 240px) minmax(0, 1fr);
  align-items: center;
  gap: 30px;
  padding: 28px 32px;
  border-radius: 30px;
  background:
    linear-gradient(135deg, rgba(255, 251, 245, 0.96), rgba(245, 237, 223, 0.92)),
    linear-gradient(180deg, rgba(222, 210, 189, 0.24), rgba(247, 240, 228, 0));
}

.footer-qr-stage {
  display: flex;
  justify-content: center;
}

.footer-qr-frame {
  padding: 16px;
  border-radius: 28px;
  background: rgba(255, 250, 242, 0.92);
  box-shadow: 0 20px 40px rgba(72, 45, 24, 0.12);
}

.footer-qr-image {
  width: 150px;
  height: 150px;
  object-fit: contain;
}

.footer-copy {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-width: 0;
}

.footer-eyebrow {
  margin: 0;
  color: var(--color-secondary);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.footer-description {
  margin: 0;
  font-size: clamp(18px, 2.1vw, 24px);
  line-height: 1.7;
  color: var(--color-primary-deep);
}

.footer-filing-block {
  display: inline-flex;
  flex-direction: column;
  gap: 8px;
  width: fit-content;
  max-width: 100%;
  padding: 14px 18px;
  border-radius: 18px;
  background: rgba(110, 134, 97, 0.09);
}

.footer-filing-label {
  color: var(--color-secondary);
  font-size: 13px;
  letter-spacing: 0.12em;
}

.footer-filing-copy {
  margin: 0;
  color: var(--color-text-soft);
  line-height: 1.7;
  word-break: break-all;
}

.empty-card,
.loading-card {
  padding: 32px;
}

:global(.nav-dropdown-popover.el-popper) {
  border-radius: 20px;
  border: 1px solid rgba(99, 66, 42, 0.12);
  background: rgba(255, 249, 241, 0.96);
  box-shadow: 0 18px 38px rgba(72, 45, 24, 0.14);
  backdrop-filter: blur(14px);
}

:global(.nav-dropdown-popover .el-dropdown-menu) {
  padding: 8px;
}

:global(.nav-dropdown-popover .el-dropdown-menu__item) {
  min-width: 164px;
  padding: 12px 14px;
  border-radius: 14px;
  color: var(--color-text);
  transition: background-color 0.2s ease, color 0.2s ease;
}

:global(.nav-dropdown-popover .el-dropdown-menu__item:not(.is-disabled):hover) {
  background: rgba(141, 79, 42, 0.12);
  color: var(--color-primary-deep);
}

@media (max-width: 1024px) {
  .story-card,
  .news-grid,
  .product-grid,
  .footer-panel {
    grid-template-columns: 1fr;
  }

  .footer-qr-stage {
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .topbar-inner {
    gap: 12px;
    min-height: 68px;
    padding: 10px 16px;
  }

  .brand-group {
    gap: 10px;
  }

  .brand-title {
    font-size: clamp(20px, 6vw, 26px);
  }

  .nav-trigger {
    padding: 10px 16px;
  }

  .story-card {
    padding: 18px;
  }

  .story-image {
    min-height: 220px;
  }

  .transition-ridge {
    min-height: 142px;
  }

  .terrace-line:nth-child(1) { width: calc(100% - 56px); }
  .terrace-line:nth-child(2) { width: calc(100% - 92px); }
  .terrace-line:nth-child(3) { width: calc(100% - 128px); }
  .terrace-line:nth-child(4) { width: calc(100% - 164px); }
  .terrace-line:nth-child(5) { width: calc(100% - 212px); }

  .footer-shell {
    margin-top: -24px;
  }

  .footer-panel {
    gap: 18px;
    padding: 22px 18px;
  }

  .footer-qr-image {
    width: 120px;
    height: 120px;
  }
}
</style>
