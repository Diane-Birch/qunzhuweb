<template>
  <div class="dashboard-page earthy-panel">
    <header class="dashboard-header">
      <div>
        <p class="dashboard-eyebrow">内容管理后台</p>
        <h1>红河文化后台管理</h1>
      </div>
      <div class="header-actions">
        <el-button @click="refreshAll">刷新数据</el-button>
        <el-button type="danger" plain @click="handleLogout">退出登录</el-button>
      </div>
    </header>

    <main class="dashboard-main surface-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="轮播图" name="banners">
          <section class="panel-toolbar">
            <span>在这里管理轮播图的排序、发布状态、按钮文案、媒体类型和文字样式。</span>
            <el-button type="primary" @click="openBannerDialog()">新增轮播图</el-button>
          </section>
          <el-table :data="bannerState.items" v-loading="bannerState.loading">
            <el-table-column prop="sort_order" label="排序" width="90" />
            <el-table-column prop="title" label="标题" min-width="220" />
            <el-table-column label="媒体" width="100">
              <template #default="scope">{{ resolveMediaType(scope.row.media_type) }}</template>
            </el-table-column>
            <el-table-column label="文字位置" min-width="140">
              <template #default="scope">{{ getPositionLabel(scope.row.text_position) }}</template>
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

        <el-tab-pane label="版块管理" name="sections">
          <section class="panel-toolbar">
            <span>管理首页文化版块、介绍内容及其配套媒体素材。</span>
            <el-button type="primary" @click="openSectionDialog()">新增版块</el-button>
          </section>
          <el-table :data="sectionState.items" v-loading="sectionState.loading">
            <el-table-column prop="sort_order" label="排序" width="90" />
            <el-table-column prop="name" label="名称" width="150" />
            <el-table-column prop="key" label="标识" width="140" />
            <el-table-column prop="title" label="标题" min-width="220" />
            <el-table-column label="媒体" width="100">
              <template #default="scope">{{ resolveMediaType(scope.row.media_type) }}</template>
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
            <span>规格 JSON 仍可编辑，媒体内容支持图片或视频二选一。</span>
            <el-button type="primary" @click="openProductDialog()">新增产品</el-button>
          </section>
          <el-table :data="productState.items" v-loading="productState.loading">
            <el-table-column prop="sort_order" label="排序" width="90" />
            <el-table-column prop="name" label="产品名称" min-width="180" />
            <el-table-column prop="subtitle" label="副标题" min-width="180" />
            <el-table-column label="媒体" width="100">
              <template #default="scope">{{ resolveMediaType(scope.row.media_type) }}</template>
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

        <el-tab-pane label="动态管理" name="news">
          <section class="panel-toolbar">
            <span>动态卡片支持图片封面或视频封面二选一。</span>
            <el-button type="primary" @click="openNewsDialog()">新增动态</el-button>
          </section>
          <el-table :data="newsState.items" v-loading="newsState.loading">
            <el-table-column prop="sort_order" label="排序" width="90" />
            <el-table-column prop="title" label="标题" min-width="220" />
            <el-table-column prop="summary" label="摘要" min-width="220" show-overflow-tooltip />
            <el-table-column label="媒体" width="100">
              <template #default="scope">{{ resolveMediaType(scope.row.media_type) }}</template>
            </el-table-column>
            <el-table-column label="发布时间" min-width="180">
              <template #default="scope">{{ formatDate(scope.row.published_at) }}</template>
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

        <el-tab-pane label="站点设置" name="site-settings">
          <section class="panel-toolbar">
            <span>管理首页底部二维码区域和备案信息区域。</span>
            <el-button type="primary" :loading="footerSettingsState.saving" @click="submitFooterSettings">保存设置</el-button>
          </section>

          <div class="site-setting-panel" v-loading="footerSettingsState.loading">
            <el-row :gutter="22">
              <el-col :lg="12" :md="24">
                <section class="site-card surface-card">
                  <div class="site-card-header">
                    <h3>二维码区域</h3>
                    <el-switch v-model="footerSettingsState.form.qr_is_active" />
                  </div>
                  <MediaField
                    :mode="'image'"
                    :allow-video="false"
                    label="二维码图片"
                    v-model:image-url="footerSettingsState.form.qr_image_url"
                    image-placeholder="支持输入图片链接，或上传本地图片"
                    image-tip="首页底部将直接渲染这里保存的二维码图片。"
                  />
                  <el-form label-position="top" :model="footerSettingsState.form">
                    <el-form-item label="二维码标题">
                      <el-input v-model="footerSettingsState.form.qr_name" />
                    </el-form-item>
                    <el-form-item label="二维码说明">
                      <el-input v-model="footerSettingsState.form.qr_description" maxlength="255" show-word-limit />
                    </el-form-item>
                  </el-form>
                </section>
              </el-col>

              <el-col :lg="12" :md="24">
                <section class="site-card surface-card">
                  <div class="site-card-header">
                    <h3>备案区域</h3>
                    <el-switch v-model="footerSettingsState.form.filing_is_active" />
                  </div>
                  <el-form label-position="top" :model="footerSettingsState.form">
                    <el-form-item label="备案标题">
                      <el-input v-model="footerSettingsState.form.filing_name" />
                    </el-form-item>
                    <el-form-item label="备案内容">
                      <el-input v-model="footerSettingsState.form.filing_text" type="textarea" :rows="5" maxlength="255" show-word-limit />
                    </el-form-item>
                  </el-form>
                  <div class="filing-preview surface-card">
                    <span class="filing-preview-label">{{ footerSettingsState.form.filing_name || '备案信息' }}</span>
                    <p>{{ footerSettingsState.form.filing_text || '备案信息将在这里显示。' }}</p>
                  </div>
                </section>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
      </el-tabs>
    </main>

    <el-dialog v-model="bannerDialog.visible" :title="bannerDialog.form.id ? '编辑轮播图' : '新增轮播图'" width="860px">
      <el-form label-position="top" :model="bannerDialog.form">
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="标题"><el-input v-model="bannerDialog.form.title" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="副标题"><el-input v-model="bannerDialog.form.subtitle" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="描述"><el-input v-model="bannerDialog.form.description" type="textarea" :rows="4" /></el-form-item>
        <MediaField label="轮播图媒体" v-model:mode="bannerDialog.form.media_type" v-model:image-url="bannerDialog.form.image_url" v-model:video-url="bannerDialog.form.video_url" />
        <div class="style-grid">
          <div class="style-group surface-card">
            <h4>标题字号</h4>
            <div class="size-control">
              <el-select :model-value="bannerDialog.form.title_font_size" @change="(value) => applyBannerSizePreset('title_font_size', value)">
                <el-option v-for="option in titleSizeOptions" :key="option.value" :label="option.label" :value="option.value" />
              </el-select>
              <el-input-number v-model="bannerDialog.form.title_font_size" :min="12" :max="160" />
            </div>
          </div>
          <div class="style-group surface-card">
            <h4>副标题字号</h4>
            <div class="size-control">
              <el-select :model-value="bannerDialog.form.subtitle_font_size" @change="(value) => applyBannerSizePreset('subtitle_font_size', value)">
                <el-option v-for="option in subtitleSizeOptions" :key="option.value" :label="option.label" :value="option.value" />
              </el-select>
              <el-input-number v-model="bannerDialog.form.subtitle_font_size" :min="10" :max="72" />
            </div>
          </div>
          <div class="style-group surface-card">
            <h4>描述字号</h4>
            <div class="size-control">
              <el-select :model-value="bannerDialog.form.description_font_size" @change="(value) => applyBannerSizePreset('description_font_size', value)">
                <el-option v-for="option in descriptionSizeOptions" :key="option.value" :label="option.label" :value="option.value" />
              </el-select>
              <el-input-number v-model="bannerDialog.form.description_font_size" :min="10" :max="72" />
            </div>
          </div>
          <div class="style-group surface-card">
            <h4>文案位置</h4>
            <el-select v-model="bannerDialog.form.text_position">
              <el-option v-for="option in positionOptions" :key="option.value" :label="option.label" :value="option.value" />
            </el-select>
          </div>
        </div>
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="按钮文案"><el-input v-model="bannerDialog.form.cta_text" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="按钮链接"><el-input v-model="bannerDialog.form.cta_link" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="排序"><el-input-number v-model="bannerDialog.form.sort_order" :min="0" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="启用"><el-switch v-model="bannerDialog.form.is_active" /></el-form-item></el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="bannerDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="bannerDialog.submitting" @click="submitBanner">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="sectionDialog.visible" :title="sectionDialog.form.id ? '编辑版块' : '新增版块'" width="820px">
      <el-form label-position="top" :model="sectionDialog.form">
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="版块名称"><el-input v-model="sectionDialog.form.name" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="版块标识"><el-input v-model="sectionDialog.form.key" placeholder="brand_story" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="标题"><el-input v-model="sectionDialog.form.title" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="副标题"><el-input v-model="sectionDialog.form.subtitle" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="正文"><el-input v-model="sectionDialog.form.body" type="textarea" :rows="5" /></el-form-item>
        <MediaField label="版块媒体" v-model:mode="sectionDialog.form.media_type" v-model:image-url="sectionDialog.form.image_url" v-model:video-url="sectionDialog.form.video_url" />
        <el-form-item label="扩展 JSON"><el-input v-model="sectionDialog.form.extra_json" type="textarea" :rows="5" placeholder='{"tags": ["eco"], "stats": [{"label": "Altitude", "value": "1400m+"}]}' /></el-form-item>
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="排序"><el-input-number v-model="sectionDialog.form.sort_order" :min="0" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="启用"><el-switch v-model="sectionDialog.form.is_active" /></el-form-item></el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="sectionDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="sectionDialog.submitting" @click="submitSection">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="productDialog.visible" :title="productDialog.form.id ? '编辑产品' : '新增产品'" width="820px">
      <el-form label-position="top" :model="productDialog.form">
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="产品名称"><el-input v-model="productDialog.form.name" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="副标题"><el-input v-model="productDialog.form.subtitle" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="描述"><el-input v-model="productDialog.form.description" type="textarea" :rows="5" /></el-form-item>
        <MediaField label="产品媒体" v-model:mode="productDialog.form.media_type" v-model:image-url="productDialog.form.cover_image" v-model:video-url="productDialog.form.video_url" />
        <el-form-item label="规格 JSON"><el-input v-model="productDialog.form.specs_json" type="textarea" :rows="5" placeholder='{"Net Weight": "2kg", "Texture": "soft"}' /></el-form-item>
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="排序"><el-input-number v-model="productDialog.form.sort_order" :min="0" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="启用"><el-switch v-model="productDialog.form.is_active" /></el-form-item></el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="productDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="productDialog.submitting" @click="submitProduct">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="newsDialog.visible" :title="newsDialog.form.id ? '编辑动态' : '新增动态'" width="820px">
      <el-form label-position="top" :model="newsDialog.form">
        <el-form-item label="标题"><el-input v-model="newsDialog.form.title" /></el-form-item>
        <el-form-item label="摘要"><el-input v-model="newsDialog.form.summary" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="正文内容"><el-input v-model="newsDialog.form.content" type="textarea" :rows="6" /></el-form-item>
        <MediaField label="动态媒体" v-model:mode="newsDialog.form.media_type" v-model:image-url="newsDialog.form.cover_image" v-model:video-url="newsDialog.form.video_url" />
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="发布时间"><el-date-picker v-model="newsDialog.form.published_at" type="datetime" value-format="YYYY-MM-DDTHH:mm:ss" placeholder="请选择时间" style="width: 100%" /></el-form-item></el-col>
          <el-col :md="6"><el-form-item label="排序"><el-input-number v-model="newsDialog.form.sort_order" :min="0" /></el-form-item></el-col>
          <el-col :md="6"><el-form-item label="启用"><el-switch v-model="newsDialog.form.is_active" /></el-form-item></el-col>
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

import MediaField from "../../components/admin/MediaField.vue";
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
} from "../../api/content";
import { clearToken } from "../../utils/auth";

const router = useRouter();
const activeTab = ref("banners");
const titleSizeOptions = [
  { label: "展示大号 72px", value: 72 },
  { label: "主视觉 84px", value: 84 },
  { label: "紧凑 60px", value: 60 },
];
const subtitleSizeOptions = [
  { label: "轻量 13px", value: 13 },
  { label: "舒适 16px", value: 16 },
  { label: "醒目 18px", value: 18 },
];
const descriptionSizeOptions = [
  { label: "标准 17px", value: 17 },
  { label: "舒适 19px", value: 19 },
  { label: "紧凑 15px", value: 15 },
];
const positionOptions = [
  { label: "左侧居中", value: "left-center" },
  { label: "居中", value: "center" },
  { label: "右侧居中", value: "right-center" },
  { label: "左上", value: "left-top" },
  { label: "上方居中", value: "center-top" },
  { label: "右上", value: "right-top" },
  { label: "左下", value: "left-bottom" },
  { label: "下方居中", value: "center-bottom" },
  { label: "右下", value: "right-bottom" },
];

const createListState = (pageSize) => reactive({ items: [], total: 0, page: 1, pageSize, loading: false });
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
  media_type: "image",
  video_url: "",
  cta_text: "",
  cta_link: "",
  title_font_size: 72,
  subtitle_font_size: 13,
  description_font_size: 17,
  text_position: "left-center",
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
  media_type: "image",
  video_url: "",
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
  media_type: "image",
  video_url: "",
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
  media_type: "image",
  video_url: "",
  published_at: new Date().toISOString().slice(0, 19),
  sort_order: 0,
  is_active: true,
});
const createFooterSettingsForm = () => ({
  qr_name: "底部二维码",
  qr_description: "扫码关注",
  qr_image_url: "",
  qr_is_active: true,
  filing_name: "备案信息",
  filing_text: "",
  filing_is_active: true,
});

const normalizeMediaMode = (row) => row?.media_type || (row?.video_url ? "video" : "image");
const bannerDialog = reactive({ visible: false, submitting: false, form: createBannerForm() });
const sectionDialog = reactive({ visible: false, submitting: false, form: createSectionForm() });
const productDialog = reactive({ visible: false, submitting: false, form: createProductForm() });
const newsDialog = reactive({ visible: false, submitting: false, form: createNewsForm() });
const footerSettingsState = reactive({ loading: false, saving: false, form: createFooterSettingsForm() });

const syncList = (state, data, page) => {
  state.items = data.items;
  state.total = data.total;
  state.page = page;
};

const resolveMediaType = (value) => ((value || "image") === "video" ? "视频" : "图片");
const getPositionLabel = (value) => positionOptions.find((item) => item.value === (value || "left-center"))?.label || "左侧居中";
const resolveContentType = (type) => ({ banner: "轮播图", section: "版块", product: "产品", news: "动态" }[type] || "内容");
const applyBannerSizePreset = (field, value) => {
  bannerDialog.form[field] = value;
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
      qr_name: data.footer_qr?.name || "底部二维码",
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
  qr_name: footerSettingsState.form.qr_name || null,
  qr_description: footerSettingsState.form.qr_description || "",
  qr_image_url: footerSettingsState.form.qr_image_url || null,
  qr_is_active: Boolean(footerSettingsState.form.qr_is_active),
  filing_name: footerSettingsState.form.filing_name || null,
  filing_text: footerSettingsState.form.filing_text || "",
  filing_is_active: Boolean(footerSettingsState.form.filing_is_active),
});

const refreshAll = async () => {
  await Promise.all([loadBanners(1), loadSections(1), loadProducts(1), loadNews(1), loadFooterSettings()]);
};

const openBannerDialog = (row = null) => {
  bannerDialog.form = {
    ...createBannerForm(),
    ...(row || {}),
    media_type: normalizeMediaMode(row),
  };
  bannerDialog.visible = true;
};

const openSectionDialog = (row = null) => {
  sectionDialog.form = {
    ...createSectionForm(),
    ...(row || {}),
    media_type: normalizeMediaMode(row),
  };
  sectionDialog.visible = true;
};

const openProductDialog = (row = null) => {
  productDialog.form = {
    ...createProductForm(),
    ...(row || {}),
    media_type: normalizeMediaMode(row),
  };
  productDialog.visible = true;
};

const openNewsDialog = (row = null) => {
  newsDialog.form = {
    ...createNewsForm(),
    ...(row || {}),
    media_type: normalizeMediaMode(row),
    published_at: row?.published_at ? String(row.published_at).slice(0, 19) : createNewsForm().published_at,
  };
  newsDialog.visible = true;
};

const submitBanner = async () => {
  bannerDialog.submitting = true;
  try {
    const payload = { ...bannerDialog.form };
    if (payload.media_type === "video") {
      payload.image_url = null;
    } else {
      payload.video_url = null;
    }
    if (payload.id) {
      await updateBanner(payload.id, payload);
    } else {
      await createBanner(payload);
    }
    ElMessage.success("轮播图已保存");
    bannerDialog.visible = false;
    await loadBanners(payload.id ? bannerState.page : 1);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "轮播图保存失败");
  } finally {
    bannerDialog.submitting = false;
  }
};

const submitSection = async () => {
  sectionDialog.submitting = true;
  try {
    const payload = { ...sectionDialog.form };
    if (payload.media_type === "video") {
      payload.image_url = null;
    } else {
      payload.video_url = null;
    }
    if (payload.id) {
      await updateSection(payload.id, payload);
    } else {
      await createSection(payload);
    }
    ElMessage.success("版块已保存");
    sectionDialog.visible = false;
    await loadSections(payload.id ? sectionState.page : 1);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "版块保存失败");
  } finally {
    sectionDialog.submitting = false;
  }
};

const submitProduct = async () => {
  productDialog.submitting = true;
  try {
    const payload = { ...productDialog.form };
    if (payload.media_type === "video") {
      payload.cover_image = null;
    } else {
      payload.video_url = null;
    }
    if (payload.id) {
      await updateProduct(payload.id, payload);
    } else {
      await createProduct(payload);
    }
    ElMessage.success("产品已保存");
    productDialog.visible = false;
    await loadProducts(payload.id ? productState.page : 1);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "产品保存失败");
  } finally {
    productDialog.submitting = false;
  }
};
const submitNews = async () => {
  newsDialog.submitting = true;
  try {
    const payload = { ...newsDialog.form };
    if (payload.media_type === "video") {
      payload.cover_image = null;
    } else {
      payload.video_url = null;
    }
    if (payload.id) {
      await updateNews(payload.id, payload);
    } else {
      await createNews(payload);
    }
    ElMessage.success("动态已保存");
    newsDialog.visible = false;
    await loadNews(payload.id ? newsState.page : 1);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "动态保存失败");
  } finally {
    newsDialog.submitting = false;
  }
};

const submitFooterSettings = async () => {
  footerSettingsState.saving = true;
  try {
    await saveFooterSettings(buildFooterSettingsPayload());
    ElMessage.success("站点设置已保存");
    await loadFooterSettings();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "站点设置保存失败");
  } finally {
    footerSettingsState.saving = false;
  }
};

const handleDelete = async (type, row) => {
  try {
    await ElMessageBox.confirm(`确认删除该${resolveContentType(type)}吗？`, "删除确认", {
      type: "warning",
      confirmButtonText: "删除",
      cancelButtonText: "取消",
    });

    if (type === "banner") {
      await deleteBanner(row.id);
      await loadBanners(bannerState.page);
    } else if (type === "section") {
      await deleteSection(row.id);
      await loadSections(sectionState.page);
    } else if (type === "product") {
      await deleteProduct(row.id);
      await loadProducts(productState.page);
    } else if (type === "news") {
      await deleteNews(row.id);
      await loadNews(newsState.page);
    }

    ElMessage.success("内容已删除");
  } catch (error) {
    if (error === "cancel") {
      return;
    }
    ElMessage.error(error.response?.data?.detail || "删除失败");
  }
};

const handleLogout = async () => {
  clearToken();
  await router.push({ name: "admin-login" });
};

const formatDate = (value) => {
  if (!value) {
    return "";
  }
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
  max-width: 1320px;
  margin: 0 auto;
  padding: 32px 20px 56px;
}

.dashboard-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 22px;
}

.dashboard-eyebrow {
  margin: 0 0 10px;
  color: var(--color-secondary);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.dashboard-header h1 {
  margin: 0;
  font-family: var(--font-display);
  color: var(--color-primary-deep);
}

.header-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.dashboard-main {
  padding: 22px;
  border-radius: 28px;
}

.panel-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin: 8px 0 18px;
}

.panel-toolbar span {
  color: var(--color-text-soft);
  line-height: 1.6;
}

.pager {
  margin-top: 18px;
  justify-content: flex-end;
}

.site-setting-panel {
  padding-top: 8px;
}

.site-card {
  height: 100%;
  padding: 20px;
  border-radius: 24px;
}

.site-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.site-card-header h3,
.style-group h4 {
  margin: 0;
  font-family: var(--font-display);
  color: var(--color-primary-deep);
}

.filing-preview {
  margin-top: 16px;
  padding: 18px;
  border-radius: 18px;
}

.filing-preview-label {
  display: inline-flex;
  margin-bottom: 10px;
  color: var(--color-secondary);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.filing-preview p {
  margin: 0;
  color: var(--color-text-soft);
  line-height: 1.7;
}

.style-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin: 18px 0;
}

.style-group {
  padding: 16px;
  border-radius: 20px;
}

.size-control {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  margin-top: 12px;
}

@media (max-width: 960px) {
  .dashboard-header,
  .panel-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .dashboard-main {
    padding: 16px;
  }

  .style-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .dashboard-page {
    padding-inline: 12px;
  }

  .size-control {
    grid-template-columns: 1fr;
  }
}
</style>


