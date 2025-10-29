// useVoiceRecording.js - 語音錄音功能組合式API
import { ref, computed } from 'vue'

export function useVoiceRecording() {
  // 錄音狀態
  const isListening = ref(false)
  const isThinking = ref(false)
  const isSpeaking = ref(false)
  
  // 錄音相關
  const audioBlob = ref(null)
  const recorder = ref(null)
  const recordingTime = ref(0)
  const recordingTimer = ref(null)
  
  // 可視化
  const visualBars = ref(Array(40).fill(5))
  const visualInterval = ref(null)

  // 計算屬性
  const buttonText = computed(() => {
    if (isListening.value) return "正在聆聽..."
    if (isThinking.value) return "正在思考..."
    if (isSpeaking.value) return "正在回應..."
    return "按住開始對話"
  })

  const buttonStyle = computed(() => {
    const baseStyle = {
      width: "120px !important",
      height: "120px !important",
      borderRadius: "50% !important",
      border: "none !important",
      color: "white !important",
      fontSize: "18px !important",
      fontWeight: "600 !important",
      cursor: "pointer !important",
      transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important",
      userSelect: "none",
    }

    if (isListening.value) {
      return {
        ...baseStyle,
        background: "linear-gradient(135deg, #ff4757, #ff6b7a) !important",
        boxShadow: "0 0 30px rgba(255, 71, 87, 0.6) !important",
      }
    } else if (isThinking.value) {
      return {
        ...baseStyle,
        background: "linear-gradient(135deg, #ffa502, #ffb142) !important",
        boxShadow: "0 0 25px rgba(255, 165, 2, 0.5) !important",
      }
    } else if (isSpeaking.value) {
      return {
        ...baseStyle,
        background: "linear-gradient(135deg, #2ed573, #7bed9f) !important",
        boxShadow: "0 0 25px rgba(46, 213, 115, 0.5) !important",
      }
    } else {
      return {
        ...baseStyle,
        background: "linear-gradient(135deg, #4361ee, #4cc9f0) !important",
        boxShadow: "0 8px 25px rgba(67, 97, 238, 0.3) !important",
      }
    }
  })

  // 開始錄音
  const startRecording = async () => {
    console.log("🎙️ startRecording 開始執行")
    try {
      console.log("📱 請求麥克風權限...")
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      })
      console.log("✅ 麥克風權限獲取成功，stream:", stream)

      recorder.value = new MediaRecorder(stream)
      console.log("🎬 MediaRecorder 創建成功:", recorder.value)

      const audioChunks = []
      recorder.value.ondataavailable = (event) => {
        console.log("📊 收到音頻數據，大小:", event.data.size)
        if (event.data.size > 0) {
          audioChunks.push(event.data)
        }
      }

      recorder.value.onstop = () => {
        console.log(
          "🔴 錄音停止，總共收集到",
          audioChunks.length,
          "個音頻塊"
        )
        audioBlob.value = new Blob(audioChunks, { type: "audio/wav" })
        console.log(
          "💾 音頻Blob創建完成，大小:",
          audioBlob.value.size,
          "bytes"
        )
        stream.getTracks().forEach((track) => track.stop())
        console.log("🔌 麥克風流已關閉")
      }

      recorder.value.start()
      console.log("🔴 開始錄音，狀態:", recorder.value.state)
      startTimer()
      startVisualization()
    } catch (error) {
      console.error("❌ 錄音失敗:", error)
      throw new Error("無法訪問麥克風: " + error.message)
    }
  }

  // 停止錄音
  const stopRecording = async () => {
    console.log("🛑 stopRecording 開始執行")
    console.log("錄音器狀態:", recorder.value ? recorder.value.state : "null")

    if (recorder.value) {
      console.log("🔴 停止錄音器...")
      recorder.value.stop()
      console.log("⏰ 停止計時器...")
      stopTimer()
      console.log("📊 停止可視化...")
      stopVisualization()

      // 等待錄音完全停止
      await new Promise((resolve) => {
        if (recorder.value.state === "inactive") {
          resolve()
        } else {
          recorder.value.addEventListener("stop", resolve, { once: true })
        }
      })

      console.log("✅ 錄音完全停止")
    } else {
      console.log("❌ 錄音器不存在")
    }
  }

  // 計時器
  const startTimer = () => {
    recordingTime.value = 0
    recordingTimer.value = setInterval(() => {
      recordingTime.value++
    }, 1000)
  }

  const stopTimer = () => {
    if (recordingTimer.value) {
      clearInterval(recordingTimer.value)
      recordingTimer.value = null
    }
  }

  // 可視化
  const startVisualization = () => {
    visualInterval.value = setInterval(() => {
      visualBars.value = visualBars.value.map(() =>
        isListening.value ? Math.floor(Math.random() * 30) + 5 : 5
      )
    }, 100)
  }

  const stopVisualization = () => {
    if (visualInterval.value) {
      clearInterval(visualInterval.value)
      visualInterval.value = null
    }
    setTimeout(() => {
      visualBars.value = Array(40).fill(5)
    }, 300)
  }

  // 重置狀態
  const resetStates = () => {
    console.log("🔄 重置所有狀態")
    isListening.value = false
    isThinking.value = false
    isSpeaking.value = false
    audioBlob.value = null
  }

  // 調試方法
  const forceListening = () => {
    console.log("🔴 強制設為聆聽狀態")
    isListening.value = true
    isThinking.value = false
    isSpeaking.value = false
  }

  const resetAllStates = () => {
    console.log("🔄 重置所有狀態")
    isListening.value = false
    isThinking.value = false
    isSpeaking.value = false
  }

  const testAudioBlob = () => {
    if (audioBlob.value) {
      console.log("🎵 音頻Blob詳細信息:")
      console.log("- 大小:", audioBlob.value.size, "bytes")
      console.log("- 類型:", audioBlob.value.type)
      console.log("- 時間戳:", new Date().toLocaleTimeString())

      // 創建音頻URL進行播放測試
      const audioURL = URL.createObjectURL(audioBlob.value)
      const audio = new Audio(audioURL)
      audio
        .play()
        .then(() => {
          console.log("✅ 音頻播放測試成功")
        })
        .catch((error) => {
          console.error("❌ 音頻播放測試失敗:", error)
        })
    } else {
      console.log("❌ 沒有音頻文件")
    }
  }

  // 清理函數
  const cleanup = () => {
    stopTimer()
    stopVisualization()
    if (recorder.value && isListening.value) {
      recorder.value.stop()
    }
  }

  return {
    // 狀態
    isListening,
    isThinking,
    isSpeaking,
    audioBlob,
    recorder,
    recordingTime,
    visualBars,
    
    // 計算屬性
    buttonText,
    buttonStyle,
    
    // 方法
    startRecording,
    stopRecording,
    resetStates,
    forceListening,
    resetAllStates,
    testAudioBlob,
    cleanup
  }
}