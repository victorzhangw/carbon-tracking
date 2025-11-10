"""
Elderly Voice Detector - 高齡語音檢測器
自動檢測音頻中的高齡語音特徵
"""

import logging
import numpy as np
from typing import Dict, Any
import librosa

logger = logging.getLogger(__name__)


class ElderlyVoiceDetector:
    """
    高齡語音檢測器
    
    功能:
    1. 語速檢測（高齡者通常語速較慢）
    2. 音量檢測（高齡者可能音量較小）
    3. 顫抖檢測（聲音顫抖特徵）
    4. 停頓檢測（停頓較多、較長）
    5. 綜合判斷
    
    高齡語音特徵:
    - 語速較慢（每秒音節數較少）
    - 音量較小或不穩定
    - 聲音可能有顫抖
    - 停頓較多、較長
    - 音調範圍可能較窄
    """
    
    def __init__(self):
        """初始化高齡語音檢測器"""
        logger.info("初始化高齡語音檢測器...")
        
        # 檢測閾值（可調整）
        self.thresholds = {
            'speech_rate_low': 2.5,  # 每秒音節數下限
            'speech_rate_high': 4.5,  # 每秒音節數上限（正常 4-6）
            'volume_low': 0.02,  # 音量下限
            'volume_std_high': 0.15,  # 音量標準差上限
            'tremor_freq_low': 4.0,  # 顫抖頻率下限 (Hz)
            'tremor_freq_high': 8.0,  # 顫抖頻率上限 (Hz)
            'pause_ratio_high': 0.4,  # 停頓比例上限
            'pitch_range_low': 100,  # 音調範圍下限 (Hz)
        }
        
        logger.info("✓ 高齡語音檢測器初始化完成")
    
    def detect(self, 
               audio: np.ndarray,
               sample_rate: int = 16000) -> Dict[str, Any]:
        """
        檢測音頻中的高齡語音特徵
        
        Args:
            audio: 音頻數組 (numpy array)
            sample_rate: 採樣率
        
        Returns:
            檢測結果字典
        """
        try:
            # 1. 語速檢測
            speech_rate, speech_rate_score = self._detect_speech_rate(audio, sample_rate)
            
            # 2. 音量檢測
            volume_mean, volume_std, volume_score = self._detect_volume(audio)
            
            # 3. 顫抖檢測
            tremor_detected, tremor_score = self._detect_tremor(audio, sample_rate)
            
            # 4. 停頓檢測
            pause_ratio, pause_score = self._detect_pauses(audio, sample_rate)
            
            # 5. 音調範圍檢測
            pitch_range, pitch_score = self._detect_pitch_range(audio, sample_rate)
            
            # 6. 綜合判斷
            # 計算總分（各項特徵加權）
            total_score = (
                speech_rate_score * 0.25 +
                volume_score * 0.20 +
                tremor_score * 0.20 +
                pause_score * 0.20 +
                pitch_score * 0.15
            )
            
            # 判定閾值
            is_elderly = total_score > 0.5
            confidence = total_score
            
            result = {
                "is_elderly": is_elderly,
                "confidence": float(confidence),
                "features": {
                    "speech_rate": float(speech_rate),
                    "speech_rate_score": float(speech_rate_score),
                    "volume_mean": float(volume_mean),
                    "volume_std": float(volume_std),
                    "volume_score": float(volume_score),
                    "tremor_detected": tremor_detected,
                    "tremor_score": float(tremor_score),
                    "pause_ratio": float(pause_ratio),
                    "pause_score": float(pause_score),
                    "pitch_range": float(pitch_range),
                    "pitch_score": float(pitch_score)
                },
                "detection_method": "acoustic_features"
            }
            
            if is_elderly:
                logger.info(f"  檢測到高齡語音 (置信度: {confidence:.3f})")
            
            return result
            
        except Exception as e:
            logger.error(f"高齡語音檢測失敗: {e}", exc_info=True)
            return {
                "is_elderly": False,
                "confidence": 0.0,
                "features": {},
                "error": str(e)
            }
    
    def _detect_speech_rate(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """
        檢測語速
        
        使用零交叉率和能量包絡估算語速
        高齡者通常語速較慢
        
        Returns:
            (語速, 分數)
        """
        try:
            # 計算能量包絡
            hop_length = 512
            frame_length = 2048
            
            # RMS 能量
            rms = librosa.feature.rms(
                y=audio,
                frame_length=frame_length,
                hop_length=hop_length
            )[0]
            
            # 檢測語音段（能量高於閾值）
            threshold = np.mean(rms) * 0.5
            speech_frames = rms > threshold
            
            # 計算語音段的數量（近似音節數）
            # 使用形態學操作去除短暫的噪音
            from scipy import ndimage
            speech_frames_filtered = ndimage.binary_closing(speech_frames, structure=np.ones(5))
            
            # 計算語音段邊界
            diff = np.diff(speech_frames_filtered.astype(int))
            speech_onsets = np.where(diff == 1)[0]
            
            # 估算語速（每秒音節數）
            duration = len(audio) / sample_rate
            syllable_count = len(speech_onsets)
            speech_rate = syllable_count / duration if duration > 0 else 0
            
            # 計算分數
            # 語速越慢，分數越高（表示越可能是高齡語音）
            if speech_rate < self.thresholds['speech_rate_low']:
                score = 1.0  # 非常慢
            elif speech_rate < self.thresholds['speech_rate_high']:
                # 線性插值
                score = 1.0 - (speech_rate - self.thresholds['speech_rate_low']) / \
                        (self.thresholds['speech_rate_high'] - self.thresholds['speech_rate_low'])
            else:
                score = 0.0  # 正常或快速
            
            return speech_rate, score
            
        except Exception as e:
            logger.warning(f"語速檢測失敗: {e}")
            return 0.0, 0.0
    
    def _detect_volume(self, audio: np.ndarray) -> tuple:
        """
        檢測音量特徵
        
        高齡者可能音量較小或不穩定
        
        Returns:
            (平均音量, 音量標準差, 分數)
        """
        try:
            # 計算 RMS 能量（音量）
            rms = np.sqrt(np.mean(audio**2))
            
            # 計算音量變化（標準差）
            frame_length = 2048
            hop_length = 512
            rms_frames = librosa.feature.rms(
                y=audio,
                frame_length=frame_length,
                hop_length=hop_length
            )[0]
            rms_std = np.std(rms_frames)
            
            # 計算分數
            volume_score = 0.0
            
            # 音量較小
            if rms < self.thresholds['volume_low']:
                volume_score += 0.5
            
            # 音量不穩定（標準差大）
            if rms_std > self.thresholds['volume_std_high']:
                volume_score += 0.5
            
            return rms, rms_std, volume_score
            
        except Exception as e:
            logger.warning(f"音量檢測失敗: {e}")
            return 0.0, 0.0, 0.0
    
    def _detect_tremor(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """
        檢測聲音顫抖
        
        高齡者聲音可能有 4-8 Hz 的顫抖
        
        Returns:
            (是否檢測到顫抖, 分數)
        """
        try:
            # 提取基頻（F0）
            f0 = librosa.yin(
                audio,
                fmin=librosa.note_to_hz('C2'),
                fmax=librosa.note_to_hz('C7'),
                sr=sample_rate
            )
            
            # 移除無聲部分
            f0_voiced = f0[f0 > 0]
            
            if len(f0_voiced) < 20:
                return False, 0.0
            
            # 計算 F0 的頻譜（檢測週期性變化）
            f0_fft = np.fft.fft(f0_voiced - np.mean(f0_voiced))
            f0_power = np.abs(f0_fft[:len(f0_fft)//2])**2
            
            # 頻率軸
            hop_length = 512
            frame_rate = sample_rate / hop_length
            freqs = np.fft.fftfreq(len(f0_voiced), 1/frame_rate)[:len(f0_fft)//2]
            
            # 檢測 4-8 Hz 範圍的能量
            tremor_range = (freqs >= self.thresholds['tremor_freq_low']) & \
                          (freqs <= self.thresholds['tremor_freq_high'])
            
            if np.any(tremor_range):
                tremor_power = np.max(f0_power[tremor_range])
                total_power = np.sum(f0_power)
                
                # 顫抖能量比例
                tremor_ratio = tremor_power / total_power if total_power > 0 else 0
                
                # 判定
                tremor_detected = tremor_ratio > 0.1
                score = min(tremor_ratio * 5, 1.0)  # 歸一化到 0-1
                
                return tremor_detected, score
            
            return False, 0.0
            
        except Exception as e:
            logger.warning(f"顫抖檢測失敗: {e}")
            return False, 0.0
    
    def _detect_pauses(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """
        檢測停頓特徵
        
        高齡者可能停頓較多、較長
        
        Returns:
            (停頓比例, 分數)
        """
        try:
            # 計算能量
            hop_length = 512
            frame_length = 2048
            rms = librosa.feature.rms(
                y=audio,
                frame_length=frame_length,
                hop_length=hop_length
            )[0]
            
            # 檢測靜音段（能量低於閾值）
            threshold = np.mean(rms) * 0.3
            silence_frames = rms < threshold
            
            # 計算停頓比例
            pause_ratio = np.sum(silence_frames) / len(silence_frames)
            
            # 計算分數
            # 停頓比例越高，分數越高
            if pause_ratio > self.thresholds['pause_ratio_high']:
                score = 1.0
            else:
                score = pause_ratio / self.thresholds['pause_ratio_high']
            
            return pause_ratio, score
            
        except Exception as e:
            logger.warning(f"停頓檢測失敗: {e}")
            return 0.0, 0.0
    
    def _detect_pitch_range(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """
        檢測音調範圍
        
        高齡者音調範圍可能較窄
        
        Returns:
            (音調範圍, 分數)
        """
        try:
            # 提取基頻
            f0 = librosa.yin(
                audio,
                fmin=librosa.note_to_hz('C2'),
                fmax=librosa.note_to_hz('C7'),
                sr=sample_rate
            )
            
            # 移除無聲部分
            f0_voiced = f0[f0 > 0]
            
            if len(f0_voiced) < 10:
                return 0.0, 0.0
            
            # 計算音調範圍
            pitch_range = np.max(f0_voiced) - np.min(f0_voiced)
            
            # 計算分數
            # 音調範圍越窄，分數越高
            if pitch_range < self.thresholds['pitch_range_low']:
                score = 1.0
            else:
                score = max(0.0, 1.0 - (pitch_range - self.thresholds['pitch_range_low']) / 200)
            
            return pitch_range, score
            
        except Exception as e:
            logger.warning(f"音調範圍檢測失敗: {e}")
            return 0.0, 0.0
    
    def update_thresholds(self, new_thresholds: Dict[str, float]):
        """
        更新檢測閾值
        
        Args:
            new_thresholds: 新的閾值字典
        """
        self.thresholds.update(new_thresholds)
        logger.info(f"更新檢測閾值: {new_thresholds}")
    
    def get_detector_info(self) -> Dict[str, Any]:
        """獲取檢測器信息"""
        return {
            "detector": "elderly_voice",
            "version": "1.0.0",
            "method": "acoustic_features",
            "thresholds": self.thresholds
        }
