<template>
  <div class="rich-editor surface-card">
    <div class="rich-editor-toolbar">
      <el-button-group>
        <el-button @click="formatBlock('P')">段落</el-button>
        <el-button @click="formatBlock('H2')">H2</el-button>
        <el-button @click="formatBlock('H3')">H3</el-button>
      </el-button-group>
      <el-button-group>
        <el-button @click="exec('bold')">加粗</el-button>
        <el-button @click="exec('italic')">斜体</el-button>
        <el-button @click="exec('underline')">下划线</el-button>
      </el-button-group>
      <el-button-group>
        <el-button @click="exec('insertUnorderedList')">无序列表</el-button>
        <el-button @click="exec('insertOrderedList')">有序列表</el-button>
        <el-button @click="formatBlock('BLOCKQUOTE')">引用</el-button>
      </el-button-group>
      <el-button-group>
        <el-button @click="insertLink">插入链接</el-button>
        <el-button :loading="uploading" @click="openImagePicker">上传图片</el-button>
        <el-button @click="insertImageByUrl">图片链接</el-button>
        <el-button @click="exec('removeFormat')">清除格式</el-button>
      </el-button-group>
      <input ref="fileInputRef" type="file" accept="image/*" class="sr-only" @change="handleFileChange" />
    </div>

    <div
      ref="editorRef"
      class="rich-editor-body"
      :data-placeholder="placeholder"
      contenteditable="true"
      @input="emitContent"
      @blur="emitContent"
      @paste="handlePaste"
    />
  </div>
</template>

<script setup>
import { nextTick, onMounted, ref, watch } from "vue";
import { ElMessage } from "element-plus";

import { uploadMediaAsset } from "../../api/content";

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  placeholder: {
    type: String,
    default: "请输入正文内容",
  },
});

const emit = defineEmits(["update:modelValue"]);
const editorRef = ref(null);
const fileInputRef = ref(null);
const uploading = ref(false);

const setEditorHtml = (value) => {
  if (!editorRef.value) {
    return;
  }
  const normalized = value || "";
  if (editorRef.value.innerHTML !== normalized) {
    editorRef.value.innerHTML = normalized;
  }
};

const emitContent = () => {
  emit("update:modelValue", editorRef.value?.innerHTML || "");
};

const focusEditor = async () => {
  await nextTick();
  editorRef.value?.focus();
};

const exec = async (command, value = null) => {
  await focusEditor();
  document.execCommand(command, false, value);
  emitContent();
};

const formatBlock = async (tagName) => {
  await focusEditor();
  document.execCommand("formatBlock", false, tagName);
  emitContent();
};

const insertLink = async () => {
  const url = window.prompt("请输入链接地址");
  if (!url) {
    return;
  }
  await exec("createLink", url.trim());
};

const insertHtml = async (html) => {
  await focusEditor();
  document.execCommand("insertHTML", false, html);
  emitContent();
};

const insertImageByUrl = async () => {
  const url = window.prompt("请输入图片地址");
  if (!url) {
    return;
  }
  await insertHtml(`<img src="${url.trim()}" alt="插入图片" />`);
};

const openImagePicker = () => {
  fileInputRef.value?.click();
};

const handleFileChange = async (event) => {
  const file = event.target.files?.[0];
  if (!file) {
    return;
  }

  uploading.value = true;
  try {
    const data = await uploadMediaAsset(file, "image");
    await insertHtml(`<img src="${data.url}" alt="${file.name}" />`);
    ElMessage.success("正文图片已插入");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "正文图片上传失败");
  } finally {
    uploading.value = false;
    event.target.value = "";
  }
};

const handlePaste = (event) => {
  event.preventDefault();
  const text = event.clipboardData?.getData("text/plain") || "";
  document.execCommand("insertText", false, text);
  emitContent();
};

watch(
  () => props.modelValue,
  (value) => {
    setEditorHtml(value);
  },
  { immediate: true }
);

onMounted(() => {
  setEditorHtml(props.modelValue);
});
</script>

<style scoped>
.rich-editor {
  padding: 16px;
  border-radius: 20px;
}

.rich-editor-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 14px;
}

.rich-editor-body {
  min-height: 320px;
  padding: 18px;
  border: 1px solid rgba(99, 66, 42, 0.14);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.72);
  line-height: 1.85;
  color: var(--color-text);
  outline: none;
}

.rich-editor-body:empty::before {
  content: attr(data-placeholder);
  color: rgba(104, 87, 74, 0.7);
}

.rich-editor-body :deep(img) {
  display: block;
  max-width: min(100%, 560px);
  margin: 18px 0;
  border-radius: 16px;
}

.rich-editor-body :deep(a) {
  color: var(--color-primary);
}

.sr-only {
  display: none;
}

@media (max-width: 768px) {
  .rich-editor-body {
    min-height: 260px;
    padding: 14px;
  }
}
</style>
