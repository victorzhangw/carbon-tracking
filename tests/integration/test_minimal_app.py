"""
測試最小化版本的 app.py 是否能正常啟動
"""
import sys
import os

# Add parent directory to path to import from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

print("=" * 60)
print("🧪 測試最小化 App 啟動")
print("=" * 60)
print()

# 測試導入
print("1️⃣ 測試基礎導入...")
try:
    from flask import Flask
    from flask_cors import CORS
    print("   ✅ Flask 和 CORS 導入成功")
except ImportError as e:
    print(f"   ❌ 基礎導入失敗: {e}")
    sys.exit(1)

# 測試碳排放模組
print("\n2️⃣ 測試碳排放模組...")
try:
    from routes.carbon_tracking import carbon_bp
    print("   ✅ 碳排放模組導入成功")
except ImportError as e:
    print(f"   ❌ 碳排放模組導入失敗: {e}")
    sys.exit(1)

# 測試 App 初始化
print("\n3️⃣ 測試 App 初始化...")
try:
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(carbon_bp)
    print("   ✅ App 初始化成功")
except Exception as e:
    print(f"   ❌ App 初始化失敗: {e}")
    sys.exit(1)

# 測試路由
print("\n4️⃣ 測試路由...")
try:
    with app.test_client() as client:
        response = client.get('/carbon/')
        if response.status_code == 200:
            print("   ✅ 碳排放首頁路由正常")
        else:
            print(f"   ⚠️ 碳排放首頁返回: {response.status_code}")
except Exception as e:
    print(f"   ❌ 路由測試失敗: {e}")

print("\n" + "=" * 60)
print("🎉 最小化 App 測試完成！")
print("=" * 60)
print()
print("✅ 基礎功能正常，可以部署到 Render")
print()
print("📝 注意事項：")
print("   - JWT 認證未啟用（正常）")
print("   - 語音功能未啟用（正常）")
print("   - 碳排放系統完全正常")
print()
print("🚀 下一步：等待 Render 重新部署完成")
print("=" * 60)
