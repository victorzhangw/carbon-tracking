<!-- ConversationStatus.vue - 對話狀態提示組件 -->
<template>
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
        <span>{{ getWaitingText() }}</span>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "ConversationStatus",
  props: {
    isListening: {
      type: Boolean,
      default: false
    },
    isThinking: {
      type: Boolean,
      default: false
    },
    isSpeaking: {
      type: Boolean,
      default: false
    },
    conversationHistory: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    getWaitingText() {
      const waitingTexts = [
        "按住按鈕開始對話",
        "或點擊示例問題快速開始",
        "我準備好回答您的問題了",
        "有什麼可以幫助您的嗎？",
      ];
      return this.conversationHistory.length === 0
        ? waitingTexts[Math.floor(Date.now() / 3000) % waitingTexts.length]
        : "按住按鈕繼續對話";
    }
  }
}
</script>

<style scoped>
.conversation-status {
  margin: 30px 0;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 25px;
  border-radius: 25px;
  font-size: 16px;
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

@keyframes wave {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.7;
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
</style>