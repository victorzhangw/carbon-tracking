<!-- VoiceInteractionFlow.vue - 完整的語音互動流程 -->
<template>
  <div class="voice-interaction-flow">
    <Card class="main-card" :bordered="false">
      <template #title>
        <div class="card-title">
          <Icon type="ios-mic" size="24" />
          <span>語音互動系統</span>
        </div>
      </template>

      <!-- 一鍵式對話控制區域 -->
      <div class="conversation-control-section">
        <div class="talk-button-container">
          <!-- 音頻可視化 -->
          <div
            class="audio-visualizer"
            ref="visualizer"
            :class="{ active: isListening }"
          >
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
              :style="{
                background: isListening
                  ? 'linear-gradient(135deg, #ff4757, #ff6b7a) !important'
                  : isThinking
                  ? 'linear-gradient(135deg, #ffa502, #ffb142) !important'
                  : isSpeaking
                  ? 'linear-gradient(135deg, #2ed573, #7bed9f) !important'
                  : 'linear-gradient(135deg, #4361ee, #4cc9f0) !important',
              }"
            >
              <Icon
                v-if="!isListening && !isThinking && !isSpeaking"
                type="ios-mic"
                size="40"
              />
              <Icon v-if="isListening" type="ios-radio-button-on" size="40" />
              <Spin v-if="isThinking || isSpeaking" size="large" />
            </Button>

            <div class="button-text">
              {{ buttonText }}
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
              <span>正在思考回應...</span>
            </div>

            <div
              v-else-if="isSpeaking"
              class="status-item speaking"
              key="speaking"
            >
              <Icon type="ios-volume-high" />
              <span>AI客服正在回應...</span>
            </div>

            <div v-else class="status-item waiting" key="waiting">
              <Icon type="ios-chatbubbles" />
              <span>按住按鈕開始對話</span>
            </div>
          </transition>
        </div>
      </div>

      <Divider>對話內容</Divider>

      <!-- 對話氣泡顯示區域 -->
      <div class="chat-container" ref="chatContainer">
        <div
          v-for="message in conversationHistory"
          :key="message.id"
          class="message-bubble"
          :class="message.type"
        >
          <!-- 用戶消息氣泡 (右側藍色) -->
          <div v-if="message.type === 'user'" class="user-bubble">
            <div class="bubble-content">{{ message.text }}</div>
            <div class="bubble-time">{{ message.time }}</div>
          </div>

          <!-- AI消息氣泡 (左側灰色) -->
          <div v-else class="ai-bubble-container">
            <Avatar class="ai-avatar" icon="ios-help-buoy" />
            <div class="ai-bubble">
              <div class="bubble-content">
                <div class="ai-text">{{ message.text }}</div>
                <div v-if="message.sentiment" class="sentiment-tag">
                  <!-- Fixed: Removed size prop and added custom CSS class -->
                  <Tag
                    :color="getSentimentColor(message.sentiment)"
                    class="sentiment-tag-custom"
                    >{{ message.sentiment }}</Tag
                  >
                </div>
                <!-- 語音播放器 -->
                <div v-if="message.audioUrl" class="voice-player">
                  <audio
                    :src="message.audioUrl"
                    controls
                    :ref="`audio_${message.id}`"
                    @loadstart="onAudioLoadStart"
                    @canplay="() => onAudioReady(message.id)"
                    class="audio-control"
                  >
                    您的瀏覽器不支援音頻播放
                  </audio>
                </div>
              </div>
              <div class="bubble-time">{{ message.time }}</div>
            </div>
          </div>
        </div>

        <!-- 空狀態 -->
        <div v-if="conversationHistory.length === 0" class="empty-chat-state">
          <Icon type="ios-chatbubbles" size="64" color="#c7ecee" />
          <p>開始語音對話</p>
          <p class="sub-text">按住下方按鈕開始說話，松開自動發送</p>
        </div>
      </div>

      <!-- 狀態調試顯示 -->
      <div
        class="debug-status"
        style="
          margin: 20px 0;
          padding: 15px;
          background: #f0f8ff;
          border-radius: 8px;
          border-left: 4px solid #1890ff;
        "
      >
        <h4>🔍 當前狀態</h4>
        <p><strong>isListening:</strong> {{ isListening }} (應該變紅色)</p>
        <p><strong>isThinking:</strong> {{ isThinking }} (應該變橙色)</p>
        <p><strong>isSpeaking:</strong> {{ isSpeaking }} (應該變綠色)</p>
        <p><strong>按鈕文字:</strong> {{ buttonText }}</p>
        <Button @click="forceListening" type="primary" size="small"
          >強制設為聆聽狀態</Button
        >
        <Button
          @click="resetAllStates"
          type="default"
          size="small"
          style="margin-left: 10px"
          >重置狀態</Button
        >
      </div>

      <!-- 使用說明 -->
      <div
        class="usage-guide"
        style="
          margin: 20px 0;
          padding: 15px;
          background: #e8f5e8;
          border-radius: 8px;
          border-left: 4px solid #52c41a;
        "
      >
        <h4>📖 使用說明</h4>
        <p>
          <strong>按住說話</strong
          >：按住下方大按鈕開始錄音，按鈕會變紅色並顯示脈衝動畫
        </p>
        <p>
          <strong>松開發送</strong
          >：松開按鈕自動停止錄音並處理，按鈕會變橙色表示正在思考
        </p>
        <p>
          <strong>自動播放</strong
          >：AI回應生成後會自動播放語音，按鈕變綠色表示正在回應
        </p>
      </div>

      <!-- 客服選擇 -->
      <div class="staff-selection">
        <Form>
          <FormItem label="選擇客服語音模型:">
            <Select
              v-model="selectedStaff"
              placeholder="選擇客服"
              style="width: 200px"
            >
              <Option value="admin">管理員</Option>
              <Option value="staff001">客服001</Option>
              <Option value="staff002">客服002</Option>
            </Select>
          </FormItem>
        </Form>
      </div>
    </Card>

    <!-- 錯誤提示 -->
    <Modal v-model="errorModal" title="處理錯誤" @on-ok="errorModal = false">
      <p>{{ errorMessage }}</p>
    </Modal>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "VoiceInteractionFlow",
  data() {
    return {
      // 一鍵式對話狀態
      isListening: false,
      isThinking: false,
      isSpeaking: false,

      // 錄音相關
      audioBlob: null,
      recorder: null,
      recordingTime: 0,
      recordingTimer: null,

      // 可視化
      visualBars: Array(40).fill(5),
      visualInterval: null,

      // 對話歷史
      conversationHistory: [],
      messageIdCounter: 1,

      // 客服選擇
      selectedStaff: "admin",

      // 錯誤處理
      errorModal: false,
      errorMessage: "",
    };
  },

  computed: {
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
      return "按住說話";
    },
  },

  methods: {
    // 一鍵式對話 - 按住開始說話
    startTalk() {
      console.log("🎤 startTalk 被調用");
      console.log("調用前狀態:", {
        isListening: this.isListening,
        isThinking: this.isThinking,
        isSpeaking: this.isSpeaking,
      });

      if (this.isThinking || this.isSpeaking) {
        console.log("❌ 按鈕被禁用，無法開始錄音");
        return;
      }

      // 強制更新狀態
      console.log("🔄 強制更新狀態為聆聽中...");
      this.$set(this, "isListening", true);
      this.$set(this, "isThinking", false);
      this.$set(this, "isSpeaking", false);

      // 強制Vue重新渲染
      this.$forceUpdate();

      console.log("調用後狀態:", {
        isListening: this.isListening,
        isThinking: this.isThinking,
        isSpeaking: this.isSpeaking,
      });

      this.startRecording();

      // 觸覺反馈 (移動端)
      if (navigator.vibrate) {
        navigator.vibrate(50);
      }

      // 顯示用戶提示
      this.$Message.info("🎤 開始錄音，請說話...");
    },

    // 一鍵式對話 - 松開自動處理
    async endTalk() {
      console.log("🛑 endTalk 被調用");
      console.log("松開前狀態:", {
        isListening: this.isListening,
        isThinking: this.isThinking,
        isSpeaking: this.isSpeaking,
      });

      if (!this.isListening) {
        console.log("❌ 不在聆聽狀態，無法結束");
        return;
      }

      // 強制更新狀態
      console.log("🔄 強制更新狀態為思考中...");
      this.$set(this, "isListening", false);
      this.$set(this, "isThinking", true);
      this.$set(this, "isSpeaking", false);

      // 強制Vue重新渲染
      this.$forceUpdate();

      try {
        // 停止錄音
        await this.stopRecording();

        if (!this.audioBlob) {
          throw new Error("錄音失敗，請重試");
        }

        // 語音識別
        const transcript = await this.performSpeechRecognition();
        this.addMessage("user", transcript);

        // AI分析和語音生成
        console.log("🔄 強制更新狀態為回應中...");
        this.$set(this, "isListening", false);
        this.$set(this, "isThinking", false);
        this.$set(this, "isSpeaking", true);
        this.$forceUpdate();

        const aiResponse = await this.performAIAnalysis(transcript);
        this.addMessage(
          "ai",
          aiResponse.text,
          aiResponse.audioUrl,
          aiResponse.sentiment
        );
      } catch (error) {
        this.showError(error.message);
      } finally {
        console.log("🔄 強制重置所有狀態...");
        this.$set(this, "isListening", false);
        this.$set(this, "isThinking", false);
        this.$set(this, "isSpeaking", false);
        this.$forceUpdate();
        this.audioBlob = null; // 清理音頻數據
      }
    },

    // 開始錄音
    async startRecording() {
      console.log("🎙️ startRecording 開始執行");
      try {
        console.log("📱 請求麥克風權限...");
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        console.log("✅ 麥克風權限獲取成功，stream:", stream);

        this.recorder = new MediaRecorder(stream);
        console.log("🎬 MediaRecorder 創建成功:", this.recorder);

        const audioChunks = [];
        this.recorder.ondataavailable = (event) => {
          console.log("📊 收到音頻數據，大小:", event.data.size);
          if (event.data.size > 0) {
            audioChunks.push(event.data);
          }
        };

        this.recorder.onstop = () => {
          console.log(
            "🔴 錄音停止，總共收集到",
            audioChunks.length,
            "個音頻塊"
          );
          this.audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          console.log(
            "💾 音頻Blob創建完成，大小:",
            this.audioBlob.size,
            "bytes"
          );
          stream.getTracks().forEach((track) => track.stop());
          console.log("🔌 麥克風流已關閉");
        };

        this.recorder.start();
        console.log("🔴 開始錄音，狀態:", this.recorder.state);
        this.startTimer();
        this.startVisualization();
      } catch (error) {
        console.error("❌ 錄音失敗:", error);
        this.$Message.error("無法訪問麥克風: " + error.message);
        this.$set(this, "isListening", false);
      }
    },

    // 停止錄音
    async stopRecording() {
      console.log("🛑 stopRecording 開始執行");
      console.log("錄音器狀態:", this.recorder ? this.recorder.state : "null");

      if (this.recorder) {
        console.log("🔴 停止錄音器...");
        this.recorder.stop();
        console.log("⏰ 停止計時器...");
        this.stopTimer();
        console.log("📊 停止可視化...");
        this.stopVisualization();

        // 等待錄音完全停止
        await new Promise((resolve) => {
          if (this.recorder.state === "inactive") {
            resolve();
          } else {
            this.recorder.addEventListener("stop", resolve, { once: true });
          }
        });

        console.log("✅ 錄音完全停止");
      } else {
        console.log("❌ 錄音器不存在");
      }
    },

    // 執行語音識別
    async performSpeechRecognition() {
      const formData = new FormData();
      formData.append("file", this.audioBlob, "recording.wav");

      const response = await axios.post("/process_audio", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 60000, // 60秒超时
      });

      if (response.data.transcript) {
        return response.data.transcript;
      } else {
        throw new Error("語音識別失敗");
      }
    },

    // 執行AI分析
    async performAIAnalysis(transcript) {
      const response = await axios.post(
        "/voice_clone/generate_response_voice",
        {
          user_input: transcript,
          staff_code: this.selectedStaff,
        },
        {
          timeout: 120000, // 120秒超时 (语音生成需要更长时间)
        }
      );

      if (response.data.status === "success") {
        return {
          text: response.data.ai_analysis.response_text,
          sentiment: response.data.ai_analysis.sentiment,
          audioUrl: response.data.voice_output.audio_url,
        };
      } else {
        throw new Error(response.data.message || "AI分析失敗");
      }
    },

    // 添加消息到對話歷史
    addMessage(type, text, audioUrl = null, sentiment = null) {
      const message = {
        id: this.messageIdCounter++,
        type, // 'user' | 'ai'
        text,
        audioUrl,
        sentiment,
        time: new Date().toLocaleTimeString(),
        timestamp: new Date(),
      };

      this.conversationHistory.push(message);
      this.scrollToBottom();

      // 自動播放AI回應
      if (type === "ai" && audioUrl) {
        this.$nextTick(() => {
          this.playLatestAudio(message.id);
        });
      }
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

    // 播放最新的AI音頻
    playLatestAudio(messageId) {
      const audioRef = this.$refs[`audio_${messageId}`];
      if (audioRef && audioRef[0]) {
        audioRef[0].play().catch((error) => {
          console.warn("自動播放失敗，可能需要用戶互動:", error);
          this.$Message.warning("請點擊播放按鈕聆聽AI語音回應");
        });
      }
    },

    // 重置對話
    resetConversation() {
      this.conversationHistory = [];
      this.messageIdCounter = 1;
    },

    // 計時器相關
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

    // 可視化相關
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

    // 情感顏色
    getSentimentColor(sentiment) {
      const colors = {
        正面: "success",
        中性: "default",
        負面: "error",
      };
      return colors[sentiment] || "default";
    },

    // 音頻事件
    onAudioLoadStart() {
      console.log("音頻開始加載");
    },

    onAudioReady(messageId) {
      console.log("音頻準備就緒，嘗試自動播放...");
      // 延遲一下確保音頻完全載入
      setTimeout(() => {
        this.playLatestAudio(messageId);
      }, 300);
    },

    // 調試方法
    forceListening() {
      console.log("🔴 強制設為聆聽狀態");
      this.isListening = true;
      this.isThinking = false;
      this.isSpeaking = false;
    },

    resetAllStates() {
      console.log("🔄 重置所有狀態");
      this.isListening = false;
      this.isThinking = false;
      this.isSpeaking = false;
    },

    // 錯誤處理
    showError(message) {
      this.errorMessage = message;
      this.errorModal = true;
      this.$Message.error(message);
    },
  },

  beforeDestroy() {
    // 清理資源
    this.stopTimer();
    this.stopVisualization();
    if (this.recorder && this.isListening) {
      this.recorder.stop();
    }
  },
};
</script>

<style scoped>
/* 一鍵式對話控制區域 */
.conversation-control-section {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 20px;
  margin-bottom: 30px;
}

.talk-button-container {
  position: relative;
  display: inline-block;
}

/* 音頻可視化 */
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

/* 一鍵式對話按鈕 */
.talk-button-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.talk-button {
  width: 120px !important;
  height: 120px !important;
  border-radius: 50% !important;
  border: none !important;
  background: linear-gradient(135deg, #4361ee, #4cc9f0) !important;
  color: white !important;
  font-size: 18px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 0 8px 25px rgba(67, 97, 238, 0.3) !important;
  user-select: none;
  -webkit-user-select: none;
}

.talk-button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 35px rgba(67, 97, 238, 0.4) !important;
}

.talk-button.is-listening {
  background: linear-gradient(135deg, #ff4757, #ff6b7a) !important;
  transform: scale(1.1) !important;
  box-shadow: 0 0 30px rgba(255, 71, 87, 0.6) !important;
  animation: pulse 1.5s infinite;
}

.talk-button.is-thinking {
  background: linear-gradient(135deg, #ffa502, #ffb142) !important;
  transform: scale(1.05) !important;
  box-shadow: 0 0 25px rgba(255, 165, 2, 0.5) !important;
}

.talk-button.is-speaking {
  background: linear-gradient(135deg, #2ed573, #7bed9f) !important;
  transform: scale(1.05) !important;
  box-shadow: 0 0 25px rgba(46, 213, 115, 0.5) !important;
}

.talk-button:disabled {
  cursor: not-allowed !important;
  opacity: 0.7 !important;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1.1);
  }
  50% {
    transform: scale(1.15);
  }
}

.button-text {
  font-size: 16px;
  font-weight: 500;
  color: #2b2d42;
  margin-top: 5px;
}

/* 智能狀態提示 */
.conversation-status {
  margin-top: 20px;
  min-height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.status-item.listening {
  background: rgba(255, 71, 87, 0.1);
  color: #ff4757;
  border: 1px solid rgba(255, 71, 87, 0.2);
}

.status-item.thinking {
  background: rgba(255, 165, 2, 0.1);
  color: #ffa502;
  border: 1px solid rgba(255, 165, 2, 0.2);
}

.status-item.speaking {
  background: rgba(46, 213, 115, 0.1);
  color: #2ed573;
  border: 1px solid rgba(46, 213, 115, 0.2);
}

.status-item.waiting {
  background: rgba(67, 97, 238, 0.1);
  color: #4361ee;
  border: 1px solid rgba(67, 97, 238, 0.2);
}

.voice-wave {
  width: 20px;
  height: 3px;
  background: currentColor;
  border-radius: 2px;
  animation: wave 1s infinite ease-in-out;
}

@keyframes wave {
  0%,
  100% {
    transform: scaleY(1);
  }
  50% {
    transform: scaleY(0.3);
  }
}

/* 對話氣泡容器 */
.chat-container {
  max-height: 500px;
  overflow-y: auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 15px;
  border: 1px solid #e9ecef;
}

.message-bubble {
  margin-bottom: 20px;
  animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 用戶消息氣泡 (右側藍色) */
.message-bubble.user {
  display: flex;
  justify-content: flex-end;
}

.user-bubble {
  max-width: 70%;
  background: linear-gradient(135deg, #007aff, #0056cc);
  color: white;
  border-radius: 20px 20px 5px 20px;
  padding: 12px 18px;
  box-shadow: 0 2px 10px rgba(0, 122, 255, 0.2);
}

.user-bubble .bubble-content {
  font-size: 15px;
  line-height: 1.4;
  word-wrap: break-word;
}

.user-bubble .bubble-time {
  font-size: 11px;
  opacity: 0.8;
  margin-top: 5px;
  text-align: right;
}

/* AI消息氣泡 (左側灰色) */
.message-bubble.ai {
  display: flex;
  justify-content: flex-start;
}

.ai-bubble-container {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 80%;
}

.ai-avatar {
  flex-shrink: 0;
  margin-top: 5px;
}

.ai-bubble {
  background: #f8f9fa;
  color: #2b2d42;
  border-radius: 20px 20px 20px 5px;
  padding: 12px 18px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
}

.ai-bubble .bubble-content {
  font-size: 15px;
  line-height: 1.4;
}

.ai-bubble .ai-text {
  word-wrap: break-word;
  margin-bottom: 8px;
}

.ai-bubble .sentiment-tag {
  margin-bottom: 10px;
}

/* Custom CSS for sentiment tag to replace size prop */
.sentiment-tag-custom {
  font-size: 12px !important;
  padding: 2px 6px !important;
  line-height: 1.2 !important;
}

.ai-bubble .bubble-time {
  font-size: 11px;
  color: #8d99ae;
  margin-top: 8px;
}

/* 語音播放器 */
.voice-player {
  margin-top: 10px;
}

.audio-control {
  width: 100%;
  max-width: 300px;
  height: 35px;
  border-radius: 8px;
  outline: none;
}

/* 空狀態 */
.empty-chat-state {
  text-align: center;
  padding: 60px 20px;
  color: #8d99ae;
}

.empty-chat-state p {
  font-size: 18px;
  font-weight: 500;
  margin: 15px 0 5px 0;
}

.empty-chat-state .sub-text {
  font-size: 14px;
  opacity: 0.8;
}

/* 過渡動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 響應式設計 */
@media (max-width: 768px) {
  .conversation-control-section {
    padding: 30px 15px;
  }

  .talk-button {
    width: 100px !important;
    height: 100px !important;
    font-size: 16px !important;
  }

  .audio-visualizer {
    height: 50px;
  }

  .chat-container {
    max-height: 400px;
    padding: 15px;
  }

  .ai-bubble-container {
    max-width: 90%;
  }

  .user-bubble {
    max-width: 85%;
  }
}

/* 客服選擇區域 */
.staff-selection {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}
</style>
