<!-- QuickActions.vue - 快捷操作按鈕組件 -->
<template>
  <div class="quick-actions">
    <Button
      type="text"
      size="small"
      @click="$emit('clear-conversation')"
      :disabled="conversationCount === 0"
    >
      <Icon type="ios-trash" />
      清空對話
    </Button>
    <Button
      type="text"
      size="small"
      @click="$emit('export-conversation')"
      :disabled="conversationCount === 0"
    >
      <Icon type="ios-download" />
      導出對話
    </Button>
    <Button 
      type="text" 
      size="small" 
      @click="$emit('toggle-auto-play')"
    >
      <Icon
        :type="autoPlayEnabled ? 'ios-volume-high' : 'ios-volume-mute'"
      />
      {{ autoPlayEnabled ? "關閉" : "開啟" }}自動播放
    </Button>
    <Button 
      type="text" 
      size="small" 
      @click="$emit('toggle-debug')"
    >
      <Icon type="ios-bug" />
      {{ showDebug ? "隱藏" : "顯示" }}調試
    </Button>
  </div>
</template>

<script>
export default {
  name: "QuickActions",
  props: {
    autoPlayEnabled: {
      type: Boolean,
      default: true
    },
    showDebug: {
      type: Boolean,
      default: false
    },
    conversationCount: {
      type: Number,
      default: 0
    }
  },
  emits: [
    'clear-conversation',
    'export-conversation',
    'toggle-auto-play',
    'toggle-debug'
  ]
}
</script>

<style scoped>
.quick-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.quick-actions .ivu-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.quick-actions .ivu-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.quick-actions .ivu-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quick-actions .ivu-btn:disabled:hover {
  transform: none;
  box-shadow: none;
}
</style>