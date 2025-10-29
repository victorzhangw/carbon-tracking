<!-- EmptyState.vue - 空狀態組件 -->
<template>
  <div class="empty-chat-state">
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
        @click="$emit('ask-sample-question', question)"
        class="example-question"
      >
        {{ question }}
      </Button>
    </div>
  </div>
</template>

<script>
export default {
  name: "EmptyState",
  props: {
    sampleQuestions: {
      type: Array,
      default: () => [
        "你好，請介紹一下你自己",
        "今天天氣如何？",
        "推薦一些學習資源",
        "幫我制定學習計劃",
      ]
    }
  },
  emits: ['ask-sample-question']
}
</script>

<style scoped>
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

.example-question:active {
  transform: translateY(0);
}
</style>