"""
FunASR 模型下載腳本
自動下載 Paraformer 模型到本地
"""

import os
import sys


def download_model():
    """下載 FunASR 模型"""
    
    print("=" * 70)
    print("FunASR Paraformer 模型下載工具")
    print("=" * 70)
    
    # 檢查 modelscope 是否安裝
    try:
        from modelscope.hub.snapshot_download import snapshot_download
    except ImportError:
        print("\n✗ ModelScope 未安裝")
        print("\n請先安裝 ModelScope:")
        print("  pip install modelscope")
        return False
    
    # 創建模型目錄
    models_dir = './models'
    os.makedirs(models_dir, exist_ok=True)
    print(f"\n✓ 模型目錄: {os.path.abspath(models_dir)}")
    
    # 模型信息
    model_id = 'iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch'
    print(f"\n模型 ID: {model_id}")
    print("模型大小: 約 270-320 MB")
    print("\n開始下載...")
    print("這可能需要幾分鐘，請耐心等待...")
    print("-" * 70)
    
    try:
        # 下載模型
        model_dir = snapshot_download(
            model_id,
            cache_dir=models_dir,
            revision='master'
        )
        
        print("-" * 70)
        print("\n✓ 模型下載成功！")
        print(f"\n模型路徑: {model_dir}")
        
        # 檢查關鍵文件
        print("\n檢查模型文件...")
        required_files = ['am.mvn', 'config.yaml', 'tokens.txt']
        all_exist = True
        
        for file in required_files:
            file_path = os.path.join(model_dir, file)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"  ✓ {file} ({size:,} bytes)")
            else:
                print(f"  ✗ {file} (缺失)")
                all_exist = False
        
        # 檢查模型權重文件
        model_files = ['model.pb', 'model.pt', 'model.pth']
        model_found = False
        for mf in model_files:
            mf_path = os.path.join(model_dir, mf)
            if os.path.exists(mf_path):
                size = os.path.getsize(mf_path)
                print(f"  ✓ {mf} ({size:,} bytes)")
                model_found = True
                break
        
        if not model_found:
            print(f"  ✗ 模型權重文件 (缺失)")
            all_exist = False
        
        if all_exist:
            print("\n✓ 所有必需文件已就緒")
            
            # 創建符號鏈接或複製到標準位置
            standard_path = os.path.join(models_dir, 'paraformer-zh')
            if not os.path.exists(standard_path):
                print(f"\n創建標準路徑鏈接: {standard_path}")
                try:
                    # Windows 使用 junction，Linux/Mac 使用 symlink
                    if sys.platform == 'win32':
                        os.system(f'mklink /J "{standard_path}" "{model_dir}"')
                    else:
                        os.symlink(model_dir, standard_path)
                    print("✓ 鏈接創建成功")
                except Exception as e:
                    print(f"⚠ 鏈接創建失敗: {e}")
                    print(f"請手動使用路徑: {model_dir}")
            
            print("\n" + "=" * 70)
            print("下一步:")
            print("=" * 70)
            print("\n1. 運行測試:")
            print("   python test_funasr_engine.py")
            print("\n2. 在代碼中使用:")
            print("   from services.asr.funasr_engine import FunASREngine")
            print(f"   engine = FunASREngine(local_model_path='{model_dir}')")
            print("\n3. 或設置環境變量:")
            print(f"   set FUNASR_MODEL_PATH={model_dir}")
            print("=" * 70)
            
            return True
        else:
            print("\n✗ 部分文件缺失，請重新下載")
            return False
            
    except Exception as e:
        print("-" * 70)
        print(f"\n✗ 下載失敗: {e}")
        print("\n可能的原因:")
        print("  1. 網絡連接問題")
        print("  2. ModelScope 服務器問題")
        print("  3. 磁盤空間不足")
        print("\n解決方案:")
        print("  1. 檢查網絡連接")
        print("  2. 配置代理: set HTTP_PROXY=http://proxy:port")
        print("  3. 稍後重試")
        print("  4. 參考手動安裝指南: docs/funasr_manual_install.md")
        return False


if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
