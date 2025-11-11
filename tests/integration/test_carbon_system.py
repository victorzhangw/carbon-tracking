"""
測試碳排放追蹤系統
"""

print("="*60)
print("測試碳排放追蹤系統")
print("="*60)

# 測試1：檢查資料庫
print("\n1. 檢查資料庫...")
try:
    import sys
    import os
    # Add parent directory to path to import from root
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    
    from modules.carbon_tracking.database_carbon_tracking import CarbonTrackingDB
    db = CarbonTrackingDB()
    print("   ✓ 資料庫連線成功")
    
    # 檢查資料
    stats = db.get_statistics_summary('2024-06-01', '2024-09-30')
    print(f"   ✓ 資料庫有資料：{stats['total_visits']} 筆訪視記錄")
except Exception as e:
    print(f"   ✗ 資料庫錯誤：{e}")

# 測試2：檢查路由
print("\n2. 檢查路由模組...")
try:
    from routes.carbon_tracking import carbon_bp
    print("   ✓ 路由模組載入成功")
    print(f"   ✓ 路由前綴：{carbon_bp.url_prefix}")
except Exception as e:
    print(f"   ✗ 路由模組錯誤：{e}")

# 測試3：檢查Flask應用
print("\n3. 檢查Flask應用...")
try:
    from app import app
    print("   ✓ Flask應用載入成功")
    
    # 列出所有路由
    print("\n   已註冊的碳排放路由：")
    for rule in app.url_map.iter_rules():
        if 'carbon' in rule.rule:
            print(f"   - {rule.rule}")
    
except Exception as e:
    print(f"   ✗ Flask應用錯誤：{e}")
    import traceback
    traceback.print_exc()

# 測試4：測試啟動
print("\n4. 測試Flask啟動...")
try:
    from app import app
    
    # 建立測試客戶端
    with app.test_client() as client:
        # 測試首頁
        response = client.get('/carbon/')
        print(f"   ✓ /carbon/ 回應狀態：{response.status_code}")
        
        # 測試API
        response = client.get('/carbon/api/statistics-summary?start_date=2024-06-01&end_date=2024-09-30')
        print(f"   ✓ API 回應狀態：{response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✓ API 資料正常：{data}")
        
except Exception as e:
    print(f"   ✗ 測試錯誤：{e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("測試完成")
print("="*60)
print("\n如果所有測試都通過，請執行：")
print("  python app.py")
print("\n然後訪問：")
print("  http://localhost:5000/carbon/")
print("="*60)
