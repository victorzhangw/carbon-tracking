<!-- DebugPanel.vue - 調試面板組件 -->
<template>
  <div class="debug-status">
    <h4>🔍 系統狀態診斷</h4>
    <Row :gutter="16">
      <Col span="6">
        <p>
          <strong>聆聽:</strong>
          <span :style="{ color: isListening ? '#ff4757' : '#666' }">
            {{ isListening }}
          </span>
        </p>
      </Col>
      <Col span="6">
        <p>
          <strong>思考:</strong>
          <span :style="{ color: isThinking ? '#ffa502' : '#666' }">
            {{ isThinking }}
          </span>
        </p>
      </Col>
      <Col span="6">
        <p>
          <strong>回應:</strong>
          <span :style="{ color: isSpeaking ? '#2ed573' : '#666' }">
            {{ isSpeaking }}
          </span>
        </p>
      </Col>
      <Col span="6">
        <p><strong>輪次:</strong> {{ conversationRounds }}</p>
      </Col>
    </Row>
    <Row :gutter="16" style="margin-top: 10px">
      <Col span="8">
        <p>
          <strong>錄音器:</strong>
          {{ recorder ? recorder.state : "未初始化" }}
        </p>
      </Col>
      <Col span="8">
        <p>
          <strong>音頻文件:</strong>
          {{ audioBlob ? `${Math.round(audioBlob.size / 1024)}KB` : "無" }}
        </p>
      </Col>
      <Col span="8">
        <p><strong>按鈕文字:</strong> {{ buttonText }}</p>
      </Col>
    </Row>
    <div style="margin-top: 10px">
      <Button 
        @click="$emit('force-listening')" 
        type="primary" 
        size="small"
      >
        測試聆聽
      </Button>
      <Button
        @click="$emit('reset-all-states')"
        type="default"
        size="small"
        style="margin-left: 8px"
      >
        重置狀態
      </Button>
      <Button
        @click="$emit('toggle-debug')"
        type="text"
        size="small"
        style="margin-left: 8px"
      >
        隱藏調試
      </Button>
      <Button
        @click="$emit('test-audio-blob')"
        type="text"
        size="small"
        style="margin-left: 8px"
      >
        檢查音頻
      </Button>
    </div>
  </div>
</template>

<script>
export default {
  name: "DebugPanel",
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
    conversationRounds: {
      type: Number,
      default: 0
    },
    recorder: {
      type: Object,
      default: null
    },
    audioBlob: {
      type: Object,
      default: null
    },
    buttonText: {
      type: String,
      default: ""
    }
  },
  emits: [
    'force-listening',
    'reset-all-states',
    'toggle-debug',
    'test-audio-blob'
  ]
}
</script>

<style scoped>
.debug-status {
  margin-top: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border: 2px dashed #ddd;
  border-radius: 10px;
  font-family: 'Courier New', monospace;
}

.debug-status h4 {
  margin-bottom: 15px;
  color: #333;
  font-size: 16px;
}

.debug-status p {
  margin: 5px 0;
  font-size: 13px;
  line-height: 1.4;
}

.debug-status strong {
  color: #333;
  font-weight: 600;
}

.debug-status .ivu-btn {
  margin-right: 8px;
  margin-bottom: 8px;
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 6px;
}

.debug-status .ivu-btn-primary {
  background: #4361ee;
  border-color: #4361ee;
}

.debug-status .ivu-btn-default {
  background: #f8f9fa;
  border-color: #ddd;
  color: #666;
}

.debug-status .ivu-btn-text {
  color: #666;
  padding: 4px 8px;
}

.debug-status .ivu-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>