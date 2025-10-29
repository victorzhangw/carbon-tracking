// VoiceRecorderMixin.js - 語音錄音相關邏輯
import axios from "axios";

export default {
  methods: {
    // 檢查麥克風權限
    async checkMicrophonePermission() {
      try {
        if (navigator.permissions) {
          const permission = await navigator.permissions.query({
            name: "microphone",
          });
          this.microphonePermission = permission.state;

          console.log("麥克風權限狀態:", permission.state);

          // 監聽權限變化
          permission.onchange = () => {
            this.microphonePermission = permission.state;
            console.log("權限狀態變化:", permission.state);
          };
        }
      } catch (error) {
        console.warn("無法檢查麥克風權限:", error);
      }
    },

    // 預先初始化錄音器
    async preInitializeRecorder() {
      try {
        if (this.microphonePermission === "denied") {
          return;
        }

        // 嘗試獲取麥克風流來預熱
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        console.log("✅ 麥克風預熱成功");

        // 立即關閉流，因為這只是為了預熱
        stream.getTracks().forEach((track) => track.stop());
        this.isRecorderReady = true;
      } catch (error) {
        console.log("麥克風預熱失敗（正常情況）:", error.message);
        this.isRecorderReady = false;
      }
    },

    // 開始錄音
    async startRecording() {
      console.log("🎙️ startRecording 開始執行");

      try {
        this.retryCount = 0;
        await this.attemptRecording();
      } catch (error) {
        console.error("❌ 錄音完全失敗:", error);
        throw error;
      }
    },

    // 嘗試錄音（包含重試邏輯）
    async attemptRecording() {
      try {
        console.log(`📱 嘗試錄音 (第${this.retryCount + 1}次)...`);

        // 檢查基本支持
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          throw new Error("您的瀏覽器不支持錄音功能");
        }

        // 檢查權限狀態
        if (this.microphonePermission === "denied") {
          throw new Error("麥克風權限被拒絕，請在瀏覽器設置中允許麥克風訪問");
        }

        // 請求麥克風權限時增加超時處理
        const stream = await Promise.race([
          navigator.mediaDevices.getUserMedia({
            audio: {
              echoCancellation: true,
              noiseSuppression: true,
              autoGainControl: true,
            },
          }),
          new Promise((_, reject) =>
            setTimeout(() => reject(new Error("麥克風權限請求超時")), 10000)
          ),
        ]);

        console.log("✅ 麥克風權限獲取成功");

        // 檢查音軌
        const audioTracks = stream.getAudioTracks();
        if (audioTracks.length === 0) {
          throw new Error("沒有可用的音頻軌道");
        }

        console.log("音頻軌道信息:", audioTracks[0].getSettings());

        // 創建 MediaRecorder
        this.recorder = new MediaRecorder(stream, {
          mimeType: this.getSupportedMimeType(),
        });

        console.log("🎬 MediaRecorder 創建成功");

        const audioChunks = [];

        // 設置事件處理器
        this.setupRecorderEvents(audioChunks, stream);

        // 等待錄音器準備就緒
        await this.waitForRecorderReady();

        // 開始錄音
        this.recorder.start(100);
        console.log("🔴 開始錄音，狀態:", this.recorder.state);

        // 啟動計時器和可視化
        this.startTimer();
        this.startVisualization();

        // 更新權限狀態
        this.microphonePermission = "granted";
      } catch (error) {
        console.error(`❌ 第${this.retryCount + 1}次錄音嘗試失敗:`, error);

        // 重試邏輯
        if (this.shouldRetry(error)) {
          this.retryCount++;
          console.log(`🔄 準備第${this.retryCount + 1}次重試...`);

          await new Promise((resolve) => setTimeout(resolve, 1000));
          return this.attemptRecording();
        } else {
          throw error;
        }
      }
    },

    // 設置錄音器事件
    setupRecorderEvents(audioChunks, stream) {
      this.recorder.ondataavailable = (event) => {
        console.log("📊 收到音頻數據，大小:", event.data.size);
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      this.recorder.onstop = () => {
        console.log("🔴 錄音停止，總共收集到", audioChunks.length, "個音頻塊");
        if (audioChunks.length > 0) {
          this.audioBlob = new Blob(audioChunks, {
            type: this.recorder.mimeType || "audio/wav",
          });
          console.log(
            "💾 音頻Blob創建完成，大小:",
            this.audioBlob.size,
            "bytes"
          );
        } else {
          console.warn("⚠️ 沒有收集到音頻數據");
        }

        // 關閉媒體流
        stream.getTracks().forEach((track) => track.stop());
        console.log("🔌 麥克風流已關閉");
      };

      this.recorder.onerror = (event) => {
        console.error("錄音器錯誤:", event.error);
        throw new Error(`錄音器錯誤: ${event.error}`);
      };
    },

    // 等待錄音器準備就緒
    async waitForRecorderReady() {
      return new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          reject(new Error("錄音器初始化超時"));
        }, 5000);

        if (this.recorder.state === "inactive") {
          clearTimeout(timeout);
          resolve();
        } else {
          setTimeout(() => {
            clearTimeout(timeout);
            if (this.recorder.state === "inactive") {
              resolve();
            } else {
              reject(new Error(`錄音器狀態異常: ${this.recorder.state}`));
            }
          }, 100);
        }
      });
    },

    // 判斷是否應該重試
    shouldRetry(error) {
      return (
        this.retryCount < this.maxRetryCount &&
        !error.message.includes("權限被拒絕") &&
        !error.message.includes("Permission denied") &&
        !error.message.includes("NotAllowedError")
      );
    },

    // 停止錄音
    async stopRecording() {
      console.log("🛑 stopRecording 開始執行");

      if (this.recorder && this.recorder.state === "recording") {
        console.log("🔴 停止錄音器...");
        this.recorder.stop();
        this.stopTimer();
        this.stopVisualization();

        // 等待錄音完全停止
        await new Promise((resolve) => {
          if (this.recorder.state === "inactive") {
            resolve();
          } else {
            this.recorder.addEventListener("stop", resolve, { once: true });
          }
        });

        console.log("✅ 錄音完全停止");
      } else {
        console.log("❌ 錄音器不存在或未在錄音");
      }
    },

    // 獲取支持的音頻格式
    getSupportedMimeType() {
      const types = [
        "audio/webm;codecs=opus",
        "audio/webm",
        "audio/ogg;codecs=opus",
        "audio/wav",
      ];

      for (const type of types) {
        if (MediaRecorder.isTypeSupported(type)) {
          console.log("使用音頻格式:", type);
          return type;
        }
      }

      console.log("使用默認音頻格式");
      return undefined;
    },

    // 執行語音識別
    async performSpeechRecognition() {
      console.log("🎯 開始語音識別...");
      console.log("音頻Blob信息:", {
        size: this.audioBlob?.size,
        type: this.audioBlob?.type,
      });

      if (!this.audioBlob || this.audioBlob.size === 0) {
        throw new Error("沒有錄音數據");
      }

      const formData = new FormData();
      formData.append("file", this.audioBlob, "recording.wav");

      console.log("📤 發送語音識別請求...");

      const response = await axios.post("/process_audio", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 60000,
      });

      console.log("📥 語音識別響應:", response.data);

      if (response.data.transcript) {
        console.log("✅ 語音識別成功:", response.data.transcript);
        return response.data.transcript;
      } else {
        console.error("❌ 語音識別失敗，響應:", response.data);
        throw new Error("語音識別失敗，請重試");
      }
    },

    // 計時器
    startTimer() {
      this.recordingTime = 0;
      this.recordingTimer = setInterval(() => {
        this.recordingTime++;
      }, 1000);
    },

    stopTimer() {
      if (this.recordingTimer) {
        clearInterval(this.recordingTimer);
        this.recordingTimer = null;
      }
    },

    // 可視化
    startVisualization() {
      if (this.visualInterval) {
        clearInterval(this.visualInterval);
      }

      this.visualInterval = setInterval(() => {
        if (this.isListening) {
          // 生成更自然的可視化數據
          this.visualBars = this.visualBars.map(
            () => Math.floor(Math.random() * 25) + 5
          );
        }
      }, 100);
    },

    stopVisualization() {
      if (this.visualInterval) {
        clearInterval(this.visualInterval);
        this.visualInterval = null;
      }

      // 平滑回到靜止狀態
      setTimeout(() => {
        this.visualBars = Array(40).fill(5);
      }, 300);
    },

    // 測試音頻Blob
    testAudioBlob() {
      if (this.audioBlob) {
        console.log("🎵 音頻Blob詳細信息:");
        console.log("- 大小:", this.audioBlob.size, "bytes");
        console.log("- 類型:", this.audioBlob.type);
        console.log("- 時間戳:", new Date().toLocaleTimeString());

        // 創建音頻URL進行播放測試
        const audioURL = URL.createObjectURL(this.audioBlob);
        const audio = new Audio(audioURL);

        audio
          .play()
          .then(() => {
            console.log("✅ 音頻播放測試成功");
            this.$Message.success("音頻文件正常，可以播放");
          })
          .catch((error) => {
            console.error("❌ 音頻播放測試失敗:", error);
            this.$Message.error("音頻文件損壞或格式不支持");
          })
          .finally(() => {
            URL.revokeObjectURL(audioURL);
          });
      } else {
        console.log("❌ 沒有音頻文件");
        this.$Message.warning("請先錄音再測試");
      }
    },

    // 清理資源
    cleanup() {
      this.stopTimer();
      this.stopVisualization();

      if (this.recorder && this.recorder.state === "recording") {
        this.recorder.stop();
      }

      if (this.audioBlob) {
        this.audioBlob = null;
      }
    },
  },

  data() {
    return {
      visualBars: Array(40).fill(5),
      visualInterval: null,
    };
  },

  beforeDestroy() {
    this.cleanup();
  },
};
