<template>
  <section class="hero">
    <el-carousel v-if="items.length" height="68vh" indicator-position="outside">
      <el-carousel-item v-for="item in items" :key="item.id">
        <div class="hero-slide" :style="{ backgroundImage: `linear-gradient(rgba(31, 19, 10, 0.35), rgba(31, 19, 10, 0.45)), url(${item.image_url})` }">
          <div class="page-shell hero-inner">
            <div class="hero-copy">
              <p v-if="item.subtitle" class="hero-subtitle">{{ item.subtitle }}</p>
              <h1>{{ item.title }}</h1>
              <p v-if="item.description" class="hero-description">{{ item.description }}</p>
              <a v-if="item.cta_text && item.cta_link" class="hero-cta" :href="item.cta_link">{{ item.cta_text }}</a>
            </div>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
    <div v-else class="hero-empty page-shell surface-card">
      <el-empty description="后台暂未发布轮播内容" />
    </div>
  </section>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => [],
  },
});
</script>

<style scoped>
.hero {
  position: relative;
}

.hero-slide {
  min-height: 68vh;
  display: flex;
  align-items: center;
  background-size: cover;
  background-position: center;
}

.hero-inner {
  width: 100%;
}

.hero-copy {
  max-width: 640px;
  color: #fff8ef;
}

.hero-subtitle {
  margin: 0 0 16px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-size: 13px;
}

h1 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(36px, 7vw, 72px);
  line-height: 1.05;
}

.hero-description {
  margin: 24px 0 32px;
  font-size: 17px;
  line-height: 1.8;
  color: rgba(255, 248, 239, 0.92);
}

.hero-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 26px;
  border-radius: 999px;
  color: #fff;
  background: rgba(141, 79, 42, 0.92);
}

.hero-empty {
  margin-top: 32px;
  padding: 48px 0;
}

:deep(.el-carousel__button) {
  background-color: rgba(255, 255, 255, 0.85);
}

@media (max-width: 768px) {
  .hero-slide {
    min-height: 58vh;
  }

  .hero-description {
    font-size: 15px;
  }
}
</style>
