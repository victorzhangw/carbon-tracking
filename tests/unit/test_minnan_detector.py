"""
測試閩南語檢測器
"""

import numpy as np
import logging
import sys
import os

# Add parent directory to path to import from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.asr.minnan_detector import MinnanLanguageDetector

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_text_detection():
    """測試文本特徵檢測"""
    
    print("=" * 70)
    print("閩南語檢測器 - 文本特徵測試")
    print("=" * 70)
    
    detector = MinnanLanguageDetector()
    
    # 測試案例
    test_cases = [
        {
            "text": "你好，今天天氣很好",
            "expected": "華語",
            "description": "純華語"
        },
        {
            "text": "你好，今天天氣足好",
            "expected": "閩南語",
            "description": "閩南語（含'足'）"
        },
        {
            "text": "啥物人講按怎做",
            "expected": "閩南語",
            "description": "純閩南語"
        },
        {
            "text": "我毋知這個按怎做",
            "expected": "閩南語",
            "description": "混合語（含'毋知'、'按怎'）"
        },
        {
            "text": "阮欲去佗位食飯",
            "expected": "閩南語",
            "description": "閩南語（含'阮'、'欲'、'佗位'、'食'）"
        },
        {
            "text": "這個真好吃",
            "expected": "可能閩南語",
            "description": "含閩南語詞彙'真'"
        }
    ]
    
    print("\n測試案例:")
    print("-" * 70)
    
    for i, case in enumerate(test_cases, 1):
        text = case["text"]
        expected = case["expected"]
        description = case["description"]
        
        # 檢測
        result = detector.detect(
            audio=np.zeros(16000),  # 空音頻
            text_hint=text,
            sample_rate=16000
        )
        
        print(f"\n案例 {i}: {description}")
        print(f"  文本: {text}")
        print(f"  預期: {expected}")
        print(f"  結果: {'閩南語' if result['is_minnan'] else '華語'}")
        print(f"  置信度: {result['confidence']:.3f}")
        print(f"  文本分數: {result['text_score']:.3f}")
        print(f"  混合比: {result['mix_ratio']:.3f}")
        
        # 判斷是否符合預期
        is_correct = (
            (expected == "閩南語" and result['is_minnan']) or
            (expected == "華語" and not result['is_minnan']) or
            (expected == "可能閩南語")  # 這種情況不做嚴格判斷
        )
        
        status = "✓" if is_correct else "✗"
        print(f"  狀態: {status}")
    
    print("\n" + "=" * 70)
    print("✓ 文本特徵測試完成")
    print("=" * 70)


def test_audio_detection():
    """測試音頻特徵檢測"""
    
    print("\n" + "=" * 70)
    print("閩南語檢測器 - 音頻特徵測試")
    print("=" * 70)
    
    detector = MinnanLanguageDetector()
    
    # 測試案例
    test_cases = [
        {
            "name": "靜音",
            "audio": np.zeros(16000 * 3),  # 3秒靜音
            "description": "靜音音頻"
        },
        {
            "name": "白噪音",
            "audio": np.random.randn(16000 * 3) * 0.1,  # 3秒白噪音
            "description": "隨機噪音"
        },
        {
            "name": "正弦波",
            "audio": np.sin(2 * np.pi * 440 * np.linspace(0, 3, 16000 * 3)),  # 440Hz正弦波
            "description": "單一頻率"
        },
        {
            "name": "複雜音調",
            "audio": _generate_complex_tone(duration=3),
            "description": "模擬複雜音調變化"
        }
    ]
    
    print("\n測試案例:")
    print("-" * 70)
    
    for case in test_cases:
        name = case["name"]
        audio = case["audio"].astype(np.float32)
        description = case["description"]
        
        # 檢測
        result = detector.detect(
            audio=audio,
            text_hint=None,
            sample_rate=16000
        )
        
        print(f"\n案例: {name}")
        print(f"  描述: {description}")
        print(f"  音頻長度: {len(audio) / 16000:.2f} 秒")
        print(f"  結果: {'閩南語' if result['is_minnan'] else '華語'}")
        print(f"  置信度: {result['confidence']:.3f}")
        print(f"  音頻分數: {result['audio_score']:.3f}")
        print(f"  混合比: {result['mix_ratio']:.3f}")
    
    print("\n" + "=" * 70)
    print("✓ 音頻特徵測試完成")
    print("=" * 70)


def _generate_complex_tone(duration=3, sample_rate=16000):
    """生成複雜音調（模擬語音）"""
    t = np.linspace(0, duration, sample_rate * duration)
    
    # 多個頻率疊加，模擬語音的複雜性
    audio = (
        np.sin(2 * np.pi * 200 * t) +
        0.5 * np.sin(2 * np.pi * 400 * t) +
        0.3 * np.sin(2 * np.pi * 600 * t) +
        0.2 * np.random.randn(len(t))  # 添加噪音
    )
    
    # 添加音調變化（模擬聲調）
    modulation = 1 + 0.3 * np.sin(2 * np.pi * 3 * t)  # 3Hz 調製
    audio = audio * modulation
    
    # 正規化
    audio = audio / np.max(np.abs(audio))
    
    return audio


def test_combined_detection():
    """測試音頻+文本綜合檢測"""
    
    print("\n" + "=" * 70)
    print("閩南語檢測器 - 綜合檢測測試")
    print("=" * 70)
    
    detector = MinnanLanguageDetector()
    
    # 測試案例
    test_cases = [
        {
            "audio": np.random.randn(16000 * 3) * 0.1,
            "text": "你好，今天天氣很好",
            "expected": "華語",
            "description": "華語音頻+華語文本"
        },
        {
            "audio": _generate_complex_tone(duration=3),
            "text": "啥物人講按怎做",
            "expected": "閩南語",
            "description": "複雜音頻+閩南語文本"
        },
        {
            "audio": np.random.randn(16000 * 3) * 0.1,
            "text": "我毋知這個按怎做",
            "expected": "閩南語",
            "description": "簡單音頻+混合文本"
        }
    ]
    
    print("\n測試案例:")
    print("-" * 70)
    
    for i, case in enumerate(test_cases, 1):
        audio = case["audio"].astype(np.float32)
        text = case["text"]
        expected = case["expected"]
        description = case["description"]
        
        # 檢測
        result = detector.detect(
            audio=audio,
            text_hint=text,
            sample_rate=16000
        )
        
        print(f"\n案例 {i}: {description}")
        print(f"  文本: {text}")
        print(f"  預期: {expected}")
        print(f"  結果: {'閩南語' if result['is_minnan'] else '華語'}")
        print(f"  置信度: {result['confidence']:.3f}")
        print(f"  音頻分數: {result['audio_score']:.3f}")
        print(f"  文本分數: {result['text_score']:.3f}")
        print(f"  混合比: {result['mix_ratio']:.3f}")
        
        # 判斷是否符合預期
        is_correct = (
            (expected == "閩南語" and result['is_minnan']) or
            (expected == "華語" and not result['is_minnan'])
        )
        
        status = "✓" if is_correct else "✗"
        print(f"  狀態: {status}")
    
    print("\n" + "=" * 70)
    print("✓ 綜合檢測測試完成")
    print("=" * 70)


def test_detector_info():
    """測試檢測器信息"""
    
    print("\n" + "=" * 70)
    print("閩南語檢測器 - 信息查詢")
    print("=" * 70)
    
    detector = MinnanLanguageDetector()
    info = detector.get_detector_info()
    
    print("\n檢測器信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        # 運行所有測試
        test_text_detection()
        test_audio_detection()
        test_combined_detection()
        test_detector_info()
        
        print("\n" + "=" * 70)
        print("✓ 所有測試完成")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
