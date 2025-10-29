<!-- components/AudioPlayer.vue -->
<template>
  <Modal
    v-model="isVisible"
    class="audio-player-modal"
    width="500"
    @on-visible-change="handleVisibleChange"
  >
    <template #header>
      <div class="audio-modal-header">
        <div class="audio-title">
          <Icon type="ios-musical-notes" />
          {{ audio.name }}
        </div>
      </div>
    </template>

    <div class="audio-player-container">
      <div class="audio-info">
        <p>
          <Icon type="ios-person" />
          專員: {{ audio.staff_name || "未指定" }}
        </p>
        <p>
          <Icon type="ios-time" />
          時長: {{ formatDuration(audio.duration) }}
        </p>
        <p>
          <Icon type="ios-calendar" />
          建立時間: {{ formatDateTime(audio.created_at) }}
        </p>
      </div>

      <div class="audio-player">
        <audio
          ref="audioPlayer"
          controls
          :src="src"
          class="player"
          @ended="isVisible = false"
        ></audio>
      </div>

      <div class="audio-description" v-if="audio.description">
        <Divider>描述</Divider>
        <div class="description-content">
          {{ audio.description }}
        </div>
      </div>
    </div>

    <template #footer>
      <div class="audio-modal-footer">
        <Button @click="isVisible = false">關閉</Button>
        <Button type="primary" @click="handleDownload">下載</Button>
      </div>
    </template>
  </Modal>
</template>

<script>
export default {
  name: "AudioPlayer",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    audio: {
      type: Object,
      default: () => ({}),
    },
    src: {
      type: String,
      default: "",
    },
  },
  emits: ["update:visible", "download"],
  data() {
    return {
      isVisible: this.visible,
    };
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
      if (visible && this.$refs.audioPlayer) {
        this.$nextTick(() => {
          this.$refs.audioPlayer.load();
          this.$refs.audioPlayer.play();
        });
      }
    },
    handleDownload() {
      this.$emit("download", this.audio.id);
    },
    formatDuration(seconds) {
      if (seconds === null || seconds === undefined) return "-";

      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
        .toString()
        .padStart(2, "0")}`;
    },
    formatDateTime(dateTimeStr) {
      if (!dateTimeStr) return "-";

      try {
        const date = new Date(dateTimeStr);
        return date.toLocaleString("zh-TW");
      } catch (e) {
        return dateTimeStr;
      }
    },
  },
};
</script>

<style scoped>
.audio-player-modal :deep(.ivu-modal-content) {
  border-radius: 8px;
  overflow: hidden;
}

.audio-modal-header {
  padding: 16px;
  background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
  color: white;
  border-radius: 8px 8px 0 0;
}

.audio-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: bold;
}

.audio-player-container {
  padding: 20px;
}

.audio-info {
  margin-bottom: 20px;
  color: #515a6e;
}

.audio-info p {
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.audio-player {
  margin: 20px 0;
}

.audio-player .player {
  width: 100%;
  height: 40px;
  border-radius: 4px;
  outline: none;
}

.description-content {
  padding: 10px;
  background-color: #f8f8f9;
  border-radius: 4px;
  color: #515a6e;
  min-height: 60px;
  white-space: pre-wrap;
  word-break: break-word;
}

.audio-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
