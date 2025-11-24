# AI 廣播劇章節內容顯示診斷指南

## 問題：點擊章節後右側沒有顯示文字

### 診斷步驟

#### 1. 檢查瀏覽器 Console（最重要）

1. 按 F12 打開開發者工具
2. 切換到 Console 標籤
3. 點擊任一章節
4. 查看是否有錯誤訊息

**可能的錯誤：**

- `loadChapterText is not defined` → JavaScript 函數未載入
- `transcriptContent is null` → HTML 元素不存在
- `404 Not Found` → API 端點錯誤
- `bookId is not defined` → 書籍 ID 未初始化

#### 2. 檢查 Network 請求

1. 在開發者工具中切換到 Network 標籤
2. 點擊任一章節
3. 查看是否有 `/api/audiobook/book/.../chapter/.../content` 的請求
4. 點擊該請求查看回應內容

**預期回應：**

```json
{
  "status": "success",
  "data": {
    "book_id": "...",
    "chapter_id": "...",
    "content": "章節文字內容..." 或 null
  }
}
```

#### 3. 檢查書籍檔案

確認書籍目錄下是否有 .txt 檔案：

```
static/audiobooks/<book_id>/
  ├── chapter_001.mp3
  ├── chapter_001.txt  ← 需要這個檔案
  ├── chapter_002.mp3
  ├── chapter_002.txt  ← 需要這個檔案
  └── ...
```

**檢查方法：**

```powershell
# 在 PowerShell 中執行
Get-ChildItem "static\audiobooks\*\*.txt" -Recurse
```

如果沒有 .txt 檔案，表示：

- 書籍是在修改前上傳的（舊書籍）
- 需要重新上傳書籍

#### 4. 清除瀏覽器快取

1. 按 Ctrl + Shift + Delete
2. 選擇「快取的圖片和檔案」
3. 清除快取
4. 重新載入頁面（Ctrl + F5）

### 解決方案

#### 方案 1：重新上傳書籍（推薦）

1. 刪除舊書籍
2. 重新上傳 EPUB 檔案
3. 系統會自動生成 .txt 檔案
4. 測試章節內容顯示

#### 方案 2：手動創建測試檔案

如果只是想測試功能，可以手動創建一個 .txt 檔案：

1. 找到書籍目錄：`static/audiobooks/<book_id>/`
2. 創建檔案：`chapter_001.txt`
3. 寫入測試內容：

```
第一章 測試內容

這是測試用的章節文字內容。
可以包含多行文字。
```

4. 重新載入頁面並點擊該章節

#### 方案 3：檢查伺服器日誌

查看 Flask 伺服器的輸出，看是否有錯誤訊息。

### 常見問題

**Q: 顯示「章節文字內容功能開發中」**
A: 這表示 API 正常運作，但沒有找到 .txt 檔案。需要重新上傳書籍。

**Q: 完全沒有任何反應**
A: 檢查 Console 是否有 JavaScript 錯誤。

**Q: 顯示「載入中...」後沒有變化**
A: API 請求可能失敗，檢查 Network 標籤。

### 測試用 JavaScript 代碼

在 Console 中執行以下代碼來測試：

```javascript
// 測試 1：檢查元素是否存在
console.log(
  "transcriptContent 元素:",
  document.getElementById("transcriptContent")
);

// 測試 2：檢查 bookId 是否定義
console.log("bookId:", typeof bookId !== "undefined" ? bookId : "未定義");

// 測試 3：手動調用函數
if (typeof loadChapterText === "function") {
  console.log("loadChapterText 函數存在");
  // loadChapterText('chapter_001', '測試章節');
} else {
  console.log("loadChapterText 函數不存在");
}

// 測試 4：手動發送 API 請求
fetch(`/api/audiobook/book/${bookId}/chapter/chapter_001/content`)
  .then((r) => r.json())
  .then((d) => console.log("API 回應:", d))
  .catch((e) => console.error("API 錯誤:", e));
```

### 確認修改已生效

確保以下修改已應用：

1. ✅ `routes/audiobook.py` - 添加了 `get_chapter_content` API
2. ✅ `modules/voice_processing/audiobook_service.py` - 在生成音頻時儲存 .txt
3. ✅ `templates/qwen_audiobook_detail.html` - `playChapter` 函數調用 `loadChapterText`

### 需要幫助？

如果以上步驟都無法解決問題，請提供：

1. Console 中的錯誤訊息（截圖）
2. Network 標籤中的 API 請求回應
3. 書籍目錄中的檔案列表
