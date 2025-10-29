// useAudioPlayer.js - 音頻播放功能組合式API
import { ref } from 'vue'

export function useAudioPlayer() {
  // 音頻管理
  const playingAudioId = ref(null)
  const autoPlayEnabled = ref(true)

  // 播放音頻
  const playAudio = (messageId, audioRefs) => {
    const audioRef = audioRefs[`audio_${messageId}`]
    if (audioRef && audioRef[0]) {
      playingAudioId.value = messageId
      audioRef[0].play().catch((error) => {
        console.warn("播放失敗:", error)
        // 這裡需要在組件中處理消息提示
      })
    }
  }

  // 音頻播放結束
  const onAudioEnded = () => {
    playingAudioId.value = null
    // 這裡可以觸發其他狀態更新
  }

  // 音頻事件處理
  const onAudioLoadStart = () => {
    console.log("音頻開始加載")
  }

  const onAudioReady = (messageId) => {
    console.log("音頻準備就緒:", messageId)
  }

  // 切換自動播放
  const toggleAutoPlay = () => {
    autoPlayEnabled.value = !autoPlayEnabled.value
    console.log(
      autoPlayEnabled.value ? "已開啟自動播放" : "已關閉自動播放"
    )
  }

  // 自動播放AI回應
  const autoPlayAIResponse = (message, audioRefs, nextTick) => {
    if (message.type === "ai" && message.audioUrl && autoPlayEnabled.value) {
      nextTick(() => {
        playAudio(message.id, audioRefs)
      })
    }
  }

  return {
    // 狀態
    playingAudioId,
    autoPlayEnabled,
    
    // 方法
    playAudio,
    onAudioEnded,
    onAudioLoadStart,
    onAudioReady,
    toggleAutoPlay,
    autoPlayAIResponse
  }
}