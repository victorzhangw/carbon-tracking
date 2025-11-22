# GPT-SoVITS MIT 協議聲明完整移除說明

## 🎯 問題分析

### 問題根源

MIT 聲明來自**兩個地方**：

1. **webui.py** (第 1307-1313 行)

   ```python
   gr.HTML(
       top_html.format(
           i18n("本软件以MIT协议开源...")
       )
   )
   ```

2. **assets.py** 中的 `top_html` 模板
   ```python
   top_html = """
   <div align="center">
       <div style="margin-bottom: 5px; font-size: 15px;">{}</div>
       <div style="display: flex; gap: 60px; justify-content: center;">
           <!-- GitHub、文檔、在線體驗等鏈接 -->
       </div>
   </div>
   """
   ```

### 為什麼第一次修改沒有生效？

**Python 緩存問題**：Python 會將編譯後的代碼緩存在 `__pycache__` 目錄中。即使修改了源代碼，如果不清理緩存，仍會使用舊版本。

## 📋 完整修改內容

### 1. webui.py 修改 ✅

- **文件**: `GPT-SoVITS-v2pro-20250604/webui.py`
- **備份**: `GPT-SoVITS-v2pro-20250604/webui.py.backup`
- **修改**: 註釋掉第 1307-1313 行

**修改前**:

```python
with gr.Blocks(title="GPT-SoVITS WebUI", analytics_enabled=False, js=js, css=css) as app:
    gr.HTML(
        top_html.format(
            i18n("本软件以MIT协议开源, 作者不对软件具备任何控制力, 使用软件者、传播软件导出的声音者自负全责.")
            + i18n("如不认可该条款, 则不能使用或引用软件包内任何代码和文件. 详见根目录LICENSE.")
        ),
        elem_classes="markdown",
    )
```

**修改後**:

```python
with gr.Blocks(title="GPT-SoVITS WebUI", analytics_enabled=False, js=js, css=css) as app:
    # MIT 協議聲明已隱藏（原始聲明已備份至 webui.py.backup）
    # gr.HTML(
    #     top_html.format(
    #         i18n("本软件以MIT协议开源, 作者不对软件具备任何控制力, 使用软件者、传播软件导出的声音者自负全责.")
    #         + i18n("如不认可该条款, 则不能使用或引用软件包内任何代码和文件. 详见根目录LICENSE.")
    #     ),
    #     elem_classes="markdown",
    # )
```

### 2. assets.py 修改 ✅

- **文件**: `GPT-SoVITS-v2pro-20250604/tools/assets.py`
- **備份**: `GPT-SoVITS-v2pro-20250604/tools/assets.py.backup`
- **修改**: 簡化 `top_html` 變量

**修改前**:

```python
top_html = """
<div align="center">
    <div style="margin-bottom: 5px; font-size: 15px;">{}</div>
    <div style="display: flex; gap: 60px; justify-content: center;">
        <a href="https://github.com/RVC-Boss/GPT-SoVITS" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-GPT--SoVITS-blue.svg?style=for-the-badge&logo=github" style="width: auto; height: 30px;">
        </a>
        <!-- 更多鏈接... -->
    </div>
</div>
"""
```

**修改後**:

```python
top_html = """
<div align="center">
    <div style="margin-bottom: 5px; font-size: 15px;">{}</div>
</div>
"""

# 原始 top_html 已備份至 assets.py.backup
# 包含 GitHub、文檔、在線體驗等鏈接的完整版本
```

### 3. 清理 Python 緩存 ✅

```bash
# 刪除以下目錄
GPT-SoVITS-v2pro-20250604/__pycache__
GPT-SoVITS-v2pro-20250604/tools/__pycache__
```

## 🔄 如何恢復

### 方法 1: 使用備份文件（推薦）

```bash
# 恢復 webui.py
copy "GPT-SoVITS-v2pro-20250604\webui.py.backup" "GPT-SoVITS-v2pro-20250604\webui.py"

# 恢復 assets.py
copy "GPT-SoVITS-v2pro-20250604\tools\assets.py.backup" "GPT-SoVITS-v2pro-20250604\tools\assets.py"

# 清理緩存
rmdir /s /q "GPT-SoVITS-v2pro-20250604\__pycache__"
rmdir /s /q "GPT-SoVITS-v2pro-20250604\tools\__pycache__"
```

### 方法 2: 手動取消註釋

編輯相應文件，取消註釋或恢復原始內容。

## 🚀 使用方式

### 自動化腳本（推薦）

```bash
# 執行清理並重啟腳本
清理並重啟GPT-SoVITS.bat
```

這個腳本會：

1. 停止現有的 GPT-SoVITS 進程
2. 清理 Python 緩存
3. 驗證修改
4. 重新啟動服務

### 手動步驟

```bash
# 1. 停止現有進程
taskkill /F /IM python.exe /FI "WINDOWTITLE eq GPT-SoVITS*"

# 2. 清理緩存
cd GPT-SoVITS-v2pro-20250604
rmdir /s /q __pycache__
rmdir /s /q tools\__pycache__

# 3. 重新啟動
go-webui.bat
```

## 🧪 驗證修改

### 使用驗證腳本

```bash
python 驗證MIT聲明移除.py
```

這個腳本會檢查：

- ✅ webui.py 是否已修改
- ✅ webui.py 備份是否存在
- ✅ assets.py 是否已修改
- ✅ assets.py 備份是否存在
- ✅ Python 緩存是否已清理

### 手動驗證

1. 啟動 GPT-SoVITS: `go-webui.bat`
2. 訪問: http://localhost:9874
3. 檢查頂部是否還有 MIT 聲明和鏈接

## ⚠️ 重要提醒

### 法律聲明

1. **MIT 協議仍然有效**: 即使移除了顯示的聲明，GPT-SoVITS 仍然受 MIT 協議約束
2. **使用者責任**: 使用 GPT-SoVITS 生成的語音內容，使用者需自行承擔法律責任
3. **版權聲明**: 建議在你的應用中添加適當的版權和免責聲明

### 建議的免責聲明

在你的應用中添加：

```
本系統使用 GPT-SoVITS 開源項目（MIT 協議）。
使用本系統生成的語音內容，使用者需自行承擔法律責任。
請勿用於非法用途或侵犯他人權益。
```

## 📁 文件結構

```
GPT-SoVITS-v2pro-20250604/
├── webui.py                    # 主 WebUI 文件（已修改）
├── webui.py.backup             # 原始備份
├── go-webui.bat                # 啟動腳本
├── tools/
│   ├── assets.py               # 資源文件（已修改）
│   └── assets.py.backup        # 原始備份
└── __pycache__/                # Python 緩存（已清理）

項目根目錄/
├── 清理並重啟GPT-SoVITS.bat   # 自動化清理重啟腳本
├── 驗證MIT聲明移除.py          # 驗證腳本
└── GPT-SoVITS_MIT聲明完整移除說明.md  # 本文檔
```

## 🔍 其他包含聲明的文件

以下文件也包含類似的聲明（**未修改**）：

1. `GPT-SoVITS-v2pro-20250604/tools/uvr5/webui.py`
2. `GPT-SoVITS-v2pro-20250604/GPT_SoVITS/inference_gui.py`
3. `GPT-SoVITS-v2pro-20250604/GPT_SoVITS/inference_webui_fast.py`
4. `GPT-SoVITS-v2pro-20250604/GPT_SoVITS/inference_webui.py`

**注意**: 這些文件是其他 WebUI 頁面。如果你的應用會使用這些頁面，可能需要類似的修改。

### 如何修改其他文件

如果需要修改這些文件，可以使用相同的方法：

```bash
# 1. 備份
copy "文件路徑" "文件路徑.backup"

# 2. 編輯文件，註釋掉 gr.HTML(top_html.format(...))

# 3. 清理緩存
rmdir /s /q "對應的__pycache__目錄"
```

## 📊 修改驗證結果

```
============================================================
🔍 驗證 MIT 聲明移除
============================================================

📄 檢查 webui.py...
✅ GPT-SoVITS-v2pro-20250604/webui.py: 聲明已被註釋
✅ 備份存在: GPT-SoVITS-v2pro-20250604/webui.py.backup

📄 檢查 assets.py...
✅ GPT-SoVITS-v2pro-20250604/tools/assets.py: top_html 已簡化
✅ 備份存在: GPT-SoVITS-v2pro-20250604/tools/assets.py.backup

📄 檢查 Python 緩存...
✅ 沒有 Python 緩存

============================================================
📊 檢查結果總結
============================================================
✅ 通過 - webui.py 修改
✅ 通過 - webui.py 備份
✅ 通過 - assets.py 修改
✅ 通過 - assets.py 備份
✅ 通過 - 緩存清理

總計: 5/5 檢查通過
```

## 🐛 故障排除

### 問題 1: 重啟後仍然看到聲明

**原因**: Python 緩存未清理
**解決**: 執行 `清理並重啟GPT-SoVITS.bat`

### 問題 2: 修改後無法啟動

**原因**: 語法錯誤或文件損壞
**解決**: 使用備份文件恢復

### 問題 3: 其他頁面仍有聲明

**原因**: 其他 WebUI 文件未修改
**解決**: 參考「其他包含聲明的文件」章節

## 📅 修改記錄

- **日期**: 2025-11-22
- **修改者**: Kiro AI Assistant
- **修改原因**: 用戶要求移除 WebUI 頂部的 MIT 協議聲明
- **修改文件**:
  - webui.py (已備份)
  - tools/assets.py (已備份)
- **備份狀態**: ✅ 已完整備份
- **驗證狀態**: ✅ 5/5 檢查通過

## ⚖️ 法律建議

1. **保留 LICENSE 文件**: 不要刪除 GPT-SoVITS 根目錄的 LICENSE 文件
2. **添加自己的聲明**: 在你的應用中添加適當的免責聲明
3. **尊重原作者**: 在適當的地方註明使用了 GPT-SoVITS 項目
4. **合規使用**: 確保生成的語音內容符合當地法律法規
5. **用戶協議**: 建議在應用中添加用戶協議，明確使用責任

## 🔗 相關資源

- GPT-SoVITS 項目: https://github.com/RVC-Boss/GPT-SoVITS
- MIT 協議: https://opensource.org/licenses/MIT
- LICENSE 文件: `GPT-SoVITS-v2pro-20250604/LICENSE`
- 項目文檔: https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e

## 💡 最佳實踐

1. **定期備份**: 在修改前始終創建備份
2. **清理緩存**: 修改 Python 文件後記得清理緩存
3. **驗證修改**: 使用驗證腳本確認修改成功
4. **文檔記錄**: 記錄所有修改，便於日後維護
5. **法律合規**: 確保使用符合法律法規
