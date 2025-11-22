# Material Icons 實施指南

## 📋 已完成

✅ 創建 `static/css/material-icons.css` - Material Icons 樣式文件
✅ 創建 `Material_Icons_替換方案.md` - 完整的替換方案文檔

## 🎯 實施步驟

### 步驟 1: 在每個頁面添加 Material Icons CSS

在所有 HTML 文件的 `<head>` 部分添加：

```html
<!-- Material Icons -->
<link
  rel="stylesheet"
  href="{{ url_for('static', filename='css/material-icons.css') }}"
/>
```

### 步驟 2: 替換 Emoji 為 Material Icons

使用以下對照表進行替換：

## 🔄 快速替換對照表

### 常用圖標

| Emoji | HTML 替換                                                         | 用途        |
| ----- | ----------------------------------------------------------------- | ----------- |
| 🎤    | `<span class="material-icons">mic</span>`                         | 麥克風/錄音 |
| 📊    | `<span class="material-icons">bar_chart</span>`                   | 數據分析    |
| 😊    | `<span class="material-icons">sentiment_satisfied</span>`         | 開心        |
| 😢    | `<span class="material-icons">sentiment_dissatisfied</span>`      | 悲傷        |
| 😠    | `<span class="material-icons">sentiment_very_dissatisfied</span>` | 憤怒        |
| 😐    | `<span class="material-icons">sentiment_neutral</span>`           | 中性        |
| 🎙️    | `<span class="material-icons">record_voice_over</span>`           | 語音/TTS    |
| 📝    | `<span class="material-icons">edit_note</span>`                   | 文字/編輯   |
| 💬    | `<span class="material-icons">chat</span>`                        | 對話/聊天   |
| ⏱️    | `<span class="material-icons">schedule</span>`                    | 時間        |
| 🤖    | `<span class="material-icons">smart_toy</span>`                   | AI/機器人   |
| 👤    | `<span class="material-icons">person</span>`                      | 用戶        |
| 👨‍💼    | `<span class="material-icons">admin_panel_settings</span>`        | 管理員      |
| 👥    | `<span class="material-icons">group</span>`                       | 群組        |
| 🔬    | `<span class="material-icons">science</span>`                     | 測試/實驗   |
| 📁    | `<span class="material-icons">folder</span>`                      | 文件夾      |
| 🎵    | `<span class="material-icons">music_note</span>`                  | 音樂/音頻   |
| 🗣️    | `<span class="material-icons">hearing</span>`                     | 語音識別    |
| ⭐    | `<span class="material-icons">star</span>`                        | 評分/星級   |
| 💡    | `<span class="material-icons">lightbulb</span>`                   | 建議/提示   |
| 🏁    | `<span class="material-icons">flag</span>`                        | 結束        |
| 📈    | `<span class="material-icons">trending_up</span>`                 | 趨勢/成長   |
| 🎯    | `<span class="material-icons">gps_fixed</span>`                   | 目標/準確   |
| ✅    | `<span class="material-icons">check_circle</span>`                | 完成/確認   |
| ❌    | `<span class="material-icons">cancel</span>`                      | 取消/錯誤   |
| ⚠️    | `<span class="material-icons">warning</span>`                     | 警告        |
| ℹ️    | `<span class="material-icons">info</span>`                        | 資訊        |

### 操作圖標

| Emoji | HTML 替換                                        | 用途     |
| ----- | ------------------------------------------------ | -------- |
| ⏹️    | `<span class="material-icons">stop</span>`       | 停止     |
| ▶️    | `<span class="material-icons">play_arrow</span>` | 播放     |
| ⏸️    | `<span class="material-icons">pause</span>`      | 暫停     |
| 🔄    | `<span class="material-icons">refresh</span>`    | 重新載入 |
| 🔍    | `<span class="material-icons">search</span>`     | 搜尋     |
| ⚙️    | `<span class="material-icons">settings</span>`   | 設定     |
| 🗑️    | `<span class="material-icons">delete</span>`     | 刪除     |
| ✏️    | `<span class="material-icons">edit</span>`       | 編輯     |
| 💾    | `<span class="material-icons">save</span>`       | 儲存     |
| 📤    | `<span class="material-icons">upload</span>`     | 上傳     |
| 📥    | `<span class="material-icons">download</span>`   | 下載     |

## 📄 需要修改的文件清單

### 優先級 1（核心頁面）

1. ✅ `templates/login.html` - 已更新為 Material Design 風格
2. `templates/portal.html`
3. `templates/emotion_analysis.html`
4. `templates/voice_testing_hub.html`

### 優先級 2（功能頁面）

5. `templates/score_report_modal_v2.html`
6. `templates/asr_test.html`
7. `templates/voice_interaction_realtime_index.html`
8. `templates/voice_interaction_realtime_roy.html`
9. `templates/voice_interaction_realtime_nofish.html`

### 優先級 3（其他頁面）

10. `templates/voice_interaction_realtime.html`
11. `templates/voice_interaction_enhanced.html`
12. `templates/audiobook_library.html`
13. `templates/score_analysis_enhanced.html`

## 🛠️ 實施工具

### 使用 VS Code 批量替換

1. 打開 VS Code
2. 按 `Ctrl + Shift + H` 打開全局搜尋替換
3. 使用正則表達式模式
4. 在 "files to include" 輸入: `templates/*.html`

### 替換範例

**搜尋**: `🎤`
**替換**: `<span class="material-icons">mic</span>`

**搜尋**: `📊`
**替換**: `<span class="material-icons">bar_chart</span>`

## 📝 特殊情況處理

### 1. 按鈕中的圖標

```html
<!-- 之前 -->
<button>🎤 開始錄音</button>

<!-- 之後 -->
<button>
  <span class="material-icons">mic</span>
  開始錄音
</button>
```

### 2. 標題中的圖標

```html
<!-- 之前 -->
<h1>🔬 語音測試訓練模組</h1>

<!-- 之後 -->
<h1>
  <span class="material-icons md-36">science</span>
  語音測試訓練模組
</h1>
```

### 3. JavaScript 動態生成的圖標

```javascript
// 之前
avatar.textContent = "🤖";

// 之後
avatar.innerHTML = '<span class="material-icons">smart_toy</span>';
```

### 4. 情緒圖標（需要特別處理）

```javascript
// 之前
const emotionMap = {
  happy: { class: "happy", text: "😊 開心" },
  sad: { class: "sad", text: "😢 悲傷" },
};

// 之後
const emotionMap = {
  happy: {
    class: "happy",
    text: "開心",
    icon: "sentiment_satisfied",
  },
  sad: {
    class: "sad",
    text: "悲傷",
    icon: "sentiment_dissatisfied",
  },
};

// 使用時
const html = `
  <span class="material-icons">${emotionInfo.icon}</span>
  ${emotionInfo.text}
`;
```

## 🎨 樣式調整建議

### 調整圖標大小

```html
<!-- 小圖標 (18px) -->
<span class="material-icons md-18">mic</span>

<!-- 標準圖標 (24px) -->
<span class="material-icons">mic</span>

<!-- 大圖標 (36px) -->
<span class="material-icons md-36">mic</span>

<!-- 超大圖標 (48px) -->
<span class="material-icons md-48">mic</span>
```

### 調整圖標顏色

```css
/* 在 CSS 中 */
.icon-primary {
  color: #667eea;
}

.icon-success {
  color: #28a745;
}

.icon-danger {
  color: #dc3545;
}

.icon-warning {
  color: #ffc107;
}
```

```html
<!-- 在 HTML 中 -->
<span class="material-icons icon-primary">mic</span>
```

## ✅ 測試檢查清單

完成替換後，請檢查：

- [ ] 所有圖標正確顯示
- [ ] 圖標大小適當
- [ ] 圖標與文字對齊正確
- [ ] 按鈕中的圖標間距合適
- [ ] 動態生成的圖標正常工作
- [ ] 不同瀏覽器中顯示一致
- [ ] 響應式設計下圖標正常
- [ ] 無控制台錯誤

## 🚀 快速開始

### 最小化實施（只修改核心頁面）

如果時間有限，至少完成以下頁面：

1. `login.html` - ✅ 已完成
2. `portal.html` - 系統入口，用戶第一眼看到
3. `emotion_analysis.html` - 主要功能頁面
4. `voice_testing_hub.html` - 功能導航頁面

這四個頁面覆蓋了用戶的主要使用流程。

## 📞 需要幫助？

如果在實施過程中遇到問題：

1. 查看 `Material_Icons_替換方案.md` 獲取詳細說明
2. 參考 `static/css/material-icons.css` 了解可用的樣式類
3. 訪問 [Material Icons 官方文檔](https://fonts.google.com/icons)

## 🎉 預期效果

完成後，系統將：

- 擁有統一、專業的圖標系統
- 更好的視覺一致性
- 更容易維護和更新
- 更好的可訪問性
- 更現代的外觀

---

**注意**: 這是一個大工程，建議分階段完成。先完成核心頁面，測試無誤後再繼續其他頁面。
