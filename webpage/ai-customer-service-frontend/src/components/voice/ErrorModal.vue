<!-- ErrorModal.vue - 錯誤處理模態框組件 -->
<template>
  <Modal 
    :value="value" 
    title="處理錯誤" 
    @on-ok="handleClose"
    @on-cancel="handleClose"
    @input="$emit('input', $event)"
  >
    <div class="error-content">
      <Icon type="ios-warning" size="48" color="#ff4757" />
      <p class="error-message">{{ errorMessage }}</p>
    </div>
    
    <div slot="footer" class="error-actions">
      <Button @click="handleRetry" type="primary" size="small">
        <Icon type="ios-refresh" />
        重試
      </Button>
      <Button @click="handleReset" type="text" size="small">
        <Icon type="ios-trash" />
        重新開始
      </Button>
      <Button @click="handleClose" type="default" size="small">
        關閉
      </Button>
    </div>
  </Modal>
</template>

<script>
export default {
  name: "ErrorModal",
  props: {
    value: {
      type: Boolean,
      default: false
    },
    errorMessage: {
      type: String,
      default: ""
    }
  },
  emits: [
    'input',
    'retry',
    'reset'
  ],
  methods: {
    handleClose() {
      this.$emit('input', false);
    },
    handleRetry() {
      this.$emit('retry');
      this.handleClose();
    },
    handleReset() {
      this.$emit('reset');
      this.handleClose();
    }
  }
}
</script>

<style scoped>
.error-content {
  text-align: center;
  padding: 20px 0;
}

.error-message {
  font-size: 16px;
  color: #333;
  margin-top: 15px;
  line-height: 1.5;
}

.error-actions {
  text-align: center;
  padding: 10px 0;
}

.error-actions .ivu-btn {
  margin: 0 5px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.error-actions .ivu-btn-primary {
  background: #4361ee;
  border-color: #4361ee;
}

.error-actions .ivu-btn-primary:hover {
  background: #3651d4;
  border-color: #3651d4;
}
</style>