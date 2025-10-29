<!-- ConversationSettings.vue - 對話設置組件 -->
<template>
  <div class="conversation-settings">
    <Row :gutter="16">
      <Col span="8">
        <Form>
          <FormItem label="選擇AI助手:">
            <Select
              :value="selectedStaff"
              placeholder="選擇助手"
              @on-change="handleStaffChange"
            >
              <Option value="admin">通用助手</Option>
              <Option value="staff001">專業客服</Option>
              <Option value="staff002">技術支援</Option>
              <Option value="staff003">創意助手</Option>
            </Select>
          </FormItem>
        </Form>
      </Col>
      <Col span="8">
        <Form>
          <FormItem label="回應語調:">
            <Select 
              :value="responseStyle" 
              placeholder="選擇語調"
              @on-change="handleResponseStyleChange"
            >
              <Option value="friendly">友好親切</Option>
              <Option value="professional">專業正式</Option>
              <Option value="casual">輕鬆隨意</Option>
              <Option value="detailed">詳細解說</Option>
            </Select>
          </FormItem>
        </Form>
      </Col>
      <Col span="8">
        <Form>
          <FormItem label="對話模式:">
            <Select 
              :value="conversationMode" 
              placeholder="選擇模式"
              @on-change="handleConversationModeChange"
            >
              <Option value="continuous">連續對話</Option>
              <Option value="qa">問答模式</Option>
              <Option value="creative">創意模式</Option>
            </Select>
          </FormItem>
        </Form>
      </Col>
    </Row>
  </div>
</template>

<script>
export default {
  name: "ConversationSettings",
  props: {
    selectedStaff: {
      type: String,
      default: "admin"
    },
    responseStyle: {
      type: String,
      default: "friendly"
    },
    conversationMode: {
      type: String,
      default: "continuous"
    }
  },
  emits: [
    'update:selectedStaff',
    'update:responseStyle', 
    'update:conversationMode',
    'staff-change'
  ],
  methods: {
    handleStaffChange(value) {
      this.$emit('update:selectedStaff', value);
      this.$emit('staff-change', value);
    },
    handleResponseStyleChange(value) {
      this.$emit('update:responseStyle', value);
    },
    handleConversationModeChange(value) {
      this.$emit('update:conversationMode', value);
    }
  }
}
</script>

<style scoped>
.conversation-settings {
  margin: 30px 0;
  padding: 25px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.conversation-settings .ivu-form-item-label {
  font-weight: 500;
  color: #333;
}

.conversation-settings .ivu-select {
  width: 100%;
}

.conversation-settings .ivu-select-selection {
  border-radius: 8px;
  border-color: rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.conversation-settings .ivu-select-selection:hover {
  border-color: #4361ee;
}

.conversation-settings .ivu-select-focused .ivu-select-selection {
  border-color: #4361ee;
  box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.2);
}
</style>