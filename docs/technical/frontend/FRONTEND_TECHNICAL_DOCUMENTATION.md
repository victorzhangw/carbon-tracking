# AI 客服語音克隆系統 - 前端技術說明文件

## 📋 系統概述

本系統前端是基於 Vue.js 2.x 的單頁應用程式 (SPA)，提供直觀的語音錄製、即時對話、情緒顯示等功能，專為 AI 客服場景設計。

## 🏗️ 技術架構

### 核心技術棧

- **前端框架**: Vue.js 2.6.14
- **UI 組件庫**: iView 3.5.4
- **HTTP 客戶端**: Axios
- **音頻處理**: Web Audio API, MediaRecorder API
- **狀態管理**: Vue 組件內部狀態管理
- **路由管理**: Vue Router
- **建構工具**: Webpack (Vue CLI)
- **樣式預處理**: CSS3 + Scoped Styles

### 系統架構圖

```
┌─────────────────────────────────────────────────────────┐
│                    Vue.js 應用層                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────┐ │
│  │  語音交互組件   │  │   佈局組件      │  │ 工具組件 │ │
│  │ VoiceInteraction│  │  MainLayout     │  │   ...    │ │
│  │   Container     │  │                 │  │          │ │
│  └─────────────────┘  └─────────────────┘  └──────────┘ │
├─────────────────────────────────────────────────────────┤
│                   瀏覽器 API 層                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────┐ │
│  │ MediaRecorder   │  │   Web Audio     │  │  Axios   │ │
│  │      API        │  │      API        │  │   HTTP   │ │
│  └─────────────────┘  └─────────────────┘  └──────────┘ │
├─────────────────────────────────────────────────────────┤
│                    後端 API 層                          │
│              Flask RESTful API                          │
└─────────────────────────────────────────────────────────┘
```

## 🎯 核心功能模組

### 1. 語音交互容器組件 (`VoiceInteractionContainer.vue`)

#### 技術路線

- **組件化設計**: 單一職責原則，專注語音交互功能
- **響應式佈局**: 兩欄式設計，左側控制面板，右側對話區域
- **狀態管理**: 使用 Vue 響應式數據管理複雜的語音狀態
- **事件驅動**: 基於用戶交互事件觸發語音處理流程

#### 核心狀態管理

```javascript
data() {
  return {
    // 語音狀態
    isListening: false,      // 正在聆聽
    isThinking: false,       // AI 思考中
    isSpeaking: false,       // AI 回應中

    // 錄音相關
    audioBlob: null,         // 音頻數據
    recorder: null,          // MediaRecorder 實例
    recordingTime: 0,        // 錄音時長

    // 對話管理
    conversationHistory: [], // 對話歷史
    messageIdCounter: 1,     // 消息 ID 計數器
    conversationRounds: 0,   // 對話輪次

    // 系統設置
    selectedStaff: "admin",  // 選擇的 AI 助手
    responseStyle: "friendly", // 回應風格
    autoPlayEnabled: true,   // 自動播放設定
  }
}
```

#### 語音處理演算法

**錄音流程**:

```javascript
async startRecording() {
  // 1. 權限檢查
  await this.ensureMicrophonePermission();

  // 2. 獲取媒體流
  const stream = await navigator.mediaDevices.getUserMedia({
    audio: {
      echoCancellation: true,
      noiseSuppression: true,
      autoGainControl: true,
      sampleRate: 44100
    }
  });

  // 3. 創建錄音器
  this.recorder = new MediaRecorder(stream, {
    mimeType: MediaRecorder.isTypeSupported('audio/webm')
      ? 'audio/webm' : 'audio/wav'
  });

  // 4. 數據收集
  const audioChunks = [];
  this.recorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      audioChunks.push(event.data);
    }
  };

  // 5. 錄音完成處理
  this.recorder.onstop = () => {
    this.audioBlob = new Blob(audioChunks, {
      type: this.recorder.mimeType || "audio/wav"
    });
  };
}
```

**語音識別與情緒分析**:

```javascript
async performSpeechRecognition() {
  const formData = new FormData();
  formData.append("file", this.audioBlob, "recording.wav");

  const response = await axios.post("/process_audio", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    timeout: 60000
  });

  // 同時進行情緒識別
  this.performEmotionAnalysis();

  return response.data.transcript;
}

async performEmotionAnalysis() {
  const formData = new FormData();
  formData.append("file", this.audioBlob, "recording.wav");
  formData.append("method", "basic"); // 或 "advanced"

  const response = await axios.post("/api/emotion/upload-and-analyze", formData);

  // 更新最後一條用戶消息的情緒資訊
  if (this.conversationHistory.length > 0) {
    const lastMessage = this.conversationHistory[this.conversationHistory.length - 1];
    if (lastMessage.type === 'user') {
      this.$set(lastMessage, 'emotionAnalysis', response.data);
      this.$set(lastMessage, 'detectedEmotion', response.data.predicted_emotion);
      this.$set(lastMessage, 'emotionConfidence', response.data.confidence);
    }
  }
}
```

### 2. 情緒標籤系統

#### 技術路線

- **多語言支援**: 英文標籤 → 繁體中文翻譯
- **視覺化設計**: 表情符號 + 顏色編碼 + 文字標籤
- **動態渲染**: 基於情緒類型動態選擇樣式

#### 情緒映射演算法

```javascript
// 情緒標籤翻譯
getEmotionLabel(emotion) {
  const labels = {
    happy: "開心",     sad: "難過",      angry: "生氣",
    neutral: "平靜",   fear: "恐懼",     surprise: "驚訝",
    calm: "冷靜",      disgust: "厭惡",  fearful: "害怕",
    surprised: "驚喜", excited: "興奮",  bored: "無聊",
    confused: "困惑",  confident: "自信", frustrated: "沮喪",
    relaxed: "放鬆"
  };
  return labels[emotion] || emotion;
}

// 情緒顏色映射
getEmotionColor(emotion) {
  const colors = {
    // 正面情緒 - 綠色系
    happy: "green", excited: "green", confident: "green",
    // 負面情緒 - 紅色系
    sad: "red", angry: "red", frustrated: "red",
    // 恐懼相關 - 橙色系
    fear: "orange", fearful: "orange", disgust: "orange",
    // 驚訝相關 - 紫色系
    surprise: "purple", surprised: "purple", confused: "purple",
    // 冷靜相關 - 藍色系
    relaxed: "blue", calm: "blue",
    // 中性情緒 - 灰色系
    neutral: "default", bored: "default"
  };
  return colors[emotion] || "default";
}

// 情緒表情符號映射
getEmotionEmoji(emotion) {
  const emojis = {
    happy: "😊", excited: "🤩", confident: "😎", relaxed: "😌",
    calm: "😇", surprised: "😄", sad: "😢", angry: "😠",
    frustrated: "😤", disgust: "🤢", fear: "😨", fearful: "😰",
    surprise: "😲", confused: "😕", neutral: "😐", bored: "😴"
  };
  return emojis[emotion] || "🎭";
}
```

### 3. 音頻可視化系統

#### 技術路線

- **即時可視化**: 錄音時顯示音頻波形動畫
- **狀態指示**: 不同狀態使用不同的視覺效果
- **性能優化**: 使用 requestAnimationFrame 優化動畫

#### 可視化演算法

```javascript
startVisualization() {
  this.visualInterval = setInterval(() => {
    this.visualBars = this.visualBars.map(() =>
      this.isListening ? Math.floor(Math.random() * 30) + 5 : 5
    );
  }, 100);
}

// CSS 動畫配合
.audio-visualizer .bar {
  width: 4px;
  background: linear-gradient(to top, #4361ee, #4cc9f0);
  border-radius: 2px;
  transition: height 0.1s ease;
  min-height: 4px;
}
```

### 4. 響應式佈局系統

#### 技術路線

- **Flexbox 佈局**: 彈性的兩欄式設計
- **組件化 CSS**: Scoped Styles 避免樣式衝突
- **主題系統**: 統一的顏色和字體規範

#### 佈局結構

```vue
<template>
  <div class="voice-interaction-flow">
    <!-- 標題區域 -->
    <div class="page-header">
      <div class="header-content">
        <Icon type="ios-mic" size="24" />
        <span class="page-title">智能AI對話助手</span>
        <div class="conversation-stats">
          <Tag color="blue">對話輪次: {{ conversationRounds }}</Tag>
          <Tag color="green">總消息: {{ totalMessages }}</Tag>
        </div>
      </div>
    </div>

    <!-- 兩欄式主布局 -->
    <div class="two-column-layout">
      <!-- 左欄 - 控制與設置區域 -->
      <div class="left-panel">
        <Card class="control-card">
          <!-- 語音控制區域 -->
          <!-- 對話設置區域 -->
        </Card>
      </div>

      <!-- 右欄 - 對話與狀態區域 -->
      <div class="right-panel">
        <Card class="chat-card">
          <!-- 對話顯示區域 -->
        </Card>
      </div>
    </div>
  </div>
</template>
```

## 🔄 資料串接模式

### API 通信架構

```javascript
// HTTP 客戶端配置
import axios from "axios";

// 語音識別 API
const speechRecognitionAPI = {
  endpoint: "/process_audio",
  method: "POST",
  contentType: "multipart/form-data",
  timeout: 60000,
};

// 情緒分析 API
const emotionAnalysisAPI = {
  endpoint: "/api/emotion/upload-and-analyze",
  method: "POST",
  contentType: "multipart/form-data",
  timeout: 30000,
};

// AI 對話 API
const aiChatAPI = {
  endpoint: "/voice_clone/generate_response_voice",
  method: "POST",
  contentType: "application/json",
  timeout: 120000,
};
```

### 資料流向圖

```
用戶語音輸入
    ↓
錄音 → audioBlob
    ↓
並行處理:
├─ 語音識別 API → transcript
└─ 情緒分析 API → emotion data
    ↓
AI 對話 API → AI response + TTS audio
    ↓
更新 UI 顯示
```

### 狀態同步機制

```javascript
// 消息對象結構
const messageStructure = {
  id: Number,                    // 消息 ID
  type: String,                  // 'user' | 'ai'
  text: String,                  // 消息文字內容
  audioUrl: String,              // 音頻 URL (AI 回應)
  sentiment: String,             // 情感分析結果
  confidence: Number,            // 置信度
  isVoice: Boolean,              // 是否為語音消息
  emotionAnalysis: Object,       // 完整情緒分析數據
  detectedEmotion: String,       // 檢測到的情緒
  emotionConfidence: Number,     // 情緒置信度
  time: String,                  // 顯示時間
  timestamp: Date                // 完整時間戳
};

// 狀態更新流程
addMessage(type, text, audioUrl, sentiment, isVoice, confidence, emotionAnalysis) {
  const message = {
    id: this.messageIdCounter++,
    type, text, audioUrl, sentiment, confidence, isVoice,
    emotionAnalysis,
    detectedEmotion: emotionAnalysis?.predicted_emotion,
    emotionConfidence: emotionAnalysis?.confidence,
    time: new Date().toLocaleTimeString(),
    timestamp: new Date()
  };

  this.conversationHistory.push(message);
  this.scrollToBottom();

  // 自動播放 AI 回應
  if (type === "ai" && audioUrl && this.autoPlayEnabled) {
    this.$nextTick(() => this.playAudio(message.id));
  }
}
```

## 🎨 UI/UX 設計模式

### 設計原則

1. **直觀操作**: 一鍵式語音交互，降低學習成本
2. **即時反饋**: 清晰的狀態指示和進度顯示
3. **情緒可視化**: 豐富的情緒標籤和顏色編碼
4. **響應式設計**: 適配不同螢幕尺寸

### 交互狀態設計

```javascript
// 按鈕狀態映射
const buttonStates = {
  idle: {
    text: "按住開始對話",
    color: "linear-gradient(135deg, #4361ee, #4cc9f0)",
    icon: "ios-mic",
  },
  listening: {
    text: "正在聆聽...",
    color: "linear-gradient(135deg, #ff4757, #ff6b7a)",
    icon: "ios-radio-button-on",
    animation: "pulse",
  },
  thinking: {
    text: "正在思考...",
    color: "linear-gradient(135deg, #ffa502, #ffb142)",
    icon: "loading",
  },
  speaking: {
    text: "正在回應...",
    color: "linear-gradient(135deg, #2ed573, #7bed9f)",
    icon: "loading",
  },
};
```

### 主題色彩系統

```css
:root {
  /* 主色調 */
  --primary-color: #4361ee;
  --primary-gradient: linear-gradient(135deg, #4361ee, #4cc9f0);

  /* 狀態色彩 */
  --listening-color: #ff4757;
  --thinking-color: #ffa502;
  --speaking-color: #2ed573;

  /* 情緒色彩 */
  --emotion-happy: #52c41a;
  --emotion-sad: #ff4d4f;
  --emotion-angry: #ff4d4f;
  --emotion-surprise: #722ed1;
  --emotion-neutral: #8c8c8c;
  --emotion-calm: #1890ff;
}
```

## 🔧 性能優化策略

### 1. 組件優化

```javascript
// 使用 $set 確保響應式更新
this.$set(lastMessage, 'emotionAnalysis', response.data);

// 使用 $nextTick 確保 DOM 更新
this.$nextTick(() => {
  this.scrollToBottom();
  this.playAudio(message.id);
});

// 組件銷毀時清理資源
beforeDestroy() {
  this.stopTimer();
  this.stopVisualization();
  if (this.recorder && this.isListening) {
    this.recorder.stop();
  }
}
```

### 2. 記憶體管理

```javascript
// 音頻資源清理
onAudioEnded() {
  this.playingAudioId = null;
  this.isSpeaking = false;
  // 清理音頻 URL 避免記憶體洩漏
  URL.revokeObjectURL(audioUrl);
}

// 定時器清理
stopTimer() {
  if (this.recordingTimer) {
    clearInterval(this.recordingTimer);
    this.recordingTimer = null;
  }
}
```

### 3. 網路優化

```javascript
// API 請求超時設定
const apiConfig = {
  speechRecognition: { timeout: 60000 },
  emotionAnalysis: { timeout: 30000 },
  aiChat: { timeout: 120000 }
};

// 錯誤重試機制
async retryRequest(apiCall, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await apiCall();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

## 🛠️ 開發工具與除錯

### 除錯面板

```javascript
// 內建除錯面板
data() {
  return {
    showDebug: true,  // 開發環境顯示
    debugPanelExpanded: false
  }
}

// 除錯資訊顯示
debugInfo: {
  isListening: this.isListening,
  isThinking: this.isThinking,
  isSpeaking: this.isSpeaking,
  conversationRounds: this.conversationRounds,
  recorderState: this.recorder?.state,
  audioBlobSize: this.audioBlob?.size
}
```

### 測試工具

```javascript
// 測試方法
methods: {
  // 強制狀態測試
  forceListening() {
    this.$set(this, "isListening", true);
  },

  // 音頻測試
  testAudioBlob() {
    if (this.audioBlob) {
      const audioURL = URL.createObjectURL(this.audioBlob);
      const audio = new Audio(audioURL);
      audio.play();
    }
  },

  // 錄音功能測試
  async testRecording() {
    await this.ensureMicrophonePermission();
    this.$set(this, "isListening", true);
    await this.startRecording();

    setTimeout(async () => {
      this.$set(this, "isListening", false);
      await this.stopRecording();
      this.testAudioBlob();
    }, 3000);
  }
}
```

## 📱 瀏覽器兼容性

### 支援的瀏覽器

- **Chrome 60+**: 完整支援
- **Firefox 55+**: 完整支援
- **Safari 14+**: 基本支援 (部分 Web Audio API 限制)
- **Edge 79+**: 完整支援

### 功能檢測

```javascript
// 檢查瀏覽器支援
checkBrowserSupport() {
  const features = {
    mediaRecorder: !!window.MediaRecorder,
    getUserMedia: !!(navigator.mediaDevices?.getUserMedia),
    webAudio: !!(window.AudioContext || window.webkitAudioContext),
    es6: typeof Symbol !== 'undefined'
  };

  const unsupported = Object.entries(features)
    .filter(([key, supported]) => !supported)
    .map(([key]) => key);

  if (unsupported.length > 0) {
    this.$Message.error(`瀏覽器不支援: ${unsupported.join(', ')}`);
    return false;
  }

  return true;
}
```

## 🚀 建構與部署

### 開發環境

```bash
# 安裝依賴
npm install

# 開發服務器
npm run serve

# 建構生產版本
npm run build

# 程式碼檢查
npm run lint
```

### 生產環境配置

```javascript
// vue.config.js
module.exports = {
  publicPath:
    process.env.NODE_ENV === "production" ? "/ai-customer-service/" : "/",
  outputDir: "dist",
  assetsDir: "static",

  // 生產環境優化
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: "all",
        cacheGroups: {
          vendor: {
            name: "chunk-vendors",
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: "initial",
          },
        },
      },
    },
  },

  // PWA 配置
  pwa: {
    name: "AI客服語音系統",
    themeColor: "#4361ee",
    msTileColor: "#000000",
    appleMobileWebAppCapable: "yes",
    appleMobileWebAppStatusBarStyle: "black",
  },
};
```

## 🔐 安全考量

### 資料安全

```javascript
// 敏感資料處理
const sanitizeUserInput = (input) => {
  return input.replace(
    /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
    ""
  );
};

// API 請求攔截
axios.interceptors.request.use((config) => {
  // 添加 CSRF Token
  config.headers["X-CSRF-Token"] = getCsrfToken();
  return config;
});
```

### 隱私保護

```javascript
// 音頻資料處理
handleAudioData(audioBlob) {
  // 本地處理，不永久儲存
  const tempUrl = URL.createObjectURL(audioBlob);

  // 使用完畢立即清理
  setTimeout(() => {
    URL.revokeObjectURL(tempUrl);
  }, 60000);
}
```

## 📊 監控與分析

### 用戶行為追蹤

```javascript
// 關鍵操作記錄
trackUserAction(action, data) {
  const event = {
    action,
    data,
    timestamp: new Date().toISOString(),
    sessionId: this.sessionId,
    userId: this.userId
  };

  // 發送到分析服務
  this.sendAnalytics(event);
}

// 使用範例
this.trackUserAction('voice_recording_start', {
  duration: this.recordingTime,
  emotion: this.detectedEmotion
});
```

### 效能監控

```javascript
// API 回應時間監控
const startTime = performance.now();
const response = await axios.post("/api/endpoint", data);
const endTime = performance.now();

this.recordMetric("api_response_time", {
  endpoint: "/api/endpoint",
  duration: endTime - startTime,
  status: response.status,
});
```

## 🔮 未來擴展方向

### 技術升級

1. **Vue 3 遷移**: 利用 Composition API 和更好的 TypeScript 支援
2. **PWA 功能**: 離線支援和推送通知
3. **WebRTC 整合**: 即時語音通信功能
4. **WebAssembly**: 客戶端音頻處理優化

### 功能擴展

1. **多語言支援**: 國際化 (i18n) 實作
2. **主題系統**: 可自訂的 UI 主題
3. **插件架構**: 可擴展的功能模組
4. **即時協作**: 多用戶同時對話支援

這份前端技術文件詳細說明了系統的架構設計、核心演算法、資料串接模式以及重要的技術決策，為前端開發和維護提供了完整的技術指南。
