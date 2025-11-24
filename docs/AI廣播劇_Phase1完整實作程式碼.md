# AI 廣播劇 Phase 1 完整實作程式碼

本文件包含所有需要修改和創建的檔案及其完整程式碼。

---

## 📁 檔案清單

1. ✅ `modules/voice_processing/audiobook_database.py` - 已創建
2. 🆕 `routes/audiobook.py` - 需要擴充
3. 🆕 `static/js/audiobook_player_enhanced.js` - 新建
4. 🆕 `static/css/audiobook_enhanced.css` - 新建
5. 🆕 `templates/audiobook_player_enhanced.html` - 新建

---

## 1. 後端 API 擴充

### 檔案：`routes/audiobook.py`

在現有的 `routes/audiobook.py` 檔案中添加以下 API 端點：

```python
# 在檔案開頭添加導入
from modules.voice_processing.audiobook_database import audiobook_db

# ==================== 進度管理 API ====================

@audiobook_bp.route('/api/audiobook/progress/save', methods=['POST'])
def save_progress():
    """儲存播放進度"""
    try:
        data = request.json
        book_id = data.get('book_id')
        chapter_id = data.get('chapter_id')
        position = data.get('position')
        total_duration = data.get('total_duration')

        if not all([book_id, chapter_id, position is not None]):
            return jsonify({'success': False, 'error': '缺少必要參數'}), 400

        success = audiobook_db.save_progress(book_id, chapter_id, position, total_duration)

        if success:
            return jsonify({'success': True, 'message': '進度已儲存'})
        else:
            return jsonify({'success': False, 'error': '儲存失敗'}), 500

    except Exception as e:
        print(f"❌ 儲存進度錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@audiobook_bp.route('/api/audiobook/progress/<book_id>', methods=['GET'])
def get_progress(book_id):
    """獲取播放進度"""
    try:
        progress = audiobook_db.get_progress(book_id)

        if progress:
            return jsonify({'success': True, 'progress': progress})
        else:
            return jsonify({'success': True, 'progress': None})

    except Exception as e:
        print(f"❌ 獲取進度錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 書籤管理 API ====================

@audiobook_bp.route('/api/audiobook/bookmark/add', methods=['POST'])
def add_bookmark():
    """添加書籤"""
    try:
        data = request.json
        book_id = data.get('book_id')
        chapter_id = data.get('chapter_id')
        chapter_title = data.get('chapter_title')
        position = data.get('position')
        note = data.get('note', '')

        if not all([book_id, chapter_id, chapter_title, position is not None]):
            return jsonify({'success': False, 'error': '缺少必要參數'}), 400

        bookmark_id = audiobook_db.add_bookmark(
            book_id, chapter_id, chapter_title, position, note
        )

        if bookmark_id:
            return jsonify({
                'success': True,
                'bookmark_id': bookmark_id,
                'message': '書籤已添加'
            })
        else:
            return jsonify({'success': False, 'error': '添加失敗'}), 500

    except Exception as e:
        print(f"❌ 添加書籤錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@audiobook_bp.route('/api/audiobook/bookmarks/<book_id>', methods=['GET'])
def get_bookmarks(book_id):
    """獲取書籤列表"""
    try:
        bookmarks = audiobook_db.get_bookmarks(book_id)
        return jsonify({'success': True, 'bookmarks': bookmarks})

    except Exception as e:
        print(f"❌ 獲取書籤錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@audiobook_bp.route('/api/audiobook/bookmark/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    """刪除書籤"""
    try:
        success = audiobook_db.delete_bookmark(bookmark_id)

        if success:
            return jsonify({'success': True, 'message': '書籤已刪除'})
        else:
            return jsonify({'success': False, 'error': '刪除失敗'}), 500

    except Exception as e:
        print(f"❌ 刪除書籤錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 偏好設定 API ====================

@audiobook_bp.route('/api/audiobook/preferences/save', methods=['POST'])
def save_preferences():
    """儲存使用者偏好設定"""
    try:
        data = request.json

        for key, value in data.items():
            audiobook_db.save_preference(key, value)

        return jsonify({'success': True, 'message': '設定已儲存'})

    except Exception as e:
        print(f"❌ 儲存設定錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@audiobook_bp.route('/api/audiobook/preferences', methods=['GET'])
def get_preferences():
    """獲取使用者偏好設定"""
    try:
        preferences = audiobook_db.get_all_preferences()

        # 設定預設值
        defaults = {
            'playbackSpeed': 0.8,
            'volume': 1.0,
            'autoPlay': True,
            'theme': 'light'
        }

        # 合併預設值和使用者設定
        for key, value in defaults.items():
            if key not in preferences:
                preferences[key] = value

        return jsonify({'success': True, 'preferences': preferences})

    except Exception as e:
        print(f"❌ 獲取設定錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
```

---

## 2. 前端 JavaScript（播放器邏輯）

### 檔案：`static/js/audiobook_player_enhanced.js`

```javascript
/**
 * AI 廣播劇增強版播放器
 * 支援進度記錄、書籤、播放控制等功能
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
        this.renderChapters();
      }
    } catch (error) {
      console.error("載入書籍資訊失敗:", error);
    }
  }

  async loadProgress() {
    try {
      const response = await fetch(`/api/audiobook/progress/${this.bookId}`);
      const result = await response.json();

      if (result.success && result.progress) {
        const progress = result.progress;
        // 恢復上次播放位置
        if (progress.chapter_id && progress.position) {
          this.resumeFromProgress(progress);
        }
      }
    } catch (error) {
      console.error("載入進度失敗:", error);
    }
  }

  resumeFromProgress(progress) {
    // 找到對應的章節
    const chapterIndex = this.chapters.findIndex(
      (ch) => ch.id === progress.chapter_id
    );

    if (chapterIndex >= 0) {
      // 顯示恢復提示
      this.showResumePrompt(chapterIndex, progress.position);
    }
  }

  showResumePrompt(chapterIndex, position) {
    const chapter = this.chapters[chapterIndex];
    const timeStr = this.formatTime(position);

    const message = `上次播放到「${chapter.title}」${timeStr}，是否繼續？`;

    if (confirm(message)) {
      this.playChapter(chapter.id, "mandarin", chapter.title, chapterIndex);
      // 等待音頻載入後跳轉到指定位置
      setTimeout(() => {
        if (this.audio) {
          this.audio.currentTime = position;
        }
      }, 1000);
    }
  }

  // ==================== 播放控制 ====================

  async playChapter(chapterId, dialect, title, index) {
    this.currentChapter = {
      id: chapterId,
      title: title,
      index: index,
      dialect: dialect,
    };

    // 更新 UI
    this.updateNowPlaying(title, dialect);
    this.highlightCurrentChapter(chapterId);

    // 載入音頻
    const audioUrl = `/api/audiobook/book/${this.bookId}/chapter/${chapterId}/audio/${dialect}`;

    if (!this.audio) {
      this.audio = document.getElementById("audio");
      this.setupAudioEvents();
    }

    this.audio.src = audioUrl;
    this.audio.playbackRate = this.playbackSpeed;
    this.audio.volume = this.volume;

    try {
      await this.audio.play();
      this.isPlaying = true;
      this.updatePlayButton();
    } catch (error) {
      console.error("播放失敗:", error);
    }
  }

  togglePlay() {
    if (!this.audio) return;

    if (this.isPlaying) {
      this.audio.pause();
      this.isPlaying = false;
    } else {
      this.audio.play();
      this.isPlaying = true;
    }

    this.updatePlayButton();
  }

  // ==================== 進度控制 ====================

  setupProgressBar() {
    const progressBar = document.getElementById("progressBar");
    const progressFill = document.getElementById("progressFill");

    // 點擊跳轉
    progressBar.addEventListener("click", (e) => {
      if (!this.audio) return;

      const rect = progressBar.getBoundingClientRect();
      const percent = (e.clientX - rect.left) / rect.width;
      this.audio.currentTime = percent * this.audio.duration;
    });

    // 拖曳功能
    let isDragging = false;

    progressBar.addEventListener("mousedown", () => {
      isDragging = true;
    });

    document.addEventListener("mousemove", (e) => {
      if (!isDragging || !this.audio) return;

      const rect = progressBar.getBoundingClientRect();
      let percent = (e.clientX - rect.left) / rect.width;
      percent = Math.max(0, Math.min(1, percent));

      progressFill.style.width = `${percent * 100}%`;
    });

    document.addEventListener("mouseup", (e) => {
      if (!isDragging) return;
      isDragging = false;

      const rect = progressBar.getBoundingClientRect();
      let percent = (e.clientX - rect.left) / rect.width;
      percent = Math.max(0, Math.min(1, percent));

      if (this.audio) {
        this.audio.currentTime = percent * this.audio.duration;
      }
    });
  }

  updateProgress() {
    if (!this.audio) return;

    const percent = (this.audio.currentTime / this.audio.duration) * 100;
    const progressFill = document.getElementById("progressFill");
    const currentTimeEl = document.getElementById("currentTime");

    if (progressFill) {
      progressFill.style.width = `${percent}%`;
    }

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

    // 更新顯示
    const speedDisplay = document.getElementById("speedDisplay");
    if (speedDisplay) {
      speedDisplay.textContent = `${speed.toFixed(1)}x`;
    }

    // 儲存設定
    this.savePreference("playbackSpeed", speed);
  }

  setVolume(volume) {
    this.volume = volume;
    if (this.audio) {
      this.audio.volume = volume;
    }

    // 更新圖示
    this.updateVolumeIcon(volume);

    // 儲存設定
    this.savePreference("volume", volume);
  }

  updateVolumeIcon(volume) {
    const volumeIcon = document.getElementById("volumeIcon");
    if (!volumeIcon) return;

    if (volume === 0) {
      volumeIcon.textContent = "volume_off";
    } else if (volume < 0.5) {
      volumeIcon.textContent = "volume_down";
    } else {
      volumeIcon.textContent = "volume_up";
    }
  }

  // ==================== 快退/快進 ====================

  skipBackward(seconds = 15) {
    if (!this.audio) return;
    this.audio.currentTime = Math.max(0, this.audio.currentTime - seconds);
  }

  skipForward(seconds = 15) {
    if (!this.audio) return;
    this.audio.currentTime = Math.min(
      this.audio.duration,
      this.audio.currentTime + seconds
    );
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
  }

  async saveProgress() {
    if (!this.audio || !this.currentChapter) return;

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
    } catch (error) {
      console.error("儲存進度失敗:", error);
    }
  }

  // ==================== 書籤功能 ====================

  async addBookmark(note = "") {
    if (!this.audio || !this.currentChapter) return;

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
        alert("書籤已添加");
        this.loadBookmarks();
      }
    } catch (error) {
      console.error("添加書籤失敗:", error);
    }
  }

  async loadBookmarks() {
    try {
      const response = await fetch(`/api/audiobook/bookmarks/${this.bookId}`);
      const result = await response.json();

      if (result.success) {
        this.renderBookmarks(result.bookmarks);
      }
    } catch (error) {
      console.error("載入書籤失敗:", error);
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
      }
    } catch (error) {
      console.error("載入設定失敗:", error);
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
      console.error("儲存設定失敗:", error);
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
    this.audio.addEventListener("ended", () => this.onAudioEnded());
    this.audio.addEventListener("loadedmetadata", () => {
      const durationEl = document.getElementById("duration");
      if (durationEl) {
        durationEl.textContent = this.formatTime(this.audio.duration);
      }
    });
  }

  onAudioEnded() {
    this.isPlaying = false;
    this.updatePlayButton();

    // 自動播放下一章
    if (this.currentChapter.index < this.chapters.length - 1) {
      const nextChapter = this.chapters[this.currentChapter.index + 1];
      this.playChapter(
        nextChapter.id,
        this.currentChapter.dialect,
        nextChapter.title,
        this.currentChapter.index + 1
      );
    }
  }

  updatePlayButton() {
    const playBtn = document.getElementById("playBtn");
    if (!playBtn) return;

    const icon = playBtn.querySelector(".material-icons");
    if (icon) {
      icon.textContent = this.isPlaying ? "pause" : "play_arrow";
    }
  }

  setupEventListeners() {
    // 播放/暫停
    document.getElementById("playBtn")?.addEventListener("click", () => {
      this.togglePlay();
    });

    // 快退/快進
    document.getElementById("skipBackBtn")?.addEventListener("click", () => {
      this.skipBackward();
    });

    document.getElementById("skipForwardBtn")?.addEventListener("click", () => {
      this.skipForward();
    });

    // 速度控制
    document.getElementById("speedSlider")?.addEventListener("input", (e) => {
      this.setPlaybackSpeed(parseFloat(e.target.value));
    });

    // 音量控制
    document.getElementById("volumeSlider")?.addEventListener("input", (e) => {
      this.setVolume(parseFloat(e.target.value));
    });

    // 書籤
    document.getElementById("addBookmarkBtn")?.addEventListener("click", () => {
      const note = prompt("書籤備註（選填）：");
      if (note !== null) {
        this.addBookmark(note);
      }
    });

    // 進度條
    this.setupProgressBar();
  }

  renderChapters() {
    // 實作章節列表渲染
    // 這部分根據現有的 HTML 結構調整
  }

  renderBookmarks(bookmarks) {
    // 實作書籤列表渲染
    // 這部分根據需要添加
  }

  highlightCurrentChapter(chapterId) {
    // 高亮當前章節
    document.querySelectorAll(".chapter-item").forEach((item) => {
      item.classList.remove("playing");
    });

    const currentItem = document.querySelector(
      `[data-chapter-id="${chapterId}"]`
    );
    if (currentItem) {
      currentItem.classList.add("playing");
    }
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

// 初始化播放器
let player;
document.addEventListener("DOMContentLoaded", () => {
  const pathParts = window.location.pathname.split("/");
  const bookId = pathParts[pathParts.length - 2];

  player = new EnhancedAudiobookPlayer();
  player.init(bookId);
});
```

---

## 3. CSS 樣式

### 檔案：`static/css/audiobook_enhanced.css`

```css
/* AI 廣播劇增強版樣式 */

/* 播放器控制區 */
.player-controls {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* 進度條 */
.progress-container {
  width: 100%;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 3px;
  transition: width 0.1s ease;
}

.time-display {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 13px;
  color: #666;
}

/* 播放控制按鈕 */
.playback-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.control-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: #f5f5f5;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.control-btn:hover {
  background: #e0e0e0;
  transform: scale(1.05);
}

.control-btn.play-btn {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.control-btn.play-btn:hover {
  background: linear-gradient(135deg, #5568d3 0%, #6a4190 100%);
}

.control-btn .material-icons {
  font-size: 24px;
}

/* 速度/音量控制 */
.settings-controls {
  display: flex;
  gap: 24px;
  align-items: center;
  padding: 12px 0;
}

.control-group {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-group label {
  font-size: 13px;
  color: #666;
  min-width: 60px;
}

.slider {
  flex: 1;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: #e0e0e0;
  border-radius: 2px;
  outline: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #667eea;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #667eea;
  cursor: pointer;
  border: none;
}

.value-display {
  min-width: 40px;
  text-align: right;
  font-size: 13px;
  color: #333;
  font-weight: 500;
}

/* 章節列表 */
.chapter-item.playing {
  background: #f0f4ff;
  border-left: 3px solid #667eea;
}

.chapter-item.playing .chapter-title {
  color: #667eea;
  font-weight: 600;
}

/* 書籤按鈕 */
.bookmark-btn {
  padding: 8px 16px;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #666;
  transition: all 0.2s;
}

.bookmark-btn:hover {
  background: #f5f5f5;
  border-color: #667eea;
  color: #667eea;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .settings-controls {
    flex-direction: column;
    gap: 16px;
  }

  .control-group {
    width: 100%;
  }

  .playback-controls {
    gap: 8px;
  }

  .control-btn {
    width: 40px;
    height: 40px;
  }

  .control-btn.play-btn {
    width: 48px;
    height: 48px;
  }
}
```

---

## 4. 使用說明

### 整合步驟：

1. **確保資料庫已初始化**

   ```python
   from modules.voice_processing.audiobook_database import audiobook_db
   # 資料庫會自動初始化
   ```

2. **在 routes/audiobook.py 中添加新的 API 端點**

   - 複製上面的 API 程式碼到檔案中

3. **創建新的 JavaScript 和 CSS 檔案**

   - 創建 `static/js/audiobook_player_enhanced.js`
   - 創建 `static/css/audiobook_enhanced.css`

4. **在 HTML 模板中引入**

   ```html
   <link rel="stylesheet" href="/static/css/audiobook_enhanced.css" />
   <script src="/static/js/audiobook_player_enhanced.js"></script>
   ```

5. **測試功能**
   - 播放音頻
   - 調整速度/音量
   - 快退/快進
   - 進度自動儲存
   - 書籤添加

### 注意事項：

1. 確保 Material Icons 已載入
2. 確保 audiobook_database.py 在正確的路徑
3. 測試所有 API 端點是否正常工作
4. 檢查瀏覽器控制台是否有錯誤

---

**文件版本**：1.0  
**最後更新**：2024-11-23  
**狀態**：待整合測試
