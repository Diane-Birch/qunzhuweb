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
            <span>点击一级板块行展开子内容，同一时间仅展开一个板块。</span>
            <el-button type="primary" :loading="sectionRootState.creating" @click="handleCreateSectionRoot">新增板块</el-button>
          </section>
          <div class="section-root-list" v-loading="sectionRootState.loading">
            <article
              v-for="root in sectionRootState.items"
              :key="root.id"
              class="section-root-card surface-card"
              :class="{ 'is-expanded': expandedSectionId === root.id }"
            >
              <button class="section-root-row" type="button" @click="toggleSectionRoot(root)">
                <div class="section-root-main">
                  <strong>{{ root.name }}</strong>
                  <span>{{ root.key }}</span>
                  <p>{{ root.title }}</p>
                </div>
                <div class="section-root-meta">
                  <span>排序 {{ root.sort_order }}</span>
                  <span>{{ root.content_count || 0 }} 条内容</span>
                  <div class="section-root-actions">
                    <el-button link type="primary" @click.stop="openSectionRootDialog(root)">编辑</el-button>
                    <el-button link type="danger" @click.stop="handleDelete('section-root', root)">删除</el-button>
                  </div>
                </div>
              </button>

              <transition name="section-expand">
                <div v-if="expandedSectionId === root.id" class="section-root-body">
                  <div class="section-root-body-head">
                    <div>
                      <strong>{{ resolveSectionSourceLabel(root.content_source) }}</strong>
                      <p>当前板块下的子内容仅在本板块内部维护。</p>
                    </div>
                    <el-button type="primary" plain @click="openChildDialog(root)">新增内容</el-button>
                  </div>

                  <div v-if="expandedSectionState.loading" class="surface-card section-child-loading">
                    <el-skeleton animated :rows="5" />
                  </div>

                  <el-table v-else :data="expandedSectionState.items">
                    <el-table-column label="标题" min-width="220">
                      <template #default="scope">{{ resolveExpandedItemTitle(scope.row, root) }}</template>
                    </el-table-column>
                    <el-table-column label="摘要" min-width="240" show-overflow-tooltip>
                      <template #default="scope">{{ resolveExpandedItemSummary(scope.row, root) }}</template>
                    </el-table-column>
                    <el-table-column label="媒体" width="100">
                      <template #default="scope">{{ resolveExpandedItemMediaType(scope.row, root) }}</template>
                    </el-table-column>
                    <el-table-column label="排序" width="120">
                      <template #default="scope">
                        <el-tag :type="scope.row.sort_order === 0 ? 'danger' : 'info'" effect="plain">
                          {{ resolveExpandedItemSortLabel(scope.row, root) }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column label="操作" width="250" fixed="right">
                      <template #default="scope">
                        <el-button link type="warning" :loading="expandedSectionState.togglingId === scope.row.id" @click="handleToggleExpandedPin(root, scope.row)">
                          {{ scope.row.sort_order === 0 ? '取消置顶' : '置顶' }}
                        </el-button>
                        <el-button link type="primary" @click="openChildDialog(root, scope.row)">编辑</el-button>
                        <el-button link type="danger" @click="handleDelete(resolveSectionDeleteType(root), scope.row)">删除</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </transition>
            </article>
          </div>
        </el-tab-pane>

        <el-tab-pane label="站点设置" name="site-settings">
          <section class="panel-toolbar">
            <span>管理首页底部多二维码区域和备案信息区域。</span>
            <el-button type="primary" :loading="footerSettingsState.saving" @click="submitFooterSettings">保存设置</el-button>
          </section>

          <div class="site-setting-panel" v-loading="footerSettingsState.loading">
            <el-row :gutter="22">
              <el-col :lg="14" :md="24">
                <section class="site-card surface-card">
                  <div class="site-card-header qr-header">
                    <div>
                      <h3>二维码区域</h3>
                      <p>支持新增、删除、排序多个二维码，前端将按顺序展示。</p>
                    </div>
                    <el-button type="primary" plain @click="addQrCode">新增二维码</el-button>
                  </div>

                  <div v-if="footerSettingsState.form.qr_codes.length" class="qr-code-list">
                    <article v-for="(item, index) in footerSettingsState.form.qr_codes" :key="item.id || `qr-${index}`" class="qr-code-card surface-card">
                      <div class="qr-card-head">
                        <div>
                          <strong>二维码 {{ index + 1 }}</strong>
                          <span>展示顺序 {{ index + 1 }}</span>
                        </div>
                        <div class="qr-card-actions">
                          <el-switch v-model="item.is_active" />
                          <el-button size="small" :disabled="index === 0" @click="moveQrCode(index, -1)">上移</el-button>
                          <el-button size="small" :disabled="index === footerSettingsState.form.qr_codes.length - 1" @click="moveQrCode(index, 1)">下移</el-button>
                          <el-button size="small" type="danger" plain @click="removeQrCode(index)">删除</el-button>
                        </div>
                      </div>

                      <MediaField
                        :mode="'image'"
                        :allow-video="false"
                        label="二维码图片"
                        v-model:image-url="item.image_url"
                        image-placeholder="支持输入图片链接，或上传本地图片"
                        image-tip="页脚二维码将直接渲染这里保存的图片。"
                      />

                      <el-form label-position="top" :model="item">
                        <el-form-item label="二维码标题">
                          <el-input v-model="item.name" placeholder="例如：企业微信 / 公众号" />
                        </el-form-item>
                        <el-form-item label="二维码说明">
                          <el-input v-model="item.description" type="textarea" :rows="3" maxlength="255" show-word-limit />
                        </el-form-item>
                      </el-form>
                    </article>
                  </div>

                  <el-empty v-else description="暂未配置二维码，点击右上角新增。" />
                </section>
              </el-col>

              <el-col :lg="10" :md="24">
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
          <el-col :md="12">
            <el-form-item label="按钮链接">
              <el-input v-model="bannerDialog.form.cta_link" placeholder="core_selling / #brand_story / https://example.com" />
              <div class="field-tip">支持填写板块标识或带 # 的锚点，点击后会平滑滚动到首页对应板块；填写完整 URL 时保持原跳转逻辑。</div>
            </el-form-item>
          </el-col>
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

    <el-dialog v-model="sectionRootDialog.visible" :title="sectionRootDialog.form.id ? '编辑板块' : '新增板块'" width="760px">
      <el-form label-position="top" :model="sectionRootDialog.form">
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="板块名称"><el-input v-model="sectionRootDialog.form.name" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="板块标识"><el-input v-model="sectionRootDialog.form.key" placeholder="section-6" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="首页标题"><el-input v-model="sectionRootDialog.form.title" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="副标题"><el-input v-model="sectionRootDialog.form.subtitle" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="摘要">
          <el-input v-model="sectionRootDialog.form.summary" type="textarea" :rows="3" maxlength="500" show-word-limit />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="排序"><el-input-number v-model="sectionRootDialog.form.sort_order" :min="0" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="启用"><el-switch v-model="sectionRootDialog.form.is_active" /></el-form-item></el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="sectionRootDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="sectionRootDialog.submitting" @click="submitSectionRoot">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="sectionDialog.visible" :title="sectionDialog.form.id ? '编辑内容' : '新增内容'" width="1040px">
      <el-form label-position="top" :model="sectionDialog.form">
        <div class="field-tip">当前所属板块：{{ sectionDialog.parentLabel || '未选择板块' }}</div>
        <el-row :gutter="16">
          <el-col :md="12"><el-form-item label="内容标题"><el-input v-model="sectionDialog.form.title" /></el-form-item></el-col>
          <el-col :md="12"><el-form-item label="副标题"><el-input v-model="sectionDialog.form.subtitle" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="摘要">
          <el-input v-model="sectionDialog.form.summary" type="textarea" :rows="3" maxlength="500" show-word-limit placeholder="用于首页卡片与列表页摘要展示。" />
        </el-form-item>
        <el-form-item label="正文">
          <RichTextEditor v-model="sectionDialog.form.body" placeholder="支持段落、标题、加粗、列表、链接、图片等内容编辑。" />
        </el-form-item>
        <MediaField label="内容媒体" v-model:mode="sectionDialog.form.media_type" v-model:image-url="sectionDialog.form.image_url" v-model:video-url="sectionDialog.form.video_url" />
        <el-form-item label="扩展 JSON"><el-input v-model="sectionDialog.form.extra_json" type="textarea" :rows="5" placeholder='{"tags": ["eco"], "stats": [{"label": "Altitude", "value": "1400m+"}]}' /></el-form-item>
        <div class="field-tip">默认按发布时间倒序展示；如需优先展示，请在列表中使用“置顶 / 取消置顶”按钮调整。</div>
        <el-row :gutter="16">
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
        <el-form-item label="&#x63CF;&#x8FF0;">
          <RichTextEditor v-model="productDialog.form.description" />
        </el-form-item>
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
        <el-form-item label="&#x6B63;&#x6587;&#x5185;&#x5BB9;">
          <RichTextEditor v-model="newsDialog.form.content" />
        </el-form-item>
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
import RichTextEditor from "../../components/admin/RichTextEditor.vue";
import {
  createBanner,
  createNews,
  createProduct,
  createSection,
  createSectionRoot,
  deleteBanner,
  deleteNews,
  deleteProduct,
  deleteSection,
  deleteSectionRoot,
  fetchBanners,
  fetchFooterSettings,
  fetchNews,
  fetchProducts,
  fetchSectionRoots,
  fetchSections,
  pinNews,
  pinProduct,
  pinSection,
  saveFooterSettings,
  unpinNews,
  unpinProduct,
  unpinSection,
  updateBanner,
  updateNews,
  updateProduct,
  updateSection,
  updateSectionRoot,
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
const sectionRootState = reactive({ items: [], loading: false, creating: false });
const expandedSectionId = ref(null);
const expandedSectionState = reactive({ root: null, items: [], loading: false, togglingId: null });

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
const createSectionRootForm = () => ({
  id: null,
  key: "",
  name: "",
  title: "",
  subtitle: "",
  summary: "",
  sort_order: 0,
  is_active: true,
});
const createSectionForm = () => ({
  id: null,
  key: "",
  parent_id: null,
  name: "",
  title: "",
  subtitle: "",
  summary: "",
  body: "",
  image_url: "",
  media_type: "image",
  video_url: "",
  extra_json: "",
  sort_order: 1,
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
const createQrCodeForm = () => ({
  id: null,
  name: "",
  description: "",
  image_url: "",
  sort_order: 0,
  is_active: true,
});
const createFooterSettingsForm = () => ({
  qr_codes: [],
  filing_name: "备案信息",
  filing_text: "",
  filing_is_active: true,
});
const normalizeMediaMode = (row) => row?.media_type || (row?.video_url ? "video" : "image");
const normalizeSectionKey = (value) => String(value || "").trim().replace(/^#/, "");
const bannerDialog = reactive({ visible: false, submitting: false, form: createBannerForm() });
const sectionRootDialog = reactive({ visible: false, submitting: false, form: createSectionRootForm() });
const sectionDialog = reactive({ visible: false, submitting: false, form: createSectionForm(), parent: null, parentLabel: "" });
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
const resolveSectionSourceLabel = (value) => ({ section: "图文内容", product: "产品内容", news: "动态内容" }[value] || "内容");
const resolveContentType = (type) =>
  ({ banner: "轮播图", "section-root": "板块", section: "内容", product: "产品", news: "动态" }[type] || "内容");
const resolveSectionDeleteType = (root) => (root?.content_source === "section" ? "section" : root?.content_source || "section");
const resolveExpandedItemTitle = (item, root) => (root?.content_source === "product" ? item.name : item.title);
const resolveExpandedItemSummary = (item, root) => (root?.content_source === "product" ? item.subtitle || "" : item.summary || "");
const resolveExpandedItemMediaType = (item) => resolveMediaType(item.media_type);
const resolveExpandedItemSortLabel = (item) => (item.sort_order === 0 ? "置顶" : "发布时间");
const applyBannerSizePreset = (field, value) => {
  bannerDialog.form[field] = value;
};

const reindexQrCodes = () => {
  footerSettingsState.form.qr_codes.forEach((item, index) => {
    item.sort_order = index;
  });
};

const addQrCode = () => {
  footerSettingsState.form.qr_codes.push(createQrCodeForm());
  reindexQrCodes();
};

const removeQrCode = (index) => {
  footerSettingsState.form.qr_codes.splice(index, 1);
  reindexQrCodes();
};

const moveQrCode = (index, delta) => {
  const targetIndex = index + delta;
  if (targetIndex < 0 || targetIndex >= footerSettingsState.form.qr_codes.length) {
    return;
  }
  const [current] = footerSettingsState.form.qr_codes.splice(index, 1);
  footerSettingsState.form.qr_codes.splice(targetIndex, 0, current);
  reindexQrCodes();
};

const loadBanners = async (page = bannerState.page) => {
  bannerState.loading = true;
  try {
    syncList(bannerState, await fetchBanners({ page, page_size: bannerState.pageSize }), page);
  } finally {
    bannerState.loading = false;
  }
};

const loadSectionRoots = async () => {
  sectionRootState.loading = true;
  try {
    sectionRootState.items = await fetchSectionRoots();
  } finally {
    sectionRootState.loading = false;
  }
};



const loadExpandedSectionItems = async (root) => {
  expandedSectionState.root = root;
  expandedSectionState.loading = true;
  try {
    if (root.content_source === "product") {
      const data = await fetchProducts({ page: 1, page_size: 200 });
      expandedSectionState.items = data.items || [];
      return;
    }
    if (root.content_source === "news") {
      const data = await fetchNews({ page: 1, page_size: 200 });
      expandedSectionState.items = data.items || [];
      return;
    }
    const data = await fetchSections({ page: 1, page_size: 200, node_type: "content", group_key: root.key });
    expandedSectionState.items = data.items || [];
  } finally {
    expandedSectionState.loading = false;
  }
};

const refreshExpandedSection = async () => {
  const root = sectionRootState.items.find((item) => item.id === expandedSectionId.value) || expandedSectionState.root;
  if (root) {
    await loadExpandedSectionItems(root);
  }
};

const loadFooterSettings = async () => {
  footerSettingsState.loading = true;
  try {
    const data = await fetchFooterSettings();
    footerSettingsState.form = {
      qr_codes: (data.footer_qr_codes || []).map((item, index) => ({
        ...createQrCodeForm(),
        ...item,
        sort_order: item?.sort_order ?? index,
      })),
      filing_name: data.footer_filing?.name || "备案信息",
      filing_text: data.footer_filing?.description || "",
      filing_is_active: data.footer_filing?.is_active ?? true,
    };
    reindexQrCodes();
  } finally {
    footerSettingsState.loading = false;
  }
};

const buildFooterSettingsPayload = () => ({
  qr_codes: footerSettingsState.form.qr_codes.map((item, index) => ({
    id: item.id || null,
    name: item.name || null,
    description: item.description || "",
    image_url: item.image_url || null,
    sort_order: index,
    is_active: Boolean(item.is_active),
  })),
  filing_name: footerSettingsState.form.filing_name || null,
  filing_text: footerSettingsState.form.filing_text || "",
  filing_is_active: Boolean(footerSettingsState.form.filing_is_active),
});

const refreshAll = async () => {
  await Promise.all([loadBanners(1), loadSectionRoots(), loadFooterSettings()]);
  await refreshExpandedSection();
};

const openBannerDialog = (row = null) => {
  bannerDialog.form = {
    ...createBannerForm(),
    ...(row || {}),
    media_type: normalizeMediaMode(row),
  };
  bannerDialog.visible = true;
};

const openSectionRootDialog = (row = null) => {
  sectionRootDialog.form = {
    ...createSectionRootForm(),
    ...(row || {}),
    key: normalizeSectionKey(row?.key || ""),
  };
  sectionRootDialog.visible = true;
};

const buildAutoContentKey = (parentKey) => `${normalizeSectionKey(parentKey)}-content-${Date.now()}`;

const openSectionDialog = (parent = null, row = null) => {
  sectionDialog.form = {
    ...createSectionForm(),
    ...(row || {}),
    key: normalizeSectionKey(row?.key || ""),
    parent_id: parent?.id || row?.parent_id || null,
    name: row?.name || row?.title || "",
    media_type: normalizeMediaMode(row),
  };
  sectionDialog.parent = parent || null;
  sectionDialog.parentLabel = parent?.name || "";
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

const toggleSectionRoot = async (root) => {
  if (expandedSectionId.value === root.id) {
    expandedSectionId.value = null;
    expandedSectionState.root = null;
    expandedSectionState.items = [];
    return;
  }
  expandedSectionId.value = root.id;
  await loadExpandedSectionItems(root);
};

const handleCreateSectionRoot = async () => {
  sectionRootState.creating = true;
  try {
    const nextIndex = sectionRootState.items.length + 1;
    const root = await createSectionRoot({
      name: `Section ${nextIndex}`,
      title: `Section ${nextIndex}`,
      subtitle: "",
      summary: "",
      sort_order: nextIndex,
      is_active: true,
    });
    await loadSectionRoots();
    openSectionRootDialog(root);
    ElMessage.success("一级板块已创建");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "板块创建失败");
  } finally {
    sectionRootState.creating = false;
  }
};

const openChildDialog = (root, row = null) => {
  if (root.content_source === "product") {
    openProductDialog(row);
    return;
  }
  if (root.content_source === "news") {
    openNewsDialog(row);
    return;
  }
  openSectionDialog(root, row);
};

const submitBanner = async () => {
  bannerDialog.submitting = true;
  try {
    const payload = {
      ...bannerDialog.form,
      cta_link: bannerDialog.form.cta_link?.trim() || "",
    };
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

const submitSectionRoot = async () => {
  sectionRootDialog.submitting = true;
  try {
    const payload = {
      ...sectionRootDialog.form,
      key: normalizeSectionKey(sectionRootDialog.form.key),
      summary: sectionRootDialog.form.summary?.trim() || "",
    };
    if (payload.id) {
      await updateSectionRoot(payload.id, payload);
    } else {
      await createSectionRoot(payload);
    }
    ElMessage.success("板块已保存");
    sectionRootDialog.visible = false;
    await loadSectionRoots();
    await refreshExpandedSection();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "板块保存失败");
  } finally {
    sectionRootDialog.submitting = false;
  }
};

const submitSection = async () => {
  sectionDialog.submitting = true;
  try {
    const payload = {
      ...sectionDialog.form,
      key: normalizeSectionKey(sectionDialog.form.key) || buildAutoContentKey(sectionDialog.parent?.key),
      parent_id: sectionDialog.parent?.id || sectionDialog.form.parent_id,
      name: sectionDialog.form.name?.trim() || sectionDialog.form.title?.trim() || "未命名内容",
      summary: sectionDialog.form.summary?.trim() || "",
      body: sectionDialog.form.body || "",
      sort_order: sectionDialog.form.sort_order === 0 ? 0 : 1,
    };
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
    ElMessage.success("内容已保存");
    sectionDialog.visible = false;
    await loadSectionRoots();
    await refreshExpandedSection();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "内容保存失败");
  } finally {
    sectionDialog.submitting = false;
  }
};

const submitProduct = async () => {
  productDialog.submitting = true;
  try {
    const payload = {
      ...productDialog.form,
      sort_order: productDialog.form.sort_order === 0 ? 0 : 1,
    };
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
    await loadSectionRoots();
    await refreshExpandedSection();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "产品保存失败");
  } finally {
    productDialog.submitting = false;
  }
};

const submitNews = async () => {
  newsDialog.submitting = true;
  try {
    const payload = {
      ...newsDialog.form,
      sort_order: newsDialog.form.sort_order === 0 ? 0 : 1,
    };
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
    await loadSectionRoots();
    await refreshExpandedSection();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "动态保存失败");
  } finally {
    newsDialog.submitting = false;
  }
};
const handleToggleExpandedPin = async (root, row) => {
  expandedSectionState.togglingId = row.id;
  try {
    if (root.content_source === "product") {
      if (row.sort_order === 0) {
        await unpinProduct(row.id);
        ElMessage.success("已取消置顶");
      } else {
        await pinProduct(row.id);
        ElMessage.success("已置顶");
      }
    } else if (root.content_source === "news") {
      if (row.sort_order === 0) {
        await unpinNews(row.id);
        ElMessage.success("已取消置顶");
      } else {
        await pinNews(row.id);
        ElMessage.success("已置顶");
      }
    } else {
      if (row.sort_order === 0) {
        await unpinSection(row.id);
        ElMessage.success("已取消置顶");
      } else {
        await pinSection(row.id);
        ElMessage.success("已置顶");
      }
    }
    await refreshExpandedSection();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "排序更新失败");
  } finally {
    expandedSectionState.togglingId = null;
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
    } else if (type === "section-root") {
      await deleteSectionRoot(row.id);
      if (expandedSectionId.value === row.id) {
        expandedSectionId.value = null;
        expandedSectionState.root = null;
        expandedSectionState.items = [];
      }
      await loadSectionRoots();
    } else if (type === "section") {
      await deleteSection(row.id);
      await loadSectionRoots();
      await refreshExpandedSection();
    } else if (type === "product") {
      await deleteProduct(row.id);
      await loadSectionRoots();
      await refreshExpandedSection();
    } else if (type === "news") {
      await deleteNews(row.id);
      await loadSectionRoots();
      await refreshExpandedSection();
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

.section-root-list {
  display: grid;
  gap: 16px;
}

.section-root-card {
  overflow: hidden;
  border-radius: 24px;
}

.section-root-row {
  width: 100%;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 18px;
  padding: 20px 22px;
  border: none;
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.section-root-main strong,
.section-root-main span,
.section-root-main p {
  display: block;
}

.section-root-main strong {
  color: var(--color-primary-deep);
  font-size: 18px;
}

.section-root-main span,
.section-root-body-head p {
  margin-top: 6px;
  color: var(--color-text-soft);
}

.section-root-main p {
  margin: 8px 0 0;
}

.section-root-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 12px;
  color: var(--color-text-soft);
}

.section-root-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-root-body {
  padding: 0 22px 22px;
}

.section-root-body-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.section-root-body-head strong {
  color: var(--color-primary-deep);
}

.section-child-loading {
  padding: 20px;
}

.section-expand-enter-active,
.section-expand-leave-active {
  transition: opacity 0.24s ease, transform 0.24s ease;
}

.section-expand-enter-from,
.section-expand-leave-to {
  opacity: 0;
  transform: translateY(-6px);
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

.site-card-header p {
  margin: 6px 0 0;
  color: var(--color-text-soft);
  line-height: 1.6;
}

.qr-header {
  align-items: flex-start;
}

.qr-code-list {
  display: grid;
  gap: 16px;
}

.qr-code-card {
  padding: 18px;
  border-radius: 20px;
}

.qr-card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.qr-card-head strong,
.qr-card-head span {
  display: block;
}

.qr-card-head span {
  margin-top: 4px;
  color: var(--color-text-soft);
  font-size: 13px;
}

.qr-card-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
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

.field-tip {
  margin-top: 8px;
  color: var(--color-text-soft);
  line-height: 1.6;
  font-size: 13px;
}

@media (max-width: 960px) {
  .dashboard-header,
  .panel-toolbar,
  .section-root-body-head,
  .site-card-header,
  .qr-card-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .dashboard-main {
    padding: 16px;
  }

  .section-root-row {
    grid-template-columns: 1fr;
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















