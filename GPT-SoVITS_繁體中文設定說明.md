# GPT-SoVITS 繁體中文語言設定說明

## ✅ 已完成設定

### 修改內容

- **文件**: `GPT-SoVITS-v2pro-20250604/go-webui.bat`
- **備份**: `GPT-SoVITS-v2pro-20250604/go-webui.bat.backup`
- **修改**: 將預設語言從 `zh_CN` (簡體中文) 改為 `zh_TW` (繁體中文)

## 📋 語言支援

### GPT-SoVITS 支援的語言

GPT-SoVITS 使用 i18n 國際化系統，支援以下語言：

| 語言代碼 | 語言名稱            | 文件位置                       |
| -------- | ------------------- | ------------------------------ |
| `en_US`  | 英文 (美國)         | `tools/i18n/locale/en_US.json` |
| `zh_CN`  | 簡體中文            | `tools/i18n/locale/zh_CN.json` |
| `zh_TW`  | **繁體中文 (台灣)** | `tools/i18n/locale/zh_TW.json` |
| `zh_HK`  | 繁體中文 (香港)     | `tools/i18n/locale/zh_HK.json` |
| `zh_SG`  | 簡體中文 (新加坡)   | `tools/i18n/locale/zh_SG.json` |
| `ja_JP`  | 日文                | `tools/i18n/locale/ja_JP.json` |
| `ko_KR`  | 韓文                | `tools/i18n/locale/ko_KR.json` |
| `es_ES`  | 西班牙文            | `tools/i18n/locale/es_ES.json` |
| `fr_FR`  | 法文                | `tools/i18n/locale/fr_FR.json` |
| `it_IT`  | 義大利文            | `tools/i18n/locale/it_IT.json` |
| `pt_BR`  | 葡萄牙文 (巴西)     | `tools/i18n/locale/pt_BR.json` |
| `ru_RU`  | 俄文                | `tools/i18n/locale/ru_RU.json` |
| `tr_TR`  | 土耳其文            | `tools/i18n/locale/tr_TR.json` |

## 🔧 修改詳情

### 修改前

```batch
runtime\python.exe -I webui.py zh_CN
```

### 修改後

```batch
runtime\python.exe -I webui.py zh_TW
```

## 🎯 i18n 工作原理

### 1. 語言參數傳遞

```batch
# 啟動腳本傳遞語言參數
runtime\python.exe -I webui.py zh_TW
                                 ^^^^^ 語言代碼
```

### 2. webui.py 接收參數

```python
# webui.py 第 67-69 行
language = sys.argv[-1] if sys.argv[-1] in scan_language_list() else "Auto"
os.environ["language"] = language
i18n = I18nAuto(language=language)
```

### 3. 載入語言文件

```python
# tools/i18n/i18n.py
def load_language_list(language):
    with open(os.path.join(I18N_JSON_DIR, f"{language}.json"), "r", encoding="utf-8") as f:
        language_list = json.load(f)
    return language_list
```

### 4. 使用翻譯

```python
# 在代碼中使用 i18n() 函數
i18n("前置数据集获取工具")  # 返回: "前置資料集獲取工具"
```

## 🔄 如何切換語言

### 方法 1: 修改啟動腳本（推薦）

編輯 `go-webui.bat`，修改最後一個參數：

```batch
# 繁體中文 (台灣)
runtime\python.exe -I webui.py zh_TW

# 簡體中文
runtime\python.exe -I webui.py zh_CN

# 英文
runtime\python.exe -I webui.py en_US

# 日文
runtime\python.exe -I webui.py ja_JP

# 自動偵測系統語言
runtime\python.exe -I webui.py Auto
```

### 方法 2: 手動啟動指定語言

```batch
cd GPT-SoVITS-v2pro-20250604
runtime\python.exe -I webui.py zh_TW
```

### 方法 3: 使用備份恢復

```batch
# 恢復原始設定 (簡體中文)
copy "GPT-SoVITS-v2pro-20250604\go-webui.bat.backup" "GPT-SoVITS-v2pro-20250604\go-webui.bat"
```

## 📝 繁體中文翻譯範例

### 界面文字對照

| 簡體中文           | 繁體中文 (zh_TW)   |
| ------------------ | ------------------ |
| 前置数据集获取工具 | 前置資料集獲取工具 |
| UVR5 人声伴奏分离  | UVR5 人聲伴奏分離  |
| 音频切分工具       | 音頻切分工具       |
| 语音识别           | 語音識別           |
| 文本标注           | 文本標註           |
| 训练集音频文件目录 | 訓練集音頻文件目錄 |
| 开始训练           | 開始訓練           |
| 推理               | 推理               |

### 完整翻譯文件

繁體中文翻譯文件位於：

```
GPT-SoVITS-v2pro-20250604/tools/i18n/locale/zh_TW.json
```

包含 **500+ 個翻譯條目**，涵蓋所有界面文字。

## 🧪 驗證設定

### 1. 檢查啟動腳本

```batch
type GPT-SoVITS-v2pro-20250604\go-webui.bat
```

應該看到：

```batch
runtime\python.exe -I webui.py zh_TW
```

### 2. 啟動並檢查

```batch
cd GPT-SoVITS-v2pro-20250604
go-webui.bat
```

### 3. 訪問 WebUI

打開瀏覽器訪問：http://localhost:9874

### 4. 確認語言

檢查界面文字是否為繁體中文：

- ✅ 「前置資料集獲取工具」
- ✅ 「UVR5 人聲伴奏分離」
- ✅ 「音頻切分工具」
- ✅ 「語音識別」

## 📁 相關文件

```
GPT-SoVITS-v2pro-20250604/
├── go-webui.bat                    # 啟動腳本（已修改為 zh_TW）
├── go-webui.bat.backup             # 原始備份（zh_CN）
├── webui.py                        # 主程式
└── tools/
    └── i18n/
        ├── i18n.py                 # i18n 核心邏輯
        └── locale/
            ├── zh_TW.json          # 繁體中文翻譯 ✅
            ├── zh_CN.json          # 簡體中文翻譯
            ├── en_US.json          # 英文翻譯
            └── ...                 # 其他語言
```

## 🔍 進階設定

### 自訂翻譯

如果需要修改翻譯，編輯 `zh_TW.json`：

```json
{
  "原始文字": "翻譯文字",
  "前置数据集获取工具": "前置資料集獲取工具"
}
```

### 添加新翻譯

如果發現未翻譯的文字，在 `zh_TW.json` 中添加：

```json
{
  "新的文字": "新的翻譯"
}
```

### 系統自動偵測

使用 `Auto` 參數時，系統會根據作業系統語言自動選擇：

```python
# i18n.py 第 25-27 行
if language in ["Auto", None]:
    language = locale.getdefaultlocale()[0]
```

Windows 繁體中文系統會自動偵測為 `zh_TW`。

## ⚠️ 注意事項

1. **修改後需重啟**: 修改語言設定後，需要重新啟動 GPT-SoVITS 才會生效

2. **備份已創建**: 原始啟動腳本已備份至 `go-webui.bat.backup`

3. **翻譯完整性**: `zh_TW.json` 包含完整翻譯，無需額外修改

4. **其他 WebUI**: 如果使用其他 WebUI（如 inference_webui.py），也需要類似修改

## 🚀 快速啟動

### 使用繁體中文啟動（當前設定）

```batch
cd GPT-SoVITS-v2pro-20250604
go-webui.bat
```

### 臨時使用其他語言

```batch
cd GPT-SoVITS-v2pro-20250604

# 簡體中文
runtime\python.exe -I webui.py zh_CN

# 英文
runtime\python.exe -I webui.py en_US

# 日文
runtime\python.exe -I webui.py ja_JP
```

## 📊 修改記錄

- **日期**: 2025-11-22
- **修改者**: Kiro AI Assistant
- **修改原因**: 用戶要求將預設語言改為繁體中文
- **修改文件**: `go-webui.bat`
- **備份狀態**: ✅ 已備份至 `go-webui.bat.backup`
- **語言設定**: `zh_CN` → `zh_TW`

## 🔗 相關資源

- GPT-SoVITS 項目: https://github.com/RVC-Boss/GPT-SoVITS
- i18n 文檔: `tools/i18n/i18n.py`
- 繁體中文翻譯: `tools/i18n/locale/zh_TW.json`
