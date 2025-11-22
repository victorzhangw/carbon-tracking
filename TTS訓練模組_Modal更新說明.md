# TTS 訓練模組 Modal 更新說明

## 📋 更新內容

### 1. 修復跳轉問題 ✅

**問題**: 點擊 TTS 訓練卡片後，頁面會跳轉到 `http://localhost:9874/`，而不是在 iframe 中顯示

**解決方案**:

- 將卡片從 `<a>` 標籤改為 `<div>` 標籤
- 使用 `onclick` 事件觸發 Modal 顯示
- 在 Modal 中使用 iframe 嵌入 TTS 訓練頁面

### 2. 移除重複卡片 ✅

**問題**: 在 `/voice-testing` 頁面中有兩個 TTS 相關卡片：

- 「TTS 語音合成」（舊的，指向 `/simple_tts/demo`）
- 「TTS 語音合成訓練」（新的，指向 `/tts-training`）

**解決方案**:

- 移除舊的「TTS 語音合成」卡片
- 保留新的「TTS 語音合成訓練」卡片
- 註釋掉 `app.py` 中的 `simple_tts` 路由註冊

## 🎨 新的使用體驗

### 點擊卡片

```
用戶點擊「TTS 語音合成訓練」卡片
    ↓
觸發 openTTSTraining() 函數
    ↓
顯示全屏 Modal
    ↓
在 Modal 中的 iframe 載入 /tts-training
    ↓
iframe 自動啟動 GPT-SoVITS 服務
    ↓
顯示 GPT-SoVITS WebUI (http://localhost:9874)
```

### 關閉 Modal

用戶可以通過以下方式關閉 Modal：

1. 點擊右上角的 ✕ 按鈕
2. 點擊 Modal 外部的背景
3. 按下 ESC 鍵

關閉 Modal 時會自動清空 iframe 的 src，停止載入。

## 📁 修改的文件

### 1. `templates/voice_testing_hub.html`

**修改內容**:

- ✅ 移除舊的「TTS 語音合成」卡片（`/simple_tts/demo`）
- ✅ 將「TTS 語音合成訓練」卡片改為 `<div>` + `onclick`
- ✅ 添加 Modal HTML 結構
- ✅ 添加 Modal CSS 樣式
- ✅ 添加 JavaScript 函數：
  - `openTTSTraining()` - 打開 Modal
  - `closeTTSTraining()` - 關閉 Modal
  - ESC 鍵監聽
  - 背景點擊監聽

### 2. `app.py`

**修改內容**:

- ✅ 註釋掉 `simple_tts` 路由註冊
- ✅ 添加註釋說明：「simple_tts 已被 GPT-SoVITS 訓練模組取代」

## 🧪 測試結果

### 測試腳本: `test_tts_training_modal.py`

```
✅ 通過 - 模板文件修改
✅ 通過 - 路由配置
✅ 通過 - 路由可訪問性

總計: 3/3 測試通過
```

### 測試項目

1. ✅ 舊的 TTS 語音合成卡片已移除
2. ✅ TTS Modal 已添加
3. ✅ TTS 卡片使用 onclick 事件
4. ✅ openTTSTraining() 函數已添加
5. ✅ closeTTSTraining() 函數已添加
6. ✅ TTS iframe 已添加
7. ✅ simple_tts 路由已被註釋
8. ✅ GPT-SoVITS 路由已註冊
9. ✅ /voice-testing 可訪問
10. ✅ /tts-training 可訪問
11. ✅ /api/gptsovits/status 可訪問

## 🚀 使用方式

### 1. 啟動應用

```bash
bStart.bat
```

### 2. 訪問語音測試模組

```
http://localhost:5000/voice-testing
```

### 3. 點擊 TTS 訓練卡片

點擊「TTS 語音合成訓練」卡片，會在 Modal 中顯示訓練界面

### 4. 等待服務啟動

首次啟動需要 20-30 秒，會顯示載入動畫

### 5. 開始使用

服務啟動後，可以使用完整的 GPT-SoVITS 訓練功能

## 🎯 技術細節

### Modal 實現

```html
<!-- Modal 結構 -->
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
```

### JavaScript 控制

```javascript
function openTTSTraining() {
  const modal = document.getElementById("ttsModal");
  const iframe = document.getElementById("ttsFrame");
  iframe.src = "/tts-training"; // 設置 iframe src
  modal.classList.add("show"); // 顯示 Modal
}

function closeTTSTraining() {
  const modal = document.getElementById("ttsModal");
  const iframe = document.getElementById("ttsFrame");
  modal.classList.remove("show"); // 隱藏 Modal
  iframe.src = ""; // 清空 iframe src
}
```

### CSS 樣式

- Modal 使用 `position: fixed` 全屏覆蓋
- Modal 內容使用 95% 寬高，居中顯示
- 背景使用半透明黑色遮罩
- iframe 填滿 Modal 內容區域

## 📊 對比

### 修改前

```
點擊卡片 → 頁面跳轉到 http://localhost:9874/
           ↓
        離開原頁面，無法返回
```

### 修改後

```
點擊卡片 → 顯示 Modal → iframe 載入訓練頁面
           ↓
        停留在原頁面，可以關閉 Modal
```

## ✨ 優點

1. **不離開原頁面**: 用戶停留在語音測試模組頁面
2. **更好的用戶體驗**: Modal 提供更流暢的交互
3. **易於關閉**: 多種方式關閉 Modal
4. **資源管理**: 關閉 Modal 時自動清理 iframe
5. **統一風格**: 與其他模組保持一致的交互方式

## 🔧 維護說明

### 如果需要修改 Modal 樣式

編輯 `templates/voice_testing_hub.html` 中的 CSS：

```css
.modal {
  /* Modal 背景 */
}
.modal-content {
  /* Modal 內容容器 */
}
.modal-header {
  /* Modal 標題欄 */
}
.modal-body {
  /* Modal 內容區 */
}
```

### 如果需要修改 Modal 行為

編輯 `templates/voice_testing_hub.html` 中的 JavaScript：

```javascript
function openTTSTraining() {
  /* 打開邏輯 */
}
function closeTTSTraining() {
  /* 關閉邏輯 */
}
```

### 如果需要恢復舊的 simple_tts 路由

取消註釋 `app.py` 中的相關代碼：

```python
try:
    from routes.simple_tts import simple_tts_bp
    app.register_blueprint(simple_tts_bp)
    optional_modules.append("TTS")
except ImportError as e:
    print(f"⚠️ TTS模組未載入: {e}")
```

## 📝 更新日期

2025-11-22

## 👤 更新者

Kiro AI Assistant
