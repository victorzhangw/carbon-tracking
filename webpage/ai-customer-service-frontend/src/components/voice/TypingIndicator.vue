<!-- TypingIndicator.vue - 打字動畫指示器組件 -->
<template>
  <div class="typing-indicator">
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
</template>

<script>
export default {
  name: "TypingIndicator"
}
</script>

<style scoped>
.typing-indicator {
  margin-bottom: 20px;
  animation: fadeInUp 0.3s ease;
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

@keyframes typing {
  0%, 80%, 100% {
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
</style>