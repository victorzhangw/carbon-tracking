<template>
  <div class="main-layout">
    <Layout class="layout-container">
      <!-- 左側導航 -->
      <Sider
        ref="sider"
        hide-trigger
        collapsible
        :collapsed-width="64"
        v-model="isCollapsed"
        class="layout-sider"
        :class="{ 'sider-collapsed': isCollapsed }"
      >
        <!-- Logo 區域 -->
        <div class="logo-container" :class="{ 'logo-collapsed': isCollapsed }">
          <div class="logo-icon">
            <Icon
              type="ios-people"
              :size="isCollapsed ? 24 : 32"
              color="#ffffff"
            />
          </div>
          <transition name="logo-text">
            <div v-if="!isCollapsed" class="logo-text">
              <h3>AI客服系統</h3>
              <span>智能管理平台</span>
            </div>
          </transition>
        </div>

        <!-- 收縮按鈕 -->
        <div class="collapse-trigger" @click="toggleCollapse">
          <Icon :type="isCollapsed ? 'ios-arrow-forward' : 'ios-arrow-back'" />
          <span v-if="!isCollapsed" class="collapse-text">收縮選單</span>
        </div>

        <!-- 導航選單 -->
        <Menu
          :active-name="activeMenu"
          theme="dark"
          width="auto"
          :class="['nav-menu', { 'menu-collapsed': isCollapsed }]"
          @on-select="handleMenuSelect"
        >
          <MenuItem name="dashboard" class="menu-item">
            <Icon type="ios-speedometer" />
            <span>儀表板</span>
          </MenuItem>

          <MenuItem
            name="voice"
            v-if="hasPermission('perm_audio_create')"
            class="menu-item"
          >
            <Icon type="ios-mic" />
            <span>語音互動</span>
          </MenuItem>

          <MenuItem
            name="voice-synthesis"
            v-if="hasPermission('perm_audio_create')"
            class="menu-item"
          >
            <Icon type="ios-volume-high" />
            <span>語音合成</span>
          </MenuItem>

          <MenuItem
            name="voice-clone"
            v-if="hasPermission('perm_audio_create')"
            class="menu-item"
          >
            <Icon type="ios-copy" />
            <span>語音克隆</span>
          </MenuItem>

          <Submenu name="management" v-if="hasAnyManagementPermission">
            <template slot="title">
              <Icon type="ios-settings" />
              <span>系統管理</span>
            </template>

            <MenuItem
              name="staff"
              v-if="hasPermission('perm_staff_read')"
              class="sub-menu-item"
            >
              <Icon type="ios-people" />
              <span>客服專員</span>
            </MenuItem>

            <MenuItem
              name="audio"
              v-if="hasPermission('perm_audio_read')"
              class="sub-menu-item"
            >
              <Icon type="ios-musical-notes" />
              <span>音頻管理</span>
            </MenuItem>
          </Submenu>

          <MenuItem
            name="analytics"
            v-if="hasRole('admin') || hasRole('manager')"
            class="menu-item"
          >
            <Icon type="ios-analytics" />
            <span>數據分析</span>
          </MenuItem>

          <MenuItem name="care-schedule" class="menu-item">
            <Icon type="ios-calendar" />
            <span>關懷排程</span>
          </MenuItem>

          <MenuItem name="care-targets" class="menu-item">
            <Icon type="ios-heart" />
            <span>關懷對象</span>
          </MenuItem>
        </Menu>
      </Sider>

      <!-- 主要內容區域 -->
      <Layout class="main-content-layout">
        <!-- 頂部導航欄 -->
        <Header class="layout-header">
          <div class="header-left">
            <Breadcrumb class="breadcrumb">
              <BreadcrumbItem>{{ currentPageTitle }}</BreadcrumbItem>
            </Breadcrumb>
          </div>

          <div class="header-right">
            <!-- 通知圖標 -->
            <div class="header-action">
              <Badge :count="notificationCount" :offset="[10, 0]">
                <Icon type="ios-notifications" size="20" />
              </Badge>
            </div>

            <!-- 全螢幕切換 -->
            <div class="header-action" @click="toggleFullscreen">
              <Icon
                :type="isFullscreen ? 'ios-contract' : 'ios-expand'"
                size="20"
              />
            </div>

            <!-- 用戶選單 -->
            <Dropdown @on-click="handleUserMenuClick" class="user-dropdown">
              <div class="user-info">
                <Avatar
                  :src="currentUser.avatar"
                  icon="ios-person"
                  class="user-avatar"
                  :style="{ backgroundColor: '#52c41a' }"
                />
                <div class="user-details" v-if="!isCollapsed">
                  <span class="username">{{
                    currentUser.full_name || currentUser.username
                  }}</span>
                </div>
                <Icon type="ios-arrow-down" class="dropdown-icon" />
              </div>

              <DropdownMenu slot="list">
                <DropdownItem name="profile">
                  <Icon type="ios-person" />
                  個人資料
                </DropdownItem>
                <DropdownItem name="settings">
                  <Icon type="ios-settings" />
                  系統設置
                </DropdownItem>
                <DropdownItem name="help">
                  <Icon type="ios-help-circle" />
                  幫助中心
                </DropdownItem>
                <DropdownItem name="logout" divided>
                  <Icon type="ios-log-out" />
                  登出系統
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </div>
        </Header>

        <!-- 內容區域 -->
        <Content class="layout-content">
          <div class="content-wrapper">
            <transition name="page-transition" mode="out-in">
              <component :is="currentComponent" :key="activeMenu" />
            </transition>
          </div>
        </Content>

        <!-- 底部 -->
        <Footer class="layout-footer">
          <div class="footer-content">
            <span>© 2024 AI客服管理系統 - 智能關懷服務平台</span>
            <div class="footer-links">
              <a href="#" @click.prevent>隱私政策</a>
              <Divider type="vertical" />
              <a href="#" @click.prevent>服務條款</a>
              <Divider type="vertical" />
              <a href="#" @click.prevent>技術支援</a>
            </div>
          </div>
        </Footer>
      </Layout>
    </Layout>

    <!-- 載入遮罩 -->
    <div v-if="isLoading" class="loading-overlay">
      <Spin size="large">
        <Icon type="ios-loading" size="18" class="spin-icon-load"></Icon>
        <div>載入中...</div>
      </Spin>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import DashboardHome from "../components/DashboardHome.vue";
import VoiceInteractionContainer from "../components/voice/VoiceInteractionContainer.vue";
import StaffManagement from "../components/StaffManagement.vue";
import AudioManagement from "../components/AudioManagement.vue";
import AnalyticsDashboard from "../components/AnalyticsDashboard.vue";
import CareCallSchedule from "../components/CareCallSchedule.vue";
import CareTargetImport from "../components/CareTargetImport.vue";
import VoiceSynthesis from "../components/VoiceSynthesis.vue";
import VoiceClone from "../components/VoiceClone.vue";

export default {
  name: "MainLayout",
  components: {
    DashboardHome,
    VoiceInteractionContainer,
    VoiceSynthesis,
    VoiceClone,
    StaffManagement,
    AudioManagement,
    AnalyticsDashboard,
    CareCallSchedule,
    CareTargetImport,
  },
  data() {
    return {
      isCollapsed: false,
      activeMenu: "dashboard",
      isLoading: false,
      isFullscreen: false,
      notificationCount: 0,
    };
  },
  computed: {
    ...mapGetters("auth", ["currentUser", "hasPermission", "hasRole"]),

    hasAnyManagementPermission() {
      return (
        this.hasPermission("perm_staff_read") ||
        this.hasPermission("perm_audio_read")
      );
    },

    primaryRole() {
      if (!this.currentUser.roles || this.currentUser.roles.length === 0)
        return "用戶";
      const roleMap = {
        admin: "系統管理員",
        manager: "管理者",
        staff: "客服專員",
        viewer: "訪客",
      };
      return roleMap[this.currentUser.roles[0]] || this.currentUser.roles[0];
    },

    currentPageTitle() {
      const titleMap = {
        dashboard: "儀表板",
        voice: "語音互動",
        "voice-synthesis": "語音合成",
        "voice-clone": "語音克隆",
        staff: "客服專員管理",
        audio: "音頻管理",
        analytics: "數據分析",
        "care-schedule": "關懷排程",
        "care-targets": "關懷對象管理",
      };
      return titleMap[this.activeMenu] || "系統首頁";
    },

    currentComponent() {
      const componentMap = {
        dashboard: "DashboardHome",
        voice: "VoiceInteractionContainer",
        "voice-synthesis": "VoiceSynthesis",
        "voice-clone": "VoiceClone",
        staff: "StaffManagement",
        audio: "AudioManagement",
        analytics: "AnalyticsDashboard",
        "care-schedule": "CareCallSchedule",
        "care-targets": "CareTargetImport",
      };
      return componentMap[this.activeMenu] || "DashboardHome";
    },
  },
  mounted() {
    // 初始化頁面
    this.initializePage();

    // 監聽視窗大小變化
    window.addEventListener("resize", this.handleResize);

    // 監聽全螢幕變化
    document.addEventListener("fullscreenchange", this.handleFullscreenChange);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
    document.removeEventListener(
      "fullscreenchange",
      this.handleFullscreenChange
    );
  },
  methods: {
    initializePage() {
      // 從路由設置活動選單
      const routeName = this.$route.name;
      if (routeName && routeName !== "Dashboard") {
        this.activeMenu = this.getMenuNameFromRoute(routeName);
      }

      // 響應式處理
      this.handleResize();
    },

    getMenuNameFromRoute(routeName) {
      const routeMap = {
        VoiceInteractionContainer: "voice",
        VoiceSynthesis: "voice-synthesis",
        VoiceClone: "voice-clone",
        StaffManagement: "staff",
        AudioManagement: "audio",
        AnalyticsDashboard: "analytics",
        CareCallSchedule: "care-schedule",
        CareTargetImport: "care-targets",
      };
      return routeMap[routeName] || "dashboard";
    },

    handleMenuSelect(name) {
      this.activeMenu = name;
      this.isLoading = true;

      // 模擬載入延遲
      setTimeout(() => {
        this.isLoading = false;
      }, 300);

      // 更新路由
      const routeMap = {
        dashboard: "/dashboard",
        voice: "/voice",
        "voice-synthesis": "/voice-synthesis",
        "voice-clone": "/voice-clone",
        staff: "/staff",
        audio: "/audio",
        analytics: "/analytics",
        "care-schedule": "/care-schedule",
        "care-targets": "/care-targets",
      };

      if (routeMap[name] && this.$route.path !== routeMap[name]) {
        this.$router.push(routeMap[name]);
      }
    },

    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
    },

    handleResize() {
      // 小螢幕自動收縮側邊欄
      if (window.innerWidth < 768) {
        this.isCollapsed = true;
      }
    },

    toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        document.exitFullscreen();
      }
    },

    handleFullscreenChange() {
      this.isFullscreen = !!document.fullscreenElement;
    },

    handleUserMenuClick(name) {
      switch (name) {
        case "profile":
          this.$Message.info("個人資料功能開發中...");
          break;
        case "settings":
          this.$Message.info("系統設置功能開發中...");
          break;
        case "help":
          this.$Message.info("幫助中心功能開發中...");
          break;
        case "logout":
          this.handleLogout();
          break;
      }
    },

    handleLogout() {
      this.$Modal.confirm({
        title: "確認登出",
        content: "您確定要登出系統嗎？",
        okText: "確認登出",
        cancelText: "取消",
        onOk: () => {
          this.$store.dispatch("auth/logout");
          this.$Message.success("已成功登出");
          this.$router.push("/login");
        },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
// 主要佈局樣式
.main-layout {
  height: 100vh;
  background: #f0f2f5;
}

.layout-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

// 側邊欄樣式
.layout-sider {
  background: linear-gradient(180deg, #8bc34a 0%, #7cb342 100%);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 100;
}

// Logo 區域
.logo-container {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;

  &.logo-collapsed {
    justify-content: center;
    padding: 20px 12px;
  }

  .logo-icon {
    flex-shrink: 0;
    margin-right: 12px;
  }

  .logo-text {
    color: white;

    h3 {
      margin: 0;
      font-size: 18px;
      font-weight: 600;
      line-height: 1.2;
    }

    span {
      font-size: 12px;
      opacity: 0.8;
      display: block;
      margin-top: 2px;
    }
  }
}

// 導航選單樣式
.nav-menu {
  background: transparent !important;
  border: none !important;

  :deep(.ivu-menu-item) {
    color: rgba(255, 255, 255, 0.85) !important;
    border: none !important;
    margin: 4px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-size: 14px;

    &:hover {
      background: rgba(255, 255, 255, 0.1) !important;
      color: #ffffff !important;
    }

    &.ivu-menu-item-active {
      background: rgba(255, 255, 255, 0.2) !important;
      color: #ffffff !important;
      font-weight: 500;
    }
  }

  :deep(.ivu-menu-submenu) {
    .ivu-menu-submenu-title {
      color: rgba(255, 255, 255, 0.85) !important;
      margin: 4px 12px;
      border-radius: 8px;
      transition: all 0.3s ease;
      font-size: 14px;

      &:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
      }
    }

    .ivu-menu {
      background: rgba(0, 0, 0, 0.1) !important;

      .ivu-menu-item {
        margin: 2px 8px;
        padding-left: 48px !important;
        font-size: 13px;
      }
    }
  }
}

// 收縮按鈕
.collapse-trigger {
  margin: 8px 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.85);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 14px;
  gap: 8px;

  &:hover {
    background: rgba(255, 255, 255, 0.15);
    color: #ffffff;
  }

  .collapse-text {
    font-size: 13px;
    font-weight: 500;
  }
}

// 頂部導航欄
.layout-header {
  background: #ffffff;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  border-bottom: 1px solid #f0f0f0;
}

.header-left {
  .breadcrumb {
    :deep(.ivu-breadcrumb-item) {
      font-size: 16px;
      font-weight: 500;
      color: #2c3e50;
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-action {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;

  &:hover {
    background: #f5f5f5;
    color: #7cb342;
  }
}

.user-dropdown {
  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    padding: 8px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;

    &:hover {
      background: #f5f5f5;
    }

    .user-avatar {
      border: 2px solid #7cb342;
    }

    .user-details {
      display: flex;
      flex-direction: column;

      .username {
        font-size: 14px;
        font-weight: 500;
        color: #2c3e50;
        line-height: 1.2;
      }

      .user-role {
        font-size: 12px;
        color: #7cb342;
        margin-top: 2px;
      }
    }

    .dropdown-icon {
      color: #999;
      transition: transform 0.3s ease;
    }
  }
}

// 主要內容區域
.main-content-layout {
  background: #f0f2f5;
}

.layout-content {
  margin: 0;
  background: #f0f2f5;
  min-height: calc(100vh - 128px);
}

// 內容區域
.layout-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-wrapper {
  padding: 10px;
  flex: 1;
  overflow-y: auto;
}

// 底部
.layout-footer {
  background: #ffffff;
  border-top: 1px solid #f0f0f0;
  padding: 16px 24px;
  flex-shrink: 0;
  z-index: 10;

  .footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #666;
    font-size: 14px;

    .footer-links {
      display: flex;
      align-items: center;
      gap: 8px;

      a {
        color: #7cb342;
        text-decoration: none;
        transition: color 0.3s ease;

        &:hover {
          color: #689f38;
        }
      }
    }
  }
}

// 載入遮罩
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

// 動畫效果
.logo-text-enter-active,
.logo-text-leave-active {
  transition: all 0.3s ease;
}

.logo-text-enter,
.logo-text-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.page-transition-enter-active,
.page-transition-leave-active {
  transition: all 0.3s ease;
}

.page-transition-enter,
.page-transition-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

// 響應式設計
@media (max-width: 768px) {
  .layout-header {
    padding: 0 16px;
  }

  .content-wrapper {
    padding: 16px;
  }

  .user-details {
    display: none !important;
  }

  .footer-content {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .header-right {
    gap: 12px;
  }

  .header-action {
    width: 36px;
    height: 36px;
  }

  .content-wrapper {
    padding: 12px;
  }
}

// 自定義滾動條
:deep(.ivu-layout-sider-children) {
  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;

    &:hover {
      background: rgba(255, 255, 255, 0.5);
    }
  }
}
</style>
