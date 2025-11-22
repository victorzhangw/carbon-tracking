# GPT-SoVITS MIT 協議聲明移除說明

## 📋 修改內容

### 修改文件

- **文件**: `GPT-SoVITS-v2pro-20250604/webui.py`
- **備份**: `GPT-SoVITS-v2pro-20250604/webui.py.backup`

### 修改位置

- **行數**: 1307-1313
- **內容**: 註釋掉頂部的 MIT 協議聲明

### 原始聲明內容

```
本软件以MIT协议开源, 作者不对软件具备任何控制力, 使用软件者、传播软件导出的声音者自负全责.
如不认可该条款, 则不能使用或引用软件包内任何代码和文件. 详见根目录LICENSE.
```

## 🔄 如何恢復

### 方法 1: 使用備份文件

```bash
copy "GPT-SoVITS-v2pro-20250604\webui.py.backup" "GPT-SoVITS-v2pro-20250604\webui.py"
```

### 方法 2: 手動取消註釋

編輯 `GPT-SoVITS-v2pro-20250604/webui.py`，找到第 1307 行附近，取消註釋：

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

## ⚠️ 重要提醒

### 法律聲明

1. **MIT 協議仍然有效**: 即使移除了顯示的聲明，GPT-SoVITS 仍然受 MIT 協議約束
2. **使用者責任**: 使用 GPT-SoVITS 生成的語音內容，使用者需自行承擔法律責任
3. **版權聲明**: 建議在你的應用中添加適當的版權和免責聲明

### 建議的免責聲明

你可以在你的應用中添加類似的聲明：

```
本系統使用 GPT-SoVITS 開源項目（MIT 協議）。
使用本系統生成的語音內容，使用者需自行承擔法律責任。
請勿用於非法用途或侵犯他人權益。
```

## 📝 修改後的代碼

### 修改前

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

### 修改後

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

## 🧪 測試

### 1. 重啟 GPT-SoVITS 服務

如果 GPT-SoVITS 正在運行，需要重啟才能看到變更：

```bash
# 停止現有服務（如果有）
# 然後重新啟動
cd GPT-SoVITS-v2pro-20250604
go-webui.bat
```

### 2. 檢查 WebUI

訪問 `http://localhost:9874`，頂部應該不再顯示 MIT 協議聲明

### 3. 通過 Flask 應用測試

```bash
bStart.bat
```

訪問 `http://localhost:5000/voice-testing`，點擊「TTS 語音合成訓練」卡片，在 Modal 中應該看不到聲明

## 📁 備份文件位置

```
GPT-SoVITS-v2pro-20250604/
├── webui.py              # 修改後的文件
└── webui.py.backup       # 原始備份
```

## 🔍 其他包含聲明的文件

如果需要，以下文件也包含類似的聲明（未修改）：

1. `GPT-SoVITS-v2pro-20250604/tools/uvr5/webui.py`
2. `GPT-SoVITS-v2pro-20250604/GPT_SoVITS/inference_gui.py`
3. `GPT-SoVITS-v2pro-20250604/GPT_SoVITS/inference_webui_fast.py`
4. `GPT-SoVITS-v2pro-20250604/GPT_SoVITS/inference_webui.py`

如果這些頁面也會被使用，可能需要類似的修改。

## 📅 修改記錄

- **日期**: 2025-11-22
- **修改者**: Kiro AI Assistant
- **修改原因**: 用戶要求移除 WebUI 頂部的 MIT 協議聲明
- **備份狀態**: ✅ 已備份至 webui.py.backup

## ⚖️ 法律建議

1. **保留 LICENSE 文件**: 不要刪除 GPT-SoVITS 根目錄的 LICENSE 文件
2. **添加自己的聲明**: 在你的應用中添加適當的免責聲明
3. **尊重原作者**: 在適當的地方註明使用了 GPT-SoVITS 項目
4. **合規使用**: 確保生成的語音內容符合當地法律法規

## 🔗 相關資源

- GPT-SoVITS 項目: https://github.com/RVC-Boss/GPT-SoVITS
- MIT 協議: https://opensource.org/licenses/MIT
- LICENSE 文件: `GPT-SoVITS-v2pro-20250604/LICENSE`
