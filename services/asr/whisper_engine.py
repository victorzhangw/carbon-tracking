"""
Whisper Engine - OpenAI Whisper 語音識別引擎
提供高品質的多語言語音識別
"""

import logging
import numpy as np
import torch
import whisper
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class WhisperEngine:
    """
    Whisper 引擎封裝
    
    特點:
    - 支援多語言識別
    - 魯棒性強，處理噪音能力好
    - 可針對閩南語和高齡語音優化參數
    """
    
    def __init__(self, model_size: str = "base", device: str = "cuda"):
        """
        初始化 Whisper 引擎
        
        Args:
            model_size: 模型大小 (tiny/base/small/medium/large-v3)
            device: 運算設備 (cuda/cpu)
        """
        self.model_size = model_size
        self.device = device if torch.cuda.is_available() else "cpu"
        
        if self.device == "cpu" and device == "cuda":
            logger.warning("CUDA 不可用，使用 CPU 模式")
        
        logger.info(f"載入 Whisper 模型: {model_size}")
        self.model = whisper.load_model(model_size, device=self.device)
        logger.info(f"✓ Whisper 模型已載入到 {self.device}")
        
        # 預設配置
        self.default_config = {
            "language": "zh",
            "task": "transcribe",
            "beam_size": 5,
            "best_of": 5,
            "temperature": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            "compression_ratio_threshold": 2.4,
            "logprob_threshold": -1.0,
            "no_speech_threshold": 0.6
        }
    
    async def recognize(self,
                       audio: np.ndarray,
                       features: Dict[str, Any],
                       options: Dict[str, Any]) -> Dict[str, Any]:
        """
        識別音頻
        
        Args:
            audio: 音頻數組 (numpy array, 16kHz)
            features: 檢測到的特徵
            options: 選項
        
        Returns:
            識別結果字典
        """
        try:
            # 確保音頻是 float32 類型
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            
            # 準備 Whisper 配置
            whisper_options = self._prepare_options(features, options)
            
            # 執行識別
            result = self.model.transcribe(
                audio,
                **whisper_options
            )
            
            # 計算置信度
            confidence = self._calculate_confidence(result)
            
            # 格式化結果
            output = {
                'text': result.get('text', '').strip(),
                'confidence': confidence,
                'language': result.get('language', 'zh'),
                'segments': result.get('segments', []),
                'engine': 'whisper',
                'model_size': self.model_size
            }
            
            return output
            
        except Exception as e:
            logger.error(f"Whisper 識別失敗: {e}", exc_info=True)
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'engine': 'whisper'
            }
    
    def _prepare_options(self,
                        features: Dict[str, Any],
                        options: Dict[str, Any]) -> Dict[str, Any]:
        """
        準備 Whisper 識別選項
        
        根據檢測到的特徵優化參數
        """
        whisper_options = self.default_config.copy()
        
        # 閩南語優化
        if features.get('is_minnan', False):
            whisper_options['language'] = 'zh'
            whisper_options['initial_prompt'] = "這是台灣閩南語，可能混合華語。"
            whisper_options['temperature'] = 0.2  # 降低溫度提高穩定性
            logger.debug("  應用閩南語優化參數")
        
        # 高齡語音優化
        elif features.get('is_elderly', False):
            whisper_options['temperature'] = 0.2
            whisper_options['beam_size'] = 10  # 增加 beam size
            whisper_options['patience'] = 2.0
            logger.debug("  應用高齡語音優化參數")
        
        # 低 SNR 環境優化
        if features.get('is_low_snr', False):
            whisper_options['compression_ratio_threshold'] = 3.0
            whisper_options['logprob_threshold'] = -1.5
            logger.debug("  應用低 SNR 優化參數")
        
        # 用戶自定義選項
        if 'language' in options:
            whisper_options['language'] = options['language']
        
        return whisper_options
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """
        計算置信度分數
        
        基於 Whisper 的 log probability 和其他指標
        """
        try:
            segments = result.get('segments', [])
            if not segments:
                return 0.5  # 預設值
            
            # 計算平均 log probability
            total_logprob = 0.0
            total_tokens = 0
            
            for segment in segments:
                # Whisper 提供 avg_logprob
                avg_logprob = segment.get('avg_logprob', -1.0)
                tokens = segment.get('tokens', [])
                
                if tokens:
                    total_logprob += avg_logprob * len(tokens)
                    total_tokens += len(tokens)
            
            if total_tokens == 0:
                return 0.5
            
            avg_logprob = total_logprob / total_tokens
            
            # 將 log probability 轉換為 0-1 的置信度
            # log prob 通常在 -2 到 0 之間
            confidence = np.clip((avg_logprob + 2) / 2, 0.0, 1.0)
            
            # 考慮 no_speech_prob
            no_speech_prob = result.get('no_speech_prob', 0.0)
            if no_speech_prob > 0.5:
                confidence *= (1 - no_speech_prob)
            
            return float(confidence)
            
        except Exception as e:
            logger.warning(f"置信度計算失敗: {e}")
            return 0.5
    
    def get_model_info(self) -> Dict[str, Any]:
        """獲取模型信息"""
        return {
            'engine': 'whisper',
            'model_size': self.model_size,
            'device': self.device,
            'cuda_available': torch.cuda.is_available(),
            'model_loaded': self.model is not None
        }
