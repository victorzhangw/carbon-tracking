/**
 * 即時語音互動前端邏輯
 * 支援 Roy（閩南語）和 Nofish（國語）兩個版本
 */

let sessionId = null;
let socket = null;
let mediaRecorder = null;
let audioContext = null;
let audioChunks = [];
let isRecording = false;

// DOM 元素
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const sessionInfo = document.getElementById("sessionInfo");
const conversationArea = document.getElementById("conversationArea");
const recordingIndicator = document.getElementById("recordingIndicator");

// 初始化
document.addEventListener("DOMContentLoaded", () => {
  startBtn.addEventListener("click", startSession);
  stopBtn.addEventListener("click", stopSession);
});

/**
 * 啟動會話
 */
async function startSession() {
  try {
    startBtn.disabled = true;
    updateStatus("connecting", "連接中...");

    // 1. 啟動後端會話
    const response = await fetch(`${API_BASE}/session/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        voice: VOICE,
        enable_vad: true,
      }),
    });

    const data = await response.json();

    if (data.status !== "success") {
      throw new Error(data.message || "啟動會話失敗");
    }

    sessionId = data.session_id;
    sessionInfo.textContent = `會話 ID: ${sessionId.substring(0, 8)}...`;

    // 2. 建立 SocketIO 連接
    socket = io("/voice_interaction_realtime", {
      transports: ["websocket", "polling"],
    });

    setupSocketEvents();

    // 3. 等待連接建立
    await new Promise((resolve) => {
      socket.on("connected", () => {
        console.log("✅ SocketIO 已連接");
        resolve();
      });
    });

    // 4. 加入會話
    socket.emit("join_session", { session_id: sessionId });

    await new Promise((resolve) => {
      socket.on("joined", () => {
        console.log("✅ 已加入會話");
        resolve();
      });
    });

    // 5. 啟動錄音
    await startRecording();

    updateStatus("connected", "已連接");
    stopBtn.disabled = false;
    clearConversation();
    addSystemMessage("✅ 會話已啟動，請開始說話");
  } catch (error) {
    console.error("❌ 啟動會話失敗:", error);
    alert(`啟動失敗: ${error.message}`);
    updateStatus("disconnected", "未連接");
    startBtn.disabled = false;
  }
}

/**
 * 結束會話
 */
async function stopSession() {
  try {
    stopBtn.disabled = true;

    // 1. 停止錄音
    stopRecording();

    // 2. 離開會話
    if (socket) {
      socket.emit("leave_session", { session_id: sessionId });
      socket.disconnect();
      socket = null;
    }

    // 3. 結束後端會話
    if (sessionId) {
      await fetch(`${API_BASE}/session/stop`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
        }),
      });
    }

    sessionId = null;
    sessionInfo.textContent = "";
    updateStatus("disconnected", "未連接");
    startBtn.disabled = false;
    addSystemMessage("✅ 會話已結束");
  } catch (error) {
    console.error("❌ 結束會話失敗:", error);
    updateStatus("disconnected", "未連接");
    startBtn.disabled = false;
  }
}

/**
 * 設置 Socket 事件
 */
function setupSocketEvents() {
  // 辨識中的文字
  socket.on("transcript_partial", (data) => {
    console.log("📝 辨識中:", data);
    updatePartialTranscript(data.text, data.stash);
  });

  // 辨識完成
  socket.on("transcript_final", (data) => {
    console.log("✅ 辨識完成:", data.text);
    addUserMessage(data.text);
  });

  // LLM 回應
  socket.on("llm_response", (data) => {
    console.log("🤖 LLM 回應:", data.text);
    addAssistantMessage(data.text, data.sentiment);
  });

  // 音頻輸出
  socket.on("audio_output", (data) => {
    if (data.audio) {
      playAudio(data.audio);
    }
    if (data.is_final) {
      console.log("✅ 音頻播放完成");
    }
  });

  // 錯誤
  socket.on("error", (data) => {
    console.error("❌ 錯誤:", data.message);
    addSystemMessage(`❌ 錯誤: ${data.message}`);
  });
}

/**
 * 啟動錄音
 */
async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        channelCount: 1,
        sampleRate: 16000,
      },
    });

    // 使用 AudioContext 處理音頻
    audioContext = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate: 16000,
    });

    const source = audioContext.createMediaStreamSource(stream);
    const processor = audioContext.createScriptProcessor(4096, 1, 1);

    processor.onaudioprocess = (e) => {
      if (!isRecording) return;

      const inputData = e.inputBuffer.getChannelData(0);
      const pcmData = convertToPCM16(inputData);
      const base64Audio = arrayBufferToBase64(pcmData);

      // 發送音頻到後端
      if (socket && sessionId) {
        socket.emit("audio_input", {
          session_id: sessionId,
          audio: base64Audio,
        });
      }
    };

    source.connect(processor);
    processor.connect(audioContext.destination);

    isRecording = true;
    recordingIndicator.classList.add("active");
    console.log("🎤 錄音已啟動");
  } catch (error) {
    console.error("❌ 啟動錄音失敗:", error);
    throw new Error("無法訪問麥克風");
  }
}

/**
 * 停止錄音
 */
function stopRecording() {
  isRecording = false;
  recordingIndicator.classList.remove("active");

  if (audioContext) {
    audioContext.close();
    audioContext = null;
  }

  console.log("🎤 錄音已停止");
}

/**
 * 轉換為 PCM16
 */
function convertToPCM16(float32Array) {
  const buffer = new ArrayBuffer(float32Array.length * 2);
  const view = new DataView(buffer);

  for (let i = 0; i < float32Array.length; i++) {
    let s = Math.max(-1, Math.min(1, float32Array[i]));
    view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }

  return buffer;
}

/**
 * ArrayBuffer 轉 Base64
 */
function arrayBufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

/**
 * 播放音頻
 * TTS 返回的是 Base64 編碼的 PCM16 數據（24kHz, 單聲道）
 */
let audioQueue = [];
let isPlaying = false;

function playAudio(base64Audio) {
  try {
    // 解碼 Base64
    const binaryString = atob(base64Audio);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    // 將 PCM16 轉換為 Float32
    const pcm16 = new Int16Array(bytes.buffer);
    const float32 = new Float32Array(pcm16.length);
    for (let i = 0; i < pcm16.length; i++) {
      float32[i] = pcm16[i] / 32768.0;
    }

    // 創建 AudioContext（如果還沒有）
    if (!audioContext || audioContext.state === "closed") {
      audioContext = new (window.AudioContext || window.webkitAudioContext)({
        sampleRate: 24000,
      });
    }

    // 創建 AudioBuffer
    const audioBuffer = audioContext.createBuffer(1, float32.length, 24000);
    audioBuffer.getChannelData(0).set(float32);

    // 加入播放隊列
    audioQueue.push(audioBuffer);

    // 如果沒在播放，開始播放
    if (!isPlaying) {
      playNextInQueue();
    }
  } catch (error) {
    console.error("❌ 播放音頻失敗:", error);
  }
}

/**
 * 播放隊列中的下一個音頻
 */
function playNextInQueue() {
  if (audioQueue.length === 0) {
    isPlaying = false;
    return;
  }

  isPlaying = true;
  const audioBuffer = audioQueue.shift();

  const source = audioContext.createBufferSource();
  source.buffer = audioBuffer;
  source.connect(audioContext.destination);

  source.onended = () => {
    playNextInQueue();
  };

  source.start(0);
}

/**
 * 更新狀態
 */
function updateStatus(status, text) {
  statusText.textContent = text;

  if (status === "connected") {
    statusDot.classList.add("connected");
  } else {
    statusDot.classList.remove("connected");
  }
}

/**
 * 清空對話區
 */
function clearConversation() {
  conversationArea.innerHTML = "";
}

/**
 * 添加系統訊息
 */
function addSystemMessage(text) {
  const messageDiv = document.createElement("div");
  messageDiv.style.textAlign = "center";
  messageDiv.style.color = "#999";
  messageDiv.style.fontSize = "14px";
  messageDiv.style.margin = "10px 0";
  messageDiv.textContent = text;
  conversationArea.appendChild(messageDiv);
  scrollToBottom();
}

/**
 * 更新即時辨識文字
 */
let partialMessageDiv = null;

function updatePartialTranscript(text, stash) {
  if (!partialMessageDiv) {
    partialMessageDiv = document.createElement("div");
    partialMessageDiv.className = "message partial";
    conversationArea.appendChild(partialMessageDiv);
  }

  const fullText = text + (stash ? ` ${stash}` : "");
  partialMessageDiv.innerHTML = `
        <div class="label">辨識中...</div>
        <div class="text">${fullText}</div>
    `;
  scrollToBottom();
}

/**
 * 添加用戶訊息
 */
function addUserMessage(text) {
  // 移除即時辨識訊息
  if (partialMessageDiv) {
    partialMessageDiv.remove();
    partialMessageDiv = null;
  }

  const messageDiv = document.createElement("div");
  messageDiv.className = "message user";
  messageDiv.innerHTML = `
        <div class="label">您</div>
        <div class="text">${text}</div>
    `;
  conversationArea.appendChild(messageDiv);
  scrollToBottom();
}

/**
 * 添加助理訊息
 */
function addAssistantMessage(text, sentiment) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message assistant";
  messageDiv.innerHTML = `
        <div class="label">AI 助理 (${sentiment})</div>
        <div class="text">${text}</div>
    `;
  conversationArea.appendChild(messageDiv);
  scrollToBottom();
}

/**
 * 滾動到底部
 */
function scrollToBottom() {
  conversationArea.scrollTop = conversationArea.scrollHeight;
}
