<template>
  <div class="section-heading">
    <p v-if="subtitle" class="eyebrow">{{ subtitle }}</p>
    <h2>{{ title }}</h2>
    <p v-if="description" class="desc">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: "",
  },
  description: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
.section-heading {
  max-width: 680px;
  margin-bottom: 36px;
}

.eyebrow {
  margin: 0 0 14px;
  color: var(--color-secondary);
  letter-spacing: 0.16em;
  text-transform: uppercase;
  font-size: 13px;
}

h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(28px, 4vw, 44px);
}

.desc {
  margin: 16px 0 0;
  color: var(--color-text-soft);
  line-height: 1.85;
}
</style>
