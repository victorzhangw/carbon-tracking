/**
 * 評分系統管理器
 * 負責會話管理、對話記錄、評分報告顯示
 */

class ScoreManager {
  constructor() {
    this.sessionId = null;
    this.sessionStartTime = null;
    this.conversationHistory = [];
    this.endSessionBtn = null;
    this.scoreModal = null;

    this.init();
  }

  /**
   * 初始化
   */
  init() {
    console.log("📊 初始化評分系統...");

    // 初始化會話
    this.initSession();

    // 綁定 DOM 元素
    this.endSessionBtn = document.getElementById("endSession");
    this.scoreModal = document.getElementById("scoreModal");

    // 綁定事件
    this.bindEvents();

    console.log("✅ 評分系統初始化完成");
  }

  /**
   * 初始化會話
   */
  initSession() {
    this.sessionId = this.generateUUID();
    this.sessionStartTime = new Date();
    this.conversationHistory = [];

    console.log("✅ 會話已初始化:", this.sessionId);

    // 禁用停止對話按鈕
    if (this.endSessionBtn) {
      this.endSessionBtn.disabled = true;
    }
  }

  /**
   * 生成 UUID
   */
  generateUUID() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
      /[xy]/g,
      function (c) {
        const r = (Math.random() * 16) | 0;
        const v = c === "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      }
    );
  }

  /**
   * 綁定事件
   */
  bindEvents() {
    // 停止對話按鈕
    if (this.endSessionBtn) {
      this.endSessionBtn.addEventListener("click", () =>
        this.handleEndSession()
      );
    }

    // 關閉彈窗按鈕
    const closeBtn = document.querySelector(".score-modal-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => this.closeScoreModal());
    }

    // 點擊背景關閉
    if (this.scoreModal) {
      this.scoreModal.addEventListener("click", (e) => {
        if (e.target.id === "scoreModal") {
          this.closeScoreModal();
        }
      });
    }
  }

  /**
   * 記錄對話
   */
  recordConversation(speaker, text, sentiment = null, sentimentScore = null) {
    this.conversationHistory.push({
      speaker: speaker,
      text: text,
      sentiment: sentiment,
      sentiment_score: sentimentScore,
      word_count: text.length,
      timestamp: new Date().toISOString(),
    });

    // 啟用停止對話按鈕（至少1次對話後）
    if (this.conversationHistory.length >= 2 && this.endSessionBtn) {
      this.endSessionBtn.disabled = false;
    }

    console.log(
      `📝 記錄對話 #${
        this.conversationHistory.length
      }: ${speaker} - ${text.substring(0, 20)}...`
    );
  }

  /**
   * 處理停止對話
   */
  async handleEndSession() {
    if (this.conversationHistory.length < 2) {
      alert("至少需要一輪對話才能生成評分報告");
      return;
    }

    const confirmed = confirm("確定要結束對話嗎？\n系統將為您生成評分報告。");
    if (!confirmed) return;

    await this.endSessionAndShowReport();
  }

  /**
   * 結束對話並顯示報告
   */
  async endSessionAndShowReport() {
    try {
      // 更新狀態（假設有 updateStatus 函數）
      if (typeof updateStatus === "function") {
        updateStatus("📊 正在生成評分報告...", true);
      }

      // 計算持續時間
      const duration = Math.floor((new Date() - this.sessionStartTime) / 1000);

      // 發送請求
      const response = await fetch("/api/end-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: this.sessionId,
          user_id: "default",
          conversation_history: this.conversationHistory,
          duration: duration,
        }),
      });

      const result = await response.json();

      if (result.status === "success") {
        // 顯示評分報告
        this.showScoreReport(result);

        if (typeof updateStatus === "function") {
          updateStatus("✅ 評分報告已生成", false);
        }
      } else {
        throw new Error(result.message || "生成評分報告失敗");
      }
    } catch (error) {
      console.error("生成評分報告失敗:", error);
      alert("生成評分報告失敗，請稍後再試");

      if (typeof updateStatus === "function") {
        updateStatus("❌ 生成失敗", false);
      }
    }
  }

  /**
   * 顯示評分報告
   */
  showScoreReport(data) {
    console.log("📊 顯示評分報告:", data);

    // 填充評分數據
    this.setElementText("emotionScoreValue", data.scores.emotion);
    this.setElementText("voiceScoreValue", data.scores.voice);
    this.setElementText("contentScoreValue", data.scores.content);
    this.setElementText("overallScoreValue", data.scores.overall);

    // 填充等級和星級
    this.setElementText("overallGrade", `${data.grade} - ${data.title}`);
    this.setElementText("overallStars", "⭐".repeat(data.stars));

    // 填充進度條
    this.setElementWidth("emotionScoreFill", data.scores.emotion);
    this.setElementWidth("voiceScoreFill", data.scores.voice);
    this.setElementWidth("contentScoreFill", data.scores.content);

    // 填充建議
    this.renderSuggestions(data.suggestions);

    // 填充統計資訊
    this.setElementText(
      "statConversations",
      data.statistics.conversation_count
    );
    this.setElementText("statWords", data.statistics.total_words);
    this.setElementText(
      "statDuration",
      this.formatDuration(data.statistics.duration)
    );

    // 繪製雷達圖
    this.drawRadarChart(data.scores);

    // 顯示彈窗
    if (this.scoreModal) {
      this.scoreModal.style.display = "flex";
    }
  }

  /**
   * 渲染建議列表
   */
  renderSuggestions(suggestions) {
    const suggestionsList = document.getElementById("suggestionsList");
    if (!suggestionsList) return;

    suggestionsList.innerHTML = "";

    if (suggestions && suggestions.length > 0) {
      suggestions.forEach((suggestion) => {
        const item = document.createElement("div");
        item.className = `suggestion-item suggestion-priority-${suggestion.priority}`;
        item.innerHTML = `
          <div class="suggestion-icon">${suggestion.icon}</div>
          <div class="suggestion-content">
            <div class="suggestion-category">${suggestion.category}</div>
            <div class="suggestion-text">${suggestion.text}</div>
          </div>
        `;
        suggestionsList.appendChild(item);
      });
    } else {
      suggestionsList.innerHTML =
        '<p style="color: #666; text-align: center;">太棒了！沒有需要改進的地方 🎉</p>';
    }
  }

  /**
   * 繪製雷達圖
   */
  drawRadarChart(scores) {
    const canvas = document.getElementById("scoreRadarChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    // 設置 canvas 大小
    canvas.width = 400;
    canvas.height = 400;

    const centerX = 200;
    const centerY = 200;
    const radius = 150;

    // 清空畫布
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 數據
    const data = [
      { label: "情緒表達", value: scores.emotion },
      { label: "語音品質", value: scores.voice },
      { label: "文字內容", value: scores.content },
    ];

    const angleStep = (Math.PI * 2) / data.length;

    // 繪製背景網格
    ctx.strokeStyle = "#e0e0e0";
    ctx.lineWidth = 1;

    for (let i = 1; i <= 5; i++) {
      ctx.beginPath();
      const r = (radius / 5) * i;
      for (let j = 0; j <= data.length; j++) {
        const angle = angleStep * j - Math.PI / 2;
        const x = centerX + r * Math.cos(angle);
        const y = centerY + r * Math.sin(angle);
        if (j === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.closePath();
      ctx.stroke();
    }

    // 繪製軸線和標籤
    data.forEach((item, index) => {
      const angle = angleStep * index - Math.PI / 2;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();

      // 繪製標籤
      const labelX = centerX + (radius + 30) * Math.cos(angle);
      const labelY = centerY + (radius + 30) * Math.sin(angle);
      ctx.fillStyle = "#333";
      ctx.font = "14px Arial";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(item.label, labelX, labelY);
    });

    // 繪製數據區域
    ctx.beginPath();
    ctx.fillStyle = "rgba(102, 126, 234, 0.2)";
    ctx.strokeStyle = "rgba(102, 126, 234, 1)";
    ctx.lineWidth = 2;

    data.forEach((item, index) => {
      const angle = angleStep * index - Math.PI / 2;
      const r = (radius / 100) * item.value;
      const x = centerX + r * Math.cos(angle);
      const y = centerY + r * Math.sin(angle);

      if (index === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });

    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // 繪製數據點
    data.forEach((item, index) => {
      const angle = angleStep * index - Math.PI / 2;
      const r = (radius / 100) * item.value;
      const x = centerX + r * Math.cos(angle);
      const y = centerY + r * Math.sin(angle);

      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(102, 126, 234, 1)";
      ctx.fill();
    });
  }

  /**
   * 關閉評分報告
   */
  closeScoreModal() {
    if (this.scoreModal) {
      this.scoreModal.style.display = "none";
    }

    // 重新初始化會話
    this.initSession();
  }

  /**
   * 輔助函數：設置元素文字
   */
  setElementText(id, text) {
    const element = document.getElementById(id);
    if (element) {
      element.textContent = text;
    }
  }

  /**
   * 輔助函數：設置元素寬度
   */
  setElementWidth(id, percentage) {
    const element = document.getElementById(id);
    if (element) {
      element.style.width = percentage + "%";
    }
  }

  /**
   * 格式化持續時間
   */
  formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}分${secs}秒`;
  }
}

// 全局函數：查看歷史（供 HTML 調用）
function viewHistory() {
  alert("歷史記錄功能開發中...");
}

// 全局函數：關閉彈窗（供 HTML 調用）
function closeScoreModal() {
  if (window.scoreManager) {
    window.scoreManager.closeScoreModal();
  }
}
