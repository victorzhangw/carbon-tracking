<template>
  <div class="voice-synthesis-container">
    <Card class="synthesis-card">
      <div slot="title" class="card-title">
        <Icon type="ios-mic" />
        <span>AI 語音合成</span>
      </div>

      <!-- 語音合成區域 -->
      <div class="synthesis-section">
        <div class="input-group">
          <label>要合成的文字：</label>
          <Input
            v-model="synthesisText"
            type="textarea"
            :rows="3"
            placeholder="請輸入要轉換為語音的文字..."
            class="text-input"
          />
        </div>

        <div class="voice-options">
          <div class="option-group">
            <label>語言選擇：</label>
            <Select v-model="selectedLanguage" class="language-select">
              <Option value="zh">中文</Option>
              <Option value="en">English</Option>
              <Option value="ja">日本語</Option>
              <Option value="ko">한국어</Option>
              <Option value="yue">粵語</Option>
            </Select>
          </div>

          <div class="option-group">
            <label>語音速度：</label>
            <Slider
              v-model="speechSpeed"
              :min="0.5"
              :max="2.0"
              :step="0.1"
              show-input
              class="speed-slider"
            />
          </div>
        </div>

        <!-- 參考音頻上傳 -->
        <div class="reference-section">
          <h4>參考音頻 (聲音克隆)</h4>
          <Upload
            :before-upload="handleReferenceUpload"
            accept="audio/*"
            :show-upload-list="false"
            class="audio-upload"
          >
            <Button icon="ios-cloud-upload-outline" type="dashed">
              上傳參考音頻 (5秒以上)
            </Button>
          </Upload>

          <div v-if="referenceAudio" class="reference-info">
            <Icon type="ios-musical-note" color="#52c41a" />
            <span>{{ referenceAudio.name }}</span>
            <Button
              type="text"
              size="small"
              @click="clearReference"
              icon="ios-close"
            />
          </div>

          <div class="reference-text-group">
            <label>參考音頻對應文字：</label>
            <Input
              v-model="referenceText"
              placeholder="請輸入參考音頻中說的話..."
              :disabled="!referenceAudio"
            />
          </div>
        </div>

        <!-- 操作按鈕 -->
        <div class="action-buttons">
          <Button
            type="primary"
            size="large"
            :loading="isSynthesizing"
            @click="synthesizeVoice"
            :disabled="!canSynthesize"
          >
            <Icon type="ios-play" />
            {{ isSynthesizing ? "合成中..." : "開始合成" }}
          </Button>

          <Button
            v-if="synthesizedAudio"
            type="success"
            size="large"
            @click="playAudio"
            :disabled="isPlaying"
          >
            <Icon type="ios-volume-high" />
            {{ isPlaying ? "播放中..." : "播放語音" }}
          </Button>

          <Button
            v-if="synthesizedAudio"
            type="default"
            size="large"
            @click="downloadAudio"
          >
            <Icon type="ios-download" />
            下載音頻
          </Button>
        </div>
      </div>

      <!-- 語音播放器 -->
      <div v-if="synthesizedAudio" class="audio-player">
        <audio
          ref="audioPlayer"
          :src="synthesizedAudio"
          @ended="onAudioEnded"
          @loadstart="onAudioLoadStart"
          @canplay="onAudioCanPlay"
          controls
          class="audio-control"
        />
      </div>

      <!-- 預設語音模板 -->
      <div class="voice-templates">
        <h4>快速模板</h4>
        <div class="template-grid">
          <Card
            v-for="template in voiceTemplates"
            :key="template.id"
            class="template-card"
            @click="useTemplate(template)"
          >
            <div class="template-content">
              <Icon :type="template.icon" size="24" />
              <h5>{{ template.name }}</h5>
              <p>{{ template.description }}</p>
            </div>
          </Card>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "VoiceSynthesis",
  data() {
    return {
      synthesisText: "",
      selectedLanguage: "zh",
      speechSpeed: 1.0,
      referenceAudio: null,
      referenceText: "",
      synthesizedAudio: null,
      isSynthesizing: false,
      isPlaying: false,

      voiceTemplates: [
        {
          id: 1,
          name: "客服問候",
          icon: "ios-person",
          description: "專業客服語音",
          text: "您好，歡迎使用我們的服務，請問有什麼可以幫助您的嗎？",
        },
        {
          id: 2,
          name: "系統通知",
          icon: "ios-notifications",
          description: "系統提醒語音",
          text: "您有新的消息，請注意查收。",
        },
        {
          id: 3,
          name: "關懷問候",
          icon: "ios-heart",
          description: "溫馨關懷語音",
          text: "您好，我是您的專屬關懷助手，今天過得怎麼樣呢？",
        },
      ],
    };
  },

  computed: {
    canSynthesize() {
      return this.synthesisText.trim() && !this.isSynthesizing;
    },
  },

  methods: {
    handleReferenceUpload(file) {
      // 驗證文件類型
      if (!file.type.startsWith("audio/")) {
        this.$Message.error("請上傳音頻文件");
        return false;
      }

      // 驗證文件大小 (最大 10MB)
      if (file.size > 10 * 1024 * 1024) {
        this.$Message.error("音頻文件不能超過 10MB");
        return false;
      }

      this.referenceAudio = file;
      this.$Message.success("參考音頻上傳成功");
      return false; // 阻止自動上傳
    },

    clearReference() {
      this.referenceAudio = null;
      this.referenceText = "";
    },

    async synthesizeVoice() {
      if (!this.canSynthesize) return;

      this.isSynthesizing = true;

      try {
        let response;

        if (this.referenceAudio && this.referenceText) {
          // 使用聲音克隆
          const formData = new FormData();
          formData.append("audio", this.referenceAudio);
          formData.append("sample_text", this.referenceText);
          formData.append("target_text", this.synthesisText);
          formData.append("language", this.selectedLanguage);

          response = await axios.post("/api/voice/clone", formData, {
            headers: { "Content-Type": "multipart/form-data" },
            responseType: "blob",
          });
        } else {
          // 使用預設語音合成
          response = await axios.post(
            "/api/voice/synthesize",
            {
              text: this.synthesisText,
              language: this.selectedLanguage,
              speed: this.speechSpeed,
              reference_audio: "/default/reference.wav", // 預設參考音頻
              reference_text: "這是一段參考語音。",
            },
            {
              responseType: "blob",
            }
          );
        }

        // 創建音頻 URL
        const audioBlob = new Blob([response.data], { type: "audio/wav" });
        this.synthesizedAudio = URL.createObjectURL(audioBlob);

        this.$Message.success("語音合成成功！");
      } catch (error) {
        console.error("語音合成失敗:", error);
        this.$Message.error("語音合成失敗，請稍後重試");
      } finally {
        this.isSynthesizing = false;
      }
    },

    playAudio() {
      if (this.synthesizedAudio && this.$refs.audioPlayer) {
        this.$refs.audioPlayer.play();
        this.isPlaying = true;
      }
    },

    downloadAudio() {
      if (this.synthesizedAudio) {
        const link = document.createElement("a");
        link.href = this.synthesizedAudio;
        link.download = `synthesized_voice_${Date.now()}.wav`;
        link.click();
      }
    },

    onAudioEnded() {
      this.isPlaying = false;
    },

    onAudioLoadStart() {
      this.isPlaying = false;
    },

    onAudioCanPlay() {
      // 音頻可以播放
    },

    useTemplate(template) {
      this.synthesisText = template.text;
      this.$Message.info(`已使用模板：${template.name}`);
    },
  },

  beforeDestroy() {
    // 清理音頻 URL
    if (this.synthesizedAudio) {
      URL.revokeObjectURL(this.synthesizedAudio);
    }
  },
};
</script>

<style lang="scss" scoped>
.voice-synthesis-container {
  padding: 20px;
}

.synthesis-card {
  max-width: 800px;
  margin: 0 auto;

  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
  }
}

.synthesis-section {
  .input-group {
    margin-bottom: 20px;

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: #2c3e50;
    }

    .text-input {
      font-size: 14px;
    }
  }

  .voice-options {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;

    .option-group {
      label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
        color: #2c3e50;
      }

      .language-select {
        width: 100%;
      }

      .speed-slider {
        width: 100%;
      }
    }
  }

  .reference-section {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;

    h4 {
      margin: 0 0 15px 0;
      color: #2c3e50;
      font-size: 16px;
    }

    .audio-upload {
      margin-bottom: 15px;
    }

    .reference-info {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      background: #e8f5e8;
      border-radius: 6px;
      margin-bottom: 15px;

      span {
        flex: 1;
        color: #52c41a;
        font-weight: 500;
      }
    }

    .reference-text-group {
      label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
        color: #2c3e50;
      }
    }
  }

  .action-buttons {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-bottom: 20px;
  }
}

.audio-player {
  text-align: center;
  margin: 20px 0;

  .audio-control {
    width: 100%;
    max-width: 400px;
  }
}

.voice-templates {
  margin-top: 30px;

  h4 {
    margin-bottom: 15px;
    color: #2c3e50;
    font-size: 16px;
  }

  .template-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;

    .template-card {
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .template-content {
        text-align: center;
        padding: 10px;

        h5 {
          margin: 10px 0 5px 0;
          color: #2c3e50;
          font-size: 14px;
        }

        p {
          margin: 0;
          color: #666;
          font-size: 12px;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .voice-options {
    grid-template-columns: 1fr !important;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .template-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
