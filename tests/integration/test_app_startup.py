"""
測試 app.py 啟動和核心功能
"""
import sys
import os

# 確保可以導入專案模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_app_startup():
    """測試應用程式啟動"""
    print("=" * 60)
    print("測試 app.py 啟動")
    print("=" * 60)
    
    try:
        # 導入 app
        from app import app
        print("✅ app.py 成功導入")
        
        # 檢查 Flask app 是否正確初始化
        assert app is not None, "Flask app 未初始化"
        print("✅ Flask app 已初始化")
        
        # 檢查碳排放路由是否註冊
        carbon_routes = [rule.rule for rule in app.url_map.iter_rules() if '/carbon' in rule.rule]
        assert len(carbon_routes) > 0, "碳排放路由未註冊"
        print(f"✅ 碳排放路由已註冊 ({len(carbon_routes)} 個路由)")
        
        # 測試應用程式上下文
        with app.app_context():
            print("✅ 應用程式上下文正常")
        
        # 測試測試客戶端
        client = app.test_client()
        print("✅ 測試客戶端建立成功")
        
        # 測試基本路由
        response = client.get('/carbon/')
        print(f"✅ /carbon/ 回應狀態: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 碳排放首頁正常")
        else:
            print(f"⚠️ 碳排放首頁返回: {response.status_code}")
        
        # 測試 API 路由
        response = client.get('/carbon/api/statistics-summary')
        print(f"✅ API 回應狀態: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API 正常運作")
        
        print("\n" + "=" * 60)
        print("✅ app.py 啟動測試完成")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_app_startup()
    sys.exit(0 if success else 1)
