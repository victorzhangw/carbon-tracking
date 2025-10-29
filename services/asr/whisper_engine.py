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
            whisper_options.update(self._get_minnan_optimization(features))
            logger.debug("  應用閩南語優化參數")
        
        # 高齡語音優化
        elif features.get('is_elderly', False):
            whisper_options.update(self._get_elderly_optimization(features))
            logger.debug("  應用高齡語音優化參數")
        
        # 低 SNR 環境優化
        if features.get('is_low_snr', False):
            whisper_options.update(self._get_low_snr_optimization(features))
            logger.debug("  應用低 SNR 優化參數")
        
        # 用戶自定義選項（優先級最高）
        if 'language' in options:
            whisper_options['language'] = options['language']
        if 'initial_prompt' in options:
            whisper_options['initial_prompt'] = options['initial_prompt']
        
        return whisper_options
    
    def _get_minnan_optimization(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        閩南語優化參數
        
        針對台灣閩南語的特殊優化：
        - 使用中文語言模式
        - 添加閩南語提示詞
        - 降低溫度提高穩定性
        - 增加 beam size 提高準確率
        """
        minnan_confidence = features.get('minnan_confidence', 0.5)
        
        # 基礎閩南語優化
        optimization = {
            'language': 'zh',
            'temperature': 0.2,  # 降低溫度
            'beam_size': 8,  # 增加 beam size
            'best_of': 8,
            'patience': 1.5,
        }
        
        # 根據閩南語置信度調整提示詞
        if minnan_confidence > 0.7:
            # 高置信度：純閩南語
            optimization['initial_prompt'] = (
                "這是台灣閩南語。常見詞彙：啥物、按怎、佗位、啥人、敢有、"
                "毋是、毋知、毋好、足、誠。"
            )
        elif minnan_confidence > 0.4:
            # 中等置信度：混合語音
            optimization['initial_prompt'] = (
                "這是台灣閩南語與華語混合的對話。"
            )
        else:
            # 低置信度：閩南語口音的華語
            optimization['initial_prompt'] = (
                "這是帶有閩南語口音的華語。"
            )
        
        return optimization
    
    def _get_elderly_optimization(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        高齡語音優化參數
        
        針對高齡者語音特徵的優化：
        - 語速較慢
        - 音量較小
        - 可能有顫抖
        - 停頓較多
        """
        return {
            'temperature': 0.2,  # 降低溫度提高穩定性
            'beam_size': 10,  # 增加 beam size
            'best_of': 10,
            'patience': 2.0,  # 增加耐心值
            'compression_ratio_threshold': 2.8,  # 放寬壓縮比閾值
            'logprob_threshold': -1.2,  # 放寬 log prob 閾值
            'no_speech_threshold': 0.5,  # 降低無語音閾值
            'condition_on_previous_text': True,  # 利用上下文
        }
    
    def _get_low_snr_optimization(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        低 SNR 環境優化參數
        
        針對噪音環境的優化：
        - 放寬各種閾值
        - 增加解碼策略的多樣性
        - 利用上下文信息
        """
        snr_db = features.get('snr_db', 0)
        
        # 基礎低 SNR 優化
        optimization = {
            'compression_ratio_threshold': 3.0,
            'logprob_threshold': -1.5,
            'no_speech_threshold': 0.7,  # 提高無語音閾值
            'condition_on_previous_text': True,
        }
        
        # 根據 SNR 級別調整
        if snr_db < -30:  # 極低 SNR
            optimization.update({
                'temperature': [0.0, 0.2, 0.4],  # 減少溫度範圍
                'beam_size': 10,
                'best_of': 10,
            })
        elif snr_db < -20:  # 很低 SNR
            optimization.update({
                'temperature': [0.0, 0.2, 0.4, 0.6],
                'beam_size': 8,
            })
        
        return optimization
    
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
    
    def optimize_for_inference(self):
        """
        優化模型以提升推理速度
        
        包括：
        - 設置為評估模式
        - 禁用梯度計算
        - 使用 torch.inference_mode
        """
        if self.model is not None:
            self.model.eval()
            for param in self.model.parameters():
                param.requires_grad = False
            logger.info("✓ 模型已優化為推理模式")
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """
        獲取記憶體使用情況
        """
        memory_info = {
            'device': self.device,
            'model_size': self.model_size
        }
        
        if self.device == 'cuda' and torch.cuda.is_available():
            memory_info.update({
                'gpu_memory_allocated': f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB",
                'gpu_memory_reserved': f"{torch.cuda.memory_reserved() / 1024**3:.2f} GB",
                'gpu_memory_total': f"{torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB"
            })
        
        return memory_info
    
    def clear_cache(self):
        """
        清理 GPU 快取
        """
        if self.device == 'cuda' and torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("✓ GPU 快取已清理")
    
    def get_model_info(self) -> Dict[str, Any]:
        """獲取模型信息"""
        info = {
            'engine': 'whisper',
            'model_size': self.model_size,
            'device': self.device,
            'cuda_available': torch.cuda.is_available(),
            'model_loaded': self.model is not None
        }
        
        # 添加記憶體信息
        if self.model is not None:
            info['memory_usage'] = self.get_memory_usage()
        
        return info
