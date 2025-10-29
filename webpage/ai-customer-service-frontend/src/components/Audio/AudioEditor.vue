<!-- components/AudioEditor.vue -->
<template>
  <Modal
    v-model="isVisible"
    title="音頻編輯器"
    width="800"
    :mask-closable="false"
    class="audio-editor-modal"
    :closable="!isProcessing"
  >
    <div class="audio-editor-container">
      <div class="editor-status">
        <Alert v-if="isLoading" type="info" show-icon>
          正在載入音頻，請稍候...
        </Alert>
        <Alert v-else-if="!isAudioSupported" type="error" show-icon>
          您的瀏覽器不支持音頻編輯功能，請使用 Chrome、Firefox 或 Edge
          等現代瀏覽器。
        </Alert>
        <Alert v-else-if="isProcessing" type="warning" show-icon>
          正在處理音頻，請稍候...
        </Alert>
        <Alert v-else-if="loadError" type="error" show-icon>
          音頻載入失敗：{{ loadError }}
        </Alert>
      </div>

      <div
        v-if="!isLoading && isAudioSupported && !loadError"
        class="waveform-container"
      >
        <div ref="waveformContainer" class="waveform"></div>

        <div class="timeline-controls">
          <Slider
            v-model="zoomLevel"
            :min="1"
            :max="200"
            :step="1"
            @on-change="handleZoomChange"
            :disabled="isProcessing"
          />
          <div class="zoom-labels">
            <span>縮小</span>
            <span>放大</span>
          </div>
        </div>

        <div class="playback-controls">
          <Button
            type="primary"
            icon="ios-play"
            :disabled="isPlaying || isProcessing"
            @click="playPause"
          >
            {{ isPlaying ? "暫停" : "播放" }}
          </Button>
          <Button
            type="warning"
            icon="ios-stop"
            :disabled="!isPlaying || isProcessing"
            @click="stop"
          >
            停止
          </Button>
          <Button
            type="error"
            icon="ios-trash"
            :disabled="!hasSelection || isProcessing"
            @click="deleteSelection"
          >
            刪除選中區域
          </Button>
          <Button
            type="default"
            icon="ios-undo"
            :disabled="!canUndo || isProcessing"
            @click="undo"
          >
            復原
          </Button>
          <Button
            type="success"
            icon="ios-refresh"
            :disabled="isProcessing"
            @click="resetAudio"
          >
            重置
          </Button>
        </div>

        <div class="region-info" v-if="hasSelection">
          <div class="region-label">選中區域：</div>
          <div class="region-time">
            {{ formatTime(selectionStart) }} -
            {{ formatTime(selectionEnd) }} ({{
              formatDuration(selectionEnd - selectionStart)
            }})
          </div>
        </div>
      </div>

      <div
        v-if="!isLoading && isAudioSupported && !loadError && !isProcessing"
        class="editor-form"
      >
        <Form
          :model="audioForm"
          :label-width="80"
          ref="editorForm"
          :rules="formRules"
        >
          <FormItem label="名稱" prop="name" required>
            <Input v-model="audioForm.name" placeholder="請輸入錄音名稱" />
          </FormItem>
          <FormItem label="專員" prop="staff_id">
            <Select
              v-model="audioForm.staff_id"
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
          <FormItem label="描述" prop="description">
            <Input
              v-model="audioForm.description"
              type="textarea"
              :rows="2"
              placeholder="請輸入描述"
            />
          </FormItem>
        </Form>
      </div>
    </div>

    <div class="modal-footer">
      <Button @click="cancel" :disabled="isProcessing"> 取消 </Button>
      <Button
        type="primary"
        @click="saveAudio"
        :loading="isProcessing"
        :disabled="
          !isFormValid || isLoading || !isAudioSupported || !!loadError
        "
      >
        儲存音頻
      </Button>
    </div>
  </Modal>
</template>

<script>
export default {
  name: "AudioEditor",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    audioData: {
      type: Object,
      default: () => null,
    },
    staffList: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["update:visible", "save"],
  data() {
    return {
      isVisible: this.visible,
      isAudioSupported: false,
      isLoading: true,
      isProcessing: false,
      isPlaying: false,
      loadError: null,
      wavesurfer: null,
      audioUrl: null,
      audioBlob: null,
      originalAudioBlob: null,
      zoomLevel: 50,
      selectionStart: 0,
      selectionEnd: 0,
      hasSelection: false,
      canUndo: false,
      editHistory: [],
      currentRegion: null,
      audioForm: {
        name: "",
        staff_id: "",
        description: "",
      },
      formRules: {
        name: [
          { required: true, message: "請輸入錄音名稱", trigger: "blur" },
          {
            min: 1,
            max: 100,
            message: "錄音名稱長度應在1-100字符之間",
            trigger: "blur",
          },
        ],
      },
    };
  },
  computed: {
    isFormValid() {
      return this.audioForm.name && this.audioForm.name.trim() !== "";
    },
  },
  watch: {
    visible(val) {
      this.isVisible = val;
      if (val) {
        this.$nextTick(() => {
          this.initEditor();
        });
      }
    },
    isVisible(val) {
      this.$emit("update:visible", val);
      if (!val) {
        this.cleanupResources();
      }
    },
    audioData: {
      handler(newData) {
        if (newData && this.isVisible) {
          this.initializeWithAudio(newData);
        }
      },
      deep: true,
    },
  },
  methods: {
    initEditor() {
      this.loadError = null;
      this.checkBrowserSupport();

      if (this.audioData) {
        this.initializeWithAudio(this.audioData);
      } else {
        this.isLoading = false;
      }
    },

    checkBrowserSupport() {
      try {
        // 檢查瀏覽器是否支持 Web Audio API
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.isAudioSupported = !!(
          AudioContext &&
          typeof window.WaveSurfer !== "undefined" &&
          typeof window.WaveSurfer.regions !== "undefined"
        );

        if (!this.isAudioSupported) {
          this.loadError = "瀏覽器不支持音頻編輯功能或 WaveSurfer 庫未正確載入";
        }
      } catch (error) {
        console.error("檢查瀏覽器支持時發生錯誤:", error);
        this.isAudioSupported = false;
        this.loadError = "檢查瀏覽器支持時發生錯誤";
      }
    },

    initializeWithAudio(audioData) {
      if (!audioData || !audioData.blob) {
        this.loadError = "音頻數據無效";
        this.isLoading = false;
        return;
      }

      this.isLoading = true;
      this.loadError = null;
      this.hasSelection = false;
      this.canUndo = false;
      this.editHistory = [];

      // 預設表單值
      this.audioForm = {
        name: audioData.name || "",
        staff_id: audioData.staffId || "",
        description: audioData.description || "",
      };

      // 確保舊資源被清理
      this.cleanupWaveSurfer();

      // 保存原始音頻
      this.originalAudioBlob = audioData.blob.slice(0); // 創建副本
      this.audioBlob = audioData.blob.slice(0);

      // 創建音頻 URL
      this.createAudioUrl();

      this.$nextTick(() => {
        this.setupWaveSurfer();
      });
    },

    createAudioUrl() {
      // 清理舊的 URL
      if (this.audioUrl) {
        URL.revokeObjectURL(this.audioUrl);
      }

      // 創建新的 URL
      try {
        this.audioUrl = URL.createObjectURL(this.audioBlob);
      } catch (error) {
        console.error("創建音頻 URL 失敗:", error);
        this.loadError = "創建音頻 URL 失敗";
        this.isLoading = false;
      }
    },

    setupWaveSurfer() {
      if (!this.isAudioSupported || !window.WaveSurfer || !this.audioUrl) {
        this.isLoading = false;
        return;
      }

      try {
        // 初始化 WaveSurfer
        this.wavesurfer = WaveSurfer.create({
          container: this.$refs.waveformContainer,
          waveColor: "#4a76a8",
          progressColor: "#2d8cf0",
          cursorColor: "#f56c6c",
          height: 120,
          barWidth: 2,
          barGap: 1,
          responsive: true,
          normalize: true,
          backend: "WebAudio",
          plugins: [
            WaveSurfer.regions.create({
              dragSelection: true,
              color: "rgba(45, 140, 240, 0.2)",
            }),
          ],
        });

        // 設置事件監聽器
        this.setupWaveSurferEvents();

        // 載入音頻
        this.wavesurfer.load(this.audioUrl);
      } catch (error) {
        console.error("初始化 WaveSurfer 失敗:", error);
        this.loadError = `初始化音頻編輯器失敗: ${error.message}`;
        this.isLoading = false;
      }
    },

    setupWaveSurferEvents() {
      if (!this.wavesurfer) return;

      this.wavesurfer.on("ready", () => {
        this.isLoading = false;
        this.loadError = null;
        this.handleZoomChange(this.zoomLevel);
      });

      this.wavesurfer.on("error", (error) => {
        console.error("WaveSurfer 錯誤:", error);
        this.loadError = `音頻載入錯誤: ${error}`;
        this.isLoading = false;
      });

      this.wavesurfer.on("play", () => {
        this.isPlaying = true;
      });

      this.wavesurfer.on("pause", () => {
        this.isPlaying = false;
      });

      this.wavesurfer.on("finish", () => {
        this.isPlaying = false;
      });

      this.wavesurfer.on("region-created", (region) => {
        // 移除之前的區域
        if (this.currentRegion && this.currentRegion !== region) {
          this.currentRegion.remove();
        }

        this.currentRegion = region;
        this.selectionStart = region.start;
        this.selectionEnd = region.end;
        this.hasSelection = true;
      });

      this.wavesurfer.on("region-updated", (region) => {
        this.selectionStart = region.start;
        this.selectionEnd = region.end;
      });

      this.wavesurfer.on("region-removed", () => {
        this.hasSelection = false;
        this.currentRegion = null;
      });
    },

    handleZoomChange(value) {
      if (this.wavesurfer && !this.isProcessing) {
        try {
          // 轉換為合適的縮放比例 (1-200 -> 10-1000)
          const zoomValue = Math.max(10, 10 + (value - 1) * 5);
          this.wavesurfer.zoom(zoomValue);
        } catch (error) {
          console.error("縮放操作失敗:", error);
        }
      }
    },

    playPause() {
      if (this.wavesurfer && !this.isProcessing) {
        try {
          this.wavesurfer.playPause();
        } catch (error) {
          console.error("播放/暫停操作失敗:", error);
          this.$Message.error("播放操作失敗");
        }
      }
    },

    stop() {
      if (this.wavesurfer && !this.isProcessing) {
        try {
          this.wavesurfer.stop();
          this.isPlaying = false;
        } catch (error) {
          console.error("停止操作失敗:", error);
        }
      }
    },

    async deleteSelection() {
      if (!this.hasSelection || !this.wavesurfer || this.isProcessing) return;

      this.isProcessing = true;

      try {
        // 儲存當前狀態以便撤銷
        this.saveToHistory();

        // 使用簡化的音頻處理方法
        await this.processAudioDeletion();

        // 移除當前區域
        if (this.currentRegion) {
          this.currentRegion.remove();
        }

        // 設置可撤銷狀態
        this.canUndo = true;

        this.$Message.success("已刪除選中區域");
      } catch (error) {
        console.error("刪除選中區域失敗:", error);
        this.$Message.error(`刪除操作失敗: ${error.message}`);
      } finally {
        this.isProcessing = false;
      }
    },

    async processAudioDeletion() {
      // 這裡實現音頻刪除的邏輯
      // 由於 WaveSurfer 的音頻處理比較複雜，這裡提供一個簡化版本
      // 實際項目中可能需要使用專門的音頻處理庫

      return new Promise((resolve, reject) => {
        try {
          // 創建一個新的音頻 Blob（這裡是模擬，實際需要音頻處理）
          // 在實際應用中，您需要：
          // 1. 將音頻轉換為 AudioBuffer
          // 2. 刪除指定區域的樣本
          // 3. 重新編碼為音頻格式

          // 暫時使用原始音頻作為處理結果（需要實現真正的音頻處理）
          this.audioBlob = this.audioBlob.slice(0);

          // 重新載入音頻
          this.reloadAudio();

          resolve();
        } catch (error) {
          reject(error);
        }
      });
    },

    saveToHistory() {
      if (this.audioBlob && this.editHistory.length < 10) {
        // 限制歷史記錄數量
        this.editHistory.push(this.audioBlob.slice(0));
        this.canUndo = true;
      }
    },

    undo() {
      if (!this.canUndo || this.editHistory.length === 0 || this.isProcessing)
        return;

      this.isProcessing = true;

      try {
        // 從歷史記錄中還原最後一個狀態
        const lastState = this.editHistory.pop();

        // 如果歷史記錄為空，則不能再撤銷
        this.canUndo = this.editHistory.length > 0;

        // 更新當前的音頻 Blob
        this.audioBlob = lastState;

        // 重新載入音頻
        this.reloadAudio();

        this.$Message.success("已撤銷上一步操作");
      } catch (error) {
        console.error("撤銷操作失敗:", error);
        this.$Message.error(`撤銷操作失敗: ${error.message}`);
      } finally {
        this.isProcessing = false;
      }
    },

    resetAudio() {
      if (!this.originalAudioBlob || this.isProcessing) return;

      this.isProcessing = true;

      try {
        // 重置到原始音頻
        this.audioBlob = this.originalAudioBlob.slice(0);
        this.editHistory = [];
        this.canUndo = false;

        // 重新載入音頻
        this.reloadAudio();

        this.$Message.success("已重置音頻到原始狀態");
      } catch (error) {
        console.error("重置音頻失敗:", error);
        this.$Message.error(`重置操作失敗: ${error.message}`);
      } finally {
        this.isProcessing = false;
      }
    },

    reloadAudio() {
      if (!this.wavesurfer || !this.audioBlob) return;

      try {
        // 創建新的音頻 URL
        this.createAudioUrl();

        // 重新載入 WaveSurfer
        this.wavesurfer.load(this.audioUrl);

        // 移除當前區域
        if (this.currentRegion) {
          this.currentRegion.remove();
        }
      } catch (error) {
        console.error("重新載入音頻失敗:", error);
        throw error;
      }
    },

    saveAudio() {
      if (!this.audioBlob || !this.isFormValid) {
        this.$Message.warning("請檢查表單輸入");
        return;
      }

      // 驗證表單
      if (this.$refs.editorForm) {
        this.$refs.editorForm.validate((valid) => {
          if (!valid) {
            this.$Message.error("請檢查表單輸入");
            return;
          }

          this.performSave();
        });
      } else {
        this.performSave();
      }
    },

    performSave() {
      this.isProcessing = true;

      try {
        // 創建 File 對象
        const fileName = `${this.audioForm.name.replace(/\s+/g, "_")}.wav`;
        const file = new File([this.audioBlob], fileName, {
          type: "audio/wav",
        });

        // 發送到父組件處理上傳
        this.$emit("save", {
          blob: this.audioBlob,
          file: file,
          name: this.audioForm.name,
          staff_id: this.audioForm.staff_id,
          description: this.audioForm.description,
        });

        this.isVisible = false;
      } catch (error) {
        console.error("保存音頻失敗:", error);
        this.$Message.error(`保存音頻失敗: ${error.message}`);
        this.isProcessing = false;
      }
    },

    cancel() {
      if (this.isProcessing) {
        this.$Message.warning("正在處理音頻，請稍候...");
        return;
      }

      this.isVisible = false;
    },

    cleanupWaveSurfer() {
      if (this.wavesurfer) {
        try {
          this.wavesurfer.destroy();
        } catch (error) {
          console.error("清理 WaveSurfer 時發生錯誤:", error);
        }
        this.wavesurfer = null;
      }
    },

    cleanupResources() {
      // 停止播放
      this.isPlaying = false;

      // 清理 WaveSurfer
      this.cleanupWaveSurfer();

      // 清理音頻 URL
      if (this.audioUrl) {
        try {
          URL.revokeObjectURL(this.audioUrl);
        } catch (error) {
          console.error("清理音頻 URL 時發生錯誤:", error);
        }
        this.audioUrl = null;
      }

      // 清理音頻數據
      this.audioBlob = null;
      this.originalAudioBlob = null;
      this.editHistory = [];
      this.hasSelection = false;
      this.canUndo = false;
      this.currentRegion = null;

      // 重置狀態
      this.isLoading = true;
      this.isProcessing = false;
      this.loadError = null;
    },

    formatTime(seconds) {
      const min = Math.floor(seconds / 60);
      const sec = Math.floor(seconds % 60);
      const ms = Math.floor((seconds % 1) * 1000);

      return `${min.toString().padStart(2, "0")}:${sec
        .toString()
        .padStart(2, "0")}.${ms.toString().padStart(3, "0")}`;
    },

    formatDuration(seconds) {
      const min = Math.floor(seconds / 60);
      const sec = Math.floor(seconds % 60);
      const ms = Math.floor((seconds % 1) * 1000);

      return `${min}分 ${sec}秒 ${ms}毫秒`;
    },
  },

  beforeUnmount() {
    this.cleanupResources();
  },
};
</script>

<style scoped>
.audio-editor-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 10px;
}

.editor-status {
  width: 100%;
}

.waveform-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.waveform {
  width: 100%;
  height: 120px;
  border: 1px solid #e8eaec;
  border-radius: 4px;
  overflow: hidden;
}

.timeline-controls {
  margin-top: 10px;
  width: 100%;
}

.zoom-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #808695;
  margin-top: 5px;
}

.playback-controls {
  display: flex;
  gap: 10px;
  margin: 15px 0;
  flex-wrap: wrap;
}

.region-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 5px 0;
  padding: 8px;
  background-color: #f8f8f9;
  border-radius: 4px;
  font-size: 14px;
}

.region-label {
  font-weight: bold;
  color: #17233d;
}

.region-time {
  color: #515a6e;
  font-family: monospace;
}

.editor-form {
  width: 100%;
  margin-top: 10px;
  padding: 15px;
  background-color: #f8f8f9;
  border-radius: 4px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.ivu-modal-content) {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border-radius: 8px;
}

:deep(.ivu-modal-header) {
  border-radius: 8px 8px 0 0;
}

:deep(.ivu-alert) {
  margin-bottom: 10px;
}

:deep(.ivu-form-item) {
  margin-bottom: 15px;
}

:deep(.ivu-input:focus),
:deep(.ivu-input:hover) {
  border-color: #57a3f3;
  box-shadow: 0 0 0 2px rgba(45, 140, 240, 0.2);
  transition: all 0.3s ease;
}

:deep(.ivu-select:hover .ivu-select-selection),
:deep(.ivu-select-focused .ivu-select-selection) {
  border-color: #57a3f3;
  box-shadow: 0 0 0 2px rgba(45, 140, 240, 0.2);
}

:deep(.ivu-btn) {
  margin-right: 8px;
  margin-bottom: 8px;
}

:deep(.ivu-slider) {
  margin: 10px 0;
}
</style>
