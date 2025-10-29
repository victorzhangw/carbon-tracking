<template>
  <div class="voice-clone-container">
    <Card class="main-card">
      <div slot="title" class="card-title">
        <Icon type="ios-mic" />
        <span>AI 語音克隆系統</span>
      </div>

      <!-- 步驟指示器 -->
      <Steps :current="currentStep" class="steps-container">
        <Step title="上傳語音" content="上傳參考語音文件"></Step>
        <Step title="語音分析" content="分析語音質量"></Step>
        <Step title="文字輸入" content="輸入要合成的文字"></Step>
        <Step title="生成語音" content="克隆並生成語音"></Step>
      </Steps>

      <!-- 步驟 1: 上傳語音文件 -->
      <div v-if="currentStep === 0" class="step-content">
        <h3>📤 上傳參考語音文件</h3>
        <p class="step-description">
          請上傳一段清晰的語音文件作為參考，建議時長 5-30 秒，支持
          WAV、MP3、FLAC 格式。
        </p>

        <div class="upload-section">
          <Upload
            :before-upload="handleFileUpload"
            accept="audio/*"
            :show-upload-list="false"
            class="upload-area"
            drag
          >
            <div class="upload-content">
              <Icon type="ios-cloud-upload" size="48" color="#52c41a" />
              <p class="upload-text">點擊或拖拽音頻文件到此處</p>
              <p class="upload-hint">支持 WAV、MP3、FLAC 格式，建議 5-30 秒</p>
            </div>
          </Upload>

          <!-- 上傳進度 -->
          <div
            v-if="uploadProgress > 0 && uploadProgress < 100"
            class="upload-progress"
          >
            <Progress :percent="uploadProgress" status="active" />
            <p>正在上傳... {{ uploadProgress }}%</p>
          </div>

          <!-- 已上傳文件信息 -->
          <div v-if="uploadedFile" class="uploaded-file-info">
            <Alert type="success" show-icon>
              <div slot="desc">
                <p><strong>文件名:</strong> {{ uploadedFile.filename }}</p>
                <p>
                  <strong>時長:</strong>
                  {{ formatDuration(uploadedFile.analysis.duration) }}
                </p>
                <p>
                  <strong>質量評分:</strong>
                  <Rate
                    :value="uploadedFile.analysis.quality_score * 5"
                    disabled
                    allow-half
                  />
                  ({{
                    (uploadedFile.analysis.quality_score * 100).toFixed(1)
                  }}%)
                </p>
              </div>
            </Alert>

            <div class="step-actions">
              <Button type="primary" @click="nextStep" :disabled="!canProceed">
                下一步：分析語音
                <Icon type="ios-arrow-forward" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- 步驟 2: 語音分析結果 -->
      <div v-if="currentStep === 1" class="step-content">
        <h3>🔍 語音分析結果</h3>

        <div class="analysis-results">
          <Row :gutter="16">
            <Col span="12">
              <Card class="analysis-card">
                <div slot="title">基本信息</div>
                <div class="analysis-item">
                  <span class="label">總時長:</span>
                  <span class="value">{{
                    formatDuration(uploadedFile.analysis.duration)
                  }}</span>
                </div>
                <div class="analysis-item">
                  <span class="label">語音時長:</span>
                  <span class="value">{{
                    formatDuration(uploadedFile.analysis.speech_duration)
                  }}</span>
                </div>
                <div class="analysis-item">
                  <span class="label">採樣率:</span>
                  <span class="value"
                    >{{ uploadedFile.analysis.sample_rate }} Hz</span
                  >
                </div>
              </Card>
            </Col>
            <Col span="12">
              <Card class="analysis-card">
                <div slot="title">質量評估</div>
                <div class="analysis-item">
                  <span class="label">整體質量:</span>
                  <div class="quality-score">
                    <Rate
                      :value="uploadedFile.analysis.quality_score * 5"
                      disabled
                      allow-half
                    />
                    <span class="score-text">{{
                      getQualityText(uploadedFile.analysis.quality_score)
                    }}</span>
                  </div>
                </div>
                <div class="analysis-item">
                  <span class="label">靜音比例:</span>
                  <Progress
                    :percent="uploadedFile.analysis.silence_ratio * 100"
                    :stroke-color="
                      getSilenceColor(uploadedFile.analysis.silence_ratio)
                    "
                  />
                </div>
              </Card>
            </Col>
          </Row>
        </div>

        <div class="step-actions">
          <Button @click="prevStep">
            <Icon type="ios-arrow-back" />
            上一步
          </Button>
          <Button type="primary" @click="nextStep">
            下一步：輸入文字
            <Icon type="ios-arrow-forward" />
          </Button>
        </div>
      </div>

      <!-- 步驟 3: 文字輸入 -->
      <div v-if="currentStep === 2" class="step-content">
        <h3>✏️ 輸入要合成的文字</h3>

        <div class="text-input-section">
          <Card class="input-card">
            <div class="input-group">
              <label>參考文字 (可選):</label>
              <Input
                v-model="promptText"
                placeholder="請輸入參考音頻中說的話，留空將自動識別..."
                class="prompt-input"
              />
              <p class="input-hint">
                如果知道參考音頻中的具體內容，填入可提高克隆質量
              </p>
            </div>

            <div class="input-group">
              <label>目標文字:</label>
              <Input
                v-model="targetText"
                type="textarea"
                :rows="4"
                placeholder="請輸入要合成的文字內容..."
                class="target-input"
                show-word-limit
                :maxlength="500"
              />
            </div>

            <div class="input-group">
              <label>語言:</label>
              <Select v-model="selectedLanguage" class="language-select">
                <Option value="zh">中文</Option>
                <Option value="en">English</Option>
                <Option value="ja">日本語</Option>
                <Option value="ko">한국어</Option>
                <Option value="yue">粵語</Option>
              </Select>
            </div>
          </Card>
        </div>

        <div class="step-actions">
          <Button @click="prevStep">
            <Icon type="ios-arrow-back" />
            上一步
          </Button>
          <Button
            type="primary"
            @click="nextStep"
            :disabled="!canGenerateVoice"
          >
            下一步：生成語音
            <Icon type="ios-arrow-forward" />
          </Button>
        </div>
      </div>

      <!-- 步驟 4: 生成語音 -->
      <div v-if="currentStep === 3" class="step-content">
        <h3>🎵 生成語音</h3>

        <div class="generation-section">
          <!-- 生成按鈕 -->
          <div class="generate-controls">
            <Button
              type="primary"
              size="large"
              :loading="isGenerating"
              @click="generateVoice"
              :disabled="isGenerating"
              class="generate-btn"
            >
              <Icon type="ios-play" />
              {{ isGenerating ? "正在生成..." : "開始生成語音" }}
            </Button>

            <div v-if="isGenerating" class="generation-progress">
              <Progress :percent="generationProgress" status="active" />
              <p>{{ generationStatus }}</p>
            </div>
          </div>

          <!-- 生成結果 -->
          <div v-if="generatedAudio" class="results-section">
            <h4>🎧 生成結果</h4>

            <Card class="result-card">
              <div class="result-header">
                <h5>生成的語音</h5>
                <div class="result-actions">
                  <Button
                    type="success"
                    @click="playAudio"
                    :disabled="isPlaying"
                  >
                    <Icon type="ios-play" />
                    {{ isPlaying ? "播放中..." : "播放" }}
                  </Button>
                  <Button type="default" @click="downloadAudio">
                    <Icon type="ios-download" />
                    下載
                  </Button>
                </div>
              </div>

              <div class="audio-player">
                <audio
                  ref="audioPlayer"
                  :src="generatedAudio"
                  @ended="onAudioEnded"
                  controls
                  class="audio-control"
                />
              </div>

              <div class="result-text">
                <p><strong>合成文字:</strong> {{ targetText }}</p>
              </div>
            </Card>
          </div>
        </div>

        <div class="step-actions">
          <Button @click="prevStep">
            <Icon type="ios-arrow-back" />
            上一步
          </Button>
          <Button type="default" @click="resetProcess">
            <Icon type="ios-refresh" />
            重新開始
          </Button>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "VoiceClone",
  data() {
    return {
      currentStep: 0,

      // 文件上傳
      uploadProgress: 0,
      uploadedFile: null,

      // 文字輸入
      promptText: "",
      targetText: "",
      selectedLanguage: "zh",

      // 語音生成
      isGenerating: false,
      generationProgress: 0,
      generationStatus: "",
      generatedAudio: null,
      isPlaying: false,
    };
  },

  computed: {
    canProceed() {
      return this.uploadedFile && this.uploadedFile.analysis;
    },

    canGenerateVoice() {
      return this.targetText.trim().length > 0;
    },
  },

  methods: {
    async handleFileUpload(file) {
      try {
        this.uploadProgress = 0;

        const formData = new FormData();
        formData.append("audio", file);

        const response = await axios.post("/api/voice/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
          onUploadProgress: (progressEvent) => {
            this.uploadProgress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
          },
        });

        if (response.data.success) {
          this.uploadedFile = response.data;
          this.$Message.success("音頻文件上傳成功！");
        } else {
          this.$Message.error("上傳失敗");
        }
      } catch (error) {
        console.error("上傳失敗:", error);
        this.$Message.error("上傳失敗，請稍後重試");
      }

      return false; // 阻止自動上傳
    },

    async generateVoice() {
      try {
        this.isGenerating = true;
        this.generationProgress = 0;
        this.generationStatus = "正在生成語音...";

        const response = await axios.post(
          "/api/voice/clone",
          {
            reference_audio_path: this.uploadedFile.file_path,
            target_text: this.targetText,
            prompt_text: this.promptText,
            language: this.selectedLanguage,
          },
          {
            responseType: "blob",
            onDownloadProgress: (progressEvent) => {
              this.generationProgress = Math.round(
                (progressEvent.loaded * 80) / progressEvent.total
              );
            },
          }
        );

        const audioBlob = new Blob([response.data], { type: "audio/wav" });
        this.generatedAudio = URL.createObjectURL(audioBlob);

        this.generationProgress = 100;
        this.generationStatus = "生成完成！";
        this.$Message.success("語音生成成功！");
      } catch (error) {
        console.error("語音生成失敗:", error);
        this.$Message.error("語音生成失敗，請稍後重試");
      } finally {
        this.isGenerating = false;
      }
    },

    playAudio() {
      this.$refs.audioPlayer.play();
      this.isPlaying = true;
    },

    onAudioEnded() {
      this.isPlaying = false;
    },

    downloadAudio() {
      const link = document.createElement("a");
      link.href = this.generatedAudio;
      link.download = "cloned_voice.wav";
      link.click();
    },

    nextStep() {
      if (this.currentStep < 3) {
        this.currentStep++;
      }
    },

    prevStep() {
      if (this.currentStep > 0) {
        this.currentStep--;
      }
    },

    resetProcess() {
      this.currentStep = 0;
      this.uploadedFile = null;
      this.targetText = "";
      this.promptText = "";
      this.generatedAudio = null;
      this.uploadProgress = 0;
    },

    // 工具方法
    formatDuration(seconds) {
      if (!seconds) return "0:00";
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins}:${secs.toString().padStart(2, "0")}`;
    },

    getQualityText(score) {
      if (score >= 0.8) return "優秀";
      if (score >= 0.6) return "良好";
      if (score >= 0.4) return "一般";
      return "較差";
    },

    getSilenceColor(ratio) {
      if (ratio <= 0.2) return "#52c41a";
      if (ratio <= 0.4) return "#faad14";
      return "#f5222d";
    },
  },
};
</script>

<style lang="scss" scoped>
.voice-clone-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.main-card {
  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
  }
}

.steps-container {
  margin: 30px 0;
}

.step-content {
  margin: 30px 0;

  h3 {
    color: #2c3e50;
    margin-bottom: 15px;
    font-size: 20px;
  }

  .step-description {
    color: #666;
    margin-bottom: 20px;
    line-height: 1.6;
  }
}

.upload-section {
  .upload-area {
    margin-bottom: 20px;

    .upload-content {
      padding: 40px;
      text-align: center;

      .upload-text {
        font-size: 16px;
        color: #2c3e50;
        margin: 15px 0 5px 0;
      }

      .upload-hint {
        color: #999;
        font-size: 14px;
        margin: 0;
      }
    }
  }

  .upload-progress {
    margin: 20px 0;
    text-align: center;
  }

  .uploaded-file-info {
    margin: 20px 0;
  }
}

.analysis-results {
  .analysis-card {
    .analysis-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;

      .label {
        font-weight: 500;
        color: #2c3e50;
      }

      .value {
        color: #52c41a;
        font-weight: 500;
      }

      .quality-score {
        display: flex;
        align-items: center;
        gap: 8px;

        .score-text {
          font-size: 12px;
          color: #666;
        }
      }
    }
  }
}

.text-input-section {
  .input-card {
    .input-group {
      margin-bottom: 20px;

      label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
        color: #2c3e50;
      }

      .input-hint {
        font-size: 12px;
        color: #999;
        margin-top: 5px;
      }
    }
  }
}

.generation-section {
  .generate-controls {
    text-align: center;
    margin-bottom: 30px;

    .generate-btn {
      font-size: 16px;
      height: 50px;
      padding: 0 30px;
    }

    .generation-progress {
      margin-top: 20px;
      max-width: 400px;
      margin-left: auto;
      margin-right: auto;
    }
  }

  .results-section {
    h4 {
      color: #2c3e50;
      margin-bottom: 20px;
    }

    .result-card {
      .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;

        h5 {
          margin: 0;
          color: #2c3e50;
        }

        .result-actions {
          display: flex;
          gap: 10px;
        }
      }

      .audio-player {
        margin: 15px 0;

        .audio-control {
          width: 100%;
        }
      }

      .result-text {
        margin-top: 15px;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 6px;

        p {
          margin: 0;
          color: #2c3e50;
        }
      }
    }
  }
}

.step-actions {
  margin-top: 30px;
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 15px;
}

@media (max-width: 768px) {
  .voice-clone-container {
    padding: 10px;
  }

  .step-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>
