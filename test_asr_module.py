"""
測試 ASR 模組是否正常運作
"""

import sys
import os

def test_asr_imports():
    """測試 ASR 相關模組是否能正常導入"""
    print("=" * 60)
    print("測試 ASR 模組導入")
    print("=" * 60)
    
    try:
        print("\n1. 測試導入 ASR 路由...")
        from routes.asr import asr_bp
        print("   ✓ ASR 路由導入成功")
        
        print("\n2. 測試導入 ASR Coordinator...")
        from services.asr.coordinator import ASRCoordinator
        print("   ✓ ASR Coordinator 導入成功")
        
        print("\n3. 測試導入 Whisper 引擎...")
        from services.asr.whisper_engine import WhisperEngine
        print("   ✓ Whisper 引擎導入成功")
        
        print("\n4. 測試導入 FunASR 引擎...")
        from services.asr.funasr_engine import FunASREngine
        print("   ✓ FunASR 引擎導入成功")
        
        print("\n5. 測試導入融合算法...")
        from services.asr.fusion import ConfidenceFusion
        print("   ✓ 融合算法導入成功")
        
        print("\n6. 測試導入閩南語檢測器...")
        from services.asr.minnan_detector import MinnanLanguageDetector
        print("   ✓ 閩南語檢測器導入成功")
        
        print("\n7. 測試導入高齡語音檢測器...")
        from services.asr.elderly_detector import ElderlyVoiceDetector
        print("   ✓ 高齡語音檢測器導入成功")
        
        print("\n" + "=" * 60)
        print("✅ 所有 ASR 模組導入測試通過！")
        print("=" * 60)
        return True
        
    except ImportError as e:
        print(f"\n❌ 導入失敗: {e}")
        print("\n可能的原因:")
        print("  1. 缺少必要的依賴套件（whisper, funasr 等）")
        print("  2. 模組文件不存在或有語法錯誤")
        print("  3. Python 路徑配置問題")
        return False
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_asr_dependencies():
    """測試 ASR 所需的依賴套件"""
    print("\n" + "=" * 60)
    print("測試 ASR 依賴套件")
    print("=" * 60)
    
    dependencies = [
        ('torch', 'PyTorch'),
        ('whisper', 'OpenAI Whisper'),
        ('librosa', 'Librosa'),
        ('soundfile', 'SoundFile'),
        ('numpy', 'NumPy'),
    ]
    
    all_installed = True
    
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"✓ {display_name} 已安裝")
        except ImportError:
            print(f"✗ {display_name} 未安裝")
            all_installed = False
    
    # 測試 FunASR（可選）
    try:
        __import__('funasr')
        print(f"✓ FunASR 已安裝（可選）")
    except ImportError:
        print(f"⚠ FunASR 未安裝（可選，不影響基本功能）")
    
    print("=" * 60)
    
    if all_installed:
        print("✅ 所有必要依賴套件已安裝")
    else:
        print("❌ 部分依賴套件未安裝")
        print("\n安裝建議:")
        print("  pip install openai-whisper librosa soundfile torch")
    
    return all_installed

def main():
    """主測試函數"""
    print("\n🔍 ASR 模組測試工具\n")
    
    # 測試依賴套件
    deps_ok = test_asr_dependencies()
    
    # 測試模組導入
    imports_ok = test_asr_imports()
    
    # 總結
    print("\n" + "=" * 60)
    print("測試總結")
    print("=" * 60)
    
    if deps_ok and imports_ok:
        print("✅ ASR 模組完全正常，可以使用！")
        print("\n訪問測試頁面: http://localhost:5000/api/asr/test")
    elif imports_ok:
        print("⚠️ ASR 模組可以導入，但部分依賴套件缺失")
        print("   建議安裝缺失的套件以獲得完整功能")
    else:
        print("❌ ASR 模組無法正常使用")
        print("   請檢查錯誤信息並安裝必要的依賴套件")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
