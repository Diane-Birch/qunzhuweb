<template>
  <div class="rich-text-editor" :class="{ 'is-disabled': disabled }">
    <Toolbar
      v-if="editorRef"
      class="editor-toolbar"
      :editor="editorRef"
      :defaultConfig="toolbarConfig"
      mode="default"
    />
    <Editor
      v-model="html"
      class="editor-body"
      :defaultConfig="editorConfig"
      mode="default"
      @onCreated="handleCreated"
    />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref, shallowRef, watch } from "vue";
import { ElMessage } from "element-plus";
import { Editor, Toolbar } from "@wangeditor-next/editor-for-vue";
import "@wangeditor/editor/dist/css/style.css";

import { uploadMediaAsset } from "../../api/content";

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  placeholder: {
    type: String,
    default: "",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:modelValue"]);
const editorRef = shallowRef();
const html = ref(props.modelValue || "");

watch(
  () => props.modelValue,
  (value) => {
    const nextValue = value || "";
    if (nextValue !== html.value) {
      html.value = nextValue;
    }
  }
);

watch(html, (value) => {
  emit("update:modelValue", value || "");
});

const toolbarConfig = {
  excludeKeys: ["group-video", "insertTable", "fullScreen"],
};

const editorConfig = computed(() => ({
  placeholder: props.placeholder,
  readOnly: props.disabled,
  autoFocus: false,
  MENU_CONF: {
    uploadImage: {
      async customUpload(file, insertFn) {
        try {
          const data = await uploadMediaAsset(file, "image");
          insertFn(data.url, file.name || "image", data.url);
        } catch (error) {
          ElMessage.error(error.response?.data?.detail || "\u56fe\u7247\u4e0a\u4f20\u5931\u8d25");
          throw error;
        }
      },
    },
  },
}));

const handleCreated = (editor) => {
  editorRef.value = editor;
};

onBeforeUnmount(() => {
  const editor = editorRef.value;
  if (editor) {
    editor.destroy();
  }
});
</script>

<style scoped>
.rich-text-editor {
  overflow: hidden;
  border: 1px solid rgba(99, 66, 42, 0.12);
  border-radius: 18px;
  background: rgba(255, 251, 245, 0.96);
}

.editor-toolbar {
  border-bottom: 1px solid rgba(99, 66, 42, 0.12);
}

.editor-body :deep(.w-e-text-container) {
  min-height: 280px;
}

.rich-text-editor.is-disabled {
  opacity: 0.78;
}
</style>
