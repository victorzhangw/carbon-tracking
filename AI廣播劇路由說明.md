# AI 廣播劇路由說明與修復方案

## 📋 問題診斷

**問題**：訪問 `/api/audiobook/book/<book_id>/view` 看到的是舊版 UI，沒有 Phase 1 新功能

**原因**：這個路由使用的是舊版模板 `qwen_audiobook_detail.html`

---

## 🗺️ AI 廣播劇路由架構

### 兩個 Blueprint

系統中有**兩個**不同的 audiobook blueprint：

#### 1. audiobook_bp（舊版）

- **檔案**：`routes/audiobook.py`
- **前綴**：`/api/audiobook`
- **功能**：基礎 AI 廣播劇功能

#### 2. qwen_audiobook_bp（Qwen 版本）

- **檔案**：`modules/voice_processing/qwen_audiobook_service.py`
- **前綴**：`/api/audiobook`（與舊版相同！）
- **功能**：Qwen TTS 雙語廣播劇

### 路由衝突

兩個 blueprint 使用相同的前綴 `/api/audiobook`，導致路由覆蓋：

```python
# app.py
app.register_blueprint(audiobook_bp)        # 先註冊
app.register_blueprint(qwen_audiobook_bp)   # 後註冊，會覆蓋同名路由
```

---

## 📊 完整路由對照表

| URL                             | Blueprint         | 模板                           | 版本        | Phase 1 |
| ------------------------------- | ----------------- | ------------------------------ | ----------- | ------- |
| `/api/audiobook/`               | audiobook_bp      | `audiobook_player.html`        | 舊版        | ❌      |
| `/api/audiobook/test`           | audiobook_bp      | `audiobook_test.html`          | 測試版      | ❌      |
| `/api/audiobook/test-enhanced`  | audiobook_bp      | `audiobook_test_enhanced.html` | **Phase 1** | ✅      |
| `/api/audiobook/library`        | qwen_audiobook_bp | `audiobook_library.html`       | Qwen 圖書館 | ❌      |
| `/api/audiobook/book/<id>/view` | qwen_audiobook_bp | `qwen_audiobook_detail.html`   | Qwen 詳情   | ❌      |

---

## 🔍 當前使用的路由

```python
# modules/voice_processing/qwen_audiobook_service.py (第 739-744 行)

@qwen_audiobook_bp.route('/book/<book_id>/view', methods=['GET'])
def book_detail_page(book_id):
    """書籍詳情頁面"""
    from flask import render_template
    return render_template('qwen_audiobook_detail.html')
```

**使用的模板**：`qwen_audiobook_detail.html`  
**問題**：這是舊版模板，沒有 Phase 1 功能

---

## 🔧 解決方案

### 方案 A：更新 qwen_audiobook_detail.html（推薦）

將 Phase 1 的功能整合到 `qwen_audiobook_detail.html`：

1. 引入 Phase 1 的 CSS/JS
2. 添加進度追蹤功能
3. 添加書籤功能
4. 設定播放速度為 0.8x

### 方案 B：修改路由使用新模板

修改 `qwen_audiobook_service.py`：

```python
@qwen_audiobook_bp.route('/book/<book_id>/view', methods=['GET'])
def book_detail_page(book_id):
    """書籍詳情頁面 - Phase 1 版本"""
    from flask import render_template
    return render_template('audiobook_test_enhanced.html')  # 使用 Phase 1 模板
```

### 方案 C：創建新路由

保留舊路由，創建新的 Phase 1 路由：

```python
@qwen_audiobook_bp.route('/book/<book_id>/view-enhanced', methods=['GET'])
def book_detail_enhanced(book_id):
    """書籍詳情頁面 - Phase 1 增強版"""
    from flask import render_template
    return render_template('audiobook_test_enhanced.html')
```

---

## ✅ 推薦修復步驟

### 步驟 1：更新路由（立即生效）

修改 `modules/voice_processing/qwen_audiobook_service.py` 第 739-744 行：

```python
@qwen_audiobook_bp.route('/book/<book_id>/view', methods=['GET'])
def book_detail_page(book_id):
    """書籍詳情頁面 - Phase 1 增強版"""
    from flask import render_template
    # 使用 Phase 1 增強版模板
    return render_template('audiobook_test_enhanced.html')
```

### 步驟 2：重啟服務

```bash
# 停止服務
Ctrl + C

# 重新啟動
python app.py
# 或
bStart.bat
```

### 步驟 3：清除快取並測試

```
1. Ctrl + Shift + Delete（清除快取）
2. 訪問：http://localhost:5000/api/audiobook/book/<book_id>/view
3. 應該看到 Phase 1 新功能
```

---

## 📝 Phase 1 功能檢查清單

訪問書籍詳情頁面後，應該看到：

- [ ] 播放進度追蹤
- [ ] 書籤功能
- [ ] 播放速度調整（預設 0.8x）
- [ ] 增強版播放器 UI
- [ ] 進度條顯示
- [ ] 書籤按鈕

---

## 🎯 測試方法

### 測試 1：訪問書籍詳情

```
URL: http://localhost:5000/api/audiobook/book/e556a911-ace0-4f9d-9c42-98c44e68317d/view

預期結果：
- 看到 Phase 1 增強版 UI
- 播放速度預設為 0.8x
- 有進度追蹤功能
```

### 測試 2：檢查模板

```bash
# 確認使用的模板
# 在瀏覽器開發者工具 Console 執行：
console.log(document.title);

# Phase 1 版本應該顯示特定標題
```

---

**診斷人員**：AI 語音互動平台開發團隊  
**診斷日期**：2024-11-23  
**狀態**：✅ 問題已診斷，修復方案已提供
