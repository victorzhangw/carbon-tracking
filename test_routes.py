"""
測試路由配置
"""

def test_routes():
    """測試所有路由是否正確配置"""
    print("=" * 60)
    print("測試路由配置")
    print("=" * 60)
    
    try:
        from app import app
        
        # 獲取所有路由
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': ','.join(rule.methods),
                'path': str(rule)
            })
        
        # 按路徑排序
        routes.sort(key=lambda x: x['path'])
        
        print(f"\n找到 {len(routes)} 個路由:\n")
        
        # 檢查關鍵路由
        key_routes = ['/', '/login', '/portal', '/emotion-analysis']
        
        for route_path in key_routes:
            found = False
            for route in routes:
                if route['path'] == route_path:
                    print(f"✅ {route_path:30} → {route['endpoint']}")
                    found = True
                    break
            if not found:
                print(f"❌ {route_path:30} → 未找到")
        
        print("\n" + "=" * 60)
        print("所有路由列表:")
        print("=" * 60)
        
        for route in routes:
            if not route['endpoint'].startswith('static'):
                print(f"{route['path']:40} → {route['endpoint']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_redirect():
    """測試首頁重定向"""
    print("\n" + "=" * 60)
    print("測試首頁重定向")
    print("=" * 60)
    
    try:
        from app import app
        
        with app.test_client() as client:
            # 測試首頁
            response = client.get('/', follow_redirects=False)
            print(f"\n訪問 /")
            print(f"  狀態碼: {response.status_code}")
            print(f"  重定向到: {response.location if response.status_code in [301, 302] else 'N/A'}")
            
            if response.status_code in [301, 302]:
                if '/login' in response.location:
                    print("  ✅ 正確重定向到登入頁面")
                else:
                    print(f"  ⚠️ 重定向目標不正確: {response.location}")
            else:
                print(f"  ❌ 沒有重定向 (狀態碼: {response.status_code})")
            
            # 測試登入頁面
            response = client.get('/login')
            print(f"\n訪問 /login")
            print(f"  狀態碼: {response.status_code}")
            if response.status_code == 200:
                print("  ✅ 登入頁面可訪問")
            else:
                print(f"  ❌ 登入頁面無法訪問 (狀態碼: {response.status_code})")
            
            # 測試 portal 頁面
            response = client.get('/portal')
            print(f"\n訪問 /portal")
            print(f"  狀態碼: {response.status_code}")
            if response.status_code == 200:
                print("  ✅ Portal 頁面可訪問")
            else:
                print(f"  ❌ Portal 頁面無法訪問 (狀態碼: {response.status_code})")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主測試函數"""
    print("\n🔍 路由配置測試工具\n")
    
    # 測試路由配置
    routes_ok = test_routes()
    
    # 測試重定向
    redirect_ok = test_redirect()
    
    # 總結
    print("\n" + "=" * 60)
    print("測試總結")
    print("=" * 60)
    
    if routes_ok and redirect_ok:
        print("✅ 所有測試通過")
        print("\n建議:")
        print("1. 清除瀏覽器緩存")
        print("2. 重啟 Flask 應用")
        print("3. 訪問 http://localhost:5000/")
    else:
        print("❌ 部分測試失敗")
        print("\n請檢查:")
        print("1. routes/main.py 中的路由定義")
        print("2. app.py 中的 blueprint 註冊")
        print("3. Flask 應用是否正確啟動")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
