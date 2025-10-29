<!-- components/AudioRecorder.vue -->
<template>
  <Modal
    v-model="isVisible"
    title="錄製音頻"
    width="600"
    :mask-closable="false"
    :closable="!isRecording"
    @on-visible-change="handleVisibleChange"
    class="recorder-modal"
  >
    <div class="recorder-container">
      <div class="recorder-header">
        <div class="recorder-status">
          <div :class="['status-indicator', { recording: isRecording }]"></div>
          <span>{{ statusText }}</span>
        </div>
        <div class="recorder-timer">{{ formatTime(recordingTime) }}</div>
      </div>

      <div class="recorder-visualizer">
        <canvas ref="visualizer" width="500" height="100"></canvas>
      </div>

      <div class="recorder-controls">
        <Button
          v-if="!isRecording && !hasRecording"
          type="primary"
          icon="ios-mic"
          @click="startRecording"
          :disabled="!isAudioSupported"
        >
          開始錄音
        </Button>
        <Button
          v-if="isRecording"
          type="error"
          icon="ios-square"
          @click="stopRecording"
        >
          停止錄音
        </Button>
        <Button
          v-if="!isRecording && hasRecording"
          type="primary"
          icon="ios-play"
          @click="playRecording"
          :disabled="isPlaying"
        >
          {{ isPlaying ? "播放中..." : "播放" }}
        </Button>
        <Button
          v-if="!isRecording && hasRecording"
          type="warning"
          icon="ios-cut"
          @click="editRecording"
        >
          編輯錄音
        </Button>
        <Button
          v-if="!isRecording && hasRecording"
          type="success"
          icon="ios-redo"
          @click="startRecording"
        >
          重新錄音
        </Button>
      </div>

      <div v-if="hasRecording && !isRecording" class="recorder-form">
        <Form :model="uploadForm" :label-width="80">
          <FormItem label="名稱" required>
            <Input v-model="uploadForm.name" placeholder="請輸入錄音名稱" />
          </FormItem>
          <FormItem label="專員">
            <Select
              v-model="uploadForm.staff_id"
              filterable
              clearable
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
          <FormItem label="描述">
            <Input
              v-model="uploadForm.description"
              type="textarea"
              :rows="2"
              placeholder="請輸入描述"
            />
          </FormItem>
        </Form>
      </div>

      <div v-if="!isAudioSupported" class="browser-warning">
        <Alert type="error" show-icon>
          您的瀏覽器不支持錄音功能，請使用 Chrome、Firefox 或 Edge
          等現代瀏覽器。
        </Alert>
      </div>
    </div>

    <template #footer>
      <div class="modal-footer">
        <Button @click="closeModal" :disabled="isRecording"> 關閉 </Button>
        <Button
          v-if="hasRecording && !isRecording"
          type="primary"
          @click="uploadRecording"
          :loading="isUploading"
          :disabled="!isFormValid"
        >
          上傳錄音
        </Button>
      </div>
    </template>
  </Modal>
</template>

<script>
export default {
  name: "AudioRecorder",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    staffList: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["update:visible", "upload-success", "edit-recording"],
  data() {
    return {
      isVisible: this.visible,
      isAudioSupported: false,
      isRecording: false,
      hasRecording: false,
      isPlaying: false,
      isUploading: false,
      recordingTime: 0,
      timerInterval: null,
      mediaRecorder: null,
      audioChunks: [],
      audioBlob: null,
      audioURL: null,
      audioContext: null,
      analyser: null,
      audioPlayer: null,
      visualizerInterval: null,
      uploadForm: {
        name: "",
        staff_id: "",
        description: "",
      },
    };
  },
  computed: {
    statusText() {
      if (this.isRecording) return "正在錄音";
      if (this.hasRecording) return "錄音完成";
      return "準備錄音";
    },
    isFormValid() {
      return this.uploadForm.name.trim() !== "";
    },
  },
  watch: {
    visible(val) {
      this.isVisible = val;
    },
    isVisible(val) {
      this.$emit("update:visible", val);
    },
  },
  methods: {
    handleVisibleChange(visible) {
      if (visible) {
        this.checkAudioSupport();
        this.initAudio();
      } else {
        this.cleanupResources();
      }
    },

    checkAudioSupport() {
      this.isAudioSupported = !!(
        navigator.mediaDevices && navigator.mediaDevices.getUserMedia
      );
    },

    initAudio() {
      if (!this.isAudioSupported) return;

      this.audioContext = new (window.AudioContext ||
        window.webkitAudioContext)();
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256;

      this.audioPlayer = new Audio();
      this.audioPlayer.addEventListener("ended", () => {
        this.isPlaying = false;
        this.stopVisualization();
      });
    },

    async startRecording() {
      if (!this.isAudioSupported) return;

      // 重置之前的錄音
      if (this.hasRecording) {
        this.resetRecording();
      }

      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        this.mediaRecorder = new MediaRecorder(stream);
        this.audioChunks = [];

        // 設置錄音事件處理器
        this.mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }
        };

        this.mediaRecorder.onstop = () => {
          this.audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
          this.audioURL = URL.createObjectURL(this.audioBlob);
          this.hasRecording = true;
          this.isRecording = false;

          // 設置默認名稱
          const now = new Date();
          const timestamp = now
            .toISOString()
            .replace(/[:.]/g, "-")
            .slice(0, 19);
          this.uploadForm.name = `錄音_${timestamp}`;

          // 停止麥克風訪問
          this.stopMicrophoneAccess(stream);
        };

        // 開始錄音
        this.mediaRecorder.start();
        this.isRecording = true;

        // 設置可視化
        this.setupAudioVisualization(stream);

        // 設置計時器
        this.recordingTime = 0;
        this.timerInterval = setInterval(() => {
          this.recordingTime++;
        }, 1000);
      } catch (error) {
        console.error("錄音啟動失敗:", error);
        this.$Message.error("無法啟動錄音: " + error.message);
      }
    },

    stopRecording() {
      if (this.mediaRecorder && this.isRecording) {
        this.mediaRecorder.stop();
        clearInterval(this.timerInterval);
        this.stopVisualization();
      }
    },

    playRecording() {
      if (this.audioURL) {
        this.audioPlayer.src = this.audioURL;
        this.audioPlayer.play();
        this.isPlaying = true;

        // 播放時也顯示可視化效果
        this.setupPlaybackVisualization();
      }
    },

    stopPlayback() {
      if (this.audioPlayer && this.isPlaying) {
        this.audioPlayer.pause();
        this.audioPlayer.currentTime = 0;
        this.isPlaying = false;
        this.stopVisualization();
      }
    },

    editRecording() {
      if (this.audioBlob) {
        this.$emit("edit-recording", {
          blob: this.audioBlob,
          name: this.uploadForm.name,
          staffId: this.uploadForm.staff_id,
          description: this.uploadForm.description,
        });
        this.closeModal();
      }
    },

    setupAudioVisualization(stream) {
      const source = this.audioContext.createMediaStreamSource(stream);
      source.connect(this.analyser);
      this.drawVisualizer();
    },

    setupPlaybackVisualization() {
      const source = this.audioContext.createMediaElementSource(
        this.audioPlayer
      );
      source.connect(this.analyser);
      this.analyser.connect(this.audioContext.destination);
      this.drawVisualizer();
    },

    drawVisualizer() {
      const canvas = this.$refs.visualizer;
      if (!canvas) return;

      const canvasCtx = canvas.getContext("2d");
      const bufferLength = this.analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      canvasCtx.clearRect(0, 0, canvas.width, canvas.height);

      this.visualizerInterval = setInterval(() => {
        this.analyser.getByteFrequencyData(dataArray);

        canvasCtx.fillStyle = "rgb(20, 20, 20)";
        canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

        const barWidth = (canvas.width / bufferLength) * 2.5;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
          const barHeight = dataArray[i] / 2;

          canvasCtx.fillStyle = `rgb(
            ${Math.floor(barHeight + 100)},
            50,
            ${Math.floor(barHeight / 2)}
          )`;
          canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);

          x += barWidth + 1;
        }
      }, 50);
    },

    stopVisualization() {
      if (this.visualizerInterval) {
        clearInterval(this.visualizerInterval);
        this.visualizerInterval = null;

        // 清除畫布
        const canvas = this.$refs.visualizer;
        if (canvas) {
          const canvasCtx = canvas.getContext("2d");
          canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
        }
      }
    },

    stopMicrophoneAccess(stream) {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    },

    resetRecording() {
      if (this.audioURL) {
        URL.revokeObjectURL(this.audioURL);
      }

      this.audioChunks = [];
      this.audioBlob = null;
      this.audioURL = null;
      this.hasRecording = false;
      this.isPlaying = false;
      this.recordingTime = 0;

      // 重置表單
      this.uploadForm = {
        name: "",
        staff_id: "",
        description: "",
      };
    },

    async uploadRecording() {
      if (!this.audioBlob || !this.isFormValid) return;

      this.isUploading = true;

      try {
        // 創建 FormData
        const formData = new FormData();

        // 創建一個合適的文件名
        const fileName = `${this.uploadForm.name.replace(/\s+/g, "_")}.wav`;
        const file = new File([this.audioBlob], fileName, {
          type: "audio/wav",
        });

        formData.append("file", file);
        formData.append("name", this.uploadForm.name);

        if (this.uploadForm.staff_id) {
          formData.append("staff_id", this.uploadForm.staff_id);
        }

        if (this.uploadForm.description) {
          formData.append("description", this.uploadForm.description);
        }

        // 發送請求
        const response = await fetch("/api/audio/upload", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "上傳失敗");
        }

        this.$Message.success("錄音上傳成功");
        this.$emit("upload-success");
        this.closeModal();
      } catch (error) {
        console.error("上傳錄音失敗:", error);
        this.$Message.error(`上傳錄音失敗: ${error.message}`);
      } finally {
        this.isUploading = false;
      }
    },

    closeModal() {
      if (this.isRecording) {
        this.$Modal.confirm({
          title: "確認關閉",
          content: "錄音尚未完成，確定要關閉嗎？",
          onOk: () => {
            this.stopRecording();
            this.isVisible = false;
          },
        });
      } else {
        this.isVisible = false;
      }
    },

    cleanupResources() {
      this.stopPlayback();
      this.stopVisualization();

      if (this.isRecording) {
        this.stopRecording();
      }

      clearInterval(this.timerInterval);

      if (this.audioURL) {
        URL.revokeObjectURL(this.audioURL);
      }

      // 重置狀態
      this.resetRecording();
    },

    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60)
        .toString()
        .padStart(2, "0");
      const secs = (seconds % 60).toString().padStart(2, "0");
      return `${minutes}:${secs}`;
    },
  },
};
</script>

<style scoped>
.recorder-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 10px;
}

.recorder-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 0 10px;
}

.recorder-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #ccc;
}

.status-indicator.recording {
  background-color: #ed4014;
  animation: pulse 1.2s infinite;
}

.recorder-timer {
  font-family: monospace;
  font-size: 18px;
  font-weight: bold;
}

.recorder-visualizer {
  width: 100%;
  height: 100px;
  background-color: rgb(20, 20, 20);
  border-radius: 4px;
  overflow: hidden;
}

.recorder-controls {
  display: flex;
  gap: 10px;
  margin: 10px 0;
}

.recorder-form {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  background-color: #f8f8f9;
}

.browser-warning {
  width: 100%;
  margin-top: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(237, 64, 20, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(237, 64, 20, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(237, 64, 20, 0);
  }
}
</style>
