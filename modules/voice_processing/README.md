# Voice Processing Module

## Purpose

語音處理模組提供語音克隆、語音合成、情緒識別等 AI 語音處理功能。

## Contents

- `voice_clone_service.py` - 語音克隆服務
- `voice_synthesis_service.py` - 語音合成服務
- `simple_voice_api.py` - 簡化版語音 API
- `voice_config.py` - 語音處理配置
- `database_emotion_extension.py` - 情緒資料庫擴展

## Related Components

- **Services**: `services/gpt_sovits_service.py`, `services/tts.py` - 語音服務層
- **Assets**: `assets/audio/` - 音訊資源
- **Templates**: `templates/voice_*.html` - 語音互動頁面

## Usage

### Voice Cloning

```python
from modules.voice_processing.voice_clone_service import clone_voice

# 克隆語音
result = clone_voice(
    reference_audio="path/to/reference.wav",
    text="要合成的文字內容"
)
```

### Voice Synthesis

```python
from modules.voice_processing.voice_synthesis_service import synthesize_speech

# 合成語音
audio_data = synthesize_speech(
    text="你好，我是 AI 助手",
    emotion="friendly"
)
```

### Configuration

```python
from modules.voice_processing.voice_config import get_voice_config

# 取得語音配置
config = get_voice_config()
```

## Features

- GPT-SoVITS 語音克隆
- F5-TTS 語音合成
- 情緒識別與分類
- 音訊處理與優化
- 語音資料集驗證

## Technical Documentation

詳細技術文檔請參考：

- `docs/technical/voice/` - 語音處理技術文檔
- `docs/guides/voice_clone_guide.md` - 語音克隆使用指南
