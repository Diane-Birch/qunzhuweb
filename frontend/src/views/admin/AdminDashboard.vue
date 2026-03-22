<template>
  <div class="dashboard-page earthy-panel">
    <header class="dashboard-header">
      <div>
        <p class="dashboard-eyebrow">内容管理后台</p>
        <h1>哈尼梯田红米网站初版后台</h1>
      </div>
      <div class="header-actions">
        <el-button @click="refreshAll">刷新数据</el-button>
        <el-button type="danger" plain @click="handleLogout">退出登录</el-button>
      </div>
    </header>

    <main class="dashboard-main surface-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="轮播图管理" name="banners">
          <section class="panel-toolbar">
            <span>支持排序、上下架、文案与跳转链接编辑</span>
            <el-button type="primary" @click="openBannerDialog()">新增轮播图</el-button>
          </section>
          <el-table :data="bannerState.items" v-loading="bannerState.loading">
            <el-table-column prop="sort_order" label="排序" width="90" />
            <el-table-column prop="title" label="标题" min-width="220" />
            <el-table-column prop="subtitle" label="副标题" min-width="180" />
            <el-table-column prop="image_url" label="图片链接" min-width="240" show-overflow-tooltip />
            <el-table-column label="状态" width="100">
              <template #default="scope">{{ scope.row.is_active ? "启用" : "停用" }}</template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="scope">
                <el-button link type="primary" @click="openBannerDialog(scope.row)">编辑</el-button>
                <el-button link type="danger" @click="handleDelete('banner', scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            class="pager"
            background
            layout="total, prev, pager, next"
            :total="bannerState.total"
            :current-page="bannerState.page"
            :page-size="bannerState.pageSize"
            @current-change="(page) => loadBanners(page)"
          />
        </el-tab-pane>

        <el-tab-pane label="板块管理" name="sections">
          <section class="panel-toolbar">
            <span>维护首页核心卖点、品牌故事、产业振兴及导语区块</span>
            <el-button type="primary" @click="openSectionDialog()">新增板块</el-button>
          </section>
          <el-table :data="sectionState.items" v-loading="sectionState.loading">
            <el-table-column prop="sort_order" label="排序" width="90" />
            <el-table-column prop="name" label="名称" width="150" />
            <el-table-column prop="key" label="Key" width="140" />
            <el-table-column prop="title" label="标题" min-width="200" />
            <el-table-column prop="subtitle" label="副标题" min-width="180" />
            <el-table-column label="状态" width="100">
              <template #default="scope">{{ scope.row.is_active ? "启用" : "停用" }}</template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="scope">
                <el-button link type="primary" @click="openSectionDialog(scope.row)">编辑</el-button>
                <el-button link type="danger" @click="handleDelete('section', scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            class="pager"
            background
            layout="total, prev, pager, next"
            :total="sectionState.total"
            :current-page="sectionState.page"
            :page-size="sectionState.pageSize"
            @current-change="(page) => loadSections(page)"
          />
        </el-tab-pane>

        <el-tab-pane label="产品管理" name="products">
          <section class="panel-toolbar">
            <span>参数字段使用 JSON 文本录入，前端自动解析展示</span>
            <el-button type="primary" @click="openProductDialog()">新增产品</el-button>
          </section>
          <el-table :data="productState.items" v-loading="productState.loading">
            <el-table-column prop="sort_order" label="排序" width="90" />
            <el-table-column prop="name" label="产品名称" min-width="180" />
            <el-table-column prop="subtitle" label="产品副标题" min-width="180" />
            <el-table-column prop="cover_image" label="图片链接" min-width="220" show-overflow-tooltip />
            <el-table-column label="状态" width="100">
              <template #default="scope">{{ scope.row.is_active ? "启用" : "停用" }}</template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="scope">
                <el-button link type="primary" @click="openProductDialog(scope.row)">编辑</el-button>
                <el-button link type="danger" @click="handleDelete('product', scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            class="pager"
            background
            layout="total, prev, pager, next"
            :total="productState.total"
            :current-page="productState.page"
            :page-size="productState.pageSize"
            @current-change="(page) => loadProducts(page)"
          />
        </el-tab-pane>

        <el-tab-pane label="新闻管理" name="news">
          <section class="panel-toolbar">
            <span>发布企业动态、品牌活动和助农项目内容</span>
            <el-button type="primary" @click="openNewsDialog()">新增新闻</el-button>
          </section>
          <el-table :data="newsState.items" v-loading="newsState.loading">
            <el-table-column prop="sort_order" label="排序" width="90" />
            <el-table-column prop="title" label="新闻标题" min-width="220" />
            <el-table-column prop="summary" label="摘要" min-width="220" show-overflow-tooltip />
            <el-table-column label="发布时间" min-width="180">
              <template #default="scope">{{ formatDate(scope.row.published_at) }}</template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="scope">{{ scope.row.is_active ? "启用" : "停用" }}</template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="scope">
                <el-button link type="primary" @click="openNewsDialog(scope.row)">编辑</el-button>
                <el-button link type="danger" @click="handleDelete('news', scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            class="pager"
            background
            layout="total, prev, pager, next"
            :total="newsState.total"
            :current-page="newsState.page"
            :page-size="newsState.pageSize"
            @current-change="(page) => loadNews(page)"
          />
        </el-tab-pane>

        <el-tab-pane label="站点配置" name="site-settings">
          <section class="panel-toolbar">
            <span>维护页脚二维码、说明文字和备案信息，保存后首页自动通过接口读取</span>
            <el-button type="primary" :loading="footerSettingsState.saving" @click="submitFooterSettings">保存配置</el-button>
          </section>

          <div class="site-setting-panel" v-loading="footerSettingsState.loading">
            <el-row :gutter="22">
              <el-col :lg="12" :md="24">
                <section class="site-card surface-card">
                  <div class="site-card-header">
                    <h3>二维码展示</h3>
                    <el-switch v-model="footerSettingsState.form.qr_is_active" />
                  </div>

                  <div class="qr-preview-wrap">
                    <div class="qr-preview-panel">
                      <img v-if="footerSettingsState.form.qr_image_url" :src="footerSettingsState.form.qr_image_url" :alt="footerSettingsState.form.qr_name || '页脚二维码'" />
                      <el-empty v-else description="尚未上传二维码" />
                    </div>

                    <div class="qr-actions">
                      <el-upload accept="image/*" :show-file-list="false" :http-request="handleFooterQrUpload">
                        <el-button type="primary" :loading="footerSettingsState.uploading">上传二维码</el-button>
                      </el-upload>
                      <el-button plain @click="clearFooterQrImage">清空图片</el-button>
                      <span class="upload-tip">建议上传清晰的正方形二维码，前台默认 150 × 150px，移动端自动缩小。</span>
                    </div>
                  </div>

                  <el-form label-position="top" :model="footerSettingsState.form">
                    <el-form-item label="二维码标题">
                      <el-input v-model="footerSettingsState.form.qr_name" placeholder="例如：扫码关注我们" />
                    </el-form-item>
                    <el-form-item label="说明文字">
                      <el-input v-model="footerSettingsState.form.qr_description" maxlength="255" show-word-limit placeholder="例如：扫码关注我们，了解红河梯田新讯" />
                    </el-form-item>
                    <el-form-item label="图片链接">
                      <el-input v-model="footerSettingsState.form.qr_image_url" placeholder="上传后自动回填，也支持手动填写" />
                    </el-form-item>
                  </el-form>
                </section>
              </el-col>

              <el-col :lg="12" :md="24">
                <section class="site-card surface-card">
                  <div class="site-card-header">
                    <h3>备案信息展示</h3>
                    <el-switch v-model="footerSettingsState.form.filing_is_active" />
                  </div>

                  <el-form label-position="top" :model="footerSettingsState.form">
                    <el-form-item label="备案信息标题">
                      <el-input v-model="footerSettingsState.form.filing_name" placeholder="例如：备案信息" />
                    </el-form-item>
                    <el-form-item label="备案信息内容">
                      <el-input
                        v-model="footerSettingsState.form.filing_text"
                        type="textarea"
                        :rows="5"
                        maxlength="255"
                        show-word-limit
                        placeholder="例如：滇ICP备2026000001号-1"
                      />
                    </el-form-item>
                  </el-form>

                  <div class="filing-preview surface-card">
                    <span class="filing-preview-label">{{ footerSettingsState.form.filing_name || '备案信息' }}</span>
                    <p>{{ footerSettingsState.form.filing_text || '备案信息将在这里展示。' }}</p>
                  </div>
                </section>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
      </el-tabs>
    </main>

    <el-dialog v-model="bannerDialog.visible" :title="bannerDialog.form.id ? '编辑轮播图' : '新增轮播图'" width="720px">
      <el-form label-position="top" :model="bannerDialog.form">
        <el-row :gutter="16">
          <el-col :md="12">
            <el-form-item label="标题"><el-input v-model="bannerDialog.form.title" /></el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="副标题"><el-input v-model="bannerDialog.form.subtitle" /></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述"><el-input v-model="bannerDialog.form.description" type="textarea" :rows="4" /></el-form-item>
        <el-form-item label="图片链接"><el-input v-model="bannerDialog.form.image_url" /></el-form-item>
        <el-row :gutter="16">
          <el-col :md="12">
            <el-form-item label="按钮文字"><el-input v-model="bannerDialog.form.cta_text" /></el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="按钮链接"><el-input v-model="bannerDialog.form.cta_link" /></el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :md="12">
            <el-form-item label="排序"><el-input-number v-model="bannerDialog.form.sort_order" :min="0" /></el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="是否启用"><el-switch v-model="bannerDialog.form.is_active" /></el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="bannerDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="bannerDialog.submitting" @click="submitBanner">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="sectionDialog.visible" :title="sectionDialog.form.id ? '编辑板块' : '新增板块'" width="760px">
      <el-form label-position="top" :model="sectionDialog.form">
        <el-row :gutter="16">
          <el-col :md="12">
            <el-form-item label="板块名称"><el-input v-model="sectionDialog.form.name" /></el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="板块 Key"><el-input v-model="sectionDialog.form.key" placeholder="如 brand_story" /></el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :md="12">
            <el-form-item label="标题"><el-input v-model="sectionDialog.form.title" /></el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="副标题"><el-input v-model="sectionDialog.form.subtitle" /></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="正文"><el-input v-model="sectionDialog.form.body" type="textarea" :rows="5" /></el-form-item>
        <el-form-item label="配图链接"><el-input v-model="sectionDialog.form.image_url" /></el-form-item>
        <el-form-item label="扩展 JSON"><el-input v-model="sectionDialog.form.extra_json" type="textarea" :rows="5" placeholder='{"tags": ["生态"], "stats": [{"label": "海拔", "value": "1400m+"}]}' /></el-form-item>
        <el-row :gutter="16">
          <el-col :md="12">
            <el-form-item label="排序"><el-input-number v-model="sectionDialog.form.sort_order" :min="0" /></el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="是否启用"><el-switch v-model="sectionDialog.form.is_active" /></el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="sectionDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="sectionDialog.submitting" @click="submitSection">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="productDialog.visible" :title="productDialog.form.id ? '编辑产品' : '新增产品'" width="760px">
      <el-form label-position="top" :model="productDialog.form">
        <el-row :gutter="16">
          <el-col :md="12">
            <el-form-item label="产品名称"><el-input v-model="productDialog.form.name" /></el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="产品副标题"><el-input v-model="productDialog.form.subtitle" /></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述"><el-input v-model="productDialog.form.description" type="textarea" :rows="5" /></el-form-item>
        <el-form-item label="产品图片链接"><el-input v-model="productDialog.form.cover_image" /></el-form-item>
        <el-form-item label="参数 JSON"><el-input v-model="productDialog.form.specs_json" type="textarea" :rows="5" placeholder='{"净含量": "2kg", "口感": "糯香"}' /></el-form-item>
        <el-row :gutter="16">
          <el-col :md="12">
            <el-form-item label="排序"><el-input-number v-model="productDialog.form.sort_order" :min="0" /></el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="是否启用"><el-switch v-model="productDialog.form.is_active" /></el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="productDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="productDialog.submitting" @click="submitProduct">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="newsDialog.visible" :title="newsDialog.form.id ? '编辑新闻' : '新增新闻'" width="760px">
      <el-form label-position="top" :model="newsDialog.form">
        <el-form-item label="新闻标题"><el-input v-model="newsDialog.form.title" /></el-form-item>
        <el-form-item label="新闻摘要"><el-input v-model="newsDialog.form.summary" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="正文"><el-input v-model="newsDialog.form.content" type="textarea" :rows="6" /></el-form-item>
        <el-form-item label="封面链接"><el-input v-model="newsDialog.form.cover_image" /></el-form-item>
        <el-row :gutter="16">
          <el-col :md="12">
            <el-form-item label="发布时间">
              <el-date-picker
                v-model="newsDialog.form.published_at"
                type="datetime"
                value-format="YYYY-MM-DDTHH:mm:ss"
                placeholder="选择发布时间"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :md="6">
            <el-form-item label="排序"><el-input-number v-model="newsDialog.form.sort_order" :min="0" /></el-form-item>
          </el-col>
          <el-col :md="6">
            <el-form-item label="是否启用"><el-switch v-model="newsDialog.form.is_active" /></el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="newsDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="newsDialog.submitting" @click="submitNews">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ElMessage, ElMessageBox } from "element-plus";
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import {
  createBanner,
  createNews,
  createProduct,
  createSection,
  deleteBanner,
  deleteNews,
  deleteProduct,
  deleteSection,
  fetchBanners,
  fetchFooterSettings,
  fetchNews,
  fetchProducts,
  fetchSections,
  saveFooterSettings,
  updateBanner,
  updateNews,
  updateProduct,
  updateSection,
  uploadSiteSettingImage,
} from "../../api/content";
import { clearToken } from "../../utils/auth";

const router = useRouter();
const activeTab = ref("banners");

const createListState = (pageSize) => reactive({
  items: [],
  total: 0,
  page: 1,
  pageSize,
  loading: false,
});

const bannerState = createListState(10);
const sectionState = createListState(20);
const productState = createListState(12);
const newsState = createListState(10);

const createBannerForm = () => ({
  id: null,
  title: "",
  subtitle: "",
  description: "",
  image_url: "",
  cta_text: "",
  cta_link: "",
  sort_order: 0,
  is_active: true,
});

const createSectionForm = () => ({
  id: null,
  key: "",
  name: "",
  title: "",
  subtitle: "",
  body: "",
  image_url: "",
  extra_json: "",
  sort_order: 0,
  is_active: true,
});

const createProductForm = () => ({
  id: null,
  name: "",
  subtitle: "",
  description: "",
  cover_image: "",
  specs_json: "",
  sort_order: 0,
  is_active: true,
});

const createNewsForm = () => ({
  id: null,
  title: "",
  summary: "",
  content: "",
  cover_image: "",
  published_at: new Date().toISOString().slice(0, 19),
  sort_order: 0,
  is_active: true,
});

const createFooterSettingsForm = () => ({
  qr_name: "页脚二维码",
  qr_description: "扫码关注我们",
  qr_image_url: "",
  qr_is_active: true,
  filing_name: "备案信息",
  filing_text: "",
  filing_is_active: true,
});

const bannerDialog = reactive({ visible: false, submitting: false, form: createBannerForm() });
const sectionDialog = reactive({ visible: false, submitting: false, form: createSectionForm() });
const productDialog = reactive({ visible: false, submitting: false, form: createProductForm() });
const newsDialog = reactive({ visible: false, submitting: false, form: createNewsForm() });
const footerSettingsState = reactive({
  loading: false,
  saving: false,
  uploading: false,
  form: createFooterSettingsForm(),
});

const syncList = (state, data, page) => {
  state.items = data.items;
  state.total = data.total;
  state.page = page;
};

const loadBanners = async (page = bannerState.page) => {
  bannerState.loading = true;
  try {
    syncList(bannerState, await fetchBanners({ page, page_size: bannerState.pageSize }), page);
  } finally {
    bannerState.loading = false;
  }
};

const loadSections = async (page = sectionState.page) => {
  sectionState.loading = true;
  try {
    syncList(sectionState, await fetchSections({ page, page_size: sectionState.pageSize }), page);
  } finally {
    sectionState.loading = false;
  }
};

const loadProducts = async (page = productState.page) => {
  productState.loading = true;
  try {
    syncList(productState, await fetchProducts({ page, page_size: productState.pageSize }), page);
  } finally {
    productState.loading = false;
  }
};

const loadNews = async (page = newsState.page) => {
  newsState.loading = true;
  try {
    syncList(newsState, await fetchNews({ page, page_size: newsState.pageSize }), page);
  } finally {
    newsState.loading = false;
  }
};

const loadFooterSettings = async () => {
  footerSettingsState.loading = true;
  try {
    const data = await fetchFooterSettings();
    footerSettingsState.form = {
      qr_name: data.footer_qr?.name || "页脚二维码",
      qr_description: data.footer_qr?.description || "",
      qr_image_url: data.footer_qr?.image_url || "",
      qr_is_active: data.footer_qr?.is_active ?? true,
      filing_name: data.footer_filing?.name || "备案信息",
      filing_text: data.footer_filing?.description || "",
      filing_is_active: data.footer_filing?.is_active ?? true,
    };
  } finally {
    footerSettingsState.loading = false;
  }
};

const buildFooterSettingsPayload = () => ({
  qr_name: footerSettingsState.form.qr_name,
  qr_description: footerSettingsState.form.qr_description,
  qr_image_url: footerSettingsState.form.qr_image_url,
  qr_is_active: footerSettingsState.form.qr_is_active,
  filing_name: footerSettingsState.form.filing_name,
  filing_text: footerSettingsState.form.filing_text,
  filing_is_active: footerSettingsState.form.filing_is_active,
});

const refreshAll = async () => {
  try {
    await Promise.all([loadBanners(), loadSections(), loadProducts(), loadNews(), loadFooterSettings()]);
    ElMessage.success("数据已刷新");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "数据刷新失败");
  }
};

const openBannerDialog = (row = null) => {
  bannerDialog.form = row ? { ...row } : createBannerForm();
  bannerDialog.visible = true;
};

const openSectionDialog = (row = null) => {
  sectionDialog.form = row ? { ...row } : createSectionForm();
  sectionDialog.visible = true;
};

const openProductDialog = (row = null) => {
  productDialog.form = row ? { ...row } : createProductForm();
  productDialog.visible = true;
};

const openNewsDialog = (row = null) => {
  newsDialog.form = row
    ? { ...row, published_at: row.published_at ? row.published_at.slice(0, 19) : createNewsForm().published_at }
    : createNewsForm();
  newsDialog.visible = true;
};

const submitBanner = async () => {
  bannerDialog.submitting = true;
  try {
    if (bannerDialog.form.id) {
      await updateBanner(bannerDialog.form.id, { ...bannerDialog.form });
    } else {
      await createBanner(bannerDialog.form);
    }
    bannerDialog.visible = false;
    await loadBanners();
    ElMessage.success("轮播图已保存");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "轮播图保存失败");
  } finally {
    bannerDialog.submitting = false;
  }
};

const submitSection = async () => {
  sectionDialog.submitting = true;
  try {
    if (sectionDialog.form.extra_json) {
      JSON.parse(sectionDialog.form.extra_json);
    }
    if (sectionDialog.form.id) {
      await updateSection(sectionDialog.form.id, { ...sectionDialog.form });
    } else {
      await createSection(sectionDialog.form);
    }
    sectionDialog.visible = false;
    await loadSections();
    ElMessage.success("板块内容已保存");
  } catch (error) {
    ElMessage.error(error.message.includes("JSON") ? "扩展 JSON 格式错误" : error.response?.data?.detail || "板块保存失败");
  } finally {
    sectionDialog.submitting = false;
  }
};

const submitProduct = async () => {
  productDialog.submitting = true;
  try {
    if (productDialog.form.specs_json) {
      JSON.parse(productDialog.form.specs_json);
    }
    if (productDialog.form.id) {
      await updateProduct(productDialog.form.id, { ...productDialog.form });
    } else {
      await createProduct(productDialog.form);
    }
    productDialog.visible = false;
    await loadProducts();
    ElMessage.success("产品已保存");
  } catch (error) {
    ElMessage.error(error.message.includes("JSON") ? "参数 JSON 格式错误" : error.response?.data?.detail || "产品保存失败");
  } finally {
    productDialog.submitting = false;
  }
};

const submitNews = async () => {
  newsDialog.submitting = true;
  try {
    if (newsDialog.form.id) {
      await updateNews(newsDialog.form.id, { ...newsDialog.form });
    } else {
      await createNews(newsDialog.form);
    }
    newsDialog.visible = false;
    await loadNews();
    ElMessage.success("新闻已保存");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "新闻保存失败");
  } finally {
    newsDialog.submitting = false;
  }
};

const submitFooterSettings = async () => {
  footerSettingsState.saving = true;
  try {
    const data = await saveFooterSettings(buildFooterSettingsPayload());
    footerSettingsState.form = {
      qr_name: data.footer_qr?.name || "页脚二维码",
      qr_description: data.footer_qr?.description || "",
      qr_image_url: data.footer_qr?.image_url || "",
      qr_is_active: data.footer_qr?.is_active ?? true,
      filing_name: data.footer_filing?.name || "备案信息",
      filing_text: data.footer_filing?.description || "",
      filing_is_active: data.footer_filing?.is_active ?? true,
    };
    ElMessage.success("页脚配置已保存");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "页脚配置保存失败");
  } finally {
    footerSettingsState.saving = false;
  }
};

const handleFooterQrUpload = async (options) => {
  footerSettingsState.uploading = true;
  try {
    const data = await uploadSiteSettingImage(options.file);
    footerSettingsState.form.qr_image_url = data.url;
    options.onSuccess?.(data);
    ElMessage.success("二维码图片上传成功");
  } catch (error) {
    options.onError?.(error);
    ElMessage.error(error.response?.data?.detail || "二维码图片上传失败");
  } finally {
    footerSettingsState.uploading = false;
  }
};

const clearFooterQrImage = () => {
  footerSettingsState.form.qr_image_url = "";
};

const handleDelete = async (type, row) => {
  try {
    await ElMessageBox.confirm(`确认删除“${row.title || row.name}”吗？`, "删除确认", {
      type: "warning",
    });
    if (type === "banner") {
      await deleteBanner(row.id);
      await loadBanners();
    }
    if (type === "section") {
      await deleteSection(row.id);
      await loadSections();
    }
    if (type === "product") {
      await deleteProduct(row.id);
      await loadProducts();
    }
    if (type === "news") {
      await deleteNews(row.id);
      await loadNews();
    }
    ElMessage.success("删除成功");
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error(error.response?.data?.detail || "删除失败");
    }
  }
};

const handleLogout = () => {
  clearToken();
  router.push({ name: "admin-login" });
};

const formatDate = (value) => {
  if (!value) return "";
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
};

onMounted(refreshAll);
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  padding: 24px;
  background: linear-gradient(180deg, #ede2cf, #faf5ec);
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  width: min(1280px, 100%);
  margin: 0 auto 20px;
}

.dashboard-eyebrow {
  margin: 0 0 10px;
  color: var(--color-secondary);
  letter-spacing: 0.16em;
}

.dashboard-header h1 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(28px, 4vw, 42px);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.dashboard-main {
  width: min(1280px, 100%);
  margin: 0 auto;
  padding: 24px;
}

.panel-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 18px;
  color: var(--color-text-soft);
}

.pager {
  justify-content: flex-end;
  margin-top: 18px;
}

.site-setting-panel {
  padding-top: 6px;
}

.site-card {
  height: 100%;
  padding: 24px;
  border-radius: 24px;
}

.site-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.site-card-header h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 24px;
}

.qr-preview-wrap {
  display: grid;
  grid-template-columns: minmax(190px, 220px) minmax(0, 1fr);
  gap: 18px;
  margin-bottom: 22px;
}

.qr-preview-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 220px;
  padding: 18px;
  border-radius: 22px;
  background: rgba(255, 250, 242, 0.88);
  border: 1px solid rgba(99, 66, 42, 0.08);
}

.qr-preview-panel img {
  width: 100%;
  max-width: 170px;
  aspect-ratio: 1 / 1;
  object-fit: contain;
}

.qr-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
}

.upload-tip {
  color: var(--color-text-soft);
  line-height: 1.7;
}

.filing-preview {
  margin-top: 10px;
  padding: 18px;
  border-radius: 20px;
  background: rgba(110, 134, 97, 0.08);
}

.filing-preview-label {
  display: inline-block;
  margin-bottom: 8px;
  color: var(--color-secondary);
  letter-spacing: 0.12em;
}

.filing-preview p {
  margin: 0;
  color: var(--color-text-soft);
  line-height: 1.7;
  word-break: break-all;
}

@media (max-width: 900px) {
  .dashboard-header,
  .panel-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .qr-preview-wrap {
    grid-template-columns: 1fr;
  }
}
</style>