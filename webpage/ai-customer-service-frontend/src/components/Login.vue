<template>
  <div class="login-container">
    <div class="login-wrapper">
      <Card class="login-card" :bordered="false">
        <div class="login-header">
          <div class="logo">
            <Icon type="ios-people" size="48" color="#7cb342" />
          </div>
          <h1 class="title">AI客服管理系統</h1>
          <p class="subtitle">請登入您的帳號</p>
        </div>

        <Form
          ref="loginForm"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @submit.native.prevent="handleLogin"
        >
          <FormItem prop="username">
            <Input
              v-model="loginForm.username"
              prefix="ios-person"
              placeholder="請輸入用戶名"
              size="large"
              :disabled="loading"
              @on-enter="handleLogin"
            />
          </FormItem>

          <FormItem prop="password">
            <Input
              v-model="loginForm.password"
              type="password"
              prefix="ios-lock"
              placeholder="請輸入密碼"
              size="large"
              :disabled="loading"
              @on-enter="handleLogin"
            />
          </FormItem>

          <FormItem>
            <Checkbox v-model="loginForm.rememberMe" :disabled="loading">
              記住我
            </Checkbox>
          </FormItem>

          <FormItem>
            <Button
              type="primary"
              size="large"
              long
              :loading="loading"
              @click="handleLogin"
            >
              <span v-if="!loading">登入</span>
              <span v-else>登入中...</span>
            </Button>
          </FormItem>
        </Form>

        <div class="login-footer">
          <p class="help-text">
            <!--預設帳號：admin / 密碼：admin123-->
          </p>
        </div>
      </Card>
    </div>

    <!-- 背景裝飾 -->
    <div class="background-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      loading: false,
      loginForm: {
        username: "",
        password: "",
        rememberMe: false,
      },
      loginRules: {
        username: [
          { required: true, message: "請輸入用戶名", trigger: "blur" },
          {
            min: 3,
            max: 20,
            message: "用戶名長度在 3 到 20 個字符",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "請輸入密碼", trigger: "blur" },
          { min: 6, message: "密碼長度不能少於 6 個字符", trigger: "blur" },
        ],
      },
    };
  },
  mounted() {
    // 檢查是否已經登入
    if (this.$store.getters["auth/isAuthenticated"]) {
      this.$router.push("/dashboard");
    }

    // 從 localStorage 讀取記住的用戶名
    const rememberedUsername = localStorage.getItem("rememberedUsername");
    if (rememberedUsername) {
      this.loginForm.username = rememberedUsername;
      this.loginForm.rememberMe = true;
    }
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          this.login();
        } else {
          this.$Message.error("請檢查輸入內容");
        }
      });
    },

    async login() {
      this.loading = true;

      try {
        console.log("嘗試登入:", this.loginForm.username);
        const response = await this.$axios.post("/api/auth/login", {
          username: this.loginForm.username,
          password: this.loginForm.password,
        });

        console.log("登入響應:", response.data);
        if (response.data.access_token) {
          // 儲存認證資訊
          console.log("儲存認證資訊到 store");
          await this.$store.dispatch("auth/login", {
            token: response.data.access_token,
            refreshToken: response.data.refresh_token,
            user: response.data.user,
          });

          console.log("認證狀態:", this.$store.getters["auth/isAuthenticated"]);

          // 處理記住我功能
          if (this.loginForm.rememberMe) {
            localStorage.setItem("rememberedUsername", this.loginForm.username);
          } else {
            localStorage.removeItem("rememberedUsername");
          }

          this.$Message.success("登入成功！");

          // 處理記住我功能
          if (this.loginForm.rememberMe) {
            localStorage.setItem("rememberedUsername", this.loginForm.username);
          } else {
            localStorage.removeItem("rememberedUsername");
          }

          // 跳轉到主頁面
          const redirect = this.$route.query.redirect || "/dashboard";
          this.$router.push(redirect);
        }
      } catch (error) {
        console.error("登入錯誤:", error);

        if (
          error.response &&
          error.response.data &&
          error.response.data.error
        ) {
          this.$Message.error(error.response.data.error);
        } else {
          this.$Message.error("登入失敗，請檢查網路連接");
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8bc34a 0%, #7cb342 100%);
  position: relative;
  overflow: hidden;
}

.login-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

.login-card {
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;

  .logo {
    margin-bottom: 20px;
  }

  .title {
    font-size: 28px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 8px;
  }

  .subtitle {
    color: #7f8c8d;
    font-size: 16px;
    margin: 0;
  }
}

.login-form {
  .ivu-form-item {
    margin-bottom: 24px;
  }

  .ivu-input-wrapper {
    .ivu-input {
      height: 48px;
      border-radius: 8px;
      border: 2px solid #e8eaed;
      transition: all 0.3s ease;

      &:focus {
        border-color: #7cb342;
        box-shadow: 0 0 0 2px rgba(124, 179, 66, 0.2);
      }
    }
  }

  .ivu-btn {
    height: 48px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(124, 179, 66, 0.3);
    }
  }
}

.login-footer {
  text-align: center;
  margin-top: 30px;

  .help-text {
    color: #95a5a6;
    font-size: 14px;
    margin: 0;
  }
}

.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;

  .circle {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    animation: float 6s ease-in-out infinite;

    &.circle-1 {
      width: 200px;
      height: 200px;
      top: 10%;
      left: 10%;
      animation-delay: 0s;
    }

    &.circle-2 {
      width: 150px;
      height: 150px;
      top: 60%;
      right: 10%;
      animation-delay: 2s;
    }

    &.circle-3 {
      width: 100px;
      height: 100px;
      bottom: 20%;
      left: 20%;
      animation-delay: 4s;
    }
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

// 響應式設計
@media (max-width: 768px) {
  .login-wrapper {
    max-width: 350px;
    padding: 15px;
  }

  .login-card {
    padding: 30px 25px;
  }

  .login-header .title {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .login-wrapper {
    max-width: 320px;
    padding: 10px;
  }

  .login-card {
    padding: 25px 20px;
  }

  .login-header .title {
    font-size: 22px;
  }
}
</style>
