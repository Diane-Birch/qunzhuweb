<template>
  <div class="media-field surface-card">
    <div class="media-field-toolbar">
      <span class="media-field-label">{{ label }}</span>
      <el-radio-group v-if="allowVideo" :model-value="mode" size="small" @update:model-value="handleModeChange">
        <el-radio-button label="image">图片</el-radio-button>
        <el-radio-button label="video">视频</el-radio-button>
      </el-radio-group>
    </div>

    <div class="media-field-body">
      <el-input
        :model-value="currentUrl"
        :placeholder="resolvedPlaceholder"
        @update:model-value="updateCurrentUrl"
      />

      <div class="media-field-actions">
        <el-upload :accept="acceptedTypes" :show-file-list="false" :http-request="handleUpload">
          <el-button type="primary" :loading="uploading">{{ uploadButtonText }}</el-button>
        </el-upload>
        <el-button plain @click="clearCurrentMedia">清空</el-button>
      </div>

      <span class="media-field-tip">{{ tipText }}</span>

      <div v-if="currentUrl" class="media-preview-wrap">
        <img v-if="mode === 'image'" :src="currentUrl" alt="媒体预览" class="media-preview" />
        <video v-else :src="currentUrl" class="media-preview" controls playsinline preload="metadata" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { ElMessage } from "element-plus";

import { uploadMediaAsset } from "../../api/content";

const props = defineProps({
  label: {
    type: String,
    default: "媒体素材",
  },
  mode: {
    type: String,
    default: "image",
  },
  imageUrl: {
    type: String,
    default: "",
  },
  videoUrl: {
    type: String,
    default: "",
  },
  allowVideo: {
    type: Boolean,
    default: true,
  },
  placeholder: {
    type: String,
    default: "支持输入网络链接，或上传本地文件。",
  },
  imagePlaceholder: {
    type: String,
    default: "请输入图片链接，或上传本地图片。",
  },
  videoPlaceholder: {
    type: String,
    default: "请输入视频链接，或上传本地视频。",
  },
  imageTip: {
    type: String,
    default: "图片模式支持直接填写链接，也支持本地上传。",
  },
  videoTip: {
    type: String,
    default: "视频模式支持直接填写链接，也支持本地上传。",
  },
});

const emit = defineEmits(["update:mode", "update:imageUrl", "update:videoUrl"]);
const uploading = ref(false);

const currentUrl = computed(() => (props.mode === "video" ? props.videoUrl : props.imageUrl));
const acceptedTypes = computed(() => (props.mode === "video" ? "video/*" : "image/*"));
const resolvedPlaceholder = computed(() => (props.mode === "video" ? props.videoPlaceholder : props.imagePlaceholder || props.placeholder));
const tipText = computed(() => (props.mode === "video" ? props.videoTip : props.imageTip));
const uploadButtonText = computed(() => (props.mode === "video" ? "上传视频" : "上传图片"));

const updateCurrentUrl = (value) => {
  if (props.mode === "video") {
    emit("update:videoUrl", value);
    return;
  }
  emit("update:imageUrl", value);
};

const handleModeChange = (value) => {
  emit("update:mode", value);
  if (value === "video") {
    emit("update:imageUrl", "");
    return;
  }
  emit("update:videoUrl", "");
};

const clearCurrentMedia = () => {
  updateCurrentUrl("");
};

const handleUpload = async (options) => {
  uploading.value = true;
  try {
    const data = await uploadMediaAsset(options.file, props.mode);
    updateCurrentUrl(data.url);
    options.onSuccess?.(data);
    ElMessage.success(props.mode === "video" ? "视频上传成功" : "图片上传成功");
  } catch (error) {
    options.onError?.(error);
    ElMessage.error(error.response?.data?.detail || (props.mode === "video" ? "视频上传失败" : "图片上传失败"));
  } finally {
    uploading.value = false;
  }
};
</script>

<style scoped>
.media-field {
  padding: 18px;
  border-radius: 20px;
}

.media-field-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.media-field-label {
  font-weight: 600;
  color: var(--color-primary-deep);
}

.media-field-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.media-field-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.media-field-tip {
  color: var(--color-text-soft);
  line-height: 1.6;
}

.media-preview-wrap {
  width: min(220px, 100%);
  overflow: hidden;
  border-radius: 18px;
  background: rgba(255, 250, 242, 0.9);
  border: 1px solid rgba(99, 66, 42, 0.08);
}

.media-preview {
  width: 100%;
  aspect-ratio: 1.1 / 1;
  object-fit: cover;
  display: block;
}

@media (max-width: 768px) {
  .media-field-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

