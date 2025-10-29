"""
Confidence Fusion - 置信度加權融合算法
智能結合多個 ASR 引擎的輸出
"""

import logging
from typing import Dict, Any, Optional
import difflib

logger = logging.getLogger(__name__)


class ConfidenceFusion:
    """
    置信度融合算法
    
    策略:
    1. 基於置信度的動態權重
    2. 考慮語言特徵（閩南語偏好 FunASR）
    3. 文本相似度分析
    4. 智能降級（單引擎失敗時）
    """
    
    def __init__(self):
        """初始化融合算法"""
        # 基礎權重配置
        self.default_weights = {
            'whisper': 0.5,
            'funasr': 0.5
        }
        
        # 閩南語場景權重
        self.minnan_weights = {
            'whisper': 0.4,
            'funasr': 0.6  # FunASR 微調後對閩南語更準確
        }
        
        # 置信度閾值
        self.high_confidence_threshold = 0.9
        self.low_confidence_threshold = 0.7
    
    def fuse(self,
             whisper_result: Dict[str, Any],
             funasr_result: Optional[Dict[str, Any]],
             features: Dict[str, Any]) -> Dict[str, Any]:
        """
        融合多個引擎的結果
        
        Args:
            whisper_result: Whisper 引擎結果
            funasr_result: FunASR 引擎結果（可能為 None）
            features: 檢測到的特徵
        
        Returns:
            融合後的結果
        """
        # 單引擎模式（FunASR 未啟用或失敗）
        if funasr_result is None or funasr_result.get('error'):
            logger.info("  使用單引擎模式（僅 Whisper）")
            return self._single_engine_result(whisper_result, features)
        
        # 雙引擎模式
        return self._dual_engine_fusion(whisper_result, funasr_result, features)
    
    def _single_engine_result(self,
                             whisper_result: Dict[str, Any],
                             features: Dict[str, Any]) -> Dict[str, Any]:
        """
        單引擎結果處理
        """
        return {
            'text': whisper_result.get('text', ''),
            'confidence': whisper_result.get('confidence', 0.0),
            'fusion_method': 'single_engine',
            'engine_used': 'whisper',
            'whisper_result': whisper_result,
            'funasr_result': None,
            'fusion_info': {
                'mode': 'single',
                'reason': 'funasr_unavailable'
            }
        }
    
    def _dual_engine_fusion(self,
                           whisper_result: Dict[str, Any],
                           funasr_result: Dict[str, Any],
                           features: Dict[str, Any]) -> Dict[str, Any]:
        """
        雙引擎融合
        """
        w_text = whisper_result.get('text', '')
        f_text = funasr_result.get('text', '')
        w_conf = whisper_result.get('confidence', 0.0)
        f_conf = funasr_result.get('confidence', 0.0)
        
        logger.info(f"  雙引擎融合:")
        logger.info(f"    Whisper: '{w_text[:50]}...' (conf: {w_conf:.3f})")
        logger.info(f"    FunASR:  '{f_text[:50]}...' (conf: {f_conf:.3f})")
        
        # 1. 計算基礎權重
        weights = self._calculate_weights(w_conf, f_conf, features)
        
        # 2. 選擇最終文本
        final_text, selection_method = self._select_text(
            w_text, f_text, w_conf, f_conf, weights
        )
        
        # 3. 計算最終置信度
        final_confidence = self._calculate_final_confidence(
            w_conf, f_conf, weights, w_text, f_text
        )
        
        logger.info(f"  融合結果: '{final_text[:50]}...' (conf: {final_confidence:.3f})")
        logger.info(f"  權重: Whisper={weights['whisper']:.2f}, FunASR={weights['funasr']:.2f}")
        
        return {
            'text': final_text,
            'confidence': final_confidence,
            'fusion_method': 'dynamic_confidence_weighted',
            'selection_method': selection_method,
            'whisper_result': whisper_result,
            'funasr_result': funasr_result,
            'fusion_info': {
                'mode': 'dual',
                'weights': weights,
                'text_similarity': self._calculate_similarity(w_text, f_text)
            }
        }
    
    def _calculate_weights(self,
                          w_conf: float,
                          f_conf: float,
                          features: Dict[str, Any]) -> Dict[str, float]:
        """
        計算動態權重
        """
        # 基礎權重
        if features.get('is_minnan', False):
            base_weights = self.minnan_weights.copy()
        else:
            base_weights = self.default_weights.copy()
        
        # 動態調整
        if w_conf > self.high_confidence_threshold and f_conf < self.low_confidence_threshold:
            # Whisper 高置信度，FunASR 低置信度
            return {'whisper': 0.8, 'funasr': 0.2}
        
        elif f_conf > self.high_confidence_threshold and w_conf < self.low_confidence_threshold:
            # FunASR 高置信度，Whisper 低置信度
            return {'whisper': 0.2, 'funasr': 0.8}
        
        else:
            # 使用置信度加權
            total_conf = w_conf + f_conf
            if total_conf > 0:
                w_weight = base_weights['whisper'] * (w_conf / total_conf)
                f_weight = base_weights['funasr'] * (f_conf / total_conf)
                
                # 正規化
                total_weight = w_weight + f_weight
                return {
                    'whisper': w_weight / total_weight,
                    'funasr': f_weight / total_weight
                }
            else:
                return base_weights
    
    def _select_text(self,
                    w_text: str,
                    f_text: str,
                    w_conf: float,
                    f_conf: float,
                    weights: Dict[str, float]) -> tuple:
        """
        選擇最終文本
        
        Returns:
            (選擇的文本, 選擇方法)
        """
        # 如果兩個結果非常相似，選擇置信度高的
        similarity = self._calculate_similarity(w_text, f_text)
        
        if similarity > 0.8:
            # 高度相似，選擇置信度高的
            if w_conf >= f_conf:
                return w_text, 'high_similarity_whisper'
            else:
                return f_text, 'high_similarity_funasr'
        
        # 根據權重選擇
        if weights['whisper'] >= weights['funasr']:
            return w_text, 'weight_based_whisper'
        else:
            return f_text, 'weight_based_funasr'
    
    def _calculate_final_confidence(self,
                                   w_conf: float,
                                   f_conf: float,
                                   weights: Dict[str, float],
                                   w_text: str,
                                   f_text: str) -> float:
        """
        計算最終置信度
        """
        # 加權平均置信度
        weighted_conf = (
            weights['whisper'] * w_conf +
            weights['funasr'] * f_conf
        )
        
        # 如果兩個結果相似，提升置信度
        similarity = self._calculate_similarity(w_text, f_text)
        if similarity > 0.8:
            weighted_conf = min(weighted_conf * 1.1, 1.0)
        
        return float(weighted_conf)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        計算兩個文本的相似度
        
        使用 SequenceMatcher
        """
        if not text1 or not text2:
            return 0.0
        
        return difflib.SequenceMatcher(None, text1, text2).ratio()
