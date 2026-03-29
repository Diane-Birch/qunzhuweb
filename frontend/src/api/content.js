import http from "./http";

export const fetchHomepage = async () => {
  const { data } = await http.get("/public/home");
  return data;
};

export const fetchPublicSectionGroup = async (groupKey, params) => {
  const { data } = await http.get(`/public/section-groups/${groupKey}`, { params });
  return data;
};

export const fetchSectionDetail = async (sectionKey) => {
  const { data } = await http.get(`/public/sections/${sectionKey}`);
  return data;
};

export const fetchPublicProducts = async (params) => {
  const { data } = await http.get("/public/products", { params });
  return data;
};

export const fetchProductDetail = async (productId) => {
  const { data } = await http.get(`/public/products/${productId}`);
  return data;
};

export const fetchPublicNews = async (params) => {
  const { data } = await http.get("/public/news", { params });
  return data;
};

export const fetchNewsDetail = async (newsId) => {
  const { data } = await http.get(`/public/news/${newsId}`);
  return data;
};

export const fetchFooterSettings = async () => {
  const { data } = await http.get("/site-settings/footer-settings");
  return data;
};

export const saveFooterSettings = async (payload) => {
  const { data } = await http.put("/site-settings/footer-settings", payload);
  return data;
};

export const uploadMediaAsset = async (file, mediaType = "image") => {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await http.post("/site-settings/upload-media", formData, {
    params: { media_type: mediaType },
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return data;
};

export const uploadSiteSettingImage = async (file) => uploadMediaAsset(file, "image");

export const loginAdmin = async (payload) => {
  const { data } = await http.post("/auth/login", payload);
  return data;
};

export const fetchBanners = async (params) => {
  const { data } = await http.get("/banners", { params });
  return data;
};

export const createBanner = async (payload) => {
  const { data } = await http.post("/banners", payload);
  return data;
};

export const updateBanner = async (id, payload) => {
  const { data } = await http.put(`/banners/${id}`, payload);
  return data;
};

export const deleteBanner = async (id) => {
  const { data } = await http.delete(`/banners/${id}`);
  return data;
};

export const fetchSections = async (params) => {
  const { data } = await http.get("/sections", { params });
  return data;
};

export const fetchSectionRoots = async () => {
  const { data } = await http.get("/sections/roots");
  return data;
};

export const createSectionRoot = async (payload) => {
  const { data } = await http.post("/sections/roots", payload);
  return data;
};

export const updateSectionRoot = async (id, payload) => {
  const { data } = await http.put(`/sections/roots/${id}`, payload);
  return data;
};

export const deleteSectionRoot = async (id) => {
  const { data } = await http.delete(`/sections/roots/${id}`);
  return data;
};

export const createSection = async (payload) => {
  const { data } = await http.post("/sections", payload);
  return data;
};

export const updateSection = async (id, payload) => {
  const { data } = await http.put(`/sections/${id}`, payload);
  return data;
};

export const pinSection = async (id) => {
  const { data } = await http.post(`/sections/${id}/pin`);
  return data;
};

export const unpinSection = async (id) => {
  const { data } = await http.post(`/sections/${id}/unpin`);
  return data;
};

export const deleteSection = async (id) => {
  const { data } = await http.delete(`/sections/${id}`);
  return data;
};

export const fetchProducts = async (params) => {
  const { data } = await http.get("/products", { params });
  return data;
};

export const createProduct = async (payload) => {
  const { data } = await http.post("/products", payload);
  return data;
};

export const updateProduct = async (id, payload) => {
  const { data } = await http.put(`/products/${id}`, payload);
  return data;
};

export const pinProduct = async (id) => {
  const { data } = await http.post(`/products/${id}/pin`);
  return data;
};

export const unpinProduct = async (id) => {
  const { data } = await http.post(`/products/${id}/unpin`);
  return data;
};

export const deleteProduct = async (id) => {
  const { data } = await http.delete(`/products/${id}`);
  return data;
};

export const fetchNews = async (params) => {
  const { data } = await http.get("/news", { params });
  return data;
};

export const createNews = async (payload) => {
  const { data } = await http.post("/news", payload);
  return data;
};

export const updateNews = async (id, payload) => {
  const { data } = await http.put(`/news/${id}`, payload);
  return data;
};

export const pinNews = async (id) => {
  const { data } = await http.post(`/news/${id}/pin`);
  return data;
};

export const unpinNews = async (id) => {
  const { data } = await http.post(`/news/${id}/unpin`);
  return data;
};

export const deleteNews = async (id) => {
  const { data } = await http.delete(`/news/${id}`);
  return data;
};
