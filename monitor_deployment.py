"""
監控 Render 部署狀態
每 30 秒檢查一次，直到部署成功
"""
import requests
import time
from datetime import datetime

BASE_URL = "https://carbon-tracking.onrender.com"
CHECK_INTERVAL = 30  # 秒
MAX_ATTEMPTS = 20  # 最多檢查 20 次（10 分鐘）

def check_deployment():
    """檢查部署狀態"""
    try:
        response = requests.get(f"{BASE_URL}/carbon/", timeout=30)
        return response.status_code == 200
    except Exception:
        return False

def main():
    print("=" * 60)
    print("🔍 開始監控 Render 部署狀態")
    print(f"📍 網址: {BASE_URL}")
    print(f"⏱️  檢查間隔: {CHECK_INTERVAL} 秒")
    print("=" * 60)
    print()
    
    for attempt in range(1, MAX_ATTEMPTS + 1):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] 第 {attempt}/{MAX_ATTEMPTS} 次檢查...", end=" ")
        
        if check_deployment():
            print("✅ 成功！")
            print()
            print("=" * 60)
            print("🎉 部署成功！")
            print("=" * 60)
            print()
            print("📱 現在可以：")
            print("1. 在瀏覽器訪問：https://carbon-tracking.onrender.com/carbon/")
            print("2. 執行完整測試：python test_deployment.py")
            print("3. 開始建置 Android APK")
            print()
            print("🚀 下一步：開啟 Android Studio 建置 APK")
            print("   詳見：android_app/建置APK步驟.md")
            print("=" * 60)
            return True
        else:
            print("⏳ 部署中...")
            if attempt < MAX_ATTEMPTS:
                print(f"   等待 {CHECK_INTERVAL} 秒後重試...")
                time.sleep(CHECK_INTERVAL)
    
    print()
    print("=" * 60)
    print("⚠️ 超過最大檢查次數")
    print("=" * 60)
    print()
    print("可能原因：")
    print("1. 部署時間較長（正常，首次部署可能需要 15 分鐘）")
    print("2. 部署失敗（需要查看 Render 日誌）")
    print()
    print("建議行動：")
    print("1. 訪問 Render Dashboard：https://dashboard.render.com")
    print("2. 查看 carbon-tracking 服務狀態")
    print("3. 檢查部署日誌")
    print("4. 如有錯誤，截圖給我協助")
    print("=" * 60)
    return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 監控已停止")
        print("你可以隨時執行 python test_deployment.py 手動測試")
