"""
Minnan Language Detector - 閩南語檢測器
自動檢測音頻中的閩南語成分
"""

import logging
import numpy as np
from typing import Dict, Any, Optional
import re

logger = logging.getLogger(__name__)


class MinnanLanguageDetector:
    """
    閩南語檢測器
    
    功能:
    1. 音頻特徵檢測（基於聲學特徵）
    2. 文本特徵檢測（基於關鍵詞）
    3. 混合程度估計
    4. 綜合判斷
    """
    
    def __init__(self):
        """初始化閩南語檢測器"""
        logger.info("初始化閩南語檢測器...")
        
        # 閩南語特徵詞彙（常見閩南語詞彙）
        self.minnan_keywords = [
            # 疑問詞
            "啥物", "啥", "按怎", "佗位", "啥人", "敢有",
            # 否定詞
            "毋是", "毋知", "毋好", "毋", "無",
            # 程度副詞
            "足", "誠", "真", "蓋",
            # 常用詞
            "欲", "咧", "矣", "啦", "呢", "喔",
            # 動詞
            "食", "行", "講", "看", "聽",
            # 其他
            "阮", "恁", "伊", "咱"
        ]
        
        # 閩南語特徵字符（羅馬拼音標記）
        self.minnan_markers = [
            "ê", "ō", "ó", "ò", "ô",  # 閩南語羅馬拼音
            "á", "à", "â", "ā",
            "ú", "ù", "û", "ū"
        ]
        
        # 語言識別模型（簡化版本，使用啟發式規則）
        # TODO: 未來可以整合更精確的語言識別模型
        self.use_advanced_lid = False
        
        logger.info("✓ 閩南語檢測器初始化完成")
    
    def detect(self, 
               audio: np.ndarray,
               text_hint: Optional[str] = None,
               sample_rate: int = 16000) -> Dict[str, Any]:
        """
        檢測音頻中的閩南語成分
        
        Args:
            audio: 音頻數組 (numpy array)
            text_hint: 文本提示（如果有初步轉錄）
            sample_rate: 採樣率
        
        Returns:
            檢測結果字典
        """
        try:
            # 1. 音頻特徵檢測
            audio_score = self._detect_audio_features(audio, sample_rate)
            
            # 2. 文本特徵檢測
            text_score = 0.0
            if text_hint:
                text_score = self._detect_text_features(text_hint)
            
            # 3. 綜合判斷
            # 如果音頻或文本任一指標超過閾值，判定為閩南語
            is_minnan = (audio_score > 0.5) or (text_score > 0.3)
            
            # 置信度取最大值
            confidence = max(audio_score, text_score)
            
            # 4. 混合程度估計
            mix_ratio = self._estimate_mix_ratio(audio_score, text_score)
            
            result = {
                "is_minnan": is_minnan,
                "confidence": float(confidence),
                "mix_ratio": float(mix_ratio),  # 0=純華語, 1=純閩南語
                "audio_score": float(audio_score),
                "text_score": float(text_score),
                "detection_method": "heuristic"  # 或 "model" 如果使用模型
            }
            
            if is_minnan:
                logger.info(f"  檢測到閩南語 (置信度: {confidence:.3f}, 混合比: {mix_ratio:.3f})")
            
            return result
            
        except Exception as e:
            logger.error(f"閩南語檢測失敗: {e}", exc_info=True)
            return {
                "is_minnan": False,
                "confidence": 0.0,
                "mix_ratio": 0.0,
                "audio_score": 0.0,
                "text_score": 0.0,
                "error": str(e)
            }
    
    def _detect_audio_features(self, audio: np.ndarray, sample_rate: int) -> float:
        """
        基於音頻特徵檢測閩南語
        
        使用啟發式方法：
        1. 音調變化（閩南語有 7-8 個聲調）
        2. 語速特徵
        3. 能量分布
        
        Args:
            audio: 音頻數組
            sample_rate: 採樣率
        
        Returns:
            音頻特徵分數 (0-1)
        """
        try:
            import librosa
            
            # 提取基頻（F0）- 用於分析音調
            f0 = librosa.yin(
                audio,
                fmin=librosa.note_to_hz('C2'),
                fmax=librosa.note_to_hz('C7'),
                sr=sample_rate
            )
            
            # 移除無聲部分（F0 = 0）
            f0_voiced = f0[f0 > 0]
            
            if len(f0_voiced) < 10:
                # 音頻太短或無聲，無法判斷
                return 0.0
            
            # 計算音調變化特徵
            f0_std = np.std(f0_voiced)  # 標準差
            f0_range = np.max(f0_voiced) - np.min(f0_voiced)  # 音調範圍
            
            # 閩南語特徵：音調變化較大
            # 這是簡化的啟發式規則
            tone_variation_score = 0.0
            
            # 標準差較大表示音調變化豐富
            if f0_std > 50:  # 閾值可調整
                tone_variation_score += 0.3
            
            # 音調範圍較大
            if f0_range > 200:  # 閾值可調整
                tone_variation_score += 0.2
            
            # 計算語速特徵（零交叉率）
            zcr = librosa.feature.zero_crossing_rate(audio)[0]
            zcr_mean = np.mean(zcr)
            
            # 閩南語可能有特定的語速特徵
            # 這裡使用簡化規則
            speed_score = 0.0
            if 0.05 < zcr_mean < 0.15:
                speed_score = 0.2
            
            # 綜合分數
            audio_score = tone_variation_score + speed_score
            
            # 限制在 0-1 範圍
            audio_score = np.clip(audio_score, 0.0, 1.0)
            
            return float(audio_score)
            
        except Exception as e:
            logger.warning(f"音頻特徵提取失敗: {e}")
            return 0.0
    
    def _detect_text_features(self, text: str) -> float:
        """
        基於文本特徵檢測閩南語
        
        方法：
        1. 檢測閩南語關鍵詞
        2. 檢測閩南語特徵字符
        3. 計算匹配比例
        
        Args:
            text: 文本內容
        
        Returns:
            文本特徵分數 (0-1)
        """
        if not text or len(text.strip()) == 0:
            return 0.0
        
        text = text.strip()
        text_length = len(text)
        
        # 1. 檢測閩南語關鍵詞
        keyword_count = 0
        for keyword in self.minnan_keywords:
            if keyword in text:
                keyword_count += text.count(keyword)
        
        # 2. 檢測閩南語特徵字符（羅馬拼音）
        marker_count = 0
        for marker in self.minnan_markers:
            if marker in text:
                marker_count += text.count(marker)
        
        # 3. 計算分數
        # 關鍵詞權重較高
        keyword_score = min(keyword_count / max(text_length / 10, 1), 1.0) * 0.7
        
        # 特徵字符權重較低
        marker_score = min(marker_count / max(text_length / 20, 1), 1.0) * 0.3
        
        text_score = keyword_score + marker_score
        
        # 限制在 0-1 範圍
        text_score = np.clip(text_score, 0.0, 1.0)
        
        if text_score > 0.3:
            logger.debug(f"  文本檢測到閩南語特徵: {keyword_count} 個關鍵詞, {marker_count} 個標記")
        
        return float(text_score)
    
    def _estimate_mix_ratio(self, audio_score: float, text_score: float) -> float:
        """
        估計閩南語混合程度
        
        Args:
            audio_score: 音頻特徵分數
            text_score: 文本特徵分數
        
        Returns:
            混合比例 (0=純華語, 1=純閩南語, 0.5=混合)
        """
        # 取兩個分數的平均值作為混合比例
        mix_ratio = (audio_score + text_score) / 2.0
        
        # 調整：如果兩個分數都很高，更傾向於純閩南語
        if audio_score > 0.7 and text_score > 0.7:
            mix_ratio = min(mix_ratio * 1.2, 1.0)
        
        # 如果兩個分數都很低，更傾向於純華語
        elif audio_score < 0.3 and text_score < 0.3:
            mix_ratio = max(mix_ratio * 0.8, 0.0)
        
        return float(np.clip(mix_ratio, 0.0, 1.0))
    
    def add_custom_keywords(self, keywords: list):
        """
        添加自定義閩南語關鍵詞
        
        Args:
            keywords: 關鍵詞列表
        """
        self.minnan_keywords.extend(keywords)
        logger.info(f"添加 {len(keywords)} 個自定義閩南語關鍵詞")
    
    def get_detector_info(self) -> Dict[str, Any]:
        """獲取檢測器信息"""
        return {
            "detector": "minnan_language",
            "version": "1.0.0",
            "method": "heuristic" if not self.use_advanced_lid else "model",
            "keywords_count": len(self.minnan_keywords),
            "markers_count": len(self.minnan_markers)
        }

