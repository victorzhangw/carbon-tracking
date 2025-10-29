"""
P0-1 ASR 環境驗證腳本
驗證所有必要的依賴和模型是否正確安裝
"""

import sys
import importlib

def check_module(module_name, display_name=None):
    """檢查模組是否可導入"""
    if display_name is None:
        display_name = module_name
    
    try:
        mod = importlib.import_module(module_name)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✓ {display_name}: {version}")
        return True, mod
    except ImportError as e:
        print(f"✗ {display_name}: 未安裝 ({e})")
        return False, None

def main():
    print("=" * 60)
    print("P0-1 雙引擎 ASR 系統 - 環境驗證")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # 1. 基礎依賴檢查
    print("【1】基礎依賴檢查")
    print("-" * 60)
    
    modules_to_check = [
        ('torch', 'PyTorch'),
        ('torchaudio', 'TorchAudio'),
        ('transformers', 'Transformers'),
        ('librosa', 'Librosa'),
        ('soundfile', 'SoundFile'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('scipy', 'SciPy'),
        ('flask', 'Flask'),
        ('pydantic', 'Pydantic'),
    ]
    
    for module_name, display_name in modules_to_check:
        ok, _ = check_module(module_name, display_name)
        if not ok:
            all_ok = False
    
    print()
    
    # 2. PyTorch 和 CUDA 檢查
    print("【2】PyTorch 和 CUDA 檢查")
    print("-" * 60)
    
    ok, torch = check_module('torch')
    if ok:
        print(f"  PyTorch 版本: {torch.__version__}")
        print(f"  CUDA 可用: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"  CUDA 版本: {torch.version.cuda}")
            print(f"  GPU 數量: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
                props = torch.cuda.get_device_properties(i)
                print(f"    記憶體: {props.total_memory / 1024**3:.2f} GB")
        else:
            print("  ⚠️  警告: CUDA 不可用，將使用 CPU 模式（速度較慢）")
    else:
        all_ok = False
    
    print()
    
    # 3. Whisper 檢查
    print("【3】Whisper 模型檢查")
    print("-" * 60)
    
    ok, whisper = check_module('whisper', 'OpenAI Whisper')
    if ok:
        try:
            print("  正在載入 Whisper base 模型（測試用）...")
            model = whisper.load_model("base")
            print("  ✓ Whisper 模型載入成功")
            print(f"  模型設備: {next(model.parameters()).device}")
            del model
        except Exception as e:
            print(f"  ✗ Whisper 模型載入失敗: {e}")
            all_ok = False
    else:
        all_ok = False
    
    print()
    
    # 4. FunASR 檢查
    print("【4】FunASR 模型檢查")
    print("-" * 60)
    
    try:
        from funasr import AutoModel
        print("✓ FunASR: 已安裝")
        
        try:
            print("  正在載入 FunASR paraformer-zh 模型...")
            model = AutoModel(model="paraformer-zh")
            print("  ✓ FunASR 模型載入成功")
            del model
        except Exception as e:
            print(f"  ✗ FunASR 模型載入失敗: {e}")
            print("  提示: 首次使用需要下載模型，請確保網路連接正常")
            all_ok = False
    except ImportError as e:
        print(f"✗ FunASR: 未安裝 ({e})")
        all_ok = False
    
    print()
    
    # 5. 音頻處理測試
    print("【5】音頻處理功能測試")
    print("-" * 60)
    
    ok, librosa = check_module('librosa')
    if ok:
        try:
            import numpy as np
            
            # 創建測試音頻（1秒，440Hz 正弦波）
            sr = 16000
            duration = 1
            t = np.linspace(0, duration, sr * duration)
            audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)
            
            # 測試 MFCC 提取
            mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
            print(f"  ✓ MFCC 提取成功 (shape: {mfccs.shape})")
            
            # 測試光譜質心
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)
            print(f"  ✓ 光譜質心計算成功 (shape: {spectral_centroids.shape})")
            
            # 測試零交叉率
            zcr = librosa.feature.zero_crossing_rate(audio)
            print(f"  ✓ 零交叉率計算成功 (shape: {zcr.shape})")
            
        except Exception as e:
            print(f"  ✗ 音頻處理測試失敗: {e}")
            all_ok = False
    else:
        all_ok = False
    
    print()
    
    # 6. 異步支援檢查
    print("【6】異步處理支援檢查")
    print("-" * 60)
    
    ok, asyncio = check_module('asyncio')
    if ok:
        print("  ✓ asyncio 可用")
    
    ok, aiohttp = check_module('aiohttp')
    if ok:
        print("  ✓ aiohttp 可用")
    
    print()
    
    # 7. 總結
    print("=" * 60)
    if all_ok:
        print("✓ 環境驗證通過！所有依賴已正確安裝。")
        print()
        print("下一步:")
        print("  1. 查看設計文檔: .kiro/specs/p0-dual-engine-asr/design.md")
        print("  2. 開始實現任務 2.1: ASR Coordinator 基礎框架")
        print("  3. 參考設置指南: setup_asr_environment.md")
    else:
        print("✗ 環境驗證失敗！請檢查上述錯誤並安裝缺失的依賴。")
        print()
        print("安裝指令:")
        print("  pip install -r requirements-asr.txt")
        print()
        print("詳細設置指南請參考: setup_asr_environment.md")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
