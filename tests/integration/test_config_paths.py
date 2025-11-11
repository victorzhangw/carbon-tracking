"""
驗證配置檔案和路徑引用
"""
import sys
import os
from pathlib import Path

# 確保可以導入專案模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_config_files():
    """測試配置檔案是否存在"""
    print("=" * 80)
    print("驗證配置檔案")
    print("=" * 80)
    
    config_files = [
        'config/requirements/base.txt',
        'config/requirements/voice.txt',
        'config/requirements/asr.txt',
        'config/requirements/carbon.txt',
        'config/requirements/full.txt',
        'config/requirements/minimal.txt',
        'config/deployment/render.yaml',
        'config/deployment/Dockerfile.voice-api',
        'config/deployment/nginx-voice.conf',
    ]
    
    missing = []
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file}")
        else:
            print(f"❌ {config_file} - 不存在")
            missing.append(config_file)
    
    print()
    if missing:
        print(f"⚠️  缺少 {len(missing)} 個配置檔案")
        return False
    else:
        print("✅ 所有配置檔案都存在")
        return True

def test_static_resources():
    """測試靜態資源路徑"""
    print("\n" + "=" * 80)
    print("驗證靜態資源路徑")
    print("=" * 80)
    
    static_paths = [
        'static/manifest.json',
        'static/sw.js',
        'static/pwa-register.js',
        'static/favicon.ico',
        'static/icons',
    ]
    
    missing = []
    for path in static_paths:
        if os.path.exists(path):
            print(f"✅ {path}")
        else:
            print(f"❌ {path} - 不存在")
            missing.append(path)
    
    print()
    if missing:
        print(f"⚠️  缺少 {len(missing)} 個靜態資源")
        return False
    else:
        print("✅ 所有靜態資源都存在")
        return True

def test_database_paths():
    """測試資料庫路徑"""
    print("\n" + "=" * 80)
    print("驗證資料庫路徑")
    print("=" * 80)
    
    # 檢查資料庫目錄
    db_dir = 'data/databases'
    if os.path.exists(db_dir):
        print(f"✅ 資料庫目錄存在: {db_dir}")
        
        # 列出資料庫檔案
        db_files = [f for f in os.listdir(db_dir) if f.endswith('.db')]
        print(f"   找到 {len(db_files)} 個資料庫檔案:")
        for db_file in db_files:
            print(f"   - {db_file}")
    else:
        print(f"❌ 資料庫目錄不存在: {db_dir}")
        return False
    
    # 測試資料庫連接
    try:
        from modules.carbon_tracking.database_carbon_tracking import CarbonTrackingDB
        db = CarbonTrackingDB()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM visit_records")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ 資料庫連接正常，共有 {count} 筆訪視記錄")
        return True
    except Exception as e:
        print(f"❌ 資料庫連接失敗: {e}")
        return False

def test_log_paths():
    """測試日誌路徑"""
    print("\n" + "=" * 80)
    print("驗證日誌路徑")
    print("=" * 80)
    
    log_dir = 'data/logs'
    if os.path.exists(log_dir):
        print(f"✅ 日誌目錄存在: {log_dir}")
        
        # 列出日誌檔案
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
        if log_files:
            print(f"   找到 {len(log_files)} 個日誌檔案:")
            for log_file in log_files:
                print(f"   - {log_file}")
        else:
            print("   目前沒有日誌檔案")
        return True
    else:
        print(f"❌ 日誌目錄不存在: {log_dir}")
        return False

def test_template_paths():
    """測試模板路徑"""
    print("\n" + "=" * 80)
    print("驗證模板路徑")
    print("=" * 80)
    
    template_paths = [
        'templates/carbon_tracking/index.html',
        'templates/carbon_tracking/dashboard.html',
        'templates/carbon_tracking/visit_records.html',
        'templates/carbon_tracking/add_visit.html',
        'templates/carbon_tracking/edit_visit.html',
        'templates/carbon_tracking/statistics.html',
    ]
    
    missing = []
    for path in template_paths:
        if os.path.exists(path):
            print(f"✅ {path}")
        else:
            print(f"❌ {path} - 不存在")
            missing.append(path)
    
    print()
    if missing:
        print(f"⚠️  缺少 {len(missing)} 個模板檔案")
        return False
    else:
        print("✅ 所有模板檔案都存在")
        return True

def main():
    """執行所有驗證測試"""
    print("\n" + "=" * 80)
    print("配置和路徑驗證測試")
    print("=" * 80)
    print()
    
    results = []
    
    # 執行各項測試
    results.append(("配置檔案", test_config_files()))
    results.append(("靜態資源", test_static_resources()))
    results.append(("資料庫路徑", test_database_paths()))
    results.append(("日誌路徑", test_log_paths()))
    results.append(("模板路徑", test_template_paths()))
    
    # 總結
    print("\n" + "=" * 80)
    print("測試總結")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {name}")
    
    print()
    print(f"總計: {passed}/{total} 項測試通過")
    
    if passed == total:
        print("\n✅ 所有配置和路徑驗證通過！")
        return True
    else:
        print(f"\n⚠️  有 {total - passed} 項測試失敗")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
