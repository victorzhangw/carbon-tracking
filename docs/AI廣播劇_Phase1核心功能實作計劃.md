# AI 廣播劇 Phase 1 核心功能實作計劃

## 🎯 實作目標

專注實作最核心的功能：

1. ✅ 播放器 UI 升級（進度條可拖曳、速度/音量控制、快退/快進）
2. ✅ 進度記錄功能（自動儲存、恢復播放位置）
3. ✅ 書庫介面優化（卡片式設計、進度顯示）

## 📋 實作清單

### 1. 資料庫層 ✅

- [x] 創建 `audiobook_database.py`
- [x] 播放進度表
- [x] 書籤表
- [x] 播放列表表
- [x] 使用者偏好設定表

### 2. 後端 API 層

- [ ] 擴充 `routes/audiobook.py`
  - [ ] 進度相關 API
  - [ ] 書籤相關 API
  - [ ] 偏好設定 API

### 3. 前端 UI 層

- [ ] 升級 `qwen_audiobook_detail.html`（播放器頁面）
- [ ] 創建 `static/js/audiobook_player.js`（播放器邏輯）
- [ ] 創建 `static/css/audiobook.css`（樣式）

### 4. 測試與文檔

- [ ] 功能測試
- [ ] 使用說明文檔

## 🔧 詳細實作步驟

### Phase 1.1：後端 API 擴充

需要在 `routes/audiobook.py` 添加以下 API：

```python
# 進度管理
POST   /api/audiobook/progress/save      # 儲存進度
GET    /api/audiobook/progress/:book_id  # 獲取進度

# 書籤管理
POST   /api/audiobook/bookmark/add       # 添加書籤
GET    /api/audiobook/bookmarks/:book_id # 獲取書籤列表
DELETE /api/audiobook/bookmark/:id       # 刪除書籤

# 偏好設定
POST   /api/audiobook/preferences/save   # 儲存設定
GET    /api/audiobook/preferences         # 獲取設定
```

### Phase 1.2：播放器 UI 升級

#### 新增功能：

1. **可拖曳進度條**

   - 顯示當前時間/總時長
   - 拖曳跳轉功能
   - 懸停顯示時間預覽

2. **播放速度控制**

   - 滑桿控制（0.5x - 2.0x）
   - 預設值 0.8x
   - 即時調整

3. **音量控制**

   - 滑桿控制（0-100%）
   - 靜音按鈕
   - 記憶設定

4. **快退/快進按鈕**

   - 15 秒快退
   - 15 秒快進
   - 鍵盤快捷鍵支援

5. **自動儲存進度**
   - 每 5 秒自動儲存
   - 切換章節時儲存
   - 關閉頁面時儲存

### Phase 1.3：書庫介面優化

#### 改進項目：

1. **卡片式設計**

   - 書籍封面顯示
   - 進度條顯示
   - 最後播放時間

2. **搜尋功能**

   - 書名搜尋
   - 即時過濾

3. **排序功能**
   - 最近播放
   - 書名排序
   - 上傳時間

## 📝 實作優先順序

### 第一階段（核心功能）

1. 後端 API - 進度管理
2. 播放器 UI - 進度條可拖曳
3. 播放器 UI - 速度/音量控制
4. 自動儲存/恢復進度

### 第二階段（增強功能）

1. 快退/快進按鈕
2. 書庫介面優化
3. 搜尋/排序功能

### 第三階段（完善功能）

1. 書籤功能
2. 播放列表
3. 統計資訊

## 🎨 UI 設計規範

### 色彩

- Primary: #667eea
- Secondary: #764ba2
- Success: #4CAF50
- Background: #f5f7fa

### 字體

- 標題：Microsoft JhengHei, 16-24px
- 內文：Microsoft JhengHei, 14-16px
- 小字：12-13px

### 間距

- 容器 padding: 20-32px
- 元素間距: 12-24px
- 按鈕 padding: 8-12px

## 📊 預期成果

完成後將實現：

- ✅ 現代化的播放器介面
- ✅ 完整的播放控制功能
- ✅ 自動進度記錄與恢復
- ✅ 流暢的使用者體驗
- ✅ 響應式設計（手機/平板/桌面）

## 🔄 後續計劃

Phase 1 完成後，將進入 Phase 2：

- 書籤功能
- 睡眠定時器
- 播放列表
- 深色模式
- 統計資訊

---

**文件版本**：1.0  
**最後更新**：2024-11-23  
**狀態**：進行中
