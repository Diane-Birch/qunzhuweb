<template>
  <section class="hero">
    <el-carousel v-if="items.length" height="68vh" indicator-position="outside">
      <el-carousel-item v-for="item in items" :key="item.id">
        <div class="hero-slide">
          <MediaAsset
            :media-type="item.media_type || 'image'"
            :image-url="item.image_url"
            :video-url="item.video_url"
            alt="Banner media"
            :autoplay="(item.media_type || 'image') === 'video'"
            :muted="(item.media_type || 'image') === 'video'"
            :loop="(item.media_type || 'image') === 'video'"
            :controls="false"
            wrapper-class="hero-media-wrap"
            element-class="hero-media"
          />
          <div class="hero-overlay"></div>
          <div class="page-shell hero-inner" :class="positionClass(item.text_position)">
            <div class="hero-copy">
              <p v-if="item.subtitle" class="hero-subtitle" :style="{ fontSize: `${item.subtitle_font_size || 13}px` }">{{ item.subtitle }}</p>
              <h1 :style="{ fontSize: `clamp(36px, ${Math.max((item.title_font_size || 72) * 0.1, 4.6)}vw, ${item.title_font_size || 72}px)` }">{{ item.title }}</h1>
              <p v-if="item.description" class="hero-description" :style="{ fontSize: `${item.description_font_size || 17}px` }">{{ item.description }}</p>
              <a v-if="item.cta_text && item.cta_link" class="hero-cta" :href="item.cta_link">{{ item.cta_text }}</a>
            </div>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
    <div v-else class="hero-empty page-shell surface-card">
      <el-empty :description="'\u6682\u65e0\u5df2\u53d1\u5e03\u7684\u8f6e\u64ad\u5185\u5bb9'" />
    </div>
  </section>
</template>

<script setup>
import MediaAsset from "./MediaAsset.vue";

defineProps({
  items: {
    type: Array,
    default: () => [],
  },
});

const positionClass = (position) => {
  const map = {
    "left-center": "position-left-center",
    center: "position-center",
    "right-center": "position-right-center",
    "left-bottom": "position-left-bottom",
    "center-bottom": "position-center-bottom",
    "right-bottom": "position-right-bottom",
    "left-top": "position-left-top",
    "center-top": "position-center-top",
    "right-top": "position-right-top",
  };
  return map[position || "left-center"] || "position-left-center";
};
</script>

<style scoped>
.hero {
  position: relative;
}

.hero-slide {
  position: relative;
  min-height: 68vh;
  overflow: hidden;
}

.hero-media-wrap,
.hero-media {
  position: absolute;
  inset: 0;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(rgba(31, 19, 10, 0.35), rgba(31, 19, 10, 0.48));
}

.hero-inner {
  position: relative;
  z-index: 1;
  display: flex;
  width: 100%;
  min-height: 68vh;
  padding-block: 44px;
}

.hero-copy {
  max-width: 640px;
  color: #fff8ef;
}

.hero-subtitle {
  margin: 0 0 16px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-family: var(--font-display);
  line-height: 1.05;
}

.hero-description {
  margin: 24px 0 32px;
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

.position-left-center { align-items: center; justify-content: flex-start; text-align: left; }
.position-center { align-items: center; justify-content: center; text-align: center; }
.position-right-center { align-items: center; justify-content: flex-end; text-align: right; }
.position-left-bottom { align-items: flex-end; justify-content: flex-start; text-align: left; }
.position-center-bottom { align-items: flex-end; justify-content: center; text-align: center; }
.position-right-bottom { align-items: flex-end; justify-content: flex-end; text-align: right; }
.position-left-top { align-items: flex-start; justify-content: flex-start; text-align: left; }
.position-center-top { align-items: flex-start; justify-content: center; text-align: center; }
.position-right-top { align-items: flex-start; justify-content: flex-end; text-align: right; }

.hero-empty {
  margin-top: 32px;
  padding: 48px 0;
}

:deep(.el-carousel__button) {
  background-color: rgba(255, 255, 255, 0.85);
}

@media (max-width: 768px) {
  .hero-slide,
  .hero-inner {
    min-height: 58vh;
  }

  .hero-inner {
    padding-block: 30px;
  }

  .hero-description {
    font-size: 15px !important;
  }
}
</style>
