# Material Design Icons 替換方案

## 🎯 目標

將系統中所有 emoji 圖標替換為 Material Design Icons，提升專業度和一致性。

## 📊 Emoji 使用統計

### 主要頁面使用的 Emoji

| Emoji  | 用途          | 出現頁面                                               | Material Icon                                    |
| ------ | ------------- | ------------------------------------------------------ | ------------------------------------------------ |
| 🎤     | 麥克風/錄音   | emotion_analysis, voice_testing_hub, voice_interaction | `mic`                                            |
| 📊     | 數據分析/圖表 | emotion_analysis, voice_testing_hub                    | `analytics` / `bar_chart`                        |
| 😊😢😠 | 情緒表情      | emotion_analysis                                       | `sentiment_satisfied` / `sentiment_dissatisfied` |
| 🎙️     | 語音/TTS      | voice_testing_hub, voice_interaction                   | `record_voice_over`                              |
| 📝     | 文字/內容     | score_report_modal                                     | `description` / `edit_note`                      |
| 💬     | 對話/聊天     | emotion_analysis, voice_interaction                    | `chat` / `forum`                                 |
| ⏱️     | 時間          | score_report_modal                                     | `schedule` / `timer`                             |
| 🤖     | AI/機器人     | emotion_analysis, voice_interaction                    | `smart_toy` / `psychology`                       |
| 👤     | 用戶          | login, emotion_analysis                                | `person` / `account_circle`                      |
| 👨‍💼     | 管理員        | login                                                  | `admin_panel_settings`                           |
| 👥     | 訪客/群組     | login                                                  | `group` / `people`                               |
| 🔬     | 測試/實驗     | voice_testing_hub                                      | `science` / `biotech`                            |
| 📁     | 文件/上傳     | audiobook_library                                      | `folder` / `upload_file`                         |
| 🎵     | 音樂/音頻     | asr_test                                               | `music_note` / `audio_file`                      |
| 🗣️     | 語音識別      | voice_testing_hub                                      | `hearing` / `voice_chat`                         |
| ⭐     | 評分/星級     | score_report_modal                                     | `star` / `grade`                                 |
| 💡     | 建議/提示     | score_report_modal, voice_interaction                  | `lightbulb` / `tips_and_updates`                 |
| 🏁     | 結束          | emotion_analysis                                       | `flag` / `done`                                  |
| 📈     | 趨勢/成長     | score_analysis                                         | `trending_up` / `show_chart`                     |
| 🎯     | 目標/準確     | asr_test                                               | `target` / `gps_fixed`                           |

## 🔧 實施方案

### 方案 1: 使用 Google Material Icons CDN（推薦）

#### 優點

- 無需下載，直接使用
- 自動更新
- 輕量級

#### 實施步驟

1. **在所有頁面的 `<head>` 中添加**:

```html
<!-- Material Icons -->
<link
  href="https://fonts.googleapis.com/icon?family=Material+Icons"
  rel="stylesheet"
/>
<link
  href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined"
  rel="stylesheet"
/>
```

2. **創建通用 CSS 類**:

```css
/* Material Icons 樣式 */
.material-icons {
  font-family: "Material Icons";
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  display: inline-block;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;
  vertical-align: middle;
}

/* 不同大小 */
.material-icons.md-18 {
  font-size: 18px;
}
.material-icons.md-24 {
  font-size: 24px;
}
.material-icons.md-36 {
  font-size: 36px;
}
.material-icons.md-48 {
  font-size: 48px;
}

/* Material Symbols (更現代) */
.material-symbols-outlined {
  font-family: "Material Symbols Outlined";
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  display: inline-block;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;
  vertical-align: middle;
}
```

3. **替換 Emoji 為 Material Icons**:

```html
<!-- 之前 -->
<span>🎤</span>

<!-- 之後 -->
<span class="material-icons">mic</span>

<!-- 或使用 Material Symbols -->
<span class="material-symbols-outlined">mic</span>
```

### 方案 2: 創建圖標組件系統

創建一個統一的圖標組件文件：

```html
<!-- static/components/icons.html -->
<template id="icon-mic">
  <span class="material-icons">mic</span>
</template>

<template id="icon-analytics">
  <span class="material-icons">analytics</span>
</template>

<!-- ... 更多圖標 -->
```

## 📝 替換對照表

### 完整的 Emoji → Material Icon 映射

```javascript
const iconMap = {
  // 語音相關
  "🎤": "mic",
  "🎙️": "record_voice_over",
  "🗣️": "hearing",
  "🎵": "music_note",

  // 數據分析
  "📊": "bar_chart",
  "📈": "trending_up",
  "📉": "trending_down",

  // 情緒
  "😊": "sentiment_satisfied",
  "😢": "sentiment_dissatisfied",
  "😠": "sentiment_very_dissatisfied",
  "😐": "sentiment_neutral",
  "😨": "sentiment_stressed",
  "😲": "sentiment_excited",

  // 用戶
  "👤": "person",
  "👨‍💼": "admin_panel_settings",
  "👥": "group",
  "🤖": "smart_toy",

  // 操作
  "📝": "edit_note",
  "💬": "chat",
  "⏱️": "schedule",
  "🏁": "flag",
  "🎯": "gps_fixed",

  // 文件
  "📁": "folder",
  "📄": "description",

  // 其他
  "💡": "lightbulb",
  "⭐": "star",
  "🔬": "science",
  "✅": "check_circle",
  "❌": "cancel",
  "⚠️": "warning",
  ℹ️: "info",
};
```

## 🚀 實施優先級

### Phase 1: 核心頁面（高優先級）

1. ✅ `login.html` - 登入頁面
2. `portal.html` - 系統入口
3. `emotion_analysis.html` - 情緒識別系統
4. `voice_testing_hub.html` - 語音測試訓練模組

### Phase 2: 功能頁面（中優先級）

5. `score_report_modal_v2.html` - 評分報告
6. `asr_test.html` - ASR 測試工具
7. `voice_interaction_realtime_*.html` - 即時語音互動

### Phase 3: 其他頁面（低優先級）

8. `audiobook_library.html` - 廣播劇庫
9. `score_analysis_enhanced.html` - 評分分析
10. 其他輔助頁面

## 💻 實施代碼

### 創建通用圖標 CSS 文件

**文件**: `static/css/material-icons.css`

```css
/* Material Icons 基礎樣式 */
@import url("https://fonts.googleapis.com/icon?family=Material+Icons");
@import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200");

.material-icons,
.material-symbols-outlined {
  font-weight: normal;
  font-style: normal;
  display: inline-block;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;
  vertical-align: middle;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  -moz-osx-font-smoothing: grayscale;
  font-feature-settings: "liga";
}

.material-icons {
  font-family: "Material Icons";
  font-size: 24px;
}

.material-symbols-outlined {
  font-family: "Material Symbols Outlined";
  font-size: 24px;
  font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24;
}

/* 大小變體 */
.material-icons.md-18,
.material-symbols-outlined.md-18 {
  font-size: 18px;
}

.material-icons.md-24,
.material-symbols-outlined.md-24 {
  font-size: 24px;
}

.material-icons.md-36,
.material-symbols-outlined.md-36 {
  font-size: 36px;
}

.material-icons.md-48,
.material-symbols-outlined.md-48 {
  font-size: 48px;
}

.material-icons.md-64,
.material-symbols-outlined.md-64 {
  font-size: 64px;
}

/* 顏色變體 */
.material-icons.md-dark,
.material-symbols-outlined.md-dark {
  color: rgba(0, 0, 0, 0.87);
}

.material-icons.md-light,
.material-symbols-outlined.md-light {
  color: rgba(255, 255, 255, 1);
}

.material-icons.md-inactive,
.material-symbols-outlined.md-inactive {
  color: rgba(0, 0, 0, 0.38);
}

/* 填充變體（僅 Symbols）*/
.material-symbols-outlined.filled {
  font-variation-settings: "FILL" 1, "wght" 400, "GRAD" 0, "opsz" 24;
}

/* 粗體變體（僅 Symbols）*/
.material-symbols-outlined.bold {
  font-variation-settings: "FILL" 0, "wght" 700, "GRAD" 0, "opsz" 24;
}
```

### 創建 JavaScript 輔助函數

**文件**: `static/js/icon-helper.js`

```javascript
/**
 * Material Icons 輔助函數
 */

// 創建 Material Icon 元素
function createIcon(iconName, options = {}) {
  const {
    type = "material-icons", // 'material-icons' 或 'material-symbols-outlined'
    size = 24,
    className = "",
    filled = false,
    bold = false,
  } = options;

  const span = document.createElement("span");
  span.className = type;

  if (size !== 24) {
    span.classList.add(`md-${size}`);
  }

  if (filled && type === "material-symbols-outlined") {
    span.classList.add("filled");
  }

  if (bold && type === "material-symbols-outlined") {
    span.classList.add("bold");
  }

  if (className) {
    span.className += ` ${className}`;
  }

  span.textContent = iconName;

  return span;
}

// Emoji 到 Material Icon 的映射
const emojiToIcon = {
  "🎤": "mic",
  "🎙️": "record_voice_over",
  "📊": "bar_chart",
  "😊": "sentiment_satisfied",
  "😢": "sentiment_dissatisfied",
  "😠": "sentiment_very_dissatisfied",
  "😐": "sentiment_neutral",
  "📝": "edit_note",
  "💬": "chat",
  "⏱️": "schedule",
  "🤖": "smart_toy",
  "👤": "person",
  "👨‍💼": "admin_panel_settings",
  "👥": "group",
  "🔬": "science",
  "📁": "folder",
  "🎵": "music_note",
  "🗣️": "hearing",
  "⭐": "star",
  "💡": "lightbulb",
  "🏁": "flag",
  "📈": "trending_up",
  "🎯": "gps_fixed",
};

// 替換頁面中的所有 Emoji
function replaceEmojisWithIcons(container = document.body) {
  const walker = document.createTreeWalker(
    container,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );

  const nodesToReplace = [];
  let node;

  while ((node = walker.nextNode())) {
    const text = node.textContent;
    let hasEmoji = false;

    for (const emoji in emojiToIcon) {
      if (text.includes(emoji)) {
        hasEmoji = true;
        break;
      }
    }

    if (hasEmoji) {
      nodesToReplace.push(node);
    }
  }

  nodesToReplace.forEach((node) => {
    let html = node.textContent;

    for (const [emoji, iconName] of Object.entries(emojiToIcon)) {
      const regex = new RegExp(emoji, "g");
      html = html.replace(
        regex,
        `<span class="material-icons">${iconName}</span>`
      );
    }

    const span = document.createElement("span");
    span.innerHTML = html;
    node.parentNode.replaceChild(span, node);
  });
}

// 導出函數
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    createIcon,
    emojiToIcon,
    replaceEmojisWithIcons,
  };
}
```

## 📋 使用範例

### 範例 1: 基本使用

```html
<!-- 之前 -->
<button>🎤 開始錄音</button>

<!-- 之後 -->
<button>
  <span class="material-icons">mic</span>
  開始錄音
</button>
```

### 範例 2: 不同大小

```html
<!-- 小圖標 -->
<span class="material-icons md-18">mic</span>

<!-- 中圖標 -->
<span class="material-icons md-24">mic</span>

<!-- 大圖標 -->
<span class="material-icons md-48">mic</span>
```

### 範例 3: 使用 Material Symbols（更現代）

```html
<!-- 空心 -->
<span class="material-symbols-outlined">mic</span>

<!-- 實心 -->
<span class="material-symbols-outlined filled">mic</span>

<!-- 粗體 -->
<span class="material-symbols-outlined bold">mic</span>
```

### 範例 4: JavaScript 動態創建

```javascript
// 創建圖標
const icon = createIcon("mic", {
  size: 36,
  type: "material-symbols-outlined",
  filled: true,
});

// 添加到按鈕
button.prepend(icon);
```

## 🎨 設計指南

### 圖標大小建議

- **18px**: 內聯文字中的小圖標
- **24px**: 標準按鈕和列表項
- **36px**: 卡片標題和重要操作
- **48px**: 大型按鈕和特色區域
- **64px**: 頁面標題和主要視覺元素

### 顏色使用

- **主要操作**: 使用品牌色
- **次要操作**: 使用灰色
- **成功**: 綠色 (#28a745)
- **警告**: 黃色 (#ffc107)
- **錯誤**: 紅色 (#dc3545)
- **資訊**: 藍色 (#0d6efd)

## ✅ 檢查清單

- [ ] 創建 `static/css/material-icons.css`
- [ ] 創建 `static/js/icon-helper.js`
- [ ] 在所有頁面添加 Material Icons CDN
- [ ] 替換 `login.html` 中的圖標
- [ ] 替換 `portal.html` 中的圖標
- [ ] 替換 `emotion_analysis.html` 中的圖標
- [ ] 替換 `voice_testing_hub.html` 中的圖標
- [ ] 替換其他頁面中的圖標
- [ ] 測試所有頁面的圖標顯示
- [ ] 更新文檔

## 🎉 預期效果

替換後的系統將：

- ✅ 更加專業和現代
- ✅ 圖標大小和樣式統一
- ✅ 更好的可訪問性
- ✅ 更容易維護和更新
- ✅ 更好的跨瀏覽器兼容性
- ✅ 更小的文件大小（相比圖片）
