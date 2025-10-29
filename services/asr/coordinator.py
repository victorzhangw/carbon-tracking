"""
ASR Coordinator - 協調雙引擎 ASR 工作流程
負責音頻預處理、引擎調度、結果融合和後處理
"""

import asyncio
import time
import logging
from typing import Dict, Any, Optional, Tuple
import numpy as np
import librosa
import soundfile as sf

from .whisper_engine import WhisperEngine
# from .funasr_engine import FunASREngine  # 待啟用
from .fusion import ConfidenceFusion

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ASRCoordinator:
    """
    ASR 協調器 - 管理雙引擎 ASR 工作流程
    
    職責:
    1. 音頻預處理（格式轉換、重採樣、降噪）
    2. 特徵檢測（閩南語、高齡語音、低SNR）
    3. 並行調度雙引擎
    4. 結果融合
    5. 後處理與格式化
    """
    
    def __init__(self, 
                 whisper_model_size: str = "base",
                 enable_funasr: bool = False,
                 device: str = "cuda"):
        """
        初始化 ASR Coordinator
        
        Args:
            whisper_model_size: Whisper 模型大小 (tiny/base/small/medium/large-v3)
            enable_funasr: 是否啟用 FunASR 引擎
            device: 運算設備 (cuda/cpu)
        """
        logger.info("初始化 ASR Coordinator...")
        
        # 初始化 Whisper 引擎
        self.whisper_engine = WhisperEngine(
            model_size=whisper_model_size,
            device=device
        )
        logger.info(f"✓ Whisper 引擎已載入 (模型: {whisper_model_size}, 設備: {device})")
        
        # 初始化 FunASR 引擎（如果啟用）
        self.funasr_engine = None
        self.enable_funasr = enable_funasr
        if enable_funasr:
            try:
                # from .funasr_engine import FunASREngine
                # self.funasr_engine = FunASREngine(device=device)
                logger.warning("FunASR 引擎暫時未啟用（模型下載問題）")
                self.enable_funasr = False
            except Exception as e:
                logger.warning(f"FunASR 引擎載入失敗: {e}")
                self.enable_funasr = False
        
        # 初始化融合算法
        self.fusion_algorithm = ConfidenceFusion()
        
        # 配置參數
        self.target_sample_rate = 16000  # 目標採樣率
        self.max_audio_length = 60  # 最大音頻長度（秒）
        
        # 優化模型推理
        self.whisper_engine.optimize_for_inference()
        
        logger.info("✓ ASR Coordinator 初始化完成")
    
    async def recognize(self, 
                       audio_data: bytes,
                       options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        識別音頻
        
        Args:
            audio_data: 音頻數據（bytes）
            options: 可選參數
                - language_hint: 語言提示 (zh/zh-TW/minnan)
                - return_details: 是否返回詳細信息
                - enable_minnan_optimization: 是否啟用閩南語優化
        
        Returns:
            識別結果字典
        """
        start_time = time.time()
        options = options or {}
        
        try:
            # 1. 音頻預處理
            logger.info("步驟 1: 音頻預處理...")
            processed_audio, audio_info = self.preprocess_audio(audio_data)
            
            # 2. 特徵檢測
            logger.info("步驟 2: 特徵檢測...")
            features = self.detect_features(processed_audio, audio_info, options)
            
            # 3. 並行調用引擎
            logger.info("步驟 3: 並行調用 ASR 引擎...")
            if self.enable_funasr and self.funasr_engine:
                # 雙引擎模式
                whisper_result, funasr_result = await asyncio.gather(
                    self._call_whisper(processed_audio, features, options),
                    self._call_funasr(processed_audio, features, options)
                )
            else:
                # 單引擎模式（僅 Whisper）
                whisper_result = await self._call_whisper(processed_audio, features, options)
                funasr_result = None
            
            # 4. 結果融合
            logger.info("步驟 4: 結果融合...")
            final_result = self.fusion_algorithm.fuse(
                whisper_result,
                funasr_result,
                features
            )
            
            # 5. 後處理
            logger.info("步驟 5: 後處理...")
            output = self.postprocess_result(
                final_result,
                features,
                audio_info,
                options
            )
            
            # 添加處理時間
            processing_time = time.time() - start_time
            output['processing_time'] = round(processing_time, 3)
            
            logger.info(f"✓ 識別完成 (耗時: {processing_time:.3f}秒)")
            return output
            
        except Exception as e:
            logger.error(f"識別過程發生錯誤: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def preprocess_audio(self, audio_data: bytes) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        音頻預處理
        
        Args:
            audio_data: 原始音頻數據
        
        Returns:
            (處理後的音頻數組, 音頻信息字典)
        """
        try:
            # 載入音頻
            import io
            audio, sr = sf.read(io.BytesIO(audio_data))
            
            # 如果是立體聲，轉為單聲道
            if len(audio.shape) > 1:
                audio = np.mean(audio, axis=1)
            
            # 重採樣到目標採樣率
            if sr != self.target_sample_rate:
                audio = librosa.resample(
                    audio,
                    orig_sr=sr,
                    target_sr=self.target_sample_rate
                )
                sr = self.target_sample_rate
            
            # 音頻長度檢查
            duration = len(audio) / sr
            if duration > self.max_audio_length:
                logger.warning(f"音頻過長 ({duration:.1f}秒)，將截取前 {self.max_audio_length} 秒")
                audio = audio[:self.max_audio_length * sr]
                duration = self.max_audio_length
            
            # 正規化
            if np.max(np.abs(audio)) > 0:
                audio = audio / np.max(np.abs(audio))
            
            # 音頻信息
            audio_info = {
                'sample_rate': sr,
                'duration': duration,
                'samples': len(audio),
                'channels': 1
            }
            
            logger.info(f"  音頻預處理完成: {duration:.2f}秒, {sr}Hz")
            return audio, audio_info
            
        except Exception as e:
            logger.error(f"音頻預處理失敗: {e}")
            raise
    
    def detect_features(self, 
                       audio: np.ndarray,
                       audio_info: Dict[str, Any],
                       options: Dict[str, Any]) -> Dict[str, Any]:
        """
        檢測音頻特徵
        
        Args:
            audio: 音頻數組
            audio_info: 音頻信息
            options: 選項
        
        Returns:
            特徵字典
        """
        features = {
            'is_minnan': False,
            'is_elderly': False,
            'is_low_snr': False,
            'language_hint': options.get('language_hint', 'zh'),
            'minnan_confidence': 0.0,
            'elderly_confidence': 0.0,
            'snr_db': 0.0
        }
        
        try:
            # 計算 SNR（信噪比）
            # 簡化版本：使用 RMS 能量估計
            rms_energy = np.sqrt(np.mean(audio**2))
            features['snr_db'] = 20 * np.log10(rms_energy + 1e-10)
            
            # 低 SNR 檢測
            if features['snr_db'] < -20:  # 閾值可調整
                features['is_low_snr'] = True
                logger.info("  檢測到低 SNR 環境")
            
            # 語言提示檢測
            if options.get('language_hint') in ['minnan', 'zh-TW']:
                features['is_minnan'] = True
                features['minnan_confidence'] = 0.8
                logger.info("  根據語言提示，啟用閩南語優化")
            
            # TODO: 實現更精確的閩南語檢測器（任務 5.1）
            # TODO: 實現高齡語音檢測器（任務 6.1）
            
        except Exception as e:
            logger.warning(f"特徵檢測部分失敗: {e}")
        
        return features
    
    async def _call_whisper(self,
                           audio: np.ndarray,
                           features: Dict[str, Any],
                           options: Dict[str, Any]) -> Dict[str, Any]:
        """調用 Whisper 引擎"""
        try:
            result = await self.whisper_engine.recognize(audio, features, options)
            logger.info(f"  Whisper: '{result.get('text', '')[:50]}...' (置信度: {result.get('confidence', 0):.3f})")
            return result
        except Exception as e:
            logger.error(f"Whisper 引擎錯誤: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e)
            }
    
    async def _call_funasr(self,
                          audio: np.ndarray,
                          features: Dict[str, Any],
                          options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """調用 FunASR 引擎"""
        if not self.funasr_engine:
            return None
        
        try:
            result = await self.funasr_engine.recognize(audio, features, options)
            logger.info(f"  FunASR: '{result.get('text', '')[:50]}...' (置信度: {result.get('confidence', 0):.3f})")
            return result
        except Exception as e:
            logger.error(f"FunASR 引擎錯誤: {e}")
            return None
    
    def postprocess_result(self,
                          final_result: Dict[str, Any],
                          features: Dict[str, Any],
                          audio_info: Dict[str, Any],
                          options: Dict[str, Any]) -> Dict[str, Any]:
        """
        後處理結果
        
        Args:
            final_result: 融合後的結果
            features: 檢測到的特徵
            audio_info: 音頻信息
            options: 選項
        
        Returns:
            格式化的輸出
        """
        output = {
            'success': True,
            'text': final_result.get('text', ''),
            'confidence': final_result.get('confidence', 0.0),
            'language': features.get('language_hint', 'zh'),
            'audio_duration': audio_info.get('duration', 0.0)
        }
        
        # 如果需要詳細信息
        if options.get('return_details', False):
            output['details'] = {
                'features': features,
                'audio_info': audio_info,
                'fusion_info': final_result.get('fusion_info', {}),
                'engine_results': {
                    'whisper': final_result.get('whisper_result'),
                    'funasr': final_result.get('funasr_result')
                }
            }
        
        return output

    
    async def recognize_batch(self,
                            audio_data_list: list,
                            options: Optional[Dict[str, Any]] = None) -> list:
        """
        批次識別多個音頻
        
        Args:
            audio_data_list: 音頻數據列表
            options: 可選參數
        
        Returns:
            識別結果列表
        """
        logger.info(f"開始批次識別 {len(audio_data_list)} 個音頻...")
        
        # 並行處理所有音頻
        tasks = [
            self.recognize(audio_data, options)
            for audio_data in audio_data_list
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 處理異常
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"音頻 {i} 識別失敗: {result}")
                processed_results.append({
                    'success': False,
                    'error': str(result),
                    'index': i
                })
            else:
                result['index'] = i
                processed_results.append(result)
        
        logger.info(f"✓ 批次識別完成")
        return processed_results
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        獲取系統信息
        """
        info = {
            'coordinator': {
                'version': '1.0.0',
                'enable_funasr': self.enable_funasr,
                'target_sample_rate': self.target_sample_rate,
                'max_audio_length': self.max_audio_length
            },
            'whisper_engine': self.whisper_engine.get_model_info()
        }
        
        if self.funasr_engine:
            info['funasr_engine'] = self.funasr_engine.get_model_info()
        
        return info
    
    def clear_cache(self):
        """清理快取"""
        self.whisper_engine.clear_cache()
        if self.funasr_engine:
            self.funasr_engine.clear_cache()
        logger.info("✓ 系統快取已清理")
