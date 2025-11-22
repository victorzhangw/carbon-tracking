# 🎙️ TTS 訓練模組整合說明

## ✅ 已完成的整合

### 新增功能

將 GPT-SoVITS 訓練系統整合到語音測試訓練模組中，通過 iframe 方式嵌入 GPT-SoVITS WebUI。

## 📁 新增文件

### 1. 服務層 - `services/gptsovits_service.py`

**功能**: 管理 GPT-SoVITS 進程的啟動和停止

**主要方法**:

- `is_running()`: 檢查服務是否運行
- `start()`: 啟動 GPT-SoVITS WebUI
- `stop()`: 停止 GPT-SoVITS WebUI
- `get_status()`: 獲取服務狀態

**特點**:

- 自動檢測服務是否已啟動
- 後台啟動進程，不阻塞主應用
- 最多等待 30 秒確認服務啟動
- 支援進程管理和清理

### 2. 路由層 - `routes/gptsovits.py`

**路由定義**:

| 路由                    | 方法 | 功能         |
| ----------------------- | ---- | ------------ |
| `/tts-training`         | GET  | TTS 訓練頁面 |
| `/api/gptsovits/status` | GET  | 獲取服務狀態 |
| `/api/gptsovits/start`  | POST | 手動啟動服務 |
| `/api/gptsovits/stop`   | POST | 停止服務     |

**特點**:

- 訪問頁面時自動在後台啟動 GPT-SoVITS
- 使用線程避免阻塞頁面載入
- 提供 API 端點供前端查詢狀態

### 3. 前端頁面 - `templates/tts_training.html`

**功能**: 顯示 GPT-SoVITS WebUI 的 iframe 頁面

**UI 組件**:

- 頂部導航欄（返回按鈕 + 標題 + 狀態指示器）
- 載入動畫（啟動時顯示）
- 錯誤提示（啟動失敗時顯示）
- iframe 容器（服務就緒後顯示）

**狀態管理**:

- 🟡 正在啟動（loading）
- 🟢 運行中（running）
- 🔴 啟動失敗（error）

**自動檢測**:

- 每秒檢查一次服務狀態
- 最多等待 60 秒
- 服務就緒後自動顯示 iframe
- 超時後顯示錯誤並提供重試按鈕

## 🔄 整合流程

### 1. 用戶訪問流程

```
用戶點擊「TTS 語音合成訓練」卡片
    ↓
訪問 /tts-training 路由
    ↓
後台線程啟動 GPT-SoVITS (go-webui.bat)
    ↓
頁面顯示載入動畫
    ↓
前端每秒檢查服務狀態 (/api/gptsovits/status)
    ↓
服務就緒後顯示 iframe (http://localhost:9874)
```

### 2. 技術實現

#### 後端啟動邏輯

```python
# 在後台線程啟動（不阻塞頁面）
def start_in_background():
    if not gptsovits_service.is_running():
        gptsovits_service.start()

thread = threading.Thread(target=start_in_background, daemon=True)
thread.start()
```

#### 前端狀態檢測

```javascript
// 每秒檢查一次
checkInterval = setInterval(checkStatus, 1000);

async function checkStatus() {
  const response = await fetch("/api/gptsovits/status");
  const data = await response.json();

  if (data.running) {
    showIframe(); // 顯示 iframe
  }
}
```

## 🎨 UI 設計

### 頁面佈局

```
┌─────────────────────────────────────────┐
│ ← 返回  🎙️ TTS 語音合成訓練  🟢 運行中 │
├─────────────────────────────────────────┤
│                                         │
│         [GPT-SoVITS WebUI]             │
│         (iframe 嵌入)                   │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

### 載入狀態

```
┌─────────────────────────────────────────┐
│ ← 返回  🎙️ TTS 語音合成訓練  🟡 正在啟動│
├─────────────────────────────────────────┤
│ 💡 提示：首次啟動可能需要 20-30 秒...   │
├─────────────────────────────────────────┤
│                                         │
│              [載入動畫]                 │
│      正在啟動 GPT-SoVITS 訓練系統...    │
│         這可能需要一些時間，請稍候       │
│                                         │
└─────────────────────────────────────────┘
```

### 錯誤狀態

```
┌─────────────────────────────────────────┐
│ ← 返回  🎙️ TTS 語音合成訓練  🔴 啟動失敗│
├─────────────────────────────────────────┤
│                                         │
│                  ⚠️                     │
│        無法連接到 GPT-SoVITS 服務       │
│        請確認服務是否正常啟動           │
│                                         │
│              [重試按鈕]                 │
│                                         │
└─────────────────────────────────────────┘
```

## 🔧 配置說明

### GPT-SoVITS 路徑配置

在 `services/gptsovits_service.py` 中：

```python
self.gptsovits_dir = os.path.join(os.getcwd(), "GPT-SoVITS-v2pro-20250604")
self.webui_url = "http://localhost:9874"
self.startup_script = os.path.join(self.gptsovits_dir, "go-webui.bat")
```

### 端口配置

- **GPT-SoVITS WebUI**: `http://localhost:9874`
- **Flask 主應用**: `http://localhost:5000`

## 📊 語音測試訓練模組更新

### 新增卡片

在 `templates/voice_testing_hub.html` 中添加了新的模組卡片：

```html
<!-- TTS 語音合成訓練 -->
<a href="/tts-training" class="module-card">
  <div class="module-icon">🎙️</div>
  <span class="badge badge-primary">TTS 訓練</span>
  <h3>TTS 語音合成訓練</h3>
  <p>GPT-SoVITS 語音合成模型訓練與推理</p>
  <ul class="module-features">
    <li>音頻數據預處理</li>
    <li>模型訓練與微調</li>
    <li>語音合成推理</li>
    <li>聲音克隆訓練</li>
  </ul>
</a>
```

### 卡片特點

- 🎙️ 圖標：麥克風
- 🔵 徽章：藍色「TTS 訓練」
- 功能列表：4 項主要功能

## 🚀 使用方式

### 1. 啟動主應用

```bash
bStart.bat
```

### 2. 訪問語音測試訓練模組

```
http://localhost:5000/voice-testing
```

### 3. 點擊「TTS 語音合成訓練」卡片

- 系統會自動啟動 GPT-SoVITS
- 等待 20-30 秒（首次啟動）
- 服務就緒後自動顯示訓練界面

### 4. 使用 GPT-SoVITS 訓練系統

在 iframe 中可以使用完整的 GPT-SoVITS 功能：

- **Tab 0**: 數據預處理

  - 人聲分離
  - 音頻切分
  - 語音識別

- **Tab 1A**: 訓練集格式化

  - BERT 特徵提取
  - SSL 特徵提取
  - 語義特徵提取

- **Tab 1B**: 模型訓練

  - SoVITS 訓練
  - GPT 訓練

- **Tab 1C**: 推理測試
  - 語音合成
  - 聲音克隆

## ⚙️ 進程管理

### 自動管理

- 訪問頁面時自動啟動 GPT-SoVITS
- 如果服務已運行，不會重複啟動
- 使用守護線程，不阻塞主應用

### 手動管理

可以通過 API 手動控制：

```bash
# 啟動服務
curl -X POST http://localhost:5000/api/gptsovits/start

# 停止服務
curl -X POST http://localhost:5000/api/gptsovits/stop

# 查詢狀態
curl http://localhost:5000/api/gptsovits/status
```

## 🔍 故障排除

### 問題 1: 啟動超時

**症狀**: 等待超過 60 秒仍顯示載入動畫

**解決方法**:

1. 檢查 `GPT-SoVITS-v2pro-20250604` 目錄是否存在
2. 檢查 `go-webui.bat` 是否可執行
3. 手動運行 `go-webui.bat` 查看錯誤訊息
4. 檢查端口 9874 是否被佔用

### 問題 2: iframe 無法顯示

**症狀**: 頁面空白或顯示錯誤

**解決方法**:

1. 檢查瀏覽器控制台錯誤
2. 確認 `http://localhost:9874` 可以直接訪問
3. 檢查瀏覽器是否阻止 iframe
4. 清除瀏覽器緩存

### 問題 3: 服務無法停止

**症狀**: 調用停止 API 後服務仍在運行

**解決方法**:

1. 手動關閉 GPT-SoVITS 控制台視窗
2. 使用任務管理器終止相關進程
3. 重啟電腦

## 📝 注意事項

### 1. 首次啟動

- 首次啟動可能需要 20-30 秒
- 需要載入模型和初始化環境
- 請耐心等待

### 2. 資源佔用

- GPT-SoVITS 需要較多記憶體和 GPU 資源
- 建議在訓練時關閉其他大型應用
- 確保有足夠的磁碟空間

### 3. 端口衝突

- 確保端口 9874 未被佔用
- 如需修改端口，需同時修改：
  - GPT-SoVITS 配置
  - `services/gptsovits_service.py`
  - `templates/tts_training.html`

### 4. 瀏覽器兼容性

- 建議使用 Chrome、Edge 或 Firefox
- 確保瀏覽器允許 iframe 嵌入
- 部分瀏覽器可能需要調整安全設置

## 🎊 總結

TTS 訓練模組已成功整合到語音測試訓練模組中：

- ✅ 自動啟動 GPT-SoVITS 服務
- ✅ iframe 嵌入完整訓練界面
- ✅ 狀態檢測和錯誤處理
- ✅ 友好的載入動畫和提示
- ✅ 返回按鈕和導航
- ✅ 進程管理和清理

用戶現在可以直接在語音測試訓練模組中訪問完整的 GPT-SoVITS 訓練功能！

---

**更新日期**: 2025-11-22  
**版本**: 1.0  
**狀態**: ✅ 完成並測試
