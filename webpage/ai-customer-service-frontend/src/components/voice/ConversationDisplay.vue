<!-- ConversationDisplay.vue - 對話顯示組件 -->
<template>
  <div class="chat-container" ref="chatContainer">
    <!-- 對話消息列表 -->
    <MessageBubble
      v-for="message in conversationHistory"
      :key="message.id"
      :message="message"
      :playing-audio-id="playingAudioId"
      :regenerating-id="regeneratingId"
      @play-audio="$emit('play-audio', $event)"
      @copy-message="$emit('copy-message', $event)"
      @regenerate-response="$emit('regenerate-response', $event)"
    />

    <!-- 打字動畫 -->
    <TypingIndicator v-if="isThinking" />

    <!-- 空狀態 -->
    <EmptyState
      v-if="conversationHistory.length === 0"
      :sample-questions="sampleQuestions"
      @ask-sample-question="$emit('ask-sample-question', $event)"
    />
  </div>
</template>

<script>
import MessageBubble from './MessageBubble.vue'
import TypingIndicator from './TypingIndicator.vue'
import EmptyState from './EmptyState.vue'

export default {
  name: "ConversationDisplay",
  components: {
    MessageBubble,
    TypingIndicator,
    EmptyState
  },
  props: {
    conversationHistory: {
      type: Array,
      default: () => []
    },
    isThinking: {
      type: Boolean,
      default: false
    },
    playingAudioId: {
      type: [String, Number],
      default: null
    },
    regeneratingId: {
      type: [String, Number],
      default: null
    },
    sampleQuestions: {
      type: Array,
      default: () => []
    }
  },
  emits: [
    'play-audio',
    'copy-message',
    'regenerate-response',
    'ask-sample-question'
  ],
  watch: {
    conversationHistory: {
      handler() {
        this.scrollToBottom()
      },
      deep: true
    }
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.chatContainer) {
          this.$refs.chatContainer.scrollTop =
            this.$refs.chatContainer.scrollHeight;
        }
      });
    }
  }
}
</script>

<style scoped>
.chat-container {
  max-height: 600px;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 15px;
  margin-bottom: 20px;
}

.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.5);
}
</style>