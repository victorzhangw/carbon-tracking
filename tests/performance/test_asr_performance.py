"""
ASR 性能測試腳本
測試處理速度、記憶體使用、批次處理等
"""

import asyncio
import time
import numpy as np
import soundfile as sf
import io
import sys
import os

# Add parent directory to path to import from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.asr.coordinator import ASRCoordinator


async def test_single_audio_performance():
    """測試單個音頻的性能"""
    print("=" * 60)
    print("測試 1: 單個音頻性能")
    print("=" * 60)
    print()
    
    # 初始化
    coordinator = ASRCoordinator(
        whisper_model_size="base",
        enable_funasr=False,
        device="cuda"
    )
    
    # 創建測試音頻（10秒）
    sr = 16000
    duration = 10
    t = np.linspace(0, duration, sr * duration)
    audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)
    
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, audio, sr, format='WAV')
    audio_bytes = audio_buffer.getvalue()
    
    print(f"測試音頻: {duration}秒, {len(audio_bytes)} bytes")
    print()
    
    # 預熱（第一次會較慢）
    print("預熱中...")
    await coordinator.recognize(audio_bytes)
    print("✓ 預熱完成")
    print()
    
    # 性能測試（5次）
    print("執行性能測試（5次）...")
    times = []
    
    for i in range(5):
        start = time.time()
        result = await coordinator.recognize(audio_bytes)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"  第 {i+1} 次: {elapsed:.3f}秒 (置信度: {result.get('confidence', 0):.3f})")
    
    print()
    print("性能統計:")
    print(f"  平均時間: {np.mean(times):.3f}秒")
    print(f"  最快時間: {np.min(times):.3f}秒")
    print(f"  最慢時間: {np.max(times):.3f}秒")
    print(f"  標準差: {np.std(times):.3f}秒")
    print(f"  實時因子: {np.mean(times) / duration:.2f}x")
    print()
    
    return times


async def test_batch_processing():
    """測試批次處理性能"""
    print("=" * 60)
    print("測試 2: 批次處理性能")
    print("=" * 60)
    print()
    
    coordinator = ASRCoordinator(
        whisper_model_size="base",
        enable_funasr=False,
        device="cuda"
    )
    
    # 創建多個測試音頻
    batch_sizes = [1, 2, 4]
    sr = 16000
    duration = 5
    
    for batch_size in batch_sizes:
        print(f"批次大小: {batch_size}")
        
        # 創建音頻列表
        audio_list = []
        for _ in range(batch_size):
            t = np.linspace(0, duration, sr * duration)
            audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)
            
            audio_buffer = io.BytesIO()
            sf.write(audio_buffer, audio, sr, format='WAV')
            audio_list.append(audio_buffer.getvalue())
        
        # 批次處理
        start = time.time()
        results = await coordinator.recognize_batch(audio_list)
        elapsed = time.time() - start
        
        print(f"  總時間: {elapsed:.3f}秒")
        print(f"  平均每個: {elapsed / batch_size:.3f}秒")
        print(f"  成功數: {sum(1 for r in results if r.get('success', False))}/{batch_size}")
        print()


async def test_memory_usage():
    """測試記憶體使用"""
    print("=" * 60)
    print("測試 3: 記憶體使用")
    print("=" * 60)
    print()
    
    coordinator = ASRCoordinator(
        whisper_model_size="base",
        enable_funasr=False,
        device="cuda"
    )
    
    # 獲取系統信息
    system_info = coordinator.get_system_info()
    
    print("系統信息:")
    print(f"  Coordinator 版本: {system_info['coordinator']['version']}")
    print(f"  目標採樣率: {system_info['coordinator']['target_sample_rate']} Hz")
    print(f"  最大音頻長度: {system_info['coordinator']['max_audio_length']} 秒")
    print()
    
    print("Whisper 引擎:")
    whisper_info = system_info['whisper_engine']
    print(f"  模型大小: {whisper_info['model_size']}")
    print(f"  設備: {whisper_info['device']}")
    print(f"  CUDA 可用: {whisper_info['cuda_available']}")
    
    if 'memory_usage' in whisper_info:
        memory = whisper_info['memory_usage']
        print(f"\n  記憶體使用:")
        if 'gpu_memory_allocated' in memory:
            print(f"    GPU 已分配: {memory['gpu_memory_allocated']}")
            print(f"    GPU 已保留: {memory['gpu_memory_reserved']}")
            print(f"    GPU 總容量: {memory['gpu_memory_total']}")
    print()
    
    # 測試快取清理
    print("清理快取...")
    coordinator.clear_cache()
    print("✓ 快取已清理")
    print()


async def test_different_audio_lengths():
    """測試不同長度音頻的處理時間"""
    print("=" * 60)
    print("測試 4: 不同音頻長度")
    print("=" * 60)
    print()
    
    coordinator = ASRCoordinator(
        whisper_model_size="base",
        enable_funasr=False,
        device="cuda"
    )
    
    durations = [1, 3, 5, 10, 15]
    sr = 16000
    
    print("音頻長度 | 處理時間 | 實時因子")
    print("-" * 40)
    
    for duration in durations:
        # 創建音頻
        t = np.linspace(0, duration, sr * duration)
        audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, audio, sr, format='WAV')
        audio_bytes = audio_buffer.getvalue()
        
        # 測試
        start = time.time()
        result = await coordinator.recognize(audio_bytes)
        elapsed = time.time() - start
        
        rtf = elapsed / duration
        print(f"{duration:6d}秒 | {elapsed:8.3f}秒 | {rtf:8.2f}x")
    
    print()


async def main():
    """主測試函數"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 18 + "ASR 性能測試" + " " * 28 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # 測試 1: 單個音頻性能
        await test_single_audio_performance()
        
        # 測試 2: 批次處理
        await test_batch_processing()
        
        # 測試 3: 記憶體使用
        await test_memory_usage()
        
        # 測試 4: 不同音頻長度
        await test_different_audio_lengths()
        
        # 總結
        print("=" * 60)
        print("性能測試完成！")
        print("=" * 60)
        print()
        print("✓ 單個音頻處理測試完成")
        print("✓ 批次處理測試完成")
        print("✓ 記憶體使用測試完成")
        print("✓ 不同長度音頻測試完成")
        print()
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
