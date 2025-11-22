#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS 訓練模組 Modal 測試
測試 iframe 顯示和路由配置
"""

import os
import sys

def test_template_changes():
    """測試模板文件修改"""
    print("=" * 60)
    print("🧪 測試模板文件修改")
    print("=" * 60)
    
    template_file = "templates/voice_testing_hub.html"
    
    if not os.path.exists(template_file):
        print(f"❌ 模板文件不存在: {template_file}")
        return False
    
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查是否移除了舊的 TTS 卡片
    if 'TTS 語音合成</h3>' in content and '聲音模擬' in content:
        print("❌ 舊的 TTS 語音合成卡片仍然存在")
        return False
    else:
        print("✅ 舊的 TTS 語音合成卡片已移除")
    
    # 檢查是否添加了 Modal
    if 'id="ttsModal"' in content:
        print("✅ TTS Modal 已添加")
    else:
        print("❌ TTS Modal 未添加")
        return False
    
    # 檢查是否使用 onclick 而不是 href
    if 'onclick="openTTSTraining()"' in content:
        print("✅ TTS 卡片使用 onclick 事件")
    else:
        print("❌ TTS 卡片未使用 onclick 事件")
        return False
    
    # 檢查是否有 JavaScript 函數
    if 'function openTTSTraining()' in content:
        print("✅ openTTSTraining() 函數已添加")
    else:
        print("❌ openTTSTraining() 函數未添加")
        return False
    
    if 'function closeTTSTraining()' in content:
        print("✅ closeTTSTraining() 函數已添加")
    else:
        print("❌ closeTTSTraining() 函數未添加")
        return False
    
    # 檢查 iframe
    if '<iframe id="ttsFrame"' in content:
        print("✅ TTS iframe 已添加")
    else:
        print("❌ TTS iframe 未添加")
        return False
    
    return True

def test_app_routes():
    """測試 app.py 路由配置"""
    print("\n" + "=" * 60)
    print("🧪 測試 app.py 路由配置")
    print("=" * 60)
    
    app_file = "app.py"
    
    if not os.path.exists(app_file):
        print(f"❌ app.py 不存在")
        return False
    
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查是否註釋掉了 simple_tts
    if 'from routes.simple_tts import simple_tts_bp' in content:
        # 檢查是否被註釋
        lines = content.split('\n')
        simple_tts_lines = [line for line in lines if 'simple_tts' in line]
        
        commented = all(line.strip().startswith('#') for line in simple_tts_lines if 'simple_tts' in line)
        
        if commented:
            print("✅ simple_tts 路由已被註釋")
        else:
            print("❌ simple_tts 路由仍在使用")
            return False
    else:
        print("✅ simple_tts 路由已移除")
    
    # 檢查 GPT-SoVITS 路由是否存在
    if 'from routes.gptsovits import gptsovits_bp' in content:
        print("✅ GPT-SoVITS 路由已註冊")
    else:
        print("❌ GPT-SoVITS 路由未註冊")
        return False
    
    return True

def test_route_accessibility():
    """測試路由可訪問性"""
    print("\n" + "=" * 60)
    print("🧪 測試路由可訪問性")
    print("=" * 60)
    
    try:
        from app import app
        
        with app.test_client() as client:
            # 測試語音測試頁面
            response = client.get('/voice-testing')
            if response.status_code == 200:
                print("✅ /voice-testing 可訪問")
            else:
                print(f"❌ /voice-testing 返回 {response.status_code}")
                return False
            
            # 測試 TTS 訓練頁面
            response = client.get('/tts-training')
            if response.status_code == 200:
                print("✅ /tts-training 可訪問")
            else:
                print(f"❌ /tts-training 返回 {response.status_code}")
                return False
            
            # 測試 GPT-SoVITS API
            response = client.get('/api/gptsovits/status')
            if response.status_code == 200:
                print("✅ /api/gptsovits/status 可訪問")
            else:
                print(f"❌ /api/gptsovits/status 返回 {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 測試路由時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主測試函數"""
    print("\n" + "=" * 60)
    print("🚀 TTS 訓練模組 Modal 測試")
    print("=" * 60)
    
    results = {
        "模板文件修改": test_template_changes(),
        "路由配置": test_app_routes(),
        "路由可訪問性": test_route_accessibility()
    }
    
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {test_name}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n總計: {passed}/{total} 測試通過")
    
    if passed == total:
        print("\n🎉 所有測試通過！")
        print("\n💡 修改內容:")
        print("   1. ✅ 移除了舊的「TTS 語音合成」卡片")
        print("   2. ✅ TTS 訓練卡片改用 Modal 顯示")
        print("   3. ✅ 使用 iframe 嵌入，不會跳轉頁面")
        print("   4. ✅ 註釋掉了舊的 simple_tts 路由")
        print("\n🚀 啟動測試:")
        print("   1. 執行: bStart.bat")
        print("   2. 訪問: http://localhost:5000/voice-testing")
        print("   3. 點擊「TTS 語音合成訓練」卡片")
        print("   4. 應該在 Modal 中顯示，不會跳轉頁面")
        return 0
    else:
        print("\n❌ 部分測試失敗，請檢查錯誤信息")
        return 1

if __name__ == "__main__":
    sys.exit(main())
