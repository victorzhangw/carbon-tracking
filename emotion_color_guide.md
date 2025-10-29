# 🎨 情緒標籤文字顏色修改指南

## 📍 修改位置

在 `webpage/ai-customer-service-frontend/src/components/voice/VoiceInteractionContainer.vue` 檔案的 `<style>` 區域中。

## 🏷️ 基本文字顏色修改

### 1. 情緒標籤文字顏色

```css
.user-emotion-tags .emotion-tag {
  color: white !important; /* ← 修改這裡 */
}
```

### 2. 置信度標籤文字顏色

```css
.user-emotion-tags .confidence-tag {
  color: #4361ee !important; /* ← 修改這裡 */
}
```

## 🌈 常用顏色選項

### 基本顏色：

```css
color: #000000 !important; /* 黑色 */
color: #ffffff !important; /* 白色 */
color: #4361ee !important; /* 藍色 */
color: #52c41a !important; /* 綠色 */
color: #ff4d4f !important; /* 紅色 */
color: #faad14 !important; /* 橙色 */
color: #722ed1 !important; /* 紫色 */
color: #8c8c8c !important; /* 灰色 */
```

### 漸層色（進階）：

```css
background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

## 🎯 動態顏色（根據情緒變色）

已添加的動態顏色樣式：

```css
/* 開心 - 綠色 */
.user-emotion-tags .emotion-tag.happy {
  color: #52c41a !important;
}

/* 難過 - 紅色 */
.user-emotion-tags .emotion-tag.sad {
  color: #ff4d4f !important;
}

/* 生氣 - 紅色 */
.user-emotion-tags .emotion-tag.angry {
  color: #ff4d4f !important;
}

/* 驚訝 - 紫色 */
.user-emotion-tags .emotion-tag.surprise {
  color: #722ed1 !important;
}

/* 平靜 - 灰色 */
.user-emotion-tags .emotion-tag.neutral {
  color: #8c8c8c !important;
}

/* 冷靜 - 藍色 */
.user-emotion-tags .emotion-tag.calm {
  color: #1890ff !important;
}
```

## 🔧 如何啟用動態顏色

要啟用動態顏色功能，需要在模板中添加情緒類別：

```vue
<Tag
  :color="getEmotionColor(message.detectedEmotion)"
  :class="['emotion-tag', message.detectedEmotion]"
>
  {{ getEmotionEmoji(message.detectedEmotion) }}
  {{ getEmotionLabel(message.detectedEmotion) }}
</Tag>
```

## 📱 顯示效果

### 目前效果：

```
😊 開心 85%  (白色文字)
😠 生氣 72%  (白色文字)
😲 驚訝 91%  (白色文字)
```

### 動態顏色效果：

```
😊 開心 85%  (綠色文字)
😠 生氣 72%  (紅色文字)
😲 驚訝 91%  (紫色文字)
```

## 🎨 自訂顏色建議

### 情緒顏色心理學：

- **開心/興奮**: 綠色 `#52c41a` 或金色 `#faad14`
- **難過**: 藍色 `#1890ff` 或灰色 `#8c8c8c`
- **生氣**: 紅色 `#ff4d4f` 或深紅 `#cf1322`
- **驚訝**: 紫色 `#722ed1` 或橙色 `#fa8c16`
- **平靜**: 藍色 `#1890ff` 或灰色 `#595959`
- **恐懼**: 橙色 `#fa8c16` 或黃色 `#fadb14`

## 💡 修改建議

1. **保持對比度**: 確保文字顏色與背景有足夠對比度
2. **一致性**: 保持整體設計風格一致
3. **可讀性**: 避免使用過於鮮豔或過淡的顏色
4. **無障礙**: 考慮色盲用戶的需求
