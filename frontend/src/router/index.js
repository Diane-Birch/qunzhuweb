import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import NewsDetailView from "../views/NewsDetailView.vue";
import ProductDetailView from "../views/ProductDetailView.vue";
import SectionDetailView from "../views/SectionDetailView.vue";
import AdminDashboard from "../views/admin/AdminDashboard.vue";
import AdminLogin from "../views/admin/AdminLogin.vue";
import { getToken } from "../utils/auth";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/sections/:key",
      name: "section-detail",
      component: SectionDetailView,
      props: true,
    },
    {
      path: "/products/:id",
      name: "product-detail",
      component: ProductDetailView,
      props: true,
    },
    {
      path: "/news/:id",
      name: "news-detail",
      component: NewsDetailView,
      props: true,
    },
    {
      path: "/admin/login",
      name: "admin-login",
      component: AdminLogin,
    },
    {
      path: "/admin",
      redirect: "/admin/dashboard",
    },
    {
      path: "/admin/dashboard",
      name: "admin-dashboard",
      component: AdminDashboard,
      meta: { requiresAuth: true },
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return {
        el: to.hash,
        top: 96,
        behavior: "smooth",
      };
    }
    return { top: 0, behavior: "smooth" };
  },
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !getToken()) {
    next({ name: "admin-login" });
    return;
  }
  if (to.name === "admin-login" && getToken()) {
    next({ name: "admin-dashboard" });
    return;
  }
  next();
});

export default router;
