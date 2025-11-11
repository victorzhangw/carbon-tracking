"""
測試 FunASR 引擎
"""

import asyncio
import numpy as np
import logging
import sys
import os

# Add parent directory to path to import from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.asr.funasr_engine import FunASREngine

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_funasr_engine():
    """測試 FunASR 引擎基本功能"""
    
    print("=" * 60)
    print("FunASR 引擎測試")
    print("=" * 60)
    
    try:
        # 1. 初始化引擎
        print("\n1. 初始化 FunASR 引擎...")
        
        # 檢查是否有本地模型
        import os
        local_model_path = "models/paraformer-zh"
        
        if os.path.exists(local_model_path):
            print(f"   找到本地模型: {local_model_path}")
            engine = FunASREngine(
                model_name="paraformer-zh",
                device="cuda",
                local_model_path=local_model_path
            )
        else:
            print("   使用在線下載模型")
            engine = FunASREngine(model_name="paraformer-zh", device="cuda")
        
        print("✓ 引擎初始化成功")
        
        # 2. 獲取模型信息
        print("\n2. 模型信息:")
        model_info = engine.get_model_info()
        for key, value in model_info.items():
            print(f"   {key}: {value}")
        
        # 3. 測試音頻識別
        print("\n3. 測試音頻識別...")
        
        # 創建測試音頻（5秒，16kHz，正弦波）
        sample_rate = 16000
        duration = 5
        t = np.linspace(0, duration, sample_rate * duration)
        audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)  # 440Hz 正弦波
        
        # 測試特徵
        features = {
            'is_minnan': False,
            'is_elderly': False,
            'is_low_snr': False
        }
        
        options = {}
        
        print(f"   音頻長度: {len(audio)} 樣本 ({duration} 秒)")
        print("   執行識別...")
        
        result = await engine.recognize(audio, features, options)
        
        print("\n4. 識別結果:")
        print(f"   文本: {result.get('text', '(無)')}")
        print(f"   置信度: {result.get('confidence', 0):.3f}")
        print(f"   引擎: {result.get('engine', 'unknown')}")
        
        if 'error' in result:
            print(f"   錯誤: {result['error']}")
        
        # 5. 測試閩南語優化
        print("\n5. 測試閩南語優化...")
        features_minnan = {
            'is_minnan': True,
            'minnan_confidence': 0.8,
            'is_elderly': False,
            'is_low_snr': False
        }
        
        result_minnan = await engine.recognize(audio, features_minnan, options)
        print(f"   閩南語模式置信度: {result_minnan.get('confidence', 0):.3f}")
        
        # 6. 記憶體使用
        print("\n6. 記憶體使用:")
        memory_info = engine.get_memory_usage()
        for key, value in memory_info.items():
            print(f"   {key}: {value}")
        
        # 7. 清理快取
        print("\n7. 清理快取...")
        engine.clear_cache()
        print("✓ 快取已清理")
        
        print("\n" + "=" * 60)
        print("✓ FunASR 引擎測試完成")
        print("=" * 60)
        
        return True
        
    except ImportError as e:
        print(f"\n✗ FunASR 未安裝: {e}")
        print("請執行: pip install funasr")
        return False
        
    except Exception as e:
        print(f"\n✗ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_with_real_audio():
    """使用真實音頻測試"""
    
    print("\n" + "=" * 60)
    print("真實音頻測試")
    print("=" * 60)
    
    try:
        import soundfile as sf
        import os
        
        # 檢查測試音頻
        test_audio_path = "test_audio.wav"
        if not os.path.exists(test_audio_path):
            print(f"\n跳過真實音頻測試（找不到 {test_audio_path}）")
            return
        
        print(f"\n載入音頻: {test_audio_path}")
        audio, sr = sf.read(test_audio_path)
        
        # 轉為單聲道
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        
        # 重採樣到 16kHz
        if sr != 16000:
            import librosa
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        
        audio = audio.astype(np.float32)
        
        print(f"音頻長度: {len(audio) / 16000:.2f} 秒")
        
        # 初始化引擎
        engine = FunASREngine(device="cuda")
        
        # 識別
        features = {'is_minnan': False, 'is_elderly': False, 'is_low_snr': False}
        options = {}
        
        print("執行識別...")
        result = await engine.recognize(audio, features, options)
        
        print("\n識別結果:")
        print(f"文本: {result.get('text', '(無)')}")
        print(f"置信度: {result.get('confidence', 0):.3f}")
        
        print("\n✓ 真實音頻測試完成")
        
    except Exception as e:
        print(f"\n✗ 真實音頻測試失敗: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 運行測試
    success = asyncio.run(test_funasr_engine())
    
    if success:
        # 如果基本測試成功，嘗試真實音頻測試
        asyncio.run(test_with_real_audio())
