"""
測試高齡語音檢測器
"""

import numpy as np
import logging
from services.asr.elderly_detector import ElderlyVoiceDetector

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_slow_speech(duration=5, sample_rate=16000):
    """生成模擬慢速語音"""
    t = np.linspace(0, duration, sample_rate * duration)
    
    # 慢速語音：較少的音節，較長的停頓
    audio = np.zeros_like(t)
    
    # 添加幾個音節（間隔較長）
    syllable_positions = [0.5, 1.5, 2.5, 3.5, 4.0]
    for pos in syllable_positions:
        start_idx = int(pos * sample_rate)
        end_idx = int((pos + 0.3) * sample_rate)  # 每個音節 0.3 秒
        
        if end_idx < len(audio):
            # 生成音節（多個頻率疊加）
            syllable_t = t[start_idx:end_idx] - t[start_idx]
            syllable = (
                np.sin(2 * np.pi * 150 * syllable_t) +
                0.5 * np.sin(2 * np.pi * 300 * syllable_t)
            )
            audio[start_idx:end_idx] = syllable
    
    # 添加輕微顫抖（6 Hz）
    tremor = 1 + 0.1 * np.sin(2 * np.pi * 6 * t)
    audio = audio * tremor
    
    # 較小的音量
    audio = audio * 0.3
    
    # 正規化
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.5
    
    return audio.astype(np.float32)


def generate_normal_speech(duration=5, sample_rate=16000):
    """生成模擬正常語音"""
    t = np.linspace(0, duration, sample_rate * duration)
    
    # 正常語速：較多的音節，較短的停頓
    audio = np.zeros_like(t)
    
    # 添加更多音節（間隔較短）
    syllable_positions = np.arange(0.2, duration, 0.6)  # 每 0.6 秒一個音節
    for pos in syllable_positions:
        start_idx = int(pos * sample_rate)
        end_idx = int((pos + 0.2) * sample_rate)  # 每個音節 0.2 秒
        
        if end_idx < len(audio):
            syllable_t = t[start_idx:end_idx] - t[start_idx]
            syllable = (
                np.sin(2 * np.pi * 200 * syllable_t) +
                0.5 * np.sin(2 * np.pi * 400 * syllable_t)
            )
            audio[start_idx:end_idx] = syllable
    
    # 正常音量
    audio = audio * 0.7
    
    # 正規化
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))
    
    return audio.astype(np.float32)


def test_basic_detection():
    """測試基本檢測功能"""
    
    print("=" * 70)
    print("高齡語音檢測器 - 基本功能測試")
    print("=" * 70)
    
    detector = ElderlyVoiceDetector()
    
    # 測試案例
    test_cases = [
        {
            "name": "靜音",
            "audio": np.zeros(16000 * 3),
            "expected": "非高齡",
            "description": "靜音音頻"
        },
        {
            "name": "白噪音",
            "audio": np.random.randn(16000 * 3) * 0.1,
            "expected": "非高齡",
            "description": "隨機噪音"
        },
        {
            "name": "模擬慢速語音",
            "audio": generate_slow_speech(duration=5),
            "expected": "可能高齡",
            "description": "慢速、小音量、有顫抖"
        },
        {
            "name": "模擬正常語音",
            "audio": generate_normal_speech(duration=5),
            "expected": "非高齡",
            "description": "正常語速、正常音量"
        }
    ]
    
    print("\n測試案例:")
    print("-" * 70)
    
    for case in test_cases:
        name = case["name"]
        audio = case["audio"].astype(np.float32)
        expected = case["expected"]
        description = case["description"]
        
        # 檢測
        result = detector.detect(audio=audio, sample_rate=16000)
        
        print(f"\n案例: {name}")
        print(f"  描述: {description}")
        print(f"  音頻長度: {len(audio) / 16000:.2f} 秒")
        print(f"  預期: {expected}")
        print(f"  結果: {'高齡語音' if result['is_elderly'] else '非高齡語音'}")
        print(f"  置信度: {result['confidence']:.3f}")
        
        if 'features' in result:
            features = result['features']
            print(f"  特徵:")
            print(f"    語速: {features.get('speech_rate', 0):.2f} 音節/秒 (分數: {features.get('speech_rate_score', 0):.3f})")
            print(f"    音量: {features.get('volume_mean', 0):.3f} (分數: {features.get('volume_score', 0):.3f})")
            print(f"    顫抖: {'是' if features.get('tremor_detected', False) else '否'} (分數: {features.get('tremor_score', 0):.3f})")
            print(f"    停頓比: {features.get('pause_ratio', 0):.3f} (分數: {features.get('pause_score', 0):.3f})")
            print(f"    音調範圍: {features.get('pitch_range', 0):.1f} Hz (分數: {features.get('pitch_score', 0):.3f})")
    
    print("\n" + "=" * 70)
    print("✓ 基本功能測試完成")
    print("=" * 70)


def test_feature_detection():
    """測試各項特徵檢測"""
    
    print("\n" + "=" * 70)
    print("高齡語音檢測器 - 特徵檢測測試")
    print("=" * 70)
    
    detector = ElderlyVoiceDetector()
    
    # 生成不同特徵的音頻
    print("\n1. 測試語速檢測")
    print("-" * 70)
    
    # 慢速語音
    slow_audio = generate_slow_speech(duration=5)
    slow_result = detector.detect(slow_audio, sample_rate=16000)
    print(f"慢速語音:")
    print(f"  語速: {slow_result['features']['speech_rate']:.2f} 音節/秒")
    print(f"  語速分數: {slow_result['features']['speech_rate_score']:.3f}")
    
    # 正常語音
    normal_audio = generate_normal_speech(duration=5)
    normal_result = detector.detect(normal_audio, sample_rate=16000)
    print(f"正常語音:")
    print(f"  語速: {normal_result['features']['speech_rate']:.2f} 音節/秒")
    print(f"  語速分數: {normal_result['features']['speech_rate_score']:.3f}")
    
    print("\n2. 測試音量檢測")
    print("-" * 70)
    
    # 小音量
    quiet_audio = generate_slow_speech(duration=5) * 0.3
    quiet_result = detector.detect(quiet_audio, sample_rate=16000)
    print(f"小音量:")
    print(f"  平均音量: {quiet_result['features']['volume_mean']:.4f}")
    print(f"  音量分數: {quiet_result['features']['volume_score']:.3f}")
    
    # 正常音量
    normal_volume_audio = generate_normal_speech(duration=5)
    normal_volume_result = detector.detect(normal_volume_audio, sample_rate=16000)
    print(f"正常音量:")
    print(f"  平均音量: {normal_volume_result['features']['volume_mean']:.4f}")
    print(f"  音量分數: {normal_volume_result['features']['volume_score']:.3f}")
    
    print("\n" + "=" * 70)
    print("✓ 特徵檢測測試完成")
    print("=" * 70)


def test_threshold_adjustment():
    """測試閾值調整"""
    
    print("\n" + "=" * 70)
    print("高齡語音檢測器 - 閾值調整測試")
    print("=" * 70)
    
    detector = ElderlyVoiceDetector()
    
    # 生成測試音頻
    test_audio = generate_slow_speech(duration=5)
    
    # 使用預設閾值
    print("\n使用預設閾值:")
    result1 = detector.detect(test_audio, sample_rate=16000)
    print(f"  檢測結果: {'高齡語音' if result1['is_elderly'] else '非高齡語音'}")
    print(f"  置信度: {result1['confidence']:.3f}")
    
    # 調整閾值（更寬鬆）
    print("\n調整閾值（更寬鬆）:")
    detector.update_thresholds({
        'speech_rate_high': 5.5,  # 提高閾值
        'volume_low': 0.01  # 降低閾值
    })
    result2 = detector.detect(test_audio, sample_rate=16000)
    print(f"  檢測結果: {'高齡語音' if result2['is_elderly'] else '非高齡語音'}")
    print(f"  置信度: {result2['confidence']:.3f}")
    
    print("\n" + "=" * 70)
    print("✓ 閾值調整測試完成")
    print("=" * 70)


def test_detector_info():
    """測試檢測器信息"""
    
    print("\n" + "=" * 70)
    print("高齡語音檢測器 - 信息查詢")
    print("=" * 70)
    
    detector = ElderlyVoiceDetector()
    info = detector.get_detector_info()
    
    print("\n檢測器信息:")
    print(f"  檢測器: {info['detector']}")
    print(f"  版本: {info['version']}")
    print(f"  方法: {info['method']}")
    print(f"\n閾值設置:")
    for key, value in info['thresholds'].items():
        print(f"    {key}: {value}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        # 運行所有測試
        test_basic_detection()
        test_feature_detection()
        test_threshold_adjustment()
        test_detector_info()
        
        print("\n" + "=" * 70)
        print("✓ 所有測試完成")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
