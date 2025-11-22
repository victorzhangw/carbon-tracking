# 🎙️ GPT-SoVITS 訓練頁面說明

## 📍 主要文件位置

**主要 WebUI 文件**: `GPT-SoVITS-v2pro-20250604/webui.py`

## 🎯 訓練流程頁面結構

GPT-SoVITS 的訓練流程分為多個 Tab，按照順序進行：

### Tab 0: 前置數據集獲取工具

#### 0a - UVR5 人聲伴奏分離&去混響去延迟工具

- **功能**: 分離人聲和伴奏，去除混響和延遲
- **位置**: 第 1318 行開始

#### 0b - 語音切分工具

- **功能**: 自動切分長音頻為短片段
- **關鍵參數**:
  - `slice_inp_path`: 音頻自動切分輸入路徑（可文件可文件夾）
  - `slice_opt_root`: 切分後的子音頻的輸出根目錄（預設: `output/slicer_opt`）
  - `threshold`: 音量閾值（預設: -34）
  - `min_length`: 每段最小長度（預設: 4000ms）
  - `min_interval`: 最短切割間隔（預設: 300ms）
  - `max_sil_kept`: 切完後靜音最多留多長（預設: 500ms）
- **位置**: 第 1331 行開始

#### 0c - 語音識別工具

- **功能**: 自動識別語音內容，生成文本標註
- **位置**: 第 1400 行之後

### Tab 1: GPT-SoVITS-TTS

#### 1A - 訓練集格式化工具

- **功能**: 準備訓練數據，生成必要的特徵文件
- **關鍵輸入**:
  - `inp_text`: 文本標註文件（.list 格式）
    - 範例路徑: `D:\RVC1006\GPT-SoVITS\raw\xxx.list`
  - `inp_wav_dir`: 訓練集音頻文件目錄
    - 說明: 填切割後音頻所在目錄
- **位置**: 第 1530 行開始

**子步驟**:

- **1Aa**: BERT 特徵提取
- **1Ab**: SSL 特徵提取（使用 chinese-hubert-base）
- **1Ac**: 語義特徵提取
- **1Aabc**: 一鍵執行所有步驟

#### 1B - 微調訓練

##### 1Ba - SoVITS 訓練

- **功能**: 訓練 SoVITS 模型（語音合成模型）
- **關鍵參數**:
  - `batch_size`: 每張顯卡的 batch_size
  - `total_epoch`: 總訓練輪數（不建議太高）
  - `save_every_epoch`: 保存頻率
  - `text_low_lr_rate`: 文本模塊學習率權重（v1/v2）
  - `lora_rank`: LoRA 秩（v3/v4）
  - `if_save_latest`: 是否僅保存最新的權重文件
  - `if_save_every_weights`: 是否在每次保存時間點將最終小模型保存至 weights 文件夾
  - `gpu_numbers1Ba`: GPU 卡號（以 - 分割）
- **輸出**: 模型權重文件在 `SoVITS_weights/` 目錄
- **位置**: 第 1707 行開始

##### 1Bb - GPT 訓練

- **功能**: 訓練 GPT 模型（文本到語音特徵模型）
- **關鍵參數**:
  - `batch_size1Bb`: 每張顯卡的 batch_size
  - `total_epoch1Bb`: 總訓練輪數（預設: 15）
  - `save_every_epoch1Bb`: 保存頻率（預設: 5）
  - `if_dpo`: 是否開啟 DPO 訓練選項（實驗性）
  - `if_save_latest1Bb`: 是否僅保存最新的權重文件
  - `if_save_every_weights1Bb`: 是否保存至 weights 文件夾
  - `gpu_numbers1Bb`: GPU 卡號
- **輸出**: 模型權重文件在 `GPT_weights/` 目錄
- **位置**: 第 1790 行開始

#### 1C - 推理

- **功能**: 使用訓練好的模型進行語音合成
- **位置**: 第 1855 行開始

### Tab 2: GPT-SoVITS-變聲

- **狀態**: 施工中
- **位置**: 第 1973 行

## 📂 關鍵目錄結構

```
GPT-SoVITS-v2pro-20250604/
├── webui.py                    # 主要 WebUI 文件
├── go-webui.bat               # Windows 啟動腳本
├── GPT_SoVITS/                # 核心代碼
│   ├── s1_train.py           # GPT 訓練腳本
│   ├── s2_train.py           # SoVITS 訓練腳本（v1/v2）
│   └── s2_train_v3_lora.py   # SoVITS 訓練腳本（v3/v4）
├── output/                    # 輸出目錄
│   ├── slicer_opt/           # 切分後的音頻
│   ├── asr_opt/              # ASR 識別結果
│   └── uvr5_opt/             # UVR5 處理結果
├── logs/                      # 訓練日誌和實驗數據
├── GPT_weights/              # GPT 模型權重（v1）
├── GPT_weights_v2/           # GPT 模型權重（v2）
├── GPT_weights_v2Pro/        # GPT 模型權重（v2Pro）
├── SoVITS_weights/           # SoVITS 模型權重（v1）
├── SoVITS_weights_v2/        # SoVITS 模型權重（v2）
└── SoVITS_weights_v2Pro/     # SoVITS 模型權重（v2Pro）
```

## 🎯 完整訓練流程

### 步驟 1: 準備音頻數據

1. 準備原始音頻文件（可以是長音頻）
2. 使用 **0a - UVR5** 分離人聲（如果有背景音樂）
3. 使用 **0b - 語音切分工具** 切分為短片段（4-10 秒）
4. 使用 **0c - 語音識別工具** 生成文本標註

### 步驟 2: 格式化訓練集

1. 進入 **1A - 訓練集格式化工具**
2. 填寫文本標註文件路徑（.list 文件）
3. 填寫訓練集音頻文件目錄
4. 執行 **1Aabc** 一鍵生成所有特徵

### 步驟 3: 訓練模型

1. 進入 **1Ba - SoVITS 訓練**

   - 設置訓練參數
   - 點擊開始訓練
   - 等待訓練完成

2. 進入 **1Bb - GPT 訓練**
   - 設置訓練參數
   - 點擊開始訓練
   - 等待訓練完成

### 步驟 4: 推理測試

1. 進入 **1C - 推理**
2. 選擇訓練好的模型
3. 輸入文本進行語音合成測試

## 🔧 啟動 WebUI

### Windows

```bash
cd GPT-SoVITS-v2pro-20250604
go-webui.bat
```

### 訪問地址

預設會在瀏覽器自動打開，或手動訪問：

```
http://localhost:9874
```

## 📝 音頻文件要求

### 原始音頻

- **格式**: WAV, MP3, FLAC 等常見格式
- **採樣率**: 建議 44.1kHz 或 48kHz
- **時長**: 單個文件可以是長音頻（會自動切分）
- **質量**: 清晰、無雜音、無背景音樂（或使用 UVR5 分離）

### 切分後音頻

- **時長**: 4-10 秒為佳
- **內容**: 每段包含完整的句子或短語
- **數量**: 建議至少 100 段以上

### 文本標註格式（.list 文件）

```
audio_path|speaker_name|language|text
```

範例：

```
output/slicer_opt/audio_001.wav|speaker1|zh|你好，今天天氣很好
output/slicer_opt/audio_002.wav|speaker1|zh|我很高興見到你
```

## 💡 訓練建議

### SoVITS 訓練

- **Batch Size**: 根據顯卡記憶體調整（4-16）
- **Total Epoch**: 8-15 輪（不要太高，容易過擬合）
- **Save Every Epoch**: 每 2-4 輪保存一次

### GPT 訓練

- **Batch Size**: 4-8
- **Total Epoch**: 10-15 輪
- **Save Every Epoch**: 每 5 輪保存一次

### 硬體需求

- **GPU**: NVIDIA GPU with CUDA support（建議 6GB+ VRAM）
- **RAM**: 16GB+
- **Storage**: 10GB+ 可用空間

## 🎨 WebUI 界面特點

### Gradio 框架

- 使用 Gradio 構建 Web 界面
- 支援即時更新和進度顯示
- 友好的圖形化操作界面

### 多語言支持

- 支援中文、英文等多種語言
- 通過 `tools/i18n/i18n.py` 實現國際化

### 進程管理

- 支援多 GPU 訓練
- 可以隨時開始/停止訓練
- 顯示訓練進度和狀態

## 📊 已訓練的模型

根據目錄結構，已經有一些訓練好的模型：

### GPT 模型

- `GPT_weights_v2Pro/vic2507201114-e10.ckpt`
- `GPT_weights_v2Pro/vic2507201114-e5.ckpt`

### SoVITS 模型

- `SoVITS_weights_v2Pro/vic2507201114_e4_s100.pth`
- `SoVITS_weights_v2Pro/vic2507201114_e8_s200.pth`

## 🔍 關鍵代碼位置

### 訓練相關函數

- **SoVITS 訓練**: `open_sovits_train()` - 第 499 行
- **GPT 訓練**: `open_gpt_train()` - 第 587 行之後
- **關閉訓練**: `close1Ba()`, `close1Bb()` - 第 576, 1854 行

### UI 組件

- **Tab 定義**: 第 1315 行開始
- **按鈕事件綁定**: 文件末尾

## 🎊 總結

GPT-SoVITS 的訓練頁面位於 `webui.py` 文件中，使用 Gradio 框架構建。主要包含：

1. **Tab 0**: 數據預處理（分離、切分、識別）
2. **Tab 1A**: 訓練集格式化（特徵提取）
3. **Tab 1B**: 模型訓練（SoVITS + GPT）
4. **Tab 1C**: 推理測試

整個流程設計完善，從音頻上傳到模型訓練都有圖形化界面支援！

---

**文件**: `GPT-SoVITS-v2pro-20250604/webui.py`  
**總行數**: ~2000 行  
**框架**: Gradio  
**版本**: v2Pro
