"""
P0-1: 雙引擎 ASR 系統
整合 Whisper 和 FunASR 引擎，提供高準確率的語音識別服務
"""

from .coordinator import ASRCoordinator
from .whisper_engine import WhisperEngine
# from .funasr_engine import FunASREngine  # 待 FunASR 模型下載完成後啟用
from .fusion import ConfidenceFusion

__all__ = [
    'ASRCoordinator',
    'WhisperEngine',
    # 'FunASREngine',
    'ConfidenceFusion',
]

__version__ = '1.0.0'
