from flask import Flask
from flask_cors import CORS
import datetime
import os

# 載入環境變數
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ 環境變數已載入")
except ImportError:
    print("⚠️ python-dotenv 未安裝，使用系統環境變數")

# 初始化 Flask 應用
app = Flask(__name__)
CORS(app)

# 開發模式配置：啟用模板自動重載
app.config['TEMPLATES_AUTO_RELOAD'] = True

# SocketIO 配置（用於即時語音互動）
try:
    from flask_socketio import SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")
    print("✅ SocketIO 已啟用")
except ImportError:
    socketio = None
    print("⚠️ SocketIO 未安裝（即時語音互動功能將不可用）")

# JWT 配置（條件式）
try:
    from flask_jwt_extended import JWTManager
    app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=8)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)
    jwt = JWTManager(app)
    print("✅ JWT 認證已啟用")
except ImportError:
    print("⚠️ JWT 認證未安裝（僅基礎功能模式）")

# 碳排放追蹤系統（核心功能，必須載入）
from routes.carbon_tracking import carbon_bp
app.register_blueprint(carbon_bp)
print("✅ 碳排放追蹤系統已載入")

# 其他路由模組（條件式載入）
# 如果相關套件不存在，則跳過該模組
optional_modules = []

try:
    from routes.main import main
    app.register_blueprint(main)
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

# simple_tts 已被 GPT-SoVITS 訓練模組取代，不再需要
# try:
#     from routes.simple_tts import simple_tts_bp
#     app.register_blueprint(simple_tts_bp)
#     optional_modules.append("TTS")
# except ImportError as e:
#     print(f"⚠️ TTS模組未載入: {e}")

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

try:
    from routes.audiobook import audiobook_bp
    app.register_blueprint(audiobook_bp)
    optional_modules.append("AI廣播劇")
except ImportError as e:
    print(f"⚠️ AI廣播劇模組未載入: {e}")

try:
    from routes.voice_care import voice_care_bp
    app.register_blueprint(voice_care_bp)
    optional_modules.append("智慧語音關懷")
except ImportError as e:
    print(f"⚠️ 智慧語音關懷模組未載入: {e}")

try:
    from routes.voice_interaction_realtime import voice_interaction_realtime_bp, init_socketio_events
    app.register_blueprint(voice_interaction_realtime_bp)
    if socketio:
        init_socketio_events(socketio)
    optional_modules.append("即時語音互動")
except ImportError as e:
    print(f"⚠️ 即時語音互動模組未載入: {e}")

# Qwen AI廣播劇模組（條件式載入）
try:
    from modules.voice_processing.qwen_audiobook_service import qwen_audiobook_bp
    app.register_blueprint(qwen_audiobook_bp)
    optional_modules.append("Qwen AI廣播劇")
except ImportError as e:
    print(f"⚠️ Qwen AI廣播劇模組未載入: {e}")

# GPT-SoVITS 訓練模組（條件式載入）
try:
    from routes.gptsovits import gptsovits_bp
    app.register_blueprint(gptsovits_bp)
    optional_modules.append("GPT-SoVITS 訓練")
except ImportError as e:
    print(f"⚠️ GPT-SoVITS 訓練模組未載入: {e}")

if optional_modules:
    print(f"✅ 已載入可選模組: {', '.join(optional_modules)}")

# 系統入口頁面（需要登入）
@app.route('/portal')
def portal():
    from flask import render_template
    # Portal 頁面會在前端檢查登入狀態
    return render_template('portal.html')

# 隱私權政策路由
@app.route('/privacy')
def privacy_policy():
    from flask import render_template
    return render_template('privacy_policy.html')

# 提供 genvoice 目錄的音頻文件
@app.route('/genvoice/<path:filename>')
def serve_genvoice(filename):
    from flask import send_from_directory
    return send_from_directory('genvoice', filename)

# 應用初始化
def init_app():
    """初始化應用程序"""
    # 初始化資料庫（條件式）
    try:
        from database import init_db
        init_db()
        print("✅ 資料庫初始化成功")
    except ImportError:
        print("⚠️ 資料庫模組未載入")
    except Exception as e:
        print(f"⚠️ 資料庫初始化失敗: {e}")
    
    # 確保必要的目錄存在（條件式）
    try:
        from config import ensure_directories
        ensure_directories()
        print("✅ 目錄結構確認完成")
    except ImportError:
        print("⚠️ 配置模組未載入")
    except Exception as e:
        print(f"⚠️ 目錄初始化失敗: {e}")

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
        
        # 使用 SocketIO 運行（如果可用）
        if socketio:
            socketio.run(app, debug=debug, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
        else:
            app.run(debug=debug, host='0.0.0.0', port=port)
        
    except KeyboardInterrupt:
        print("\n服務器已停止")
    except Exception as e:
        print(f"\n❌ 啟動失敗: {e}")
        import traceback
        traceback.print_exc()