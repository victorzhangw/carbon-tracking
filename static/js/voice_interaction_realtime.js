/**
 * 即時語音互動前端邏輯 - Phase 1 增強版
 * 支援 Roy（閩南語）和 Nofish（國語）兩個版本
 * 新增功能：語音波形、對話歷史、快速回應、音量控制
 */

let sessionId = null;
let socket = null;
let mediaRecorder = null;
let audioContext = null;
let audioChunks = [];
let isRecording = false;
let waveform = null;
let currentConversation = [];
let playbackSpeed = 0.9;
let playbackVolume = 0.8;

// DOM 元素
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const conversationArea = document.getElementById("conversationArea");
const recordingIndicator = document.getElementById("recordingIndicator");
const historyList = document.getElementById("historyList");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");
const volumeSlider = document.getElementById("volumeSlider");
const volumeValue = document.getElementById("volumeValue");
const speedSlider = document.getElementById("speedSlider");
const speedValue = document.getElementById("speedValue");
const quickButtons = document.querySelectorAll(".quick-btn");
const sessionInfo = document.getElementById("sessionInfo"); // 可選元素

// 初始化
document.addEventListener("DOMContentLoaded", () => {
  startBtn.addEventListener("click", startSession);
  stopBtn.addEventListener("click", stopSession);
  clearHistoryBtn.addEventListener("click", clearHistory);

  // 快速回應按鈕
  quickButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const text = btn.getAttribute("data-text");
      sendQuickMessage(text);
    });
  });

  // 音量控制
  volumeSlider.addEventListener("input", (e) => {
    playbackVolume = e.target.value / 100;
    volumeValue.textContent = `${e.target.value}%`;
    saveSettings();
  });

  // 語速控制
  speedSlider.addEventListener("input", (e) => {
    playbackSpeed = e.target.value / 100;
    speedValue.textContent = `${playbackSpeed.toFixed(1)}x`;
    saveSettings();
  });

  // 初始化波形視覺化
  waveform = new VoiceWaveform("waveformCanvas");
  waveform.drawIdle();

  // 載入設定和歷史
  loadSettings();
  loadHistory();
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
    if (sessionInfo) {
      sessionInfo.textContent = `會話 ID: ${sessionId.substring(0, 8)}...`;
    }

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
    if (sessionInfo) {
      sessionInfo.textContent = "";
    }
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

    // 初始化波形視覺化
    if (waveform) {
      waveform.init(audioContext, stream);
    }

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

  // 停止波形視覺化
  if (waveform) {
    waveform.stop();
  }

  if (audioContext) {
    audioContext.close();
    audioContext = null;
  }

  // 儲存對話
  saveConversation();

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

async function playAudio(base64Audio) {
  try {
    console.log("🎵 收到音頻數據，長度:", base64Audio.length);

    // 解碼 Base64
    const binaryString = atob(base64Audio);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    console.log("🎵 解碼完成，字節數:", bytes.length);

    // 將 PCM16 轉換為 Float32
    const pcm16 = new Int16Array(bytes.buffer);
    const float32 = new Float32Array(pcm16.length);
    for (let i = 0; i < pcm16.length; i++) {
      float32[i] = pcm16[i] / 32768.0;
    }
    console.log("🎵 PCM 轉換完成，樣本數:", float32.length);

    // 創建 AudioContext（如果還沒有）
    if (!audioContext || audioContext.state === "closed") {
      audioContext = new (window.AudioContext || window.webkitAudioContext)({
        sampleRate: 24000,
      });
      console.log("🎵 創建新的 AudioContext");
    }

    // 恢復 AudioContext（處理瀏覽器自動播放政策）
    if (audioContext.state === "suspended") {
      console.log("🎵 AudioContext 處於 suspended 狀態，嘗試恢復...");
      await audioContext.resume();
      console.log("🎵 AudioContext 已恢復，狀態:", audioContext.state);
    }

    // 創建 AudioBuffer
    const audioBuffer = audioContext.createBuffer(1, float32.length, 24000);
    audioBuffer.getChannelData(0).set(float32);
    console.log("🎵 AudioBuffer 創建完成，時長:", audioBuffer.duration, "秒");

    // 加入播放隊列
    audioQueue.push(audioBuffer);
    console.log("🎵 加入播放隊列，當前隊列長度:", audioQueue.length);

    // 如果沒在播放，開始播放
    if (!isPlaying) {
      console.log("🎵 開始播放隊列");
      playNextInQueue();
    }
  } catch (error) {
    console.error("❌ 播放音頻失敗:", error);
    console.error("錯誤堆疊:", error.stack);
  }
}

/**
 * 播放隊列中的下一個音頻
 */
function playNextInQueue() {
  if (audioQueue.length === 0) {
    console.log("🎵 播放隊列已空，停止播放");
    isPlaying = false;
    return;
  }

  isPlaying = true;
  const audioBuffer = audioQueue.shift();
  console.log(
    "🎵 播放音頻，時長:",
    audioBuffer.duration,
    "秒，剩餘隊列:",
    audioQueue.length
  );

  const source = audioContext.createBufferSource();
  source.buffer = audioBuffer;
  // 設定播放速度和音量
  source.playbackRate.value = playbackSpeed;
  console.log("🎵 播放速度:", playbackSpeed);

  // 創建音量控制節點
  const gainNode = audioContext.createGain();
  gainNode.gain.value = playbackVolume;
  console.log("🎵 音量:", playbackVolume);

  source.connect(gainNode);
  gainNode.connect(audioContext.destination);

  source.onended = () => {
    console.log("🎵 音頻播放完成");
    playNextInQueue();
  };

  console.log("🎵 開始播放...");
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
  currentConversation = [];
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

  const time = new Date().toLocaleTimeString("zh-TW", {
    hour: "2-digit",
    minute: "2-digit",
  });

  const messageDiv = document.createElement("div");
  messageDiv.className = "message user";
  messageDiv.innerHTML = `
    <div class="message-bubble">
      <div class="message-header">
        <div class="message-avatar">
          <span class="material-icons" style="font-size: 16px">person</span>
        </div>
        <span>您</span>
      </div>
      <div class="message-text">${text}</div>
      <div class="message-time">${time}</div>
    </div>
  `;
  conversationArea.appendChild(messageDiv);
  scrollToBottom();

  // 記錄到當前對話
  currentConversation.push({
    role: "user",
    text: text,
    timestamp: new Date().toISOString(),
  });
}

/**
 * 添加助理訊息
 */
function addAssistantMessage(text, sentiment) {
  const time = new Date().toLocaleTimeString("zh-TW", {
    hour: "2-digit",
    minute: "2-digit",
  });

  const sentimentClass =
    sentiment === "positive"
      ? "sentiment-positive"
      : sentiment === "negative"
      ? "sentiment-negative"
      : "sentiment-neutral";

  const sentimentText =
    sentiment === "positive"
      ? "😊 正面"
      : sentiment === "negative"
      ? "😔 負面"
      : "😐 中性";

  const messageDiv = document.createElement("div");
  messageDiv.className = "message assistant";
  messageDiv.innerHTML = `
    <div class="message-bubble">
      <div class="message-header">
        <div class="message-avatar">
          <span class="material-icons" style="font-size: 16px">smart_toy</span>
        </div>
        <span>AI 助理</span>
        <span class="sentiment-badge ${sentimentClass}">${sentimentText}</span>
      </div>
      <div class="message-text">${text}</div>
      <div class="message-time">${time}</div>
    </div>
  `;
  conversationArea.appendChild(messageDiv);
  scrollToBottom();

  // 記錄到當前對話
  currentConversation.push({
    role: "assistant",
    text: text,
    sentiment: sentiment,
    timestamp: new Date().toISOString(),
  });
}

/**
 * 滾動到底部
 */
function scrollToBottom() {
  conversationArea.scrollTop = conversationArea.scrollHeight;
}

/**
 * 快速發送訊息
 */
function sendQuickMessage(text) {
  if (!socket || !sessionId) {
    alert("請先開始對話");
    return;
  }

  // 顯示用戶訊息
  addUserMessage(text);

  // 發送到後端（模擬語音輸入）
  socket.emit("quick_message", {
    session_id: sessionId,
    text: text,
  });
}

/**
 * 對話歷史管理
 */
function saveConversation() {
  if (currentConversation.length === 0) return;

  const conversation = {
    id: Date.now(),
    title: currentConversation[0]?.text?.substring(0, 30) || "新對話",
    messages: currentConversation,
    timestamp: new Date().toISOString(),
  };

  let history = JSON.parse(localStorage.getItem("voiceHistory") || "[]");
  history.unshift(conversation);

  // 最多保留 50 條
  if (history.length > 50) {
    history = history.slice(0, 50);
  }

  localStorage.setItem("voiceHistory", JSON.stringify(history));
  loadHistory();
}

function loadHistory() {
  const history = JSON.parse(localStorage.getItem("voiceHistory") || "[]");

  if (history.length === 0) {
    historyList.innerHTML = '<div class="history-empty">尚無對話記錄</div>';
    return;
  }

  historyList.innerHTML = history
    .map(
      (conv) => `
    <div class="history-item" onclick="viewConversation(${conv.id})">
      <div class="history-item-title">${conv.title}</div>
      <div class="history-item-time">${formatTime(conv.timestamp)}</div>
    </div>
  `
    )
    .join("");
}

function viewConversation(id) {
  const history = JSON.parse(localStorage.getItem("voiceHistory") || "[]");
  const conversation = history.find((c) => c.id === id);

  if (!conversation) return;

  // 清空當前對話
  clearConversation();

  // 顯示歷史對話
  conversation.messages.forEach((msg) => {
    if (msg.role === "user") {
      addUserMessage(msg.text);
    } else {
      addAssistantMessage(msg.text, msg.sentiment || "neutral");
    }
  });
}

function clearHistory() {
  if (!confirm("確定要清除所有對話記錄嗎？")) return;

  localStorage.removeItem("voiceHistory");
  loadHistory();
}

function formatTime(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;

  if (diff < 60000) return "剛剛";
  if (diff < 3600000) return `${Math.floor(diff / 60000)} 分鐘前`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小時前`;
  return date.toLocaleDateString();
}

/**
 * 設定管理
 */
function saveSettings() {
  const settings = {
    volume: playbackVolume,
    speed: playbackSpeed,
  };
  localStorage.setItem("voiceSettings", JSON.stringify(settings));
}

function loadSettings() {
  const settings = JSON.parse(localStorage.getItem("voiceSettings") || "{}");

  if (settings.volume !== undefined) {
    playbackVolume = settings.volume;
    volumeSlider.value = Math.round(playbackVolume * 100);
    volumeValue.textContent = `${Math.round(playbackVolume * 100)}%`;
  }

  if (settings.speed !== undefined) {
    playbackSpeed = settings.speed;
    speedSlider.value = Math.round(playbackSpeed * 100);
    speedValue.textContent = `${playbackSpeed.toFixed(1)}x`;
  }
}
