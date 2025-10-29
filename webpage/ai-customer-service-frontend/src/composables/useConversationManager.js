// useConversationManager.js - 對話管理功能組合式API
import { ref, computed } from 'vue'

export function useConversationManager() {
  // 對話管理
  const conversationHistory = ref([])
  const conversationContext = ref([]) // 對話上下文
  const messageIdCounter = ref(1)
  const conversationRounds = ref(0)
  const lastUserMessage = ref(null)

  // 系統設置
  const selectedStaff = ref("admin")
  const responseStyle = ref("friendly")
  const conversationMode = ref("continuous")

  // UI狀態
  const showDebug = ref(true) // 默認顯示調試信息以便診斷問題
  const errorModal = ref(false)
  const errorMessage = ref("")
  const exportModal = ref(false)
  const regeneratingId = ref(null)

  // 示例問題
  const sampleQuestions = ref([
    "你好，請介紹一下你自己",
    "今天天氣如何？",
    "推薦一些學習資源",
    "幫我制定學習計劃",
  ])

  // 計算屬性
  const totalMessages = computed(() => {
    return conversationHistory.value.length
  })

  // 添加消息
  const addMessage = (
    type,
    text,
    audioUrl = null,
    sentiment = null,
    isVoice = false,
    confidence = null
  ) => {
    const message = {
      id: messageIdCounter.value++,
      type,
      text,
      audioUrl,
      sentiment,
      confidence,
      isVoice,
      time: new Date().toLocaleTimeString(),
      timestamp: new Date(),
    }

    conversationHistory.value.push(message)
    return message
  }

  // 構建對話上下文
  const buildConversationContext = () => {
    // 保留最近5輪對話作為上下文
    const recentMessages = conversationHistory.value.slice(-10)
    return recentMessages.map((msg) => ({
      role: msg.type === "user" ? "user" : "assistant",
      content: msg.text,
      timestamp: msg.timestamp,
    }))
  }

  // 複製消息
  const copyMessage = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      // 這裡需要在組件中處理消息提示
      console.log("消息已複製到剪貼板")
    })
  }

  // 清空對話
  const clearConversation = () => {
    conversationHistory.value = []
    conversationContext.value = []
    messageIdCounter.value = 1
    conversationRounds.value = 0
    lastUserMessage.value = null
  }

  // 客服更換
  const onStaffChange = (staffCode) => {
    selectedStaff.value = staffCode
    console.log(`已切換到 ${staffCode} 助手`)
  }

  // 切換自動播放
  const toggleAutoPlay = () => {
    // 這個狀態在音頻播放器中管理
    console.log("切換自動播放")
  }

  // 切換調試面板
  const toggleDebug = () => {
    showDebug.value = !showDebug.value
    console.log(showDebug.value ? "已顯示調試面板" : "已隱藏調試面板")
  }

  // 導出對話
  const exportConversation = () => {
    exportModal.value = true
  }

  // 錯誤處理
  const showError = (message) => {
    console.error("❌ 系統錯誤:", message)
    errorMessage.value = message
    errorModal.value = true
  }

  const retryLastAction = () => {
    if (lastUserMessage.value) {
      // 這裡需要調用示例問題處理
      console.log("重試上次操作:", lastUserMessage.value)
    }
    errorModal.value = false
  }

  const resetConversation = () => {
    clearConversation()
    errorModal.value = false
  }

  const closeErrorModal = () => {
    errorModal.value = false
  }

  return {
    // 狀態
    conversationHistory,
    conversationContext,
    messageIdCounter,
    conversationRounds,
    lastUserMessage,
    selectedStaff,
    responseStyle,
    conversationMode,
    showDebug,
    errorModal,
    errorMessage,
    exportModal,
    regeneratingId,
    sampleQuestions,
    
    // 計算屬性
    totalMessages,
    
    // 方法
    addMessage,
    buildConversationContext,
    copyMessage,
    clearConversation,
    onStaffChange,
    toggleAutoPlay,
    toggleDebug,
    exportConversation,
    showError,
    retryLastAction,
    resetConversation,
    closeErrorModal
  }
}