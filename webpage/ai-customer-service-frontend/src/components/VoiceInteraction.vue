<!-- VoiceInteraction.vue -->
<template>
  <div class="voice-interaction">
    <Card class="interaction-card" :bordered="false">
      <template #title>
        <div class="card-title">
          <Icon type="ios-mic" size="24" />
          <span>語音互動系統</span>
        </div>
      </template>

      <div class="interaction-container">
        <div class="recording-section">
          <div
            class="audio-recorder"
            :class="{ recording: isRecording, 'has-audio': audioBlob }"
          >
            <div class="visualization" ref="visualization">
              <div
                v-for="(bar, index) in visualizationBars"
                :key="index"
                class="bar"
                :style="{ height: `${bar}px` }"
              ></div>
            </div>

            <div class="controls">
              <Button
                type="primary"
                shape="circle"
                size="large"
                :icon="isRecording ? 'ios-square' : 'ios-mic'"
                @click="toggleRecording"
                :loading="isProcessing"
              >
                {{ isRecording ? "結束錄音" : "開始錄音" }}
              </Button>

              <Button
                type="default"
                shape="circle"
                icon="ios-play"
                :disabled="!audioBlob || isRecording"
                @click="playRecording"
              >
                播放錄音
              </Button>

              <Button
                type="success"
                icon="ios-send"
                :disabled="!audioBlob || isRecording || isProcessing"
                @click="processAudio"
              >
                分析回應
              </Button>
            </div>
          </div>

          <div class="recording-timer" v-if="isRecording">
            錄音中: {{ formattedTime }}
          </div>
        </div>

        <Divider>對話紀錄</Divider>

        <div class="conversation-area">
          <div class="conversation-messages" ref="messageContainer">
            <div v-if="messages.length === 0" class="no-messages">
              <Icon type="ios-chatbubbles" size="64" />
              <p>尚未開始對話，請點擊上方錄音按鈕開始</p>
            </div>

            <div
              v-for="(msg, index) in messages"
              :key="index"
              class="message"
              :class="msg.type"
            >
              <div class="message-avatar">
                <Avatar
                  :icon="msg.type === 'user' ? 'ios-person' : 'ios-help-buoy'"
                />
              </div>
              <div class="message-content">
                <div class="message-header">
                  <span class="name">{{
                    msg.type === "user" ? "您" : "AI客服"
                  }}</span>
                  <span class="sentiment" v-if="msg.sentiment">
                    <Tag :color="getSentimentColor(msg.sentiment)">{{
                      msg.sentiment
                    }}</Tag>
                  </span>
                </div>
                <div class="message-body">
                  {{ msg.text }}
                </div>
                <div class="message-audio" v-if="msg.audioUrl">
                  <audio controls :src="msg.audioUrl"></audio>
                </div>
                <div class="message-time">
                  {{ msg.time }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="save-dialog">
        <Modal
          v-model="saveDialogVisible"
          title="儲存對話錄音"
          @on-ok="saveConversation"
        >
          <Form
            :model="saveForm"
            :rules="saveRules"
            ref="saveForm"
            :label-width="80"
          >
            <FormItem label="錄音名稱" prop="name">
              <Input v-model="saveForm.name" placeholder="請輸入錄音名稱" />
            </FormItem>
            <FormItem label="專員" prop="staffId">
              <Select
                v-model="saveForm.staffId"
                filterable
                placeholder="選擇專員"
              >
                <Option
                  v-for="staff in staffList"
                  :key="staff.id"
                  :value="staff.id"
                >
                  {{ staff.name }} ({{ staff.code }})
                </Option>
              </Select>
            </FormItem>
            <FormItem label="描述" prop="description">
              <Input
                v-model="saveForm.description"
                type="textarea"
                :rows="4"
                placeholder="請輸入描述"
              />
            </FormItem>
          </Form>
        </Modal>
      </div>
    </Card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "VoiceInteraction",
  data() {
    return {
      isRecording: false,
      isProcessing: false,
      recorder: null,
      audioBlob: null,
      audioUrl: null,
      recordingTime: 0,
      recordingTimer: null,
      messages: [],
      visualizationBars: Array(50).fill(3),
      visualizationInterval: null,
      saveDialogVisible: false,
      saveForm: {
        name: "",
        staffId: "",
        description: "",
      },
      saveRules: {
        name: [{ required: true, message: "請輸入錄音名稱", trigger: "blur" }],
      },
      staffList: [],
      savedAudioId: null, // 新增：存儲已保存錄音的ID
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.recordingTime / 60);
      const seconds = this.recordingTime % 60;
      return `${minutes.toString().padStart(2, "0")}:${seconds
        .toString()
        .padStart(2, "0")}`;
    },
  },
  methods: {
    async toggleRecording() {
      if (this.isRecording) {
        await this.stopRecording();
      } else {
        await this.startRecording();
      }
    },

    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        this.recorder = new MediaRecorder(stream);

        const audioChunks = [];
        this.recorder.ondataavailable = (e) => {
          if (e.data.size > 0) {
            audioChunks.push(e.data);
          }
        };

        this.recorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          this.audioBlob = audioBlob;
          this.audioUrl = URL.createObjectURL(audioBlob);
        };

        this.recorder.start();
        this.isRecording = true;
        this.startTimer();
        this.startVisualization();

        this.$Message.success("開始錄音");
      } catch (error) {
        this.$Message.error("無法存取麥克風: " + error.message);
        console.error("錄音失敗:", error);
      }
    },

    async stopRecording() {
      if (this.recorder && this.isRecording) {
        this.recorder.stop();
        this.isRecording = false;
        this.stopTimer();
        this.stopVisualization();

        this.recorder.stream.getTracks().forEach((track) => track.stop());
        this.$Message.success("錄音已完成");
      }
    },

    startTimer() {
      this.recordingTime = 0;
      this.recordingTimer = setInterval(() => {
        this.recordingTime++;
      }, 1000);
    },

    stopTimer() {
      clearInterval(this.recordingTimer);
    },

    startVisualization() {
      this.visualizationInterval = setInterval(() => {
        this.visualizationBars = this.visualizationBars.map(() =>
          this.isRecording ? Math.floor(Math.random() * 27) + 3 : 3
        );
      }, 100);
    },

    stopVisualization() {
      clearInterval(this.visualizationInterval);
      setTimeout(() => {
        this.visualizationBars = Array(50).fill(3);
      }, 300);
    },

    async playRecording() {
      if (!this.audioUrl) return;

      const audio = new Audio(this.audioUrl);
      audio.play();
    },

    async processAudio() {
      if (!this.audioBlob) {
        this.$Message.warning("請先錄製音頻");
        return;
      }

      try {
        this.isProcessing = true;

        // 建立 FormData 以發送文件
        const formData = new FormData();
        formData.append("file", this.audioBlob, "recording.wav");

        // 發送到後端
        const response = await axios.post("/process_audio", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        // 添加到對話中
        const now = new Date();
        const timeString = `${now.getHours().toString().padStart(2, "0")}:${now
          .getMinutes()
          .toString()
          .padStart(2, "0")}`;

        // 添加用戶消息
        this.messages.push({
          type: "user",
          text: response.data.transcript,
          time: timeString,
        });

        // 添加系統回應
        this.messages.push({
          type: "system",
          text: response.data.response,
          sentiment: response.data.sentiment,
          audioUrl: response.data.audio_url,
          time: timeString,
        });

        this.$nextTick(() => {
          // 滾動到最新消息
          if (this.$refs.messageContainer) {
            this.$refs.messageContainer.scrollTop =
              this.$refs.messageContainer.scrollHeight;
          }
        });

        // 是否儲存對話
        this.promptSaveDialog();
      } catch (error) {
        this.$Message.error(
          "處理音頻失敗: " + (error.response?.data?.error || error.message)
        );
        console.error("處理音頻失敗:", error);
      } finally {
        this.isProcessing = false;
      }
    },

    getSentimentColor(sentiment) {
      switch (sentiment.toLowerCase()) {
        case "正面":
          return "success";
        case "負面":
          return "error";
        case "中性":
          return "primary";
        default:
          return "default";
      }
    },

    promptSaveDialog() {
      this.saveForm.name = `對話記錄 ${new Date().toLocaleString("zh-TW")}`;
      this.saveDialogVisible = true;

      // 獲取專員列表
      this.fetchStaffList();
    },

    async fetchStaffList() {
      try {
        const response = await axios.get("/api/staff");
        this.staffList = response.data.items || [];
      } catch (error) {
        console.error("獲取專員列表失敗:", error);
        this.$Message.error("獲取專員列表失敗");
      }
    },

    async saveConversation() {
      this.$refs.saveForm.validate(async (valid) => {
        if (!valid || !this.audioBlob) {
          return false;
        }

        try {
          const formData = new FormData();
          formData.append("file", this.audioBlob, "recording.wav");
          formData.append("name", this.saveForm.name);
          if (this.saveForm.staffId) {
            formData.append("staff_id", this.saveForm.staffId);
          }
          formData.append("description", this.saveForm.description);

          const response = await axios.post("/api/audio/upload", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });

          // 使用 response 資料
          this.savedAudioId = response.data.id;

          // 顯示成功信息並包含錄音ID
          this.$Message.success({
            content: `錄音已成功儲存 (ID: ${this.savedAudioId})`,
            duration: 5,
            closable: true,
          });

          // 可選：在對話框中添加保存信息
          const now = new Date();
          const timeString = `${now
            .getHours()
            .toString()
            .padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}`;

          this.messages.push({
            type: "system",
            text: `錄音已保存：${this.saveForm.name} (ID: ${this.savedAudioId})`,
            time: timeString,
          });

          this.$nextTick(() => {
            // 滾動到最新消息
            if (this.$refs.messageContainer) {
              this.$refs.messageContainer.scrollTop =
                this.$refs.messageContainer.scrollHeight;
            }
          });

          this.saveDialogVisible = false;
        } catch (error) {
          this.$Message.error(
            "儲存錄音失敗: " + (error.response?.data?.error || error.message)
          );
        }
      });
    },
  },
  beforeDestroy() {
    // 清理資源
    if (this.recordingTimer) {
      clearInterval(this.recordingTimer);
    }
    if (this.visualizationInterval) {
      clearInterval(this.visualizationInterval);
    }
    if (this.audioUrl) {
      URL.revokeObjectURL(this.audioUrl);
    }
    if (this.recorder && this.isRecording) {
      this.recorder.stop();
      this.recorder.stream.getTracks().forEach((track) => track.stop());
    }
  },
};
</script>

<style scoped>
.voice-interaction {
  max-width: 1000px;
  margin: 0 auto;
}

.interaction-card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.interaction-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  color: #17233d;
}

.interaction-container {
  padding: 10px 0;
}

.recording-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.audio-recorder {
  width: 100%;
  max-width: 500px;
  padding: 20px;
  border-radius: 8px;
  background: #f8f8f9;
  border: 1px solid #e8eaec;
  transition: all 0.3s ease;
}

.audio-recorder:hover {
  border-color: #5cadff;
}

.audio-recorder.recording {
  background-color: rgba(255, 231, 231, 0.2);
  border-color: #ff9900;
  animation: pulse 1.5s infinite;
}

.audio-recorder.has-audio {
  background-color: rgba(231, 255, 236, 0.2);
  border-color: #19be6b;
}

.visualization {
  height: 60px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 2px;
  margin-bottom: 20px;
  padding: 0 20px;
}

.visualization .bar {
  width: 4px;
  background-color: #2d8cf0;
  border-radius: 2px;
  transition: height 0.1s ease;
}

.recording .visualization .bar {
  background-color: #ff9900;
}

.controls {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.recording-timer {
  margin-top: 10px;
  font-weight: bold;
  color: #ff9900;
}

.conversation-area {
  margin-top: 20px;
  height: 400px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid #e8eaec;
  overflow: hidden;
  transition: all 0.3s ease;
}

.conversation-area:hover {
  border-color: #dcdee2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.09);
}

.conversation-messages {
  height: 100%;
  padding: 15px;
  overflow-y: auto;
}

.no-messages {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #c5c8ce;
}

.message {
  display: flex;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease;
}

.message-avatar {
  margin-right: 10px;
}

.message-content {
  flex: 1;
  max-width: 85%;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.message.user .message-content {
  background-color: #ecf5ff;
  border: 1px solid #d7e8ff;
}

.message.system .message-content {
  background-color: #f8f8f9;
  border: 1px solid #e8eaec;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.message-header .name {
  font-weight: bold;
}

.message-body {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.6;
}

.message-audio {
  margin-top: 10px;
}

.message-audio audio {
  width: 100%;
  height: 32px;
}

.message-time {
  margin-top: 8px;
  text-align: right;
  font-size: 12px;
  color: #808695;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 153, 0, 0.4);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(255, 153, 0, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 153, 0, 0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
