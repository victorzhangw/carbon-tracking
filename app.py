from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import ensure_directories
from database import init_db
import datetime

# 初始化 Flask 應用
app = Flask(__name__)
CORS(app)

# JWT 配置
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'  # 生產環境請更換
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=8)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)

# 初始化 JWT
jwt = JWTManager(app)

# 碳排放追蹤系統（核心功能，必須載入）
from routes.carbon_tracking import carbon_bp
app.register_blueprint(carbon_bp)
print("✅ 碳排放追蹤系統已載入")

# 其他路由模塊（條件式載入）
# 如果相關套件不存在，則跳過該模組
optional_modules = []

try:
    from routes.main import main_bp
    app.register_blueprint(main_bp)
    optional_modules.append("主頁面")
except ImportError as e:
    print(f"⚠️ 主頁面模組未載入: {e}")

try:
    from routes.staff import staff_bp
    app.register_blueprint(staff_bp)
    optional_modules.append("員工管理")
except ImportError as e:
    print(f"⚠️ 員工管理模組未載入: {e}")

try:
    from routes.audio import audio_bp
    app.register_blueprint(audio_bp)
    optional_modules.append("音訊處理")
except ImportError as e:
    print(f"⚠️ 音訊處理模組未載入: {e}")

try:
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    optional_modules.append("認證系統")
except ImportError as e:
    print(f"⚠️ 認證系統模組未載入: {e}")

try:
    from routes.voice_clone import voice_clone_bp
    app.register_blueprint(voice_clone_bp)
    optional_modules.append("語音克隆")
except ImportError as e:
    print(f"⚠️ 語音克隆模組未載入: {e}")

try:
    from routes.simple_tts import simple_tts_bp
    app.register_blueprint(simple_tts_bp)
    optional_modules.append("TTS")
except ImportError as e:
    print(f"⚠️ TTS模組未載入: {e}")

try:
    from routes.voice_chat import voice_chat_bp
    app.register_blueprint(voice_chat_bp)
    optional_modules.append("語音對話")
except ImportError as e:
    print(f"⚠️ 語音對話模組未載入: {e}")

try:
    from routes.emotion import emotion_bp
    app.register_blueprint(emotion_bp)
    optional_modules.append("情緒識別")
except ImportError as e:
    print(f"⚠️ 情緒識別模組未載入: {e}")

try:
    from routes.asr import asr_bp
    app.register_blueprint(asr_bp)
    optional_modules.append("ASR語音識別")
except ImportError as e:
    print(f"⚠️ ASR語音識別模組未載入: {e}")

if optional_modules:
    print(f"✅ 已載入可選模組: {', '.join(optional_modules)}")

# 隱私權政策路由
@app.route('/privacy')
def privacy_policy():
    from flask import render_template
    return render_template('privacy_policy.html')

# 應用初始化
def init_app():
    """初始化應用程序"""
    # 初始化資料庫
    init_db()
    
    # 確保必要的目錄存在
    ensure_directories()

# 應用入口
if __name__ == "__main__":
    import os
    
    print("=== AI 客服語音克隆系統啟動中 ===")
    
    try:
        # 初始化應用程序
        print("正在初始化應用程序...")
        init_app()
        print("✅ 應用程序初始化成功")
        
        # 從環境變數讀取設定
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('DEBUG', 'False').lower() == 'true'
        
        print("正在啟動 Flask 服務器...")
        print(f"服務器將在 http://0.0.0.0:{port} 上運行")
        print("按 Ctrl+C 停止服務器")
        print("=" * 50)
        
        app.run(debug=debug, host='0.0.0.0', port=port)
        
    except KeyboardInterrupt:
        print("\n服務器已停止")
    except Exception as e:
        print(f"\n❌ 啟動失敗: {e}")
        import traceback
        traceback.print_exc()