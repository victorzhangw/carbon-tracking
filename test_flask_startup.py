#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask 應用啟動測試
測試應用是否能正常啟動並訪問評分系統相關路由
"""

import sys
import os

# 添加項目根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_creation():
    """測試 Flask 應用創建"""
    print("=" * 60)
    print("🧪 測試 Flask 應用創建")
    print("=" * 60)
    
    try:
        from app import app
        print("✅ Flask 應用創建成功")
        return app
    except Exception as e:
        print(f"❌ Flask 應用創建失敗: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_routes(app):
    """測試路由是否正確註冊"""
    print("\n" + "=" * 60)
    print("🧪 測試路由註冊")
    print("=" * 60)
    
    if not app:
        print("❌ 應用未創建，跳過路由測試")
        return False
    
    try:
        # 獲取所有路由
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': ','.join(rule.methods - {'HEAD', 'OPTIONS'}),
                'path': str(rule)
            })
        
        # 檢查評分系統相關路由
        required_routes = {
            '/emotion-analysis': 'GET',
            '/score-analysis': 'GET',
            '/api/end-session': 'POST',
            '/api/score-history': 'GET',
            '/voice-testing': 'GET'
        }
        
        print(f"\n找到 {len(routes)} 個路由")
        print("\n檢查評分系統相關路由:")
        
        all_found = True
        for path, method in required_routes.items():
            found = False
            for route in routes:
                if path in route['path'] and method in route['methods']:
                    print(f"✅ {method:6} {path}")
                    found = True
                    break
            
            if not found:
                print(f"❌ {method:6} {path} - 未找到")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"❌ 路由測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_templates(app):
    """測試模板文件是否存在"""
    print("\n" + "=" * 60)
    print("🧪 測試模板文件")
    print("=" * 60)
    
    templates = [
        'emotion_analysis.html',
        'score_analysis.html',
        'score_report_modal.html',
        'voice_testing_hub.html'
    ]
    
    all_exist = True
    for template in templates:
        path = os.path.join('templates', template)
        if os.path.exists(path):
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - 文件不存在")
            all_exist = False
    
    return all_exist

def test_static_files():
    """測試靜態文件是否存在"""
    print("\n" + "=" * 60)
    print("🧪 測試靜態文件")
    print("=" * 60)
    
    static_files = [
        'static/css/score_report.css',
        'static/js/score_manager.js'
    ]
    
    all_exist = True
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
            all_exist = False
    
    return all_exist

def test_services():
    """測試服務模組是否可用"""
    print("\n" + "=" * 60)
    print("🧪 測試服務模組")
    print("=" * 60)
    
    services = [
        ('services.score_database', 'score_db'),
        ('services.score_calculator', 'score_calculator')
    ]
    
    all_available = True
    for module_name, obj_name in services:
        try:
            module = __import__(module_name, fromlist=[obj_name])
            obj = getattr(module, obj_name)
            print(f"✅ {module_name}.{obj_name}")
        except Exception as e:
            print(f"❌ {module_name}.{obj_name} - {e}")
            all_available = False
    
    return all_available

def main():
    """主測試函數"""
    print("\n" + "=" * 60)
    print("🚀 Flask 應用啟動測試")
    print("=" * 60)
    print()
    
    results = []
    
    # 測試應用創建
    app = test_app_creation()
    results.append(("應用創建", app is not None))
    
    # 測試路由
    if app:
        results.append(("路由註冊", test_routes(app)))
    
    # 測試模板
    results.append(("模板文件", test_templates(app)))
    
    # 測試靜態文件
    results.append(("靜態文件", test_static_files()))
    
    # 測試服務
    results.append(("服務模組", test_services()))
    
    # 顯示測試結果
    print("\n" + "=" * 60)
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
        print("\n🎉 所有測試通過！應用可以正常啟動！")
        print("\n💡 啟動命令:")
        print("   python app.py")
        print("   或")
        print("   bStart.bat")
        print("\n📍 訪問地址:")
        print("   情緒分析: http://localhost:5000/emotion-analysis")
        print("   評分分析: http://localhost:5000/score-analysis")
        print("   語音測試: http://localhost:5000/voice-testing")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 個測試失敗，請檢查錯誤訊息")
        return 1

if __name__ == "__main__":
    sys.exit(main())
