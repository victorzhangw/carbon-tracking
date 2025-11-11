# ASR (Automatic Speech Recognition) Module

## Purpose

自動語音識別模組提供雙引擎 ASR 系統，支援 Whisper 和 FunASR 引擎，並具備台語和高齡者語音檢測功能。

## Architecture

本模組採用雙引擎架構：

- **Whisper Engine**: 通用語音識別，支援多語言
- **FunASR Engine**: 專門針對中文和台語優化

## Related Components

- **Services**: `services/asr/` - ASR 服務實作

  - `coordinator.py` - ASR 協調器，管理雙引擎切換
  - `whisper_engine.py` - Whisper 引擎實作
  - `funasr_engine.py` - FunASR 引擎實作
  - `elderly_detector.py` - 高齡者語音檢測
  - `minnan_detector.py` - 台語檢測
  - `fusion.py` - 結果融合策略

- **Routes**: `routes/asr.py` - ASR API 端點

- **Tests**:
  - `tests/unit/test_elderly_detector.py`
  - `tests/unit/test_minnan_detector.py`
  - `tests/integration/test_asr_coordinator.py`
  - `tests/integration/test_funasr_engine.py`
  - `tests/integration/test_asr_api.py`
  - `tests/performance/test_asr_performance.py`

## Usage

### Basic ASR

```python
from services.asr.coordinator import ASRCoordinator

# 初始化 ASR 協調器
coordinator = ASRCoordinator()

# 語音識別
result = coordinator.transcribe(
    audio_file="path/to/audio.wav",
    language="zh"
)

print(result['text'])
print(result['engine'])  # 使用的引擎
```

### Elderly Detection

```python
from services.asr.elderly_detector import detect_elderly_speech

# 檢測是否為高齡者語音
is_elderly = detect_elderly_speech(audio_file="path/to/audio.wav")
```

### Minnan Detection

```python
from services.asr.minnan_detector import detect_minnan

# 檢測是否包含台語
is_minnan = detect_minnan(audio_file="path/to/audio.wav")
```

## Features

- **雙引擎架構**: Whisper + FunASR
- **智能引擎選擇**: 根據語音特徵自動選擇最佳引擎
- **台語檢測**: 自動識別台語內容
- **高齡者語音優化**: 針對高齡者語音特徵優化
- **結果融合**: 多引擎結果智能融合
- **效能監控**: 完整的效能測試和監控

## API Endpoints

```
POST /asr/transcribe
- 語音轉文字

POST /asr/detect-elderly
- 高齡者語音檢測

POST /asr/detect-minnan
- 台語檢測
```

## Configuration

ASR 配置位於 `config.py` 中：

- `WHISPER_MODEL`: Whisper 模型選擇
- `FUNASR_MODEL`: FunASR 模型選擇
- `ASR_ENGINE`: 預設引擎選擇

## Technical Documentation

詳細技術文檔請參考：

- `docs/technical/asr/` - ASR 技術文檔
- `.kiro/specs/p0-dual-engine-asr/` - 雙引擎 ASR 規格文檔

## Performance

- Whisper: 適合通用場景，多語言支援
- FunASR: 中文和台語場景效能更佳
- 雙引擎融合: 提供最佳識別準確度

## Setup

詳見 `docs/technical/asr/setup_asr_environment.md`
