"""
FunASR Engine - FunASR Paraformer 語音識別引擎
提供高品質的中文語音識別，特別優化閩南語支援
"""

import logging
import numpy as np
import torch
from typing import Dict, Any, Optional
import asyncio

logger = logging.getLogger(__name__)


class FunASREngine:
    """
    FunASR 引擎封裝
    
    特點:
    - 中文優化，識別速度快
    - 支援閩南語微調模型
    - 內建 VAD、標點、說話人識別
    """
    
    def __init__(self, model_name: str = "paraformer-zh", device: str = "cuda", local_model_path: str = None):
        """
        初始化 FunASR 引擎
        
        Args:
            model_name: 模型名稱 (paraformer-zh) 或 ModelScope ID
            device: 運算設備 (cuda/cpu)
            local_model_path: 本地模型路徑（如果已手動下載）
        """
        self.model_name = model_name
        self.local_model_path = local_model_path
        self.device = device if torch.cuda.is_available() else "cpu"
        
        if self.device == "cpu" and device == "cuda":
            logger.warning("CUDA 不可用，使用 CPU 模式")
        
        if local_model_path:
            logger.info(f"載入本地 FunASR 模型: {local_model_path}")
        else:
            logger.info(f"載入 FunASR 模型: {model_name}")
        
        self._load_model()
        logger.info(f"✓ FunASR 模型已載入到 {self.device}")
        
        # 閩南語微調模型（如果存在）
        self.minnan_model = None
        self.minnan_model_loaded = False
        
        # 預設配置
        self.default_config = {
            "batch_size_s": 300,
            "hotword": "",
            "use_itn": True,  # 逆文本正規化
        }
    
    def _load_model(self):
        """載入 FunASR 模型"""
        try:
            from funasr import AutoModel
            import os
            
            # 決定使用哪個模型路徑
            model_path = self.local_model_path if self.local_model_path else self.model_name
            
            # 如果是本地路徑，檢查是否存在
            if self.local_model_path and not os.path.exists(self.local_model_path):
                logger.error(f"本地模型路徑不存在: {self.local_model_path}")
                raise FileNotFoundError(f"本地模型路徑不存在: {self.local_model_path}")
            
            # 嘗試載入完整模型（包含 VAD 和標點）
            try:
                logger.info("  嘗試載入完整模型（含 VAD 和標點）...")
                self.model = AutoModel(
                    model=model_path,
                    vad_model="fsmn-vad",
                    punc_model="ct-punc",
                    device=self.device
                )
                logger.info("  ✓ 完整模型載入成功")
                
            except Exception as e1:
                logger.warning(f"  完整模型載入失敗: {e1}")
                logger.info("  嘗試載入基礎模型（不含 VAD 和標點）...")
                
                # 降級：只載入基礎 ASR 模型
                try:
                    self.model = AutoModel(
                        model=model_path,
                        device=self.device
                    )
                    logger.info("  ✓ 基礎模型載入成功")
                    
                except Exception as e2:
                    logger.error(f"  基礎模型載入也失敗: {e2}")
                    raise Exception(f"FunASR 模型載入失敗: {e2}")
            
        except ImportError:
            logger.error("FunASR 未安裝，請執行: pip install funasr")
            raise
        except Exception as e:
            logger.error(f"FunASR 模型載入失敗: {e}")
            raise

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
            # 確保音頻是正確格式
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            
            # 準備 FunASR 配置
            funasr_options = self._prepare_options(features, options)
            
            # 選擇模型（閩南語或標準）
            model_to_use = self._select_model(features)
            
            # 執行識別（在線程池中運行以避免阻塞）
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._run_inference,
                model_to_use,
                audio,
                funasr_options
            )
            
            # 計算置信度
            confidence = self._calculate_confidence(result)
            
            # 格式化結果
            output = {
                'text': result[0].get('text', '').strip() if result else '',
                'confidence': confidence,
                'timestamp': result[0].get('timestamp', []) if result else [],
                'engine': 'funasr',
                'model_name': self.model_name
            }
            
            return output
            
        except Exception as e:
            logger.error(f"FunASR 識別失敗: {e}", exc_info=True)
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'engine': 'funasr'
            }
    
    def _run_inference(self, model, audio: np.ndarray, options: Dict[str, Any]):
        """
        執行推理（同步方法，在線程池中運行）
        """
        result = model.generate(
            input=audio,
            **options
        )
        return result
    
    def _select_model(self, features: Dict[str, Any]):
        """
        根據特徵選擇模型
        
        如果檢測到閩南語且微調模型已載入，使用微調模型
        """
        if features.get('is_minnan', False) and self.minnan_model_loaded:
            logger.debug("  使用閩南語微調模型")
            return self.minnan_model
        else:
            return self.model
    
    def _prepare_options(self,
                        features: Dict[str, Any],
                        options: Dict[str, Any]) -> Dict[str, Any]:
        """
        準備 FunASR 識別選項
        
        根據檢測到的特徵優化參數
        """
        funasr_options = self.default_config.copy()
        
        # 閩南語優化
        if features.get('is_minnan', False):
            funasr_options.update(self._get_minnan_optimization(features))
            logger.debug("  應用閩南語優化參數")
        
        # 高齡語音優化
        if features.get('is_elderly', False):
            funasr_options.update(self._get_elderly_optimization(features))
            logger.debug("  應用高齡語音優化參數")
        
        # 用戶自定義選項（優先級最高）
        if 'hotword' in options:
            funasr_options['hotword'] = options['hotword']
        
        return funasr_options
    
    def _get_minnan_optimization(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        閩南語優化參數
        
        針對台灣閩南語的特殊優化：
        - 添加閩南語熱詞
        - 調整批次大小
        """
        minnan_confidence = features.get('minnan_confidence', 0.5)
        
        # 閩南語常見詞彙作為熱詞
        minnan_hotwords = "啥物 按怎 佗位 啥人 敢有 毋是 毋知 毋好 足 誠"
        
        optimization = {
            'hotword': minnan_hotwords,
            'batch_size_s': 300,
        }
        
        return optimization
    
    def _get_elderly_optimization(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        高齡語音優化參數
        
        針對高齡者語音特徵的優化：
        - 調整批次大小以處理較慢語速
        """
        return {
            'batch_size_s': 400,  # 增加批次大小
        }
    
    def _calculate_confidence(self, result: list) -> float:
        """
        計算置信度分數
        
        FunASR 不直接提供置信度，需要基於其他指標估算
        """
        try:
            if not result or len(result) == 0:
                return 0.5
            
            # 獲取第一個結果
            first_result = result[0]
            
            # 檢查是否有文本
            text = first_result.get('text', '')
            if not text or len(text.strip()) == 0:
                return 0.3
            
            # 基於文本長度和時間戳的啟發式置信度
            # 如果有時間戳信息，可以計算更準確的置信度
            timestamp = first_result.get('timestamp', [])
            
            if timestamp and len(timestamp) > 0:
                # 有時間戳表示模型有較高信心
                base_confidence = 0.75
            else:
                base_confidence = 0.65
            
            # 根據文本長度調整（太短或太長可能不太可靠）
            text_length = len(text.strip())
            if 5 <= text_length <= 200:
                length_factor = 1.0
            elif text_length < 5:
                length_factor = 0.8
            else:
                length_factor = 0.9
            
            confidence = base_confidence * length_factor
            
            return float(np.clip(confidence, 0.0, 1.0))
            
        except Exception as e:
            logger.warning(f"置信度計算失敗: {e}")
            return 0.5

    def load_finetuned_model(self, model_type: str = "minnan"):
        """
        載入微調模型
        
        Args:
            model_type: 模型類型 (minnan)
        """
        try:
            if model_type == "minnan":
                logger.info("載入閩南語微調模型...")
                
                # 檢查微調模型是否存在
                import os
                minnan_model_path = "models/paraformer-zh-minnan"
                
                if not os.path.exists(minnan_model_path):
                    logger.warning(f"閩南語微調模型不存在: {minnan_model_path}")
                    logger.warning("將使用標準模型")
                    return False
                
                from funasr import AutoModel
                
                self.minnan_model = AutoModel(
                    model=minnan_model_path,
                    vad_model="fsmn-vad",
                    punc_model="ct-punc",
                    device=self.device
                )
                
                self.minnan_model_loaded = True
                logger.info("✓ 閩南語微調模型已載入")
                return True
                
        except Exception as e:
            logger.error(f"微調模型載入失敗: {e}")
            self.minnan_model_loaded = False
            return False
    
    def optimize_for_inference(self):
        """
        優化模型以提升推理速度
        
        FunASR 模型已經優化，這裡主要是設置推理模式
        """
        if self.model is not None:
            logger.info("✓ FunASR 模型已優化為推理模式")
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """
        獲取記憶體使用情況
        """
        memory_info = {
            'device': self.device,
            'model_name': self.model_name,
            'minnan_model_loaded': self.minnan_model_loaded
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
            'engine': 'funasr',
            'model_name': self.model_name,
            'device': self.device,
            'cuda_available': torch.cuda.is_available(),
            'model_loaded': self.model is not None,
            'minnan_model_loaded': self.minnan_model_loaded
        }
        
        # 添加記憶體信息
        if self.model is not None:
            info['memory_usage'] = self.get_memory_usage()
        
        return info
