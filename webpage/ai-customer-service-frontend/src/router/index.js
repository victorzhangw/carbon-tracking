import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store";

Vue.use(VueRouter);

// 路由組件
import LoginPage from "../components/Login.vue";
import MainLayout from "../layouts/MainLayout.vue";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: LoginPage,
    meta: {
      requiresAuth: false,
      title: "登入",
    },
  },
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: MainLayout,
    meta: {
      requiresAuth: true,
      title: "儀表板",
    },
  },
  {
    path: "/voice",
    name: "VoiceInteraction",
    component: MainLayout,
    meta: {
      requiresAuth: true,
      title: "語音互動",
      permissions: ["perm_audio_create"],
    },
  },
  {
    path: "/voice-synthesis",
    name: "VoiceSynthesis",
    component: MainLayout,
    meta: {
      requiresAuth: true,
      title: "語音合成",
      permissions: ["perm_audio_create"],
    },
  },
  {
    path: "/voice-clone",
    name: "VoiceClone",
    component: MainLayout,
    meta: {
      requiresAuth: true,
      title: "語音克隆",
      permissions: ["perm_audio_create"],
    },
  },
  {
    path: "/staff",
    name: "StaffManagement",
    component: MainLayout,
    meta: {
      requiresAuth: true,
      title: "客服專員管理",
      permissions: ["perm_staff_read"],
    },
  },
  {
    path: "/audio",
    name: "AudioManagement",
    component: MainLayout,
    meta: {
      requiresAuth: true,
      title: "音頻管理",
      permissions: ["perm_audio_read"],
    },
  },
  {
    path: "/analytics",
    name: "AnalyticsDashboard",
    component: MainLayout,
    meta: {
      requiresAuth: true,
      title: "數據分析",
      roles: ["admin", "manager"],
    },
  },
  {
    path: "/care-schedule",
    name: "CareCallSchedule",
    component: MainLayout,
    meta: {
      requiresAuth: true,
      title: "關懷排程",
      permissions: ["perm_audio_read"],
    },
  },
  {
    path: "/care-targets",
    name: "CareTargetImport",
    component: MainLayout,
    meta: {
      requiresAuth: true,
      title: "關懷對象管理",
      permissions: ["perm_staff_read"],
    },
  },
  {
    path: "*",
    redirect: "/dashboard",
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// 路由守衛
router.beforeEach((to, from, next) => {
  // 設置頁面標題
  if (to.meta.title) {
    document.title = `${to.meta.title} - AI客服管理系統`;
  }

  const isAuthenticated = store.getters["auth/isAuthenticated"];
  const userPermissions = store.getters["auth/userPermissions"];
  const userRoles = store.getters["auth/userRoles"];

  // 登入頁面邏輯
  if (to.path === "/login") {
    if (isAuthenticated) {
      // 已登入，重定向到目標頁面
      const redirect = to.query.redirect || "/dashboard";
      if (redirect === to.fullPath) {
        next("/dashboard");
      } else {
        next(redirect);
      }
    } else {
      // 未登入，允許訪問登入頁面
      next();
    }
    return;
  }

  // 受保護頁面邏輯
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      // 未登入，重定向到登入頁面
      next({
        path: "/login",
        query: { redirect: to.fullPath },
      });
      return;
    }

    // 檢查權限
    if (to.meta.permissions) {
      const hasPermission = to.meta.permissions.some((permission) =>
        userPermissions.includes(permission)
      );

      if (!hasPermission) {
        Vue.prototype.$Message.error("您沒有權限訪問此頁面");
        next("/dashboard");
        return;
      }
    }

    // 檢查角色
    if (to.meta.roles) {
      const hasRole = to.meta.roles.some((role) => userRoles.includes(role));

      if (!hasRole) {
        Vue.prototype.$Message.error("您沒有權限訪問此頁面");
        next("/dashboard");
        return;
      }
    }
  }

  // 允許訪問
  next();
});

export default router;
