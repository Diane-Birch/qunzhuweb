import http from "./http";

export const fetchHomepage = async () => {
  const { data } = await http.get("/public/home");
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

export const uploadSiteSettingImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await http.post("/site-settings/upload-image", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return data;
};

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

export const createSection = async (payload) => {
  const { data } = await http.post("/sections", payload);
  return data;
};

export const updateSection = async (id, payload) => {
  const { data } = await http.put(`/sections/${id}`, payload);
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

export const deleteNews = async (id) => {
  const { data } = await http.delete(`/news/${id}`);
  return data;
};