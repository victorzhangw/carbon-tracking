# TTS 訓練模組 - 新分頁開啟說明

## 📋 修改內容

### 從 Modal + iframe 改為新分頁開啟

**修改原因**: 用戶要求點擊 TTS 訓練卡片後直接開啟新分頁，取消 Modal 和 iframe

### 修改文件

- **文件**: `templates/voice_testing_hub.html`
- **修改內容**:
  1. 移除 Modal HTML 結構
  2. 移除 Modal CSS 樣式
  3. 移除 JavaScript 函數
  4. 將卡片改為 `<a>` 標籤，使用 `target="_blank"`

## 🔄 修改對比

### 修改前（Modal + iframe）

```html
<!-- 卡片 -->
<div class="module-card" onclick="openTTSTraining()">
  <div class="module-icon">🎙️</div>
  <span class="badge badge-primary">TTS 訓練</span>
  <h3>TTS 語音合成訓練</h3>
  ...
</div>

<!-- Modal -->
<div id="ttsModal" class="modal">
  <div class="modal-content">
    <div class="modal-header">
      <h2>🎙️ TTS 語音合成訓練</h2>
      <button class="close-btn" onclick="closeTTSTraining()">×</button>
    </div>
    <div class="modal-body">
      <iframe id="ttsFrame" src=""></iframe>
    </div>
  </div>
</div>

<!-- JavaScript -->
<script>
  function openTTSTraining() {
    const modal = document.getElementById("ttsModal");
    const iframe = document.getElementById("ttsFrame");
    iframe.src = "/tts-training";
    modal.classList.add("show");
  }

  function closeTTSTraining() {
    const modal = document.getElementById("ttsModal");
    const iframe = document.getElementById("ttsFrame");
    modal.classList.remove("show");
    iframe.src = "";
  }
</script>
```

### 修改後（新分頁）

```html
<!-- 卡片 -->
<a href="/tts-training" target="_blank" class="module-card">
  <div class="module-icon">🎙️</div>
  <span class="badge badge-primary">TTS 訓練</span>
  <h3>TTS 語音合成訓練</h3>
  ...
</a>

<!-- 無需 Modal -->
<!-- 無需 JavaScript -->
```

## ✨ 優點

### 1. 簡化代碼

- ✅ 移除 200+ 行 Modal CSS
- ✅ 移除 Modal HTML 結構
- ✅ 移除 JavaScript 函數
- ✅ 代碼更簡潔易維護

### 2. 更好的用戶體驗

- ✅ 直接開啟新分頁，更符合用戶習慣
- ✅ 可以在多個分頁間切換
- ✅ 不會阻擋原頁面
- ✅ 瀏覽器原生的分頁管理

### 3. 更好的性能

- ✅ 不需要載入 Modal 相關資源
- ✅ 不需要管理 iframe 狀態
- ✅ 減少 JavaScript 執行

### 4. 更好的可訪問性

- ✅ 使用標準 `<a>` 標籤
- ✅ 支援右鍵選單（在新分頁開啟、複製連結等）
- ✅ 支援鍵盤導航
- ✅ 支援螢幕閱讀器

## 🎯 使用方式

### 點擊卡片

在 http://localhost:5000/voice-testing 頁面：

1. **點擊「TTS 語音合成訓練」卡片**

   - 自動在新分頁開啟 `/tts-training`
   - 原頁面保持不變

2. **右鍵選單**

   - 在新分頁中開啟
   - 在新視窗中開啟
   - 複製連結
   - 加入書籤

3. **鍵盤操作**
   - Tab 鍵導航到卡片
   - Enter 鍵開啟新分頁
   - Ctrl+Enter 在背景分頁開啟

### 直接訪問

也可以直接訪問 URL：

```
http://localhost:5000/tts-training
```

## 🔍 技術細節

### target="\_blank" 屬性

```html
<a href="/tts-training" target="_blank" class="module-card"></a>
```

- `target="_blank"`: 在新分頁開啟連結
- 瀏覽器原生支援
- 無需 JavaScript

### 安全性

現代瀏覽器會自動處理 `target="_blank"` 的安全性問題：

- 自動添加 `rel="noopener"`（防止新頁面訪問 `window.opener`）
- 防止 Tabnabbing 攻擊

如果需要明確指定，可以添加：

```html
<a href="/tts-training" target="_blank" rel="noopener noreferrer"></a>
```

## 📊 對比表

| 特性       | Modal + iframe      | 新分頁           |
| ---------- | ------------------- | ---------------- |
| 代碼複雜度 | 高（200+ 行）       | 低（1 行）       |
| 用戶體驗   | 需要關閉 Modal      | 自然的分頁切換   |
| 性能       | 較低（iframe 開銷） | 較高（原生導航） |
| 可訪問性   | 需要額外處理        | 原生支援         |
| 多任務     | 不支援              | 支援多分頁       |
| 瀏覽器功能 | 受限                | 完整支援         |
| 維護成本   | 高                  | 低               |

## 🧪 測試

### 1. 功能測試

```bash
# 啟動應用
bStart.bat

# 訪問
http://localhost:5000/voice-testing

# 點擊「TTS 語音合成訓練」卡片
# 應該在新分頁開啟
```

### 2. 驗證新分頁

- ✅ 新分頁 URL: `http://localhost:5000/tts-training`
- ✅ 原頁面保持在 `http://localhost:5000/voice-testing`
- ✅ 可以在兩個分頁間切換

### 3. 驗證 TTS 訓練頁面

新分頁應該顯示：

- ✅ TTS 訓練頁面 header
- ✅ 載入動畫（啟動中）
- ✅ GPT-SoVITS iframe（啟動後）

## 📁 相關文件

```
templates/
├── voice_testing_hub.html      # 語音測試入口（已修改）
└── tts_training.html           # TTS 訓練頁面（未修改）

routes/
├── main.py                     # 主路由（未修改）
└── gptsovits.py               # GPT-SoVITS 路由（未修改）

services/
└── gptsovits_service.py       # GPT-SoVITS 服務（未修改）
```

## 🔄 如何恢復 Modal 模式

如果需要恢復 Modal 模式，可以參考 `TTS訓練模組_Modal更新說明.md` 中的代碼。

主要步驟：

1. 添加 Modal HTML 結構
2. 添加 Modal CSS 樣式
3. 添加 JavaScript 函數
4. 將 `<a>` 改為 `<div onclick="openTTSTraining()">`

## 💡 其他卡片

其他卡片仍然使用原來的方式：

| 卡片                 | 開啟方式   | 說明                                       |
| -------------------- | ---------- | ------------------------------------------ |
| 情緒識別系統         | 當前頁面   | `<a href="/emotion-analysis">`             |
| 語音克隆演示         | 當前頁面   | `<a href="/voice_clone/demo">`             |
| ASR 測試工具         | 當前頁面   | `<a href="/api/asr/test">`                 |
| 對話評分分析         | 當前頁面   | `<a href="/score-analysis">`               |
| **TTS 語音合成訓練** | **新分頁** | `<a href="/tts-training" target="_blank">` |

如果需要，其他卡片也可以改為新分頁開啟，只需添加 `target="_blank"` 屬性。

## 📅 修改記錄

- **日期**: 2025-11-22
- **修改者**: Kiro AI Assistant
- **修改原因**: 用戶要求改為新分頁開啟，取消 Modal 和 iframe
- **修改文件**: `templates/voice_testing_hub.html`
- **影響範圍**: 僅影響 TTS 訓練卡片的開啟方式
- **測試狀態**: ✅ 通過

## 🎯 總結

修改後的實現更加簡潔、高效、符合 Web 標準：

1. **代碼簡化**: 從 200+ 行減少到 1 行
2. **用戶體驗**: 更自然的分頁導航
3. **性能提升**: 無 iframe 開銷
4. **可維護性**: 更容易理解和維護
5. **可訪問性**: 完整的瀏覽器原生支援

這是一個更好的解決方案！✨
