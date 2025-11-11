# 音頻人聲分離使用指南

## 功能說明

這個工具可以對音頻檔案進行：

- 人聲與背景音樂分離
- 去除背景噪音（鍵盤聲、鈴聲等）
- 音頻濾波和增強處理
- 支援多種音頻格式（m4a, wav, mp3 等）

## 安裝步驟

### 1. 安裝 Python 套件

```bash
pip install -r requirements_audio_separation.txt
```

### 2. 安裝 FFmpeg（用於音頻格式轉換）

- Windows: 下載 FFmpeg 並加入 PATH 環境變數
- 或使用 chocolatey: `choco install ffmpeg`

## 使用方法

### 方法一：處理指定檔案

直接運行專用腳本：

```bash
python process_03041966_audio.py
```

### 方法二：通用處理

```bash
python audio_voice_separation.py "D:\python\Flask-AICares\TTS\03041966.m4a"
```

### 方法三：指定輸出目錄

```bash
python audio_voice_separation.py "D:\python\Flask-AICares\TTS\03041966.m4a" --output-dir "D:\output"
```

## 輸出檔案說明

處理完成後會在 `separated_audio` 目錄下生成以下檔案：

1. **05_vocals_final_enhanced.wav** - 🎯 **最終人聲（推薦使用）**

   - 經過完整處理的人聲，去除了背景噪音和音樂

2. **03_vocals_noise_reduced.wav** - 去噪後的人聲

   - 基本的噪音減少處理

3. **06_background_music.wav** - 背景音樂和噪音

   - 分離出的非人聲部分

4. **其他檔案** - 處理過程中的中間結果
   - 用於調試和比較效果

## 處理流程

1. **格式轉換**: m4a → wav
2. **人聲分離**: 使用 HPSS 和頻譜遮罩技術
3. **噪音減少**: 使用 spectral gating 技術
4. **濾波處理**: 高通、帶阻、低通濾波器
5. **人聲增強**: 正規化和動態範圍壓縮

## 技術特點

- **多層次處理**: 結合多種音頻處理技術
- **智能噪音檢測**: 自動識別和去除常見噪音
- **頻率濾波**: 針對特定頻率範圍的噪音進行處理
- **人聲增強**: 提升最終人聲的清晰度

## 故障排除

### 常見問題

1. **ImportError**: 缺少套件 → 執行 `pip install -r requirements_audio_separation.txt`
2. **FFmpeg 錯誤**: 未安裝 FFmpeg → 安裝 FFmpeg 並加入 PATH
3. **記憶體不足**: 音頻檔案太大 → 嘗試分段處理

### 效果調整

如果效果不理想，可以修改 `audio_voice_separation.py` 中的參數：

- `prop_decrease`: 噪音減少強度（0.6-0.9）
- `margin_i`, `margin_v`: 人聲分離敏感度
- 濾波器頻率範圍

## 注意事項

- 處理時間取決於音頻長度和電腦效能
- 建議在處理前備份原始檔案
- 不同類型的音頻可能需要調整參數以獲得最佳效果
