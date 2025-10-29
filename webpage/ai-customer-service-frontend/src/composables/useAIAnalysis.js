// useAIAnalysis.js - AI分析功能組合式API
import axios from 'axios'

export function useAIAnalysis() {
  // 執行語音識別
  const performSpeechRecognition = async (audioBlob) => {
    console.log("🎯 開始語音識別...")
    console.log("音頻Blob信息:", {
      size: audioBlob?.size,
      type: audioBlob?.type,
    })

    const formData = new FormData()
    formData.append("file", audioBlob, "recording.wav")

    console.log("📤 發送語音識別請求...")
    const response = await axios.post("/process_audio", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      timeout: 60000, // 60秒超时
    })

    console.log("📥 語音識別響應:", response.data)

    if (response.data.transcript) {
      console.log("✅ 語音識別成功:", response.data.transcript)
      return response.data.transcript
    } else {
      console.error("❌ 語音識別失敗，響應:", response.data)
      throw new Error("語音識別失敗")
    }
  }

  // AI分析 (增強版 - 支持上下文)
  const performAIAnalysis = async (transcript, options = {}) => {
    const {
      selectedStaff = "admin",
      responseStyle = "friendly",
      conversationMode = "continuous",
      conversationContext = [],
      conversationRounds = 0
    } = options

    const response = await axios.post(
      "/voice_clone/generate_response_voice",
      {
        user_input: transcript,
        staff_code: selectedStaff,
        response_style: responseStyle,
        conversation_mode: conversationMode,
        conversation_context: conversationContext,
        conversation_round: conversationRounds,
      },
      {
        timeout: 120000,
      }
    )

    if (response.data.status === "success") {
      return {
        text: response.data.ai_analysis.response_text,
        sentiment: response.data.ai_analysis.sentiment,
        confidence: response.data.ai_analysis.confidence || 0.95,
        audioUrl: response.data.voice_output.audio_url,
      }
    } else {
      throw new Error(response.data.message || "AI分析失敗")
    }
  }

  // 重新生成回應
  const regenerateResponse = async (message, lastUserMessage, options = {}) => {
    if (message.type !== "ai" || !lastUserMessage) {
      throw new Error("無法重新生成回應")
    }

    const aiResponse = await performAIAnalysis(lastUserMessage, options)
    return {
      ...message,
      text: aiResponse.text,
      audioUrl: aiResponse.audioUrl,
      sentiment: aiResponse.sentiment,
      confidence: aiResponse.confidence,
      time: new Date().toLocaleTimeString(),
    }
  }

  return {
    // 方法
    performSpeechRecognition,
    performAIAnalysis,
    regenerateResponse
  }
}