<!-- VoiceControlSection.vue - 語音控制區域組件 -->
<template>
  <div class="conversation-control-section">
    <div class="talk-button-container">
      <!-- 音頻可視化 -->
      <AudioVisualizer
        :visual-bars="visualBars"
        :is-active="isListening"
      />

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
          @mousedown.native="$emit('start-talk')"
          @mouseup.native="$emit('end-talk')"
          @mouseleave.native="$emit('end-talk')"
          @touchstart.native="$emit('start-talk')"
          @touchend.native="$emit('end-talk')"
          :disabled="isThinking || isSpeaking"
          :style="buttonStyle"
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

        <!-- 錄音時長顯示 -->
        <div v-if="isListening" class="recording-duration">
          {{ formatTime(recordingTime) }}
        </div>
      </div>
    </div>

    <!-- 智能狀態提示 -->
    <ConversationStatus
      :is-listening="isListening"
      :is-thinking="isThinking"
      :is-speaking="isSpeaking"
    />

    <!-- 快捷操作按鈕 -->
    <QuickActions
      :auto-play-enabled="autoPlayEnabled"
      :show-debug="showDebug"
      @clear-conversation="$emit('clear-conversation')"
      @export-conversation="$emit('export-conversation')"
      @toggle-auto-play="$emit('toggle-auto-play')"
      @toggle-debug="$emit('toggle-debug')"
    />
  </div>
</template>

<script>
import AudioVisualizer from './AudioVisualizer.vue'
import ConversationStatus from './ConversationStatus.vue'
import QuickActions from './QuickActions.vue'

export default {
  name: "VoiceControlSection",
  components: {
    AudioVisualizer,
    ConversationStatus,
    QuickActions
  },
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
    recordingTime: {
      type: Number,
      default: 0
    },
    visualBars: {
      type: Array,
      default: () => Array(40).fill(5)
    },
    buttonText: {
      type: String,
      default: "按住開始對話"
    },
    buttonStyle: {
      type: Object,
      default: () => ({})
    },
    autoPlayEnabled: {
      type: Boolean,
      default: true
    },
    showDebug: {
      type: Boolean,
      default: false
    }
  },
  emits: [
    'start-talk',
    'end-talk',
    'clear-conversation',
    'export-conversation',
    'toggle-auto-play',
    'toggle-debug'
  ],
  methods: {
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins.toString().padStart(2, "0")}:${secs
        .toString()
        .padStart(2, "0")}`;
    }
  }
}
</script>

<style scoped>
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
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-top: 10px;
}

.recording-duration {
  font-size: 18px;
  font-weight: 600;
  color: #ff4757;
  background: rgba(255, 71, 87, 0.1);
  padding: 8px 16px;
  border-radius: 20px;
  margin-top: 10px;
}

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
</style>