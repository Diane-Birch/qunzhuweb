<template>
  <div class="login-page">
    <div class="login-panel surface-card earthy-panel">
      <div class="panel-copy">
        <p>管理后台</p>
        <h1>哈尼梯田红米内容发布系统</h1>
        <span>登录后可统一维护前端轮播图、文化板块、产品信息与企业动态。</span>
      </div>
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleSubmit">
        <el-form-item label="账号" prop="username">
          <el-input v-model="form.username" placeholder="请输入管理员账号" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入管理员密码" />
        </el-form-item>
        <el-button type="primary" :loading="submitting" class="submit-button" @click="handleSubmit">
          登录后台
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import { loginAdmin } from "../../api/content";
import { setToken } from "../../utils/auth";

const router = useRouter();
const formRef = ref();
const submitting = ref(false);
const form = reactive({
  username: "admin",
  password: "admin123456",
});

const rules = {
  username: [{ required: true, message: "请输入管理员账号", trigger: "blur" }],
  password: [{ required: true, message: "请输入管理员密码", trigger: "blur" }],
};

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) return;
  submitting.value = true;
  try {
    const data = await loginAdmin(form);
    setToken(data.access_token);
    ElMessage.success("登录成功");
    router.push({ name: "admin-dashboard" });
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "登录失败");
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background:
    radial-gradient(circle at top left, rgba(141, 79, 42, 0.24), transparent 30%),
    radial-gradient(circle at bottom right, rgba(110, 134, 97, 0.28), transparent 28%),
    linear-gradient(180deg, #efe4d0, #f9f4eb);
}

.login-panel {
  width: min(960px, 100%);
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 380px);
  gap: 36px;
  padding: 36px;
}

.panel-copy p {
  margin: 0 0 18px;
  color: var(--color-secondary);
  letter-spacing: 0.12em;
}

.panel-copy h1 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(36px, 5vw, 56px);
  line-height: 1.1;
}

.panel-copy span {
  display: block;
  margin-top: 20px;
  color: var(--color-text-soft);
  line-height: 1.9;
}

.submit-button {
  width: 100%;
  margin-top: 12px;
}

@media (max-width: 840px) {
  .login-panel {
    grid-template-columns: 1fr;
    padding: 24px;
  }
}
</style>
