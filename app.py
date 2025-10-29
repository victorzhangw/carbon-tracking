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

# 引入各個路由模塊
from routes.main import main_bp
from routes.staff import staff_bp
from routes.audio import audio_bp
from routes.auth import auth_bp
from routes.voice_clone import voice_clone_bp
from routes.simple_tts import simple_tts_bp
from routes.voice_chat import voice_chat_bp
from routes.emotion import emotion_bp

# 註冊藍圖
app.register_blueprint(main_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(audio_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(voice_clone_bp)
app.register_blueprint(simple_tts_bp)
app.register_blueprint(voice_chat_bp)
app.register_blueprint(emotion_bp)

# 應用初始化
def init_app():
    """初始化應用程序"""
    # 初始化資料庫
    init_db()
    
    # 確保必要的目錄存在
    ensure_directories()

# 應用入口
if __name__ == "__main__":
    print("=== AI 客服語音克隆系統啟動中 ===")
    
    try:
        # 初始化應用程序
        print("正在初始化應用程序...")
        init_app()
        print("✅ 應用程序初始化成功")
        
        print("正在啟動 Flask 服務器...")
        print("服務器將在 http://127.0.0.1:5000 上運行")
        print("按 Ctrl+C 停止服務器")
        print("=" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n服務器已停止")
    except Exception as e:
        print(f"\n❌ 啟動失敗: {e}")
        import traceback
        traceback.print_exc()