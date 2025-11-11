"""
測試 Render 部署是否正常運作
"""
import requests
import json

# 你的 Render 網址
BASE_URL = "https://carbon-tracking.onrender.com"

def test_homepage():
    """測試首頁"""
    print("🧪 測試首頁...")
    try:
        response = requests.get(BASE_URL, timeout=30)
        if response.status_code == 200:
            print("✅ 首頁正常")
            return True
        else:
            print(f"❌ 首頁錯誤: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 連接失敗: {e}")
        return False

def test_carbon_system():
    """測試碳排放系統"""
    print("\n🧪 測試碳排放系統...")
    try:
        response = requests.get(f"{BASE_URL}/carbon/", timeout=30)
        if response.status_code == 200:
            print("✅ 碳排放系統正常")
            return True
        else:
            print(f"❌ 碳排放系統錯誤: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 連接失敗: {e}")
        return False

def test_api_endpoints():
    """測試 API 端點"""
    print("\n🧪 測試 API 端點...")
    
    endpoints = [
        "/carbon/api/visits",
        "/carbon/api/statistics",
        "/carbon/api/social_workers"
    ]
    
    all_ok = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=30)
            if response.status_code == 200:
                print(f"✅ {endpoint} - 正常")
            else:
                print(f"❌ {endpoint} - 錯誤: {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"❌ {endpoint} - 失敗: {e}")
            all_ok = False
    
    return all_ok

def main():
    print("=" * 60)
    print("🚀 測試 Render 部署")
    print(f"📍 網址: {BASE_URL}")
    print("=" * 60)
    
    # 測試首頁
    homepage_ok = test_homepage()
    
    # 測試碳排放系統
    carbon_ok = test_carbon_system()
    
    # 測試 API
    api_ok = test_api_endpoints()
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    print(f"首頁: {'✅ 正常' if homepage_ok else '❌ 失敗'}")
    print(f"碳排放系統: {'✅ 正常' if carbon_ok else '❌ 失敗'}")
    print(f"API 端點: {'✅ 正常' if api_ok else '❌ 失敗'}")
    
    if homepage_ok and carbon_ok and api_ok:
        print("\n🎉 所有測試通過！部署成功！")
        print("\n📱 下一步：建置 Android APK")
        print("   詳見：android_app/建置APK步驟.md")
    else:
        print("\n⚠️ 部分測試失敗，請檢查 Render 部署狀態")
        print("   1. 訪問 Render Dashboard")
        print("   2. 查看部署日誌")
        print("   3. 確認服務正在運行")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
