<!-- VoiceInteractionContainer.vue - 重構後的主容器組件 -->
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
        <Card class="control-card" :bordered="false">
          <!-- 語音控制區域 -->
          <div class="conversation-control-section">
            <div class="talk-button-container">
              <!-- 音頻可視化 -->
              <div class="audio-visualizer" :class="{ active: isListening }">
                <div
                  v-for="(bar, index) in visualBars"
                  :key="index"
                  class="bar"
                  :style="{ height: `${bar}px` }"
                ></div>
              </div>

              <!-- 一鍵式對話按鈕 -->
              <div class="talk-button-wrapper">
                <Button
                  class="talk-button"
                  :class="{
                    'is-listening': isListening,
                    'is-thinking': isThinking,
                    'is-speaking': isSpeaking,
                  }"
                  shape="circle"
                  size="large"
                  @mousedown.native="startTalk"
                  @mouseup.native="endTalk"
                  @mouseleave.native="endTalk"
                  @touchstart.native="startTalk"
                  @touchend.native="endTalk"
                  :disabled="isThinking || isSpeaking"
                  :style="buttonStyle"
                >
                  <Icon
                    v-if="!isListening && !isThinking && !isSpeaking"
                    type="ios-mic"
                    size="40"
                  />
                  <Icon
                    v-if="isListening"
                    type="ios-radio-button-on"
                    size="40"
                  />
                  <Spin v-if="isThinking || isSpeaking" size="large" />
                </Button>

                <div class="button-text">
                  {{ buttonText }}
                </div>

                <!-- 錄音時長顯示 -->
                <div v-if="isListening" class="recording-duration">
                  {{ formatTime(recordingTime) }}
                </div>
              </div>
            </div>

            <!-- 智能狀態提示 -->
            <div class="conversation-status">
              <transition name="fade" mode="out-in">
                <div
                  v-if="isListening"
                  class="status-item listening"
                  key="listening"
                >
                  <Icon type="ios-mic" />
                  <span>正在聆聽您的問題...</span>
                  <div class="voice-wave"></div>
                </div>

                <div
                  v-else-if="isThinking"
                  class="status-item thinking"
                  key="thinking"
                >
                  <Spin size="small" />
                  <span>AI正在分析與思考...</span>
                </div>

                <div
                  v-else-if="isSpeaking"
                  class="status-item speaking"
                  key="speaking"
                >
                  <Icon type="ios-volume-high" />
                  <span>AI正在回應中...</span>
                </div>

                <div v-else class="status-item waiting" key="waiting">
                  <Icon type="ios-chatbubbles" />
                  <span>按住按鈕開始對話</span>
                </div>
              </transition>
            </div>

            <!-- 快捷操作按鈕 -->
            <div class="quick-actions">
              <Button
                type="text"
                size="small"
                @click="clearConversation"
                :disabled="conversationHistory.length === 0"
              >
                <Icon type="ios-trash" />
                清空對話
              </Button>
              <Button
                type="text"
                size="small"
                @click="exportConversation"
                :disabled="conversationHistory.length === 0"
              >
                <Icon type="ios-download" />
                導出對話
              </Button>
              <Button type="text" size="small" @click="toggleAutoPlay">
                <Icon
                  :type="
                    autoPlayEnabled ? 'ios-volume-high' : 'ios-volume-mute'
                  "
                />
                {{ autoPlayEnabled ? "關閉" : "開啟" }}自動播放
              </Button>
              <Button type="text" size="small" @click="toggleDebug">
                <Icon type="ios-bug" />
                {{ showDebug ? "隱藏" : "顯示" }}調試
              </Button>
            </div>
          </div>

          <!-- 對話設置 -->
          <div class="conversation-settings">
            <div class="setting-item">
              <Form>
                <FormItem label="選擇AI助手:">
                  <Select
                    v-model="selectedStaff"
                    placeholder="選擇助手"
                    @on-change="onStaffChange"
                  >
                    <Option value="admin">通用助手</Option>
                    <Option value="staff001">專業客服</Option>
                    <Option value="staff002">技術支援</Option>
                    <Option value="staff003">創意助手</Option>
                  </Select>
                </FormItem>
              </Form>
            </div>
            <div class="setting-item">
              <Form>
                <FormItem label="回應語調:">
                  <Select v-model="responseStyle" placeholder="選擇語調">
                    <Option value="friendly">友好親切</Option>
                    <Option value="professional">專業正式</Option>
                    <Option value="casual">輕鬆隨意</Option>
                    <Option value="detailed">詳細解說</Option>
                  </Select>
                </FormItem>
              </Form>
            </div>
            <div class="setting-item">
              <Form>
                <FormItem label="對話模式:">
                  <Select v-model="conversationMode" placeholder="選擇模式">
                    <Option value="continuous">連續對話</Option>
                    <Option value="qa">問答模式</Option>
                    <Option value="creative">創意模式</Option>
                  </Select>
                </FormItem>
              </Form>
            </div>
          </div>
        </Card>
      </div>

      <!-- 右欄 - 對話與狀態區域 -->
      <div class="right-panel">
        <Card class="chat-card" :bordered="false">
          <!-- 對話顯示區域 -->
          <div class="chat-container" ref="chatContainer">
            <!-- 對話消息列表 -->
            <div
              v-for="message in conversationHistory"
              :key="message.id"
              class="message-bubble"
              :class="message.type"
            >
              <!-- 用戶消息氣泡 -->
              <div v-if="message.type === 'user'" class="user-bubble">
                <div class="bubble-content">
                  <div class="message-text">{{ message.text }}</div>

                  <!-- 用戶情緒標籤 -->
                  <div v-if="message.detectedEmotion" class="user-emotion-tags">
                    <Tag
                      :color="getEmotionColor(message.detectedEmotion)"
                      class="emotion-tag"
                    >
                      {{ getEmotionEmoji(message.detectedEmotion) }}
                      {{ getEmotionLabel(message.detectedEmotion) }}
                    </Tag>
                    <Tag
                      v-if="message.emotionConfidence"
                      color="default"
                      class="confidence-tag"
                    >
                      {{ Math.round(message.emotionConfidence * 100) }}%
                    </Tag>
                  </div>

                  <div class="message-meta">
                    <span class="bubble-time">{{ message.time }}</span>
                    <Icon
                      v-if="message.isVoice"
                      type="ios-mic"
                      size="12"
                      style="margin-left: 5px; opacity: 0.7"
                    />
                  </div>
                </div>
              </div>

              <!-- AI消息氣泡 -->
              <div v-else class="ai-bubble-container">
                <Avatar class="ai-avatar" icon="ios-help-buoy" />
                <div class="ai-bubble">
                  <div class="bubble-content">
                    <div class="ai-text">{{ message.text }}</div>

                    <!-- 情感標籤和置信度 -->
                    <div
                      v-if="message.sentiment || message.confidence"
                      class="message-tags"
                    >
                      <Tag
                        v-if="message.sentiment"
                        :color="getSentimentColor(message.sentiment)"
                        class="sentiment-tag-custom"
                      >
                        {{ message.sentiment }}
                      </Tag>
                      <Tag
                        v-if="message.confidence"
                        color="purple"
                        class="confidence-tag"
                      >
                        置信度: {{ Math.round(message.confidence * 100) }}%
                      </Tag>
                    </div>

                    <!-- 語音播放器 -->
                    <div v-if="message.audioUrl" class="voice-player">
                      <div class="audio-controls">
                        <Button
                          size="small"
                          type="text"
                          @click="playAudio(message.id)"
                          :loading="playingAudioId === message.id"
                        >
                          <Icon type="ios-play" />
                          播放語音
                        </Button>
                        <audio
                          :src="message.audioUrl"
                          :ref="`audio_${message.id}`"
                          @ended="onAudioEnded"
                          style="display: none"
                        ></audio>
                      </div>
                    </div>

                    <!-- 消息操作 -->
                    <div class="message-actions">
                      <Button
                        size="small"
                        type="text"
                        @click="copyMessage(message.text)"
                      >
                        <Icon type="ios-copy" />
                      </Button>
                      <Button
                        size="small"
                        type="text"
                        @click="regenerateResponse(message)"
                        :loading="regeneratingId === message.id"
                      >
                        <Icon type="ios-refresh" />
                      </Button>
                    </div>
                  </div>
                  <div class="bubble-time">{{ message.time }}</div>
                </div>
              </div>
            </div>

            <!-- 打字動畫 -->
            <div v-if="isThinking" class="typing-indicator">
              <div class="ai-bubble-container">
                <Avatar class="ai-avatar" icon="ios-help-buoy" />
                <div class="ai-bubble typing">
                  <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 空狀態 -->
            <div
              v-if="conversationHistory.length === 0"
              class="empty-chat-state"
            >
              <Icon type="ios-chatbubbles" size="64" color="#c7ecee" />
              <p>開始您的AI對話之旅</p>
              <p class="sub-text">按住下方按鈕開始說話，或點擊示例問題</p>

              <!-- 示例問題 -->
              <div class="example-questions">
                <Button
                  v-for="question in sampleQuestions"
                  :key="question"
                  size="small"
                  type="text"
                  @click="askSampleQuestion(question)"
                  class="example-question"
                >
                  {{ question }}
                </Button>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>

    <!-- 右側滑動調試面板 -->
    <div v-if="showDebug" class="debug-panel-overlay">
      <div class="debug-panel-slider" :class="{ expanded: debugPanelExpanded }">
        <!-- 滑動觸發器 - 依靠在面板左側 -->
        <button
          class="debug-panel-trigger"
          @click="toggleDebugPanel"
          type="button"
        >
          <Icon type="ios-bug" size="16" />
          <span class="trigger-text">診斷</span>
          <Icon
            :type="debugPanelExpanded ? 'ios-arrow-forward' : 'ios-arrow-back'"
            size="14"
            class="arrow-icon"
          />
        </button>

        <!-- 面板內容 -->
        <div class="debug-panel-content">
          <div class="debug-panel-header">
            <div class="debug-title">
              <Icon type="ios-bug" size="18" />
              <span>系統狀態診斷</span>
            </div>
            <Button
              type="text"
              size="small"
              @click="toggleDebug"
              class="close-debug-btn"
            >
              <Icon type="ios-close" />
            </Button>
          </div>

          <div class="debug-content">
            <div class="debug-item">
              <strong>聆聽:</strong>
              <span :style="{ color: isListening ? '#ff4757' : '#666' }">
                {{ isListening }}
              </span>
            </div>
            <div class="debug-item">
              <strong>思考:</strong>
              <span :style="{ color: isThinking ? '#ffa502' : '#666' }">
                {{ isThinking }}
              </span>
            </div>
            <div class="debug-item">
              <strong>回應:</strong>
              <span :style="{ color: isSpeaking ? '#2ed573' : '#666' }">
                {{ isSpeaking }}
              </span>
            </div>
            <div class="debug-item">
              <strong>輪次:</strong> {{ conversationRounds }}
            </div>
            <div class="debug-item">
              <strong>錄音器:</strong>
              {{ recorder ? recorder.state : "未初始化" }}
            </div>
            <div class="debug-item">
              <strong>音頻:</strong>
              {{ audioBlob ? `${Math.round(audioBlob.size / 1024)}KB` : "無" }}
            </div>

            <div class="debug-divider"></div>

            <div class="debug-actions">
              <Button
                @click="forceListening"
                type="primary"
                size="small"
                block
                style="margin-bottom: 8px"
              >
                測試聆聽
              </Button>
              <Button
                @click="resetAllStates"
                type="default"
                size="small"
                block
                style="margin-bottom: 8px"
              >
                重置狀態
              </Button>
              <Button @click="testAudioBlob" type="text" size="small" block>
                檢查音頻
              </Button>
              <Button
                @click="testRecording"
                type="warning"
                size="small"
                block
                style="margin-top: 8px"
              >
                測試錄音
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 錯誤提示 -->
    <Modal v-model="errorModal" title="處理錯誤" @on-ok="closeErrorModal">
      <p>{{ errorMessage }}</p>
      <div style="margin-top: 15px">
        <Button @click="retryLastAction" type="primary" size="small">
          重試
        </Button>
        <Button @click="resetConversation" type="text" size="small">
          重新開始
        </Button>
      </div>
    </Modal>

    <!-- 導出對話模態框 -->
    <Modal
      v-model="exportModal"
      title="導出對話記錄"
      @on-ok="doExportConversation"
    >
      <Form>
        <FormItem label="導出格式:">
          <RadioGroup v-model="exportFormat">
            <Radio label="text">純文字</Radio>
            <Radio label="json">JSON格式</Radio>
            <Radio label="markdown">Markdown格式</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="包含內容:">
          <CheckboxGroup v-model="exportOptions">
            <Checkbox label="timestamp">時間戳記</Checkbox>
            <Checkbox label="sentiment">情感分析</Checkbox>
            <Checkbox label="confidence">置信度</Checkbox>
          </CheckboxGroup>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "VoiceInteractionContainer",
  data() {
    return {
      // 對話狀態
      isListening: false,
      isThinking: false,
      isSpeaking: false,

      // 錄音相關
      audioBlob: null,
      recorder: null,
      recordingTime: 0,
      recordingTimer: null,
      microphonePermission: null, // 麥克風權限狀態
      isInitializingRecorder: false, // 錄音器初始化狀態

      // 可視化
      visualBars: Array(40).fill(5),
      visualInterval: null,

      // 對話管理
      conversationHistory: [],
      conversationContext: [], // 對話上下文
      messageIdCounter: 1,
      conversationRounds: 0,
      lastUserMessage: null,

      // 音頻管理
      playingAudioId: null,
      autoPlayEnabled: true,

      // 系統設置
      selectedStaff: "admin",
      responseStyle: "friendly",
      conversationMode: "continuous",

      // UI狀態
      showDebug: true, // 默認顯示調試信息以便診斷問題
      debugPanelExpanded: false, // 調試面板展開狀態
      debugPanelHoverTimer: null, // 滑鼠懸停計時器
      errorModal: false,
      errorMessage: "",
      exportModal: false,
      exportFormat: "text",
      exportOptions: ["timestamp"],
      regeneratingId: null,

      // 示例問題
      sampleQuestions: [
        "你好，請介紹一下你自己",
        "今天天氣如何？",
        "推薦一些學習資源",
        "幫我制定學習計劃",
      ],
    };
  },

  computed: {
    totalMessages() {
      return this.conversationHistory.length;
    },

    formatTime() {
      return (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, "0")}:${secs
          .toString()
          .padStart(2, "0")}`;
      };
    },

    buttonText() {
      if (this.isListening) return "正在聆聽...";
      if (this.isThinking) return "正在思考...";
      if (this.isSpeaking) return "正在回應...";
      return this.conversationHistory.length === 0
        ? "按住開始對話"
        : "繼續對話";
    },

    buttonStyle() {
      const baseStyle = {
        width: "120px !important",
        height: "120px !important",
        borderRadius: "50% !important",
        border: "none !important",
        color: "white !important",
        fontSize: "18px !important",
        fontWeight: "600 !important",
        cursor: "pointer !important",
        transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important",
        userSelect: "none",
      };

      if (this.isListening) {
        return {
          ...baseStyle,
          background: "linear-gradient(135deg, #ff4757, #ff6b7a) !important",
          boxShadow: "0 0 30px rgba(255, 71, 87, 0.6) !important",
        };
      } else if (this.isThinking) {
        return {
          ...baseStyle,
          background: "linear-gradient(135deg, #ffa502, #ffb142) !important",
          boxShadow: "0 0 25px rgba(255, 165, 2, 0.5) !important",
        };
      } else if (this.isSpeaking) {
        return {
          ...baseStyle,
          background: "linear-gradient(135deg, #2ed573, #7bed9f) !important",
          boxShadow: "0 0 25px rgba(46, 213, 115, 0.5) !important",
        };
      } else {
        return {
          ...baseStyle,
          background: "linear-gradient(135deg, #4361ee, #4cc9f0) !important",
          boxShadow: "0 8px 25px rgba(67, 97, 238, 0.3) !important",
        };
      }
    },
  },

  methods: {
    // 一鍵式對話 - 開始
    async startTalk() {
      console.log("🎤 startTalk 被調用");

      if (this.isThinking || this.isSpeaking || this.isInitializingRecorder) {
        console.log("❌ 按鈕被禁用，無法開始錄音");
        return;
      }

      try {
        // 先檢查並請求麥克風權限
        await this.ensureMicrophonePermission();

        // 強制更新狀態
        this.$set(this, "isListening", true);
        this.$set(this, "isThinking", false);
        this.$set(this, "isSpeaking", false);

        await this.startRecording();

        // 觸覺反饋 (移動端)
        if (navigator.vibrate) {
          navigator.vibrate(50);
        }

        // 顯示用戶提示
        this.$Message.info("🎤 開始錄音，請說話...");
      } catch (error) {
        console.error("❌ 開始錄音失敗:", error);
        this.$Message.error("無法開始錄音: " + error.message);
        this.resetStates();
      }
    },

    // 一鍵式對話 - 結束
    async endTalk() {
      console.log("🛑 endTalk 被調用");

      if (!this.isListening) {
        console.log("❌ 不在聆聽狀態，無法結束");
        return;
      }

      // 檢查最小錄音時間
      if (this.recordingTime < 1) {
        console.warn("⚠️ 錄音時間太短，延長到最小時間");
        this.$Message.warning("錄音時間太短，請說話時間長一點");
        return;
      }

      // 強制更新狀態
      this.$set(this, "isListening", false);
      this.$set(this, "isThinking", true);
      this.$set(this, "isSpeaking", false);

      try {
        // 停止錄音
        await this.stopRecording();

        // 多次檢查 audioBlob，給 onstop 事件更多時間
        let retryCount = 0;
        const maxRetries = 5;

        while (!this.audioBlob && retryCount < maxRetries) {
          console.log(
            `⏳ 等待 audioBlob 生成，重試 ${retryCount + 1}/${maxRetries}`
          );
          await new Promise((resolve) => setTimeout(resolve, 300));
          retryCount++;
        }

        if (!this.audioBlob) {
          console.error(
            "❌ audioBlob 為空，錄音器狀態:",
            this.recorder ? this.recorder.state : "null"
          );
          console.error("❌ 錄音時間:", this.recordingTime);
          console.error("❌ 重試次數:", retryCount);
          throw new Error("錄音失敗，請重試。請確保錄音時間超過1秒。");
        }

        console.log(
          "✅ audioBlob 檢查通過，大小:",
          this.audioBlob.size,
          "bytes"
        );

        // 語音識別
        const transcript = await this.performSpeechRecognition();
        this.addMessage("user", transcript, null, null, true);
        this.lastUserMessage = transcript;

        // AI分析和語音生成
        this.$set(this, "isListening", false);
        this.$set(this, "isThinking", false);
        this.$set(this, "isSpeaking", true);

        const aiResponse = await this.performAIAnalysis(transcript);
        this.addMessage(
          "ai",
          aiResponse.text,
          aiResponse.audioUrl,
          aiResponse.sentiment,
          false,
          aiResponse.confidence
        );

        // 更新對話輪次
        this.conversationRounds++;
      } catch (error) {
        this.showError(error.message);
      } finally {
        this.resetStates();
      }
    },

    // 示例問題
    async askSampleQuestion(question) {
      this.addMessage("user", question, null, null, false);
      this.lastUserMessage = question;
      this.isThinking = true;

      try {
        const aiResponse = await this.performAIAnalysis(question);
        this.addMessage(
          "ai",
          aiResponse.text,
          aiResponse.audioUrl,
          aiResponse.sentiment,
          false,
          aiResponse.confidence
        );
        this.conversationRounds++;
      } catch (error) {
        this.showError(error.message);
      } finally {
        this.resetStates();
      }
    },

    // 重新生成回應
    async regenerateResponse(message) {
      if (message.type !== "ai" || !this.lastUserMessage) return;

      this.regeneratingId = message.id;
      try {
        const aiResponse = await this.performAIAnalysis(this.lastUserMessage);

        // 更新消息內容
        const index = this.conversationHistory.findIndex(
          (m) => m.id === message.id
        );
        if (index !== -1) {
          this.$set(this.conversationHistory, index, {
            ...this.conversationHistory[index],
            text: aiResponse.text,
            audioUrl: aiResponse.audioUrl,
            sentiment: aiResponse.sentiment,
            confidence: aiResponse.confidence,
            time: new Date().toLocaleTimeString(),
          });
        }

        this.$Message.success("回應已重新生成");
      } catch (error) {
        this.showError("重新生成失敗: " + error.message);
      } finally {
        this.regeneratingId = null;
      }
    },

    // 預檢查麥克風可用性（不請求權限）
    async checkMicrophoneAvailability() {
      console.log("🔍 預檢查麥克風可用性...");

      // 檢查瀏覽器支援
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.warn("⚠️ 瀏覽器不支援錄音功能");
        return;
      }

      // 檢查權限狀態（不請求權限）
      if (navigator.permissions) {
        try {
          const permission = await navigator.permissions.query({
            name: "microphone",
          });
          console.log("🎤 當前麥克風權限狀態:", permission.state);
          this.microphonePermission = permission.state;

          // 監聽權限變化
          permission.onchange = () => {
            console.log("🔄 麥克風權限狀態變更:", permission.state);
            this.microphonePermission = permission.state;
          };
        } catch (permError) {
          console.warn("⚠️ 無法查詢權限狀態:", permError);
        }
      }
    },

    // 檢查並確保麥克風權限
    async ensureMicrophonePermission() {
      console.log("🔍 檢查麥克風權限...");

      // 檢查瀏覽器支援
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("您的瀏覽器不支援錄音功能");
      }

      // 檢查權限狀態
      if (navigator.permissions) {
        try {
          const permission = await navigator.permissions.query({
            name: "microphone",
          });
          console.log("🎤 麥克風權限狀態:", permission.state);
          this.microphonePermission = permission.state;

          if (permission.state === "denied") {
            throw new Error("麥克風權限被拒絕，請在瀏覽器設置中允許麥克風存取");
          }
        } catch (permError) {
          console.warn("⚠️ 無法查詢權限狀態:", permError);
        }
      }

      // 如果是第一次使用，先請求權限
      if (this.microphonePermission !== "granted") {
        console.log("📱 首次請求麥克風權限...");
        try {
          const testStream = await navigator.mediaDevices.getUserMedia({
            audio: true,
          });
          console.log("✅ 麥克風權限獲取成功");
          testStream.getTracks().forEach((track) => track.stop()); // 立即關閉測試流
          this.microphonePermission = "granted";
        } catch (error) {
          console.error("❌ 麥克風權限請求失敗:", error);
          if (error.name === "NotAllowedError") {
            throw new Error("麥克風權限被拒絕，請允許網站使用麥克風");
          } else if (error.name === "NotFoundError") {
            throw new Error("未找到麥克風設備，請檢查設備連接");
          } else {
            throw new Error("無法訪問麥克風: " + error.message);
          }
        }
      }
    },

    // 開始錄音
    async startRecording() {
      console.log("🎙️ startRecording 開始執行");

      if (this.isInitializingRecorder) {
        console.log("⚠️ 錄音器正在初始化中，請稍候...");
        return;
      }

      this.isInitializingRecorder = true;

      try {
        console.log("📱 獲取麥克風流...");
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true,
            sampleRate: 44100,
          },
        });
        console.log("✅ 麥克風流獲取成功，stream:", stream);

        // 檢查流是否有效
        if (!stream || stream.getTracks().length === 0) {
          throw new Error("無法獲取有效的音頻流");
        }

        this.recorder = new MediaRecorder(stream, {
          mimeType: MediaRecorder.isTypeSupported("audio/webm")
            ? "audio/webm"
            : "audio/wav",
        });
        console.log("🎬 MediaRecorder 創建成功:", this.recorder);

        const audioChunks = [];

        this.recorder.ondataavailable = (event) => {
          console.log("📊 收到音頻數據，大小:", event.data.size);
          if (event.data.size > 0) {
            audioChunks.push(event.data);
          }
        };

        this.recorder.onstop = () => {
          console.log("🔴 onstop 事件觸發");
          console.log("收集到的音頻塊數量:", audioChunks.length);
          console.log(
            "每個音頻塊大小:",
            audioChunks.map((chunk) => chunk.size)
          );

          if (audioChunks.length > 0) {
            const totalSize = audioChunks.reduce(
              (sum, chunk) => sum + chunk.size,
              0
            );
            console.log("音頻塊總大小:", totalSize, "bytes");

            if (totalSize > 0) {
              this.audioBlob = new Blob(audioChunks, {
                type: this.recorder.mimeType || "audio/wav",
              });
              console.log(
                "💾 音頻Blob創建完成，大小:",
                this.audioBlob.size,
                "bytes，類型:",
                this.audioBlob.type
              );
            } else {
              console.warn("⚠️ 音頻塊總大小為0");
              this.audioBlob = null;
            }
          } else {
            console.warn("⚠️ 沒有收集到音頻數據");
            this.audioBlob = null;
          }

          // 關閉麥克風流
          stream.getTracks().forEach((track) => {
            track.stop();
            console.log("🔌 音頻軌道已關閉:", track.label);
          });
        };

        this.recorder.onerror = (event) => {
          console.error("❌ MediaRecorder 錯誤:", event.error);
          this.$Message.error("錄音過程中發生錯誤: " + event.error.message);
        };

        // 等待一小段時間確保 MediaRecorder 完全初始化
        await new Promise((resolve) => setTimeout(resolve, 200));

        // 使用更頻繁的數據收集間隔，確保能收集到數據
        this.recorder.start(100); // 每100ms收集一次數據，確保不會遺漏
        console.log("🔴 開始錄音，狀態:", this.recorder.state);

        // 驗證錄音確實開始了
        await new Promise((resolve) => setTimeout(resolve, 100));
        if (this.recorder.state !== "recording") {
          throw new Error("錄音器啟動失敗，狀態: " + this.recorder.state);
        }
        console.log("✅ 錄音器狀態確認:", this.recorder.state);

        this.startTimer();
        this.startVisualization();
      } catch (error) {
        console.error("❌ 錄音失敗:", error);
        this.$Message.error("無法開始錄音: " + error.message);
        this.$set(this, "isListening", false);
        throw error;
      } finally {
        this.isInitializingRecorder = false;
      }
    },

    // 停止錄音
    async stopRecording() {
      console.log("🛑 stopRecording 開始執行");
      console.log("錄音器狀態:", this.recorder ? this.recorder.state : "null");
      console.log("當前錄音時間:", this.recordingTime, "秒");

      if (this.recorder && this.recorder.state === "recording") {
        console.log("🔴 停止錄音器...");

        // 先停止計時器和可視化
        console.log("⏰ 停止計時器...");
        this.stopTimer();
        console.log("📊 停止可視化...");
        this.stopVisualization();

        // 檢查錄音時間是否足夠
        if (this.recordingTime < 1) {
          console.warn("⚠️ 錄音時間太短:", this.recordingTime, "秒");
          // 即使時間短也要嘗試停止錄音
        }

        // 等待錄音完全停止，設置超時保護
        const stopPromise = new Promise((resolve, reject) => {
          const timeout = setTimeout(() => {
            console.error("❌ 停止錄音超時");
            reject(new Error("停止錄音超時"));
          }, 5000); // 5秒超時

          if (this.recorder.state === "inactive") {
            clearTimeout(timeout);
            console.log("✅ 錄音器已經是非活動狀態");
            resolve();
          } else {
            this.recorder.addEventListener(
              "stop",
              () => {
                clearTimeout(timeout);
                console.log("✅ 錄音停止事件觸發");
                resolve();
              },
              { once: true }
            );

            // 執行停止
            this.recorder.stop();
          }
        });

        try {
          await stopPromise;
          console.log("✅ 錄音完全停止");

          // 額外等待一點時間確保 onstop 事件處理完成
          await new Promise((resolve) => setTimeout(resolve, 200));

          console.log(
            "🔍 停止後檢查 audioBlob:",
            this.audioBlob ? `${this.audioBlob.size} bytes` : "null"
          );
        } catch (error) {
          console.error("❌ 停止錄音失敗:", error);
          throw error;
        }
      } else if (this.recorder) {
        console.log("⚠️ 錄音器狀態不是 recording:", this.recorder.state);
      } else {
        console.log("❌ 錄音器不存在");
        throw new Error("錄音器未初始化");
      }
    },

    // 執行語音識別
    async performSpeechRecognition() {
      console.log("🎯 開始語音識別...");
      console.log("音頻Blob信息:", {
        size: this.audioBlob?.size,
        type: this.audioBlob?.type,
      });

      const formData = new FormData();
      formData.append("file", this.audioBlob, "recording.wav");

      console.log("📤 發送語音識別請求...");
      const response = await axios.post("/process_audio", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 60000, // 60秒超时
      });

      console.log("📥 語音識別響應:", response.data);

      if (response.data.transcript) {
        console.log("✅ 語音識別成功:", response.data.transcript);

        // 同時進行情緒識別
        this.performEmotionAnalysis();

        return response.data.transcript;
      } else {
        console.error("❌ 語音識別失敗，響應:", response.data);
        throw new Error("語音識別失敗");
      }
    },

    // 執行情緒識別
    async performEmotionAnalysis() {
      try {
        console.log("😊 開始情緒識別...");

        const formData = new FormData();
        formData.append("file", this.audioBlob, "recording.wav");
        formData.append("method", "advanced"); // 可以改為 "basic"/"advanced"

        const response = await axios.post(
          "/api/emotion/upload-and-analyze",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
            timeout: 30000,
          }
        );

        if (response.data && !response.data.error) {
          console.log("✅ 情緒識別成功:", response.data);

          // 儲存情緒分析結果到最後一條用戶消息
          if (this.conversationHistory.length > 0) {
            const lastMessage =
              this.conversationHistory[this.conversationHistory.length - 1];
            if (lastMessage.type === "user") {
              this.$set(lastMessage, "emotionAnalysis", response.data);
              this.$set(
                lastMessage,
                "detectedEmotion",
                response.data.predicted_emotion
              );
              this.$set(
                lastMessage,
                "emotionConfidence",
                response.data.confidence
              );
            }
          }

          // 顯示情緒識別結果
          this.$Message.info(
            `檢測到情緒: ${response.data.predicted_emotion} (${Math.round(
              response.data.confidence * 100
            )}%)`
          );

          return response.data;
        }
      } catch (error) {
        console.warn("⚠️ 情緒識別失敗:", error.message);
        // 情緒識別失敗不影響主流程
      }
    },

    // AI分析
    async performAIAnalysis(transcript) {
      // 構建對話上下文
      const context = this.buildConversationContext();

      const response = await axios.post(
        "/voice_clone/generate_response_voice",
        {
          user_input: transcript,
          staff_code: this.selectedStaff,
          response_style: this.responseStyle,
          conversation_mode: this.conversationMode,
          conversation_context: context,
          conversation_round: this.conversationRounds,
        },
        {
          timeout: 120000,
        }
      );

      if (response.data.status === "success") {
        return {
          text: response.data.ai_analysis.response_text,
          sentiment: response.data.ai_analysis.sentiment,
          confidence: response.data.ai_analysis.confidence || 0.95,
          audioUrl: response.data.voice_output.audio_url,
        };
      } else {
        throw new Error(response.data.message || "AI分析失敗");
      }
    },

    // 構建對話上下文
    buildConversationContext() {
      // 保留最近5輪對話作為上下文
      const recentMessages = this.conversationHistory.slice(-10);
      return recentMessages.map((msg) => ({
        role: msg.type === "user" ? "user" : "assistant",
        content: msg.text,
        timestamp: msg.timestamp,
      }));
    },

    // 添加消息
    addMessage(
      type,
      text,
      audioUrl = null,
      sentiment = null,
      isVoice = false,
      confidence = null,
      emotionAnalysis = null
    ) {
      const message = {
        id: this.messageIdCounter++,
        type,
        text,
        audioUrl,
        sentiment,
        confidence,
        isVoice,
        emotionAnalysis,
        detectedEmotion: emotionAnalysis?.predicted_emotion,
        emotionConfidence: emotionAnalysis?.confidence,
        time: new Date().toLocaleTimeString(),
        timestamp: new Date(),
      };

      this.conversationHistory.push(message);
      this.scrollToBottom();

      // 自動播放AI回應
      if (type === "ai" && audioUrl && this.autoPlayEnabled) {
        this.$nextTick(() => {
          this.playAudio(message.id);
        });
      }
    },

    // 播放音頻
    playAudio(messageId) {
      const audioRef = this.$refs[`audio_${messageId}`];
      if (audioRef && audioRef[0]) {
        this.playingAudioId = messageId;
        audioRef[0].play().catch((error) => {
          console.warn("播放失敗:", error);
          this.$Message.warning("音頻播放失敗，請檢查設備設置");
        });
      }
    },

    // 音頻播放結束
    onAudioEnded() {
      this.playingAudioId = null;
      this.isSpeaking = false;
    },

    // 複製消息
    copyMessage(text) {
      navigator.clipboard.writeText(text).then(() => {
        this.$Message.success("消息已複製到剪貼板");
      });
    },

    // 清空對話
    clearConversation() {
      this.$Modal.confirm({
        title: "確認清空",
        content: "確定要清空所有對話記錄嗎？此操作無法撤銷。",
        onOk: () => {
          this.conversationHistory = [];
          this.conversationContext = [];
          this.messageIdCounter = 1;
          this.conversationRounds = 0;
          this.lastUserMessage = null;
          this.$Message.success("對話記錄已清空");
        },
      });
    },

    // 導出對話
    exportConversation() {
      this.exportModal = true;
    },

    // 切換自動播放
    toggleAutoPlay() {
      this.autoPlayEnabled = !this.autoPlayEnabled;
      this.$Message.info(
        this.autoPlayEnabled ? "已開啟自動播放" : "已關閉自動播放"
      );
    },

    // 客服更換
    onStaffChange() {
      this.$Message.info(`已切換到 ${this.selectedStaff} 助手`);
    },

    // 計時器
    startTimer() {
      this.recordingTime = 0;
      this.recordingTimer = setInterval(() => {
        this.recordingTime++;
      }, 1000);
    },

    stopTimer() {
      if (this.recordingTimer) {
        clearInterval(this.recordingTimer);
        this.recordingTimer = null;
      }
    },

    // 可視化
    startVisualization() {
      this.visualInterval = setInterval(() => {
        this.visualBars = this.visualBars.map(() =>
          this.isListening ? Math.floor(Math.random() * 30) + 5 : 5
        );
      }, 100);
    },

    stopVisualization() {
      if (this.visualInterval) {
        clearInterval(this.visualInterval);
        this.visualInterval = null;
      }
      setTimeout(() => {
        this.visualBars = Array(40).fill(5);
      }, 300);
    },

    // 滾動到底部
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.chatContainer) {
          this.$refs.chatContainer.scrollTop =
            this.$refs.chatContainer.scrollHeight;
        }
      });
    },

    // 重置狀態
    resetStates() {
      console.log("🔄 重置所有狀態");
      this.$set(this, "isListening", false);
      this.$set(this, "isThinking", false);
      this.$set(this, "isSpeaking", false);
      this.audioBlob = null;
    },

    // 調試方法
    forceListening() {
      console.log("🔴 強制設為聆聽狀態");
      this.$set(this, "isListening", true);
      this.$set(this, "isThinking", false);
      this.$set(this, "isSpeaking", false);
    },

    resetAllStates() {
      console.log("🔄 重置所有狀態");
      this.$set(this, "isListening", false);
      this.$set(this, "isThinking", false);
      this.$set(this, "isSpeaking", false);
    },

    testAudioBlob() {
      if (this.audioBlob) {
        console.log("🎵 音頻Blob詳細信息:");
        console.log("- 大小:", this.audioBlob.size, "bytes");
        console.log("- 類型:", this.audioBlob.type);
        console.log("- 時間戳:", new Date().toLocaleTimeString());

        // 創建音頻URL進行播放測試
        const audioURL = URL.createObjectURL(this.audioBlob);
        const audio = new Audio(audioURL);
        audio
          .play()
          .then(() => {
            console.log("✅ 音頻播放測試成功");
            this.$Message.success("音頻文件正常，可以播放");
          })
          .catch((error) => {
            console.error("❌ 音頻播放測試失敗:", error);
            this.$Message.error("音頻文件損壞或格式不支持");
          });
      } else {
        console.log("❌ 沒有音頻文件");
        this.$Message.warning("請先錄音再測試");
      }
    },

    // 測試錄音功能
    async testRecording() {
      console.log("🧪 開始測試錄音功能");
      this.$Message.info("開始測試錄音，將錄音3秒...");

      try {
        // 重置狀態
        this.resetStates();

        // 確保權限
        await this.ensureMicrophonePermission();

        // 開始錄音
        this.$set(this, "isListening", true);
        await this.startRecording();

        // 錄音3秒
        await new Promise((resolve) => setTimeout(resolve, 3000));

        // 停止錄音
        this.$set(this, "isListening", false);
        await this.stopRecording();

        // 檢查結果
        if (this.audioBlob && this.audioBlob.size > 0) {
          console.log("✅ 測試錄音成功，大小:", this.audioBlob.size, "bytes");
          this.$Message.success(
            `測試錄音成功！音頻大小: ${Math.round(
              this.audioBlob.size / 1024
            )}KB`
          );

          // 自動播放測試
          this.testAudioBlob();
        } else {
          console.error("❌ 測試錄音失敗，沒有生成音頻");
          this.$Message.error("測試錄音失敗，沒有生成音頻數據");
        }
      } catch (error) {
        console.error("❌ 測試錄音出錯:", error);
        this.$Message.error("測試錄音失敗: " + error.message);
      } finally {
        this.resetStates();
      }
    },

    // 切換調試面板
    toggleDebug() {
      this.showDebug = !this.showDebug;
      if (!this.showDebug) {
        this.debugPanelExpanded = false;
      }
      this.$Message.info(this.showDebug ? "已顯示調試面板" : "已隱藏調試面板");
    },

    // 切換調試面板展開狀態
    toggleDebugPanel() {
      console.log(
        "🔧 toggleDebugPanel 被調用，當前狀態:",
        this.debugPanelExpanded
      );
      this.debugPanelExpanded = !this.debugPanelExpanded;
      console.log("🔧 新狀態:", this.debugPanelExpanded);
      this.$Message.info(
        this.debugPanelExpanded ? "調試面板已展開" : "調試面板已收合"
      );
    },

    // 滑鼠懸停事件
    onDebugPanelHover() {
      if (this.debugPanelHoverTimer) {
        clearTimeout(this.debugPanelHoverTimer);
      }
      this.debugPanelHoverTimer = setTimeout(() => {
        if (!this.debugPanelExpanded) {
          this.debugPanelExpanded = true;
        }
      }, 500); // 500ms 後自動展開
    },

    // 滑鼠離開事件
    onDebugPanelLeave() {
      if (this.debugPanelHoverTimer) {
        clearTimeout(this.debugPanelHoverTimer);
        this.debugPanelHoverTimer = null;
      }
      // 延遲收合，給用戶時間移動到面板內容
      setTimeout(() => {
        if (!this.$el.querySelector(".debug-panel-slider:hover")) {
          this.debugPanelExpanded = false;
        }
      }, 300);
    },

    // 錯誤處理
    showError(message) {
      console.error("❌ 系統錯誤:", message);
      this.errorMessage = message;
      this.errorModal = true;
      this.$Message.error(message);
    },

    retryLastAction() {
      if (this.lastUserMessage) {
        this.askSampleQuestion(this.lastUserMessage);
      }
      this.errorModal = false;
    },

    resetConversation() {
      this.clearConversation();
      this.errorModal = false;
    },

    closeErrorModal() {
      this.errorModal = false;
    },

    // 情感顏色
    getSentimentColor(sentiment) {
      const colors = {
        正面: "green",
        中性: "default",
        負面: "red",
        積極: "green",
        消極: "orange",
      };
      return colors[sentiment] || "default";
    },

    // 情緒顏色映射
    getEmotionColor(emotion) {
      const colors = {
        // 正面情緒 - 綠色系
        happy: "green",
        excited: "green",
        confident: "green",
        relaxed: "blue",
        calm: "blue",

        // 負面情緒 - 紅色系
        sad: "red",
        angry: "red",
        frustrated: "red",
        disgust: "orange",

        // 恐懼相關 - 橙色系
        fear: "orange",
        fearful: "orange",

        // 驚訝相關 - 紫色系
        surprise: "purple",
        surprised: "purple",
        confused: "purple",

        // 中性情緒 - 灰色系
        neutral: "default",
        bored: "default",
      };
      return colors[emotion] || "default";
    },

    // 情緒標籤翻譯（繁體中文）
    getEmotionLabel(emotion) {
      const labels = {
        // 基礎情緒
        happy: "開心",
        sad: "難過",
        angry: "生氣",
        neutral: "平靜",
        fear: "恐懼",
        surprise: "驚訝",

        // 進階情緒（Wav2Vec2 模型）
        calm: "冷靜",
        disgust: "厭惡",
        fearful: "害怕",
        surprised: "驚喜",

        // 其他可能的情緒
        excited: "興奮",
        bored: "無聊",
        confused: "困惑",
        confident: "自信",
        frustrated: "沮喪",
        relaxed: "放鬆",
      };
      return labels[emotion] || emotion;
    },

    // 情緒表情符號映射
    getEmotionEmoji(emotion) {
      const emojis = {
        // 正面情緒
        happy: "😊",
        excited: "🤩",
        confident: "😎",
        relaxed: "😌",
        calm: "😇",
        surprised: "😄",

        // 負面情緒
        sad: "😢",
        angry: "😠",
        frustrated: "😤",
        disgust: "🤢",

        // 恐懼相關
        fear: "😨",
        fearful: "😰",

        // 驚訝相關
        surprise: "😲",
        confused: "😕",

        // 中性情緒
        neutral: "😐",
        bored: "😴",
      };
      return emojis[emotion] || "🎭";
    },

    // 執行導出
    doExportConversation() {
      const conversations = this.conversationHistory.map((msg) => {
        const baseData = {
          type: msg.type === "user" ? "用戶" : "AI助手",
          content: msg.text,
        };

        if (this.exportOptions.includes("timestamp")) {
          baseData.time = msg.time;
        }
        if (this.exportOptions.includes("sentiment") && msg.sentiment) {
          baseData.sentiment = msg.sentiment;
        }
        if (this.exportOptions.includes("confidence") && msg.confidence) {
          baseData.confidence = Math.round(msg.confidence * 100) + "%";
        }

        return baseData;
      });

      let exportData = "";
      const timestamp = new Date().toLocaleString();

      switch (this.exportFormat) {
        case "text":
          exportData = `對話記錄 - ${timestamp}\n\n`;
          conversations.forEach((conv) => {
            exportData += `${conv.type}: ${conv.content}\n`;
            if (conv.time) exportData += `時間: ${conv.time}\n`;
            if (conv.sentiment) exportData += `情感: ${conv.sentiment}\n`;
            if (conv.confidence) exportData += `置信度: ${conv.confidence}\n`;
            exportData += "\n";
          });
          break;

        case "json":
          exportData = JSON.stringify(
            {
              exportTime: timestamp,
              totalMessages: conversations.length,
              conversationRounds: this.conversationRounds,
              conversations,
            },
            null,
            2
          );
          break;

        case "markdown":
          exportData = `# 對話記錄\n\n**導出時間**: ${timestamp}  \n**總消息數**: ${conversations.length}  \n**對話輪次**: ${this.conversationRounds}\n\n---\n\n`;
          conversations.forEach((conv) => {
            exportData += `## ${conv.type}\n\n${conv.content}\n\n`;
            if (conv.time || conv.sentiment || conv.confidence) {
              exportData += "**詳細信息:**\n";
              if (conv.time) exportData += `- 時間: ${conv.time}\n`;
              if (conv.sentiment) exportData += `- 情感: ${conv.sentiment}\n`;
              if (conv.confidence)
                exportData += `- 置信度: ${conv.confidence}\n`;
              exportData += "\n";
            }
          });
          break;
      }

      // 下載文件
      const blob = new Blob([exportData], { type: "text/plain;charset=utf-8" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `conversation_${new Date().getTime()}.${
        this.exportFormat === "json"
          ? "json"
          : this.exportFormat === "markdown"
          ? "md"
          : "txt"
      }`;
      link.click();

      this.$Message.success("對話記錄已導出");
      this.exportModal = false;
    },
  },

  async mounted() {
    // 組件載入時預檢查麥克風權限
    try {
      await this.checkMicrophoneAvailability();
    } catch (error) {
      console.warn("⚠️ 麥克風預檢查失敗:", error.message);
    }
  },

  beforeDestroy() {
    this.stopTimer();
    this.stopVisualization();
    if (this.recorder && this.isListening) {
      this.recorder.stop();
    }
  },
};
</script>

<style scoped>
.voice-interaction-flow {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px;
  height: calc(100vh - 120px);
  overflow: hidden;
}

/* 頁面標題區域 */
.page-header {
  margin-bottom: 16px;
  flex-shrink: 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #1c1c1c;
  margin-left: 8px;
}

/* 兩欄式主布局 */
.two-column-layout {
  display: flex;
  gap: 16px;
  height: calc(100% - 80px);
  overflow: hidden;
}

/* 左欄 - 控制區域 */
.left-panel {
  width: 340px;
  flex-shrink: 0;
}

.control-card {
  height: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.control-card .ivu-card-body {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

/* 右欄 - 對話區域 */
.right-panel {
  flex: 1;
  min-width: 0;
}

.chat-card {
  height: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.chat-card .ivu-card-body {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;
}

/* 右側滑動調試面板 */
.debug-panel-overlay {
  position: fixed;
  top: 0;
  right: -20px;
  height: 100vh;
  width: 320px;
  z-index: 1000;
  pointer-events: auto;
  overflow: visible;
}

.debug-panel-slider {
  position: absolute;
  top: 50%;
  right: 0;
  width: 280px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 15px 0 0 15px;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
  border: 1px solid #e8e8e8;
  border-right: none;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateY(-50%) translateX(245px);
  pointer-events: all;
  max-height: 80vh;
  overflow: visible;
}

.debug-panel-slider.expanded {
  transform: translateY(-50%) translateX(-40px);
}

.debug-panel-trigger {
  position: absolute;
  left: -35px;
  top: 50%;
  transform: translateY(-50%);
  width: 35px;
  height: 80px;
  background: linear-gradient(135deg, #4361ee, #4cc9f0);
  border: none;
  border-radius: 8px 0 0 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  cursor: pointer !important;
  transition: all 0.3s ease;
  color: white;
  font-size: 10px;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  z-index: 10001 !important;
  pointer-events: auto !important;
  outline: none;
}

.debug-panel-trigger:hover {
  background: linear-gradient(135deg, #3651d4, #45b7d1);
  transform: translateY(-50%) translateX(-3px);
}

.trigger-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-size: 10px;
  font-weight: 500;
}

.arrow-icon {
  transition: transform 0.3s ease;
}

.debug-panel-content {
  padding: 0;
  height: 100%;
  overflow-y: auto;
}

.debug-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;
}

.debug-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  font-size: 16px;
  font-weight: 600;
  color: #1c1c1c;
}

.close-debug-btn {
  padding: 4px 8px;
  color: #666;
  font-size: 14px;
}

.close-debug-btn:hover {
  color: #1c1c1c;
  background: rgba(0, 0, 0, 0.05);
}

.debug-content {
  font-family: "SF Mono", "Monaco", "Consolas", monospace;
  font-size: 12px;
  padding: 12px 16px;
}

.debug-item {
  margin: 8px 0;
  line-height: 1.4;
  padding: 6px 0;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.debug-item:last-child {
  border-bottom: none;
}

.debug-item strong {
  color: #1c1c1c;
  font-weight: 600;
  font-size: 12px;
}

.debug-divider {
  height: 1px;
  background: #e8e8e8;
  margin: 15px 0;
}

.debug-actions {
  margin-top: 12px;
}

.debug-actions .ivu-btn {
  font-size: 12px;
  height: 32px;
  border-radius: 6px;
  margin-bottom: 6px;
}

/* 主內容區域 */
.main-content-area {
  flex: 1;
  min-width: 0;
}

.main-card {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.main-card .ivu-card-body {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
  color: #1c1c1c;
  margin-bottom: 0;
}

.conversation-stats {
  display: flex;
  gap: 8px;
}

.conversation-stats .ivu-tag {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 6px;
}

/* 語音控制區域樣式 */
.conversation-control-section {
  text-align: center;
  padding: 24px 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  margin-bottom: 16px;
  flex-shrink: 0;
}

.talk-button-container {
  position: relative;
  display: inline-block;
}

.audio-visualizer {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 60px;
  margin-bottom: 20px;
  gap: 2px;
  opacity: 0.3;
  transition: opacity 0.3s ease;
}

.audio-visualizer.active {
  opacity: 1;
}

.audio-visualizer .bar {
  width: 4px;
  background: linear-gradient(to top, #4361ee, #4cc9f0);
  border-radius: 2px;
  transition: height 0.1s ease;
  min-height: 4px;
}

.talk-button-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.talk-button {
  width: 80px !important;
  height: 80px !important;
  border-radius: 50% !important;
  border: none !important;
  background: linear-gradient(135deg, #4361ee, #4cc9f0) !important;
  color: white !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 0 4px 16px rgba(67, 97, 238, 0.25) !important;
  user-select: none;
  -webkit-user-select: none;
}

.talk-button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 35px rgba(67, 97, 238, 0.4) !important;
}

.talk-button.is-listening {
  transform: scale(1.1) !important;
  animation: pulse 1.5s infinite;
}

.talk-button.is-thinking {
  transform: scale(1.05) !important;
}

.talk-button.is-speaking {
  transform: scale(1.05) !important;
}

.button-text {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-top: 8px;
}

.recording-duration {
  font-size: 14px;
  font-weight: 600;
  color: #ff4757;
  background: rgba(255, 71, 87, 0.1);
  padding: 6px 12px;
  border-radius: 16px;
  margin-top: 8px;
}

/* 狀態提示樣式 */
.conversation-status {
  margin: 16px 0;
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.status-item.listening {
  background: linear-gradient(135deg, #ff4757, #ff6b7a);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 71, 87, 0.3);
}

.status-item.thinking {
  background: linear-gradient(135deg, #ffa502, #ffb142);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 165, 2, 0.3);
}

.status-item.speaking {
  background: linear-gradient(135deg, #2ed573, #7bed9f);
  color: white;
  box-shadow: 0 4px 15px rgba(46, 213, 115, 0.3);
}

.status-item.waiting {
  background: linear-gradient(135deg, #4361ee, #4cc9f0);
  color: white;
  box-shadow: 0 4px 15px rgba(67, 97, 238, 0.3);
}

.voice-wave {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  animation: wave 1.5s infinite;
}

/* 快捷操作樣式 */
.quick-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
  flex-wrap: wrap;
  flex-shrink: 0;
}

.quick-actions .ivu-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  border-radius: 16px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 14px;
  height: 32px;
}

.quick-actions .ivu-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 對話顯示樣式 */
.chat-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 16px;
  min-height: 0;
  max-height: calc(100vh - 300px); /* 設置最大高度確保滾動 */
  width: 100%;
  max-width: 100%;
  scrollbar-width: thin; /* Firefox 滾動條 */
  scrollbar-color: rgba(0, 0, 0, 0.3) rgba(0, 0, 0, 0.1); /* Firefox 滾動條顏色 */
}

/* Webkit 瀏覽器滾動條樣式 */
.chat-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.chat-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  margin: 4px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.4);
}

.chat-container::-webkit-scrollbar-thumb:active {
  background: rgba(0, 0, 0, 0.6);
}

/* 確保滾動條始終可見 */
.chat-container::-webkit-scrollbar-thumb {
  min-height: 20px;
}

.chat-container::-webkit-scrollbar-corner {
  background: transparent;
}

.message-bubble {
  margin-bottom: 12px;
  animation: fadeInUp 0.3s ease;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
}

.message-bubble.user {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

.message-bubble.ai {
  display: flex;
  justify-content: flex-start;
  width: 100%;
}

.user-bubble {
  max-width: 70%;
  min-width: 0;
  background: linear-gradient(135deg, #4361ee, #4cc9f0);
  color: white;
  border-radius: 16px 16px 4px 16px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(67, 97, 238, 0.25);
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  overflow: hidden;
}

.ai-bubble-container {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 80%;
  min-width: 0;
  overflow: hidden;
}

.ai-avatar {
  background: linear-gradient(135deg, #2ed573, #7bed9f);
  color: white;
  flex-shrink: 0;
  margin-top: 5px;
}

.ai-bubble {
  background: white;
  border-radius: 16px 16px 16px 4px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  flex: 1;
  min-width: 0;
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  overflow: hidden;
}

.bubble-content {
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  white-space: pre-wrap;
  max-width: 100%;
  overflow: hidden;
}

.message-text,
.ai-text {
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 6px;
  color: #1c1c1c;
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  white-space: pre-wrap;
  max-width: 100%;
  overflow: hidden;
}

.message-meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-top: 8px;
}

.bubble-time {
  font-size: 12px;
  opacity: 0.7;
}

.message-tags {
  display: flex;
  gap: 8px;
  margin: 10px 0;
  flex-wrap: wrap;
}

.voice-player {
  margin: 10px 0;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 10px;
}

.message-actions {
  display: flex;
  gap: 5px;
  margin-top: 10px;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.ai-bubble:hover .message-actions {
  opacity: 1;
}

/* 打字動畫 */
.typing-indicator {
  margin-bottom: 20px;
  animation: fadeInUp 0.3s ease;
}

.ai-bubble.typing {
  background: white;
  border-radius: 20px 20px 20px 5px;
  padding: 15px 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  flex: 1;
}

.typing-dots {
  display: flex;
  gap: 4px;
  align-items: center;
  justify-content: center;
  height: 20px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0s;
}

/* 空狀態樣式 */
.empty-chat-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-chat-state p {
  font-size: 18px;
  margin: 15px 0;
  font-weight: 500;
}

.sub-text {
  font-size: 14px !important;
  opacity: 0.8;
  margin-bottom: 30px !important;
}

.example-questions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 400px;
  margin: 0 auto;
}

.example-question {
  background: rgba(67, 97, 238, 0.1);
  border: 1px solid rgba(67, 97, 238, 0.2);
  border-radius: 20px;
  padding: 12px 20px;
  color: #4361ee;
  transition: all 0.3s ease;
  font-size: 14px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 44px;
  line-height: 1.4;
}

.example-question:hover {
  background: rgba(67, 97, 238, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.2);
}

/* 設置面板樣式 - 垂直布局 */
.conversation-settings {
  margin-top: auto;
  padding: 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.setting-item {
  margin-bottom: 16px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.conversation-settings .ivu-form-item {
  margin-bottom: 0;
}

.conversation-settings .ivu-form-item-label {
  font-size: 14px;
  font-weight: 500;
  color: #1c1c1c;
  margin-bottom: 6px;
}

.conversation-settings .ivu-select {
  width: 100%;
}

.conversation-settings .ivu-select-selection {
  height: 36px;
  border-radius: 8px;
  font-size: 14px;
  border-color: rgba(0, 0, 0, 0.15);
}

.conversation-settings .ivu-select-selection:hover {
  border-color: #4361ee;
}

.conversation-settings .ivu-select-focused .ivu-select-selection {
  border-color: #4361ee;
  box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.2);
}

/* 動畫 */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 71, 87, 0.7);
  }
  70% {
    box-shadow: 0 0 0 20px rgba(255, 71, 87, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 71, 87, 0);
  }
}

@keyframes wave {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.7;
  }
}

@keyframes typing {
  0%,
  80%,
  100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 用戶情緒標籤樣式 */
.user-emotion-tags {
  display: flex;
  gap: 6px;
  margin: 8px 0 4px 0;
  flex-wrap: wrap;
}

.user-emotion-tags .emotion-tag {
  background: rgba(255, 255, 255, 0.2) !important;
  color: white !important; /* 情緒標籤文字顏色 - 可修改為其他顏色 */
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  font-size: 11px !important;
  padding: 2px 8px !important;
  border-radius: 12px !important;
}

.user-emotion-tags .confidence-tag {
  background: rgba(255, 255, 255, 0.9) !important;
  color: #4361ee !important; /* 置信度文字顏色 - 可修改為其他顏色 */
  border: none !important;
  font-size: 10px !important;
  padding: 2px 6px !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
}

/* 根據情緒動態變色（可選進階功能） */
.user-emotion-tags .emotion-tag.happy {
  color: #52c41a !important; /* 開心 - 綠色文字 */
}
user-emotion-tags .emotion-tag.sad {
  color: #ff4d4f !important; /* 難過 - 紅色文字 */
}

.user-emotion-tags .emotion-tag.angry {
  color: #ff4d4f !important; /* 生氣 - 紅色文字 */
}

.user-emotion-tags .emotion-tag.surprise {
  color: #722ed1 !important; /* 驚訝 - 紫色文字 */
}

.user-emotion-tags .emotion-tag.neutral {
  color: #8c8c8c !important; /* 平靜 - 灰色文字 */
}

.user-emotion-tags .emotion-tag.calm {
  color: #1890ff !important; /* 冷靜 - 藍色文字 */
}
</style>
