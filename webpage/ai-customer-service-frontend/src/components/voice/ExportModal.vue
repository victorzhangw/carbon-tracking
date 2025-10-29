<!-- ExportModal.vue - 導出對話模態框組件 -->
<template>
  <Modal
    :value="value"
    title="導出對話記錄"
    @on-ok="doExportConversation"
    @on-cancel="handleClose"
    @input="$emit('input', $event)"
    ok-text="導出"
    cancel-text="取消"
  >
    <Form>
      <FormItem label="導出格式:">
        <RadioGroup v-model="exportFormat">
          <Radio label="text">純文字</Radio>
          <Radio label="json">JSON格式</Radio>
          <Radio label="markdown">Markdown格式</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="包含內容:">
        <CheckboxGroup v-model="exportOptions">
          <Checkbox label="timestamp">時間戳記</Checkbox>
          <Checkbox label="sentiment">情感分析</Checkbox>
          <Checkbox label="confidence">置信度</Checkbox>
        </CheckboxGroup>
      </FormItem>
    </Form>
  </Modal>
</template>

<script>
export default {
  name: "ExportModal",
  props: {
    value: {
      type: Boolean,
      default: false
    },
    conversationHistory: {
      type: Array,
      default: () => []
    },
    conversationRounds: {
      type: Number,
      default: 0
    }
  },
  emits: ['input'],
  data() {
    return {
      exportFormat: "text",
      exportOptions: ["timestamp"]
    }
  },
  methods: {
    handleClose() {
      this.$emit('input', false);
    },
    doExportConversation() {
      const conversations = this.conversationHistory.map((msg) => {
        const baseData = {
          type: msg.type === "user" ? "用戶" : "AI助手",
          content: msg.text,
        };

        if (this.exportOptions.includes("timestamp")) {
          baseData.time = msg.time;
        }
        if (this.exportOptions.includes("sentiment") && msg.sentiment) {
          baseData.sentiment = msg.sentiment;
        }
        if (this.exportOptions.includes("confidence") && msg.confidence) {
          baseData.confidence = Math.round(msg.confidence * 100) + "%";
        }

        return baseData;
      });

      let exportData = "";
      const timestamp = new Date().toLocaleString();

      switch (this.exportFormat) {
        case "text":
          exportData = `對話記錄 - ${timestamp}\n\n`;
          conversations.forEach((conv) => {
            exportData += `${conv.type}: ${conv.content}\n`;
            if (conv.time) exportData += `時間: ${conv.time}\n`;
            if (conv.sentiment) exportData += `情感: ${conv.sentiment}\n`;
            if (conv.confidence) exportData += `置信度: ${conv.confidence}\n`;
            exportData += "\n";
          });
          break;

        case "json":
          exportData = JSON.stringify(
            {
              exportTime: timestamp,
              totalMessages: conversations.length,
              conversationRounds: this.conversationRounds,
              conversations,
            },
            null,
            2
          );
          break;

        case "markdown":
          exportData = `# 對話記錄\n\n**導出時間**: ${timestamp}  \n**總消息數**: ${conversations.length}  \n**對話輪次**: ${this.conversationRounds}\n\n---\n\n`;
          conversations.forEach((conv) => {
            exportData += `## ${conv.type}\n\n${conv.content}\n\n`;
            if (conv.time || conv.sentiment || conv.confidence) {
              exportData += "**詳細信息:**\n";
              if (conv.time) exportData += `- 時間: ${conv.time}\n`;
              if (conv.sentiment) exportData += `- 情感: ${conv.sentiment}\n`;
              if (conv.confidence)
                exportData += `- 置信度: ${conv.confidence}\n`;
              exportData += "\n";
            }
          });
          break;
      }

      // 下載文件
      const blob = new Blob([exportData], { type: "text/plain;charset=utf-8" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `conversation_${new Date().getTime()}.${
        this.exportFormat === "json"
          ? "json"
          : this.exportFormat === "markdown"
          ? "md"
          : "txt"
      }`;
      link.click();

      this.$Message.success("對話記錄已導出");
      this.handleClose();
    }
  }
}
</script>

<style scoped>
.ivu-form-item {
  margin-bottom: 20px;
}

.ivu-radio-group {
  display: flex;
  gap: 15px;
}

.ivu-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ivu-checkbox-wrapper {
  margin-right: 0;
}
</style>