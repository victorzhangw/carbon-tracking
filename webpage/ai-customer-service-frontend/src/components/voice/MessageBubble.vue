<!-- MessageBubble.vue - 消息氣泡組件 -->
<template>
  <div class="message-bubble" :class="message.type">
    <!-- 用戶消息氣泡 -->
    <div v-if="message.type === 'user'" class="user-bubble">
      <div class="bubble-content">
        <div class="message-text">{{ message.text }}</div>
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
                @click="$emit('play-audio', message.id)"
                :loading="playingAudioId === message.id"
              >
                <Icon type="ios-play" />
                播放語音
              </Button>
              <audio
                :src="message.audioUrl"
                :ref="`audio_${message.id}`"
                @loadstart="onAudioLoadStart"
                @canplay="() => onAudioReady(message.id)"
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
              @click="$emit('copy-message', message.text)"
            >
              <Icon type="ios-copy" />
            </Button>
            <Button
              size="small"
              type="text"
              @click="$emit('regenerate-response', message)"
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
</template>

<script>
export default {
  name: "MessageBubble",
  props: {
    message: {
      type: Object,
      required: true
    },
    playingAudioId: {
      type: [String, Number],
      default: null
    },
    regeneratingId: {
      type: [String, Number],
      default: null
    }
  },
  emits: [
    'play-audio',
    'copy-message',
    'regenerate-response'
  ],
  methods: {
    getSentimentColor(sentiment) {
      const colors = {
        正面: "success",
        中性: "default",
        負面: "error",
        積極: "success",
        消極: "warning",
      };
      return colors[sentiment] || "default";
    },
    onAudioLoadStart() {
      console.log("音頻開始加載");
    },
    onAudioReady(messageId) {
      console.log("音頻準備就緒:", messageId);
    },
    onAudioEnded() {
      this.$emit('audio-ended');
    }
  }
}
</script>

<style scoped>
.message-bubble {
  margin-bottom: 20px;
  animation: fadeInUp 0.3s ease;
}

.message-bubble.user {
  display: flex;
  justify-content: flex-end;
}

.message-bubble.ai {
  display: flex;
  justify-content: flex-start;
}

.user-bubble {
  max-width: 70%;
  background: linear-gradient(135deg, #4361ee, #4cc9f0);
  color: white;
  border-radius: 20px 20px 5px 20px;
  padding: 15px 20px;
  box-shadow: 0 4px 15px rgba(67, 97, 238, 0.3);
}

.ai-bubble-container {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 80%;
}

.ai-avatar {
  background: linear-gradient(135deg, #2ed573, #7bed9f);
  color: white;
  flex-shrink: 0;
  margin-top: 5px;
}

.ai-bubble {
  background: white;
  border-radius: 20px 20px 20px 5px;
  padding: 15px 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  flex: 1;
}

.bubble-content {
  word-wrap: break-word;
}

.message-text,
.ai-text {
  font-size: 15px;
  line-height: 1.5;
  margin-bottom: 8px;
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

.sentiment-tag-custom,
.confidence-tag {
  font-size: 11px;
}

.voice-player {
  margin: 10px 0;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 10px;
}

.audio-controls {
  display: flex;
  align-items: center;
  gap: 10px;
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
</style>