/**
 * AI 廣播劇增強版播放器
 * Phase 1 核心功能實作
 */

class EnhancedAudiobookPlayer {
  constructor() {
    this.bookId = null;
    this.currentChapter = null;
    this.chapters = [];
    this.audio = null;
    this.isPlaying = false;
    this.playbackSpeed = 0.8;
    this.volume = 1.0;
    this.progressSaveInterval = null;

    // 載入使用者偏好設定
    this.loadPreferences();
  }

  // ==================== 初始化 ====================

  async init(bookId) {
    this.bookId = bookId;
    await this.loadBookInfo();
    await this.loadProgress();
    this.setupEventListeners();
    this.startProgressSaving();
  }

  async loadBookInfo() {
    try {
      const response = await fetch(`/api/audiobook/book/${this.bookId}/info`);
      const result = await response.json();

      if (result.success) {
        this.chapters = result.book.chapters;
        console.log("✅ 書籍資訊載入成功", this.chapters.length, "章");
      }
    } catch (error) {
      console.error("❌ 載入書籍資訊失敗:", error);
    }
  }

  async loadProgress() {
    try {
      const response = await fetch(`/api/audiobook/progress/${this.bookId}`);
      const result = await response.json();

      if (result.success && result.progress) {
        const progress = result.progress;
        console.log("✅ 進度載入成功:", progress);

        // 恢復上次播放位置
        if (progress.chapter_id && progress.position) {
          this.resumeFromProgress(progress);
        }
      }
    } catch (error) {
      console.error("❌ 載入進度失敗:", error);
    }
  }

  resumeFromProgress(progress) {
    const chapterIndex = this.chapters.findIndex(
      (ch) => ch.id === progress.chapter_id
    );

    if (chapterIndex >= 0) {
      const chapter = this.chapters[chapterIndex];
      const timeStr = this.formatTime(progress.position);

      const message = `上次播放到「${chapter.title}」${timeStr}，是否繼續？`;

      if (confirm(message)) {
        this.playChapter(chapter.id, "mandarin", chapter.title, null);
        // 等待音頻載入後跳轉
        setTimeout(() => {
          if (this.audio) {
            this.audio.currentTime = progress.position;
          }
        }, 1000);
      }
    }
  }

  // ==================== 播放控制 ====================

  async playChapter(chapterId, dialect, title, button) {
    this.currentChapter = {
      id: chapterId,
      title: title,
      dialect: dialect,
    };

    console.log("▶️ 播放章節:", title);

    // 更新 UI
    this.updateNowPlaying(title, dialect);

    // 載入音頻
    const audioUrl = `/api/audiobook/book/${this.bookId}/chapter/${chapterId}/audio/${dialect}`;

    if (!this.audio) {
      this.audio = document.getElementById("audio");
      if (this.audio) {
        this.setupAudioEvents();
      }
    }

    if (this.audio) {
      this.audio.src = audioUrl;
      this.audio.playbackRate = this.playbackSpeed;
      this.audio.volume = this.volume;

      try {
        await this.audio.play();
        this.isPlaying = true;
        console.log("✅ 開始播放");
      } catch (error) {
        console.error("❌ 播放失敗:", error);
      }
    }
  }

  // ==================== 進度控制 ====================

  updateProgress() {
    if (!this.audio) return;

    const percent = (this.audio.currentTime / this.audio.duration) * 100;

    // 更新進度條（如果存在）
    const progressFill = document.querySelector(".progress-fill");
    if (progressFill) {
      progressFill.style.width = `${percent}%`;
    }

    // 更新時間顯示
    const currentTimeEl = document.getElementById("currentTime");
    if (currentTimeEl) {
      currentTimeEl.textContent = this.formatTime(this.audio.currentTime);
    }
  }

  // ==================== 速度/音量控制 ====================

  setPlaybackSpeed(speed) {
    this.playbackSpeed = speed;
    if (this.audio) {
      this.audio.playbackRate = speed;
    }

    console.log("⚡ 播放速度:", speed);

    // 儲存設定
    this.savePreference("playbackSpeed", speed);
  }

  setVolume(volume) {
    this.volume = volume;
    if (this.audio) {
      this.audio.volume = volume;
    }

    console.log("🔊 音量:", volume);

    // 儲存設定
    this.savePreference("volume", volume);
  }

  // ==================== 進度儲存 ====================

  startProgressSaving() {
    // 每 5 秒自動儲存進度
    this.progressSaveInterval = setInterval(() => {
      this.saveProgress();
    }, 5000);

    // 頁面關閉時儲存
    window.addEventListener("beforeunload", () => {
      this.saveProgress();
    });

    console.log("✅ 自動儲存進度已啟動");
  }

  async saveProgress() {
    if (!this.audio || !this.currentChapter) return;
    if (isNaN(this.audio.currentTime) || isNaN(this.audio.duration)) return;

    try {
      await fetch("/api/audiobook/progress/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          book_id: this.bookId,
          chapter_id: this.currentChapter.id,
          position: this.audio.currentTime,
          total_duration: this.audio.duration,
        }),
      });

      console.log("💾 進度已儲存:", this.formatTime(this.audio.currentTime));
    } catch (error) {
      console.error("❌ 儲存進度失敗:", error);
    }
  }

  // ==================== 書籤功能 ====================

  async addBookmark(note = "") {
    if (!this.audio || !this.currentChapter) {
      alert("請先播放音頻");
      return;
    }

    try {
      const response = await fetch("/api/audiobook/bookmark/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          book_id: this.bookId,
          chapter_id: this.currentChapter.id,
          chapter_title: this.currentChapter.title,
          position: this.audio.currentTime,
          note: note,
        }),
      });

      const result = await response.json();

      if (result.success) {
        alert("✅ 書籤已添加");
        console.log("✅ 書籤已添加:", this.formatTime(this.audio.currentTime));
      }
    } catch (error) {
      console.error("❌ 添加書籤失敗:", error);
      alert("添加書籤失敗");
    }
  }

  // ==================== 偏好設定 ====================

  async loadPreferences() {
    try {
      const response = await fetch("/api/audiobook/preferences");
      const result = await response.json();

      if (result.success) {
        const prefs = result.preferences;
        this.playbackSpeed = prefs.playbackSpeed || 0.8;
        this.volume = prefs.volume || 1.0;

        console.log("✅ 偏好設定載入:", prefs);
      }
    } catch (error) {
      console.error("❌ 載入設定失敗:", error);
    }
  }

  async savePreference(key, value) {
    try {
      await fetch("/api/audiobook/preferences/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ [key]: value }),
      });
    } catch (error) {
      console.error("❌ 儲存設定失敗:", error);
    }
  }

  // ==================== 輔助函數 ====================

  formatTime(seconds) {
    if (isNaN(seconds)) return "00:00";

    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  }

  setupAudioEvents() {
    this.audio.addEventListener("timeupdate", () => this.updateProgress());
    this.audio.addEventListener("loadedmetadata", () => {
      const durationEl = document.getElementById("duration");
      if (durationEl) {
        durationEl.textContent = this.formatTime(this.audio.duration);
      }
      console.log(
        "✅ 音頻載入完成，時長:",
        this.formatTime(this.audio.duration)
      );
    });
    this.audio.addEventListener("ended", () => {
      console.log("✅ 播放結束");
      this.isPlaying = false;
    });

    console.log("✅ 音頻事件已設定");
  }

  setupEventListeners() {
    // 這裡可以添加更多事件監聽器
    console.log("✅ 事件監聽器已設定");
  }

  updateNowPlaying(title, dialect) {
    const titleEl = document.getElementById("playerTitle");
    const subtitleEl = document.getElementById("playerSubtitle");

    if (titleEl) titleEl.textContent = title;
    if (subtitleEl) {
      const langName = dialect === "mandarin" ? "國語" : "閩南語";
      subtitleEl.textContent = `正在播放：${langName}`;
    }
  }
}

// 全域變數
let player;

// 初始化函數（供外部調用）
function initEnhancedPlayer(bookId) {
  player = new EnhancedAudiobookPlayer();
  player.init(bookId);
  console.log("🎵 增強版播放器已初始化");
  return player;
}

// 如果在書籍詳情頁面，自動初始化
if (window.location.pathname.includes("/audiobook/book/")) {
  document.addEventListener("DOMContentLoaded", () => {
    const pathParts = window.location.pathname.split("/");
    const bookId = pathParts[pathParts.length - 2];

    if (bookId) {
      initEnhancedPlayer(bookId);
    }
  });
}
