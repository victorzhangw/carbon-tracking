#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
測試 GPT-SoVITS 整合
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_files_exist():
    """測試必要文件是否存在"""
    print("=" * 60)
    print("🧪 測試文件存在性")
    print("=" * 60)
    
    files = [
        'services/gptsovits_service.py',
        'routes/gptsovits.py',
        'templates/tts_training.html',
        'GPT-SoVITS-v2pro-20250604/go-webui.bat',
        'GPT-SoVITS-v2pro-20250604/webui.py'
    ]
    
    all_exist = True
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
            all_exist = False
    
    print()
    return all_exist

def test_imports():
    """測試模組導入"""
    print("=" * 60)
    print("🧪 測試模組導入")
    print("=" * 60)
    
    try:
        from services.gptsovits_service import gptsovits_service
        print("✅ gptsovits_service 導入成功")
    except Exception as e:
        print(f"❌ gptsovits_service 導入失敗: {e}")
        return False
    
    try:
        from routes.gptsovits import gptsovits_bp
        print("✅ gptsovits_bp 導入成功")
    except Exception as e:
        print(f"❌ gptsovits_bp 導入失敗: {e}")
        return False
    
    print()
    return True

def test_service_config():
    """測試服務配置"""
    print("=" * 60)
    print("🧪 測試服務配置")
    print("=" * 60)
    
    try:
        from services.gptsovits_service import gptsovits_service
        
        print(f"GPT-SoVITS 目錄: {gptsovits_service.gptsovits_dir}")
        print(f"WebUI URL: {gptsovits_service.webui_url}")
        print(f"啟動腳本: {gptsovits_service.startup_script}")
        
        if os.path.exists(gptsovits_service.gptsovits_dir):
            print("✅ GPT-SoVITS 目錄存在")
        else:
            print("❌ GPT-SoVITS 目錄不存在")
            return False
        
        if os.path.exists(gptsovits_service.startup_script):
            print("✅ 啟動腳本存在")
        else:
            print("❌ 啟動腳本不存在")
            return False
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_routes():
    """測試路由註冊"""
    print("=" * 60)
    print("🧪 測試路由註冊")
    print("=" * 60)
    
    try:
        from app import app
        
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(str(rule))
        
        required_routes = [
            '/tts-training',
            '/api/gptsovits/status',
            '/api/gptsovits/start',
            '/api/gptsovits/stop'
        ]
        
        all_found = True
        for route in required_routes:
            if any(route in r for r in routes):
                print(f"✅ 路由存在: {route}")
            else:
                print(f"❌ 路由缺失: {route}")
                all_found = False
        
        print()
        return all_found
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主測試函數"""
    print("\n" + "=" * 60)
    print("🚀 GPT-SoVITS 整合測試")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("文件存在性", test_files_exist()))
    results.append(("模組導入", test_imports()))
    results.append(("服務配置", test_service_config()))
    results.append(("路由註冊", test_routes()))
    
    print("=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {name}")
    
    print()
    print(f"總計: {passed}/{total} 測試通過")
    
    if passed == total:
        print("\n🎉 所有測試通過！")
        print("\n💡 下一步:")
        print("   1. 啟動 Flask 應用: bStart.bat")
        print("   2. 訪問語音測試訓練模組: http://localhost:5000/voice-testing")
        print("   3. 點擊「TTS 語音合成訓練」卡片")
        print("   4. 等待 GPT-SoVITS 啟動（20-30 秒）")
        print("   5. 開始使用訓練功能！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 個測試失敗")
        return 1

if __name__ == "__main__":
    sys.exit(main())
