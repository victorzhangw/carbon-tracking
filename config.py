import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 資料庫設定
DATABASE = 'data/databases/customer_service.db'
AUDIO_UPLOAD_FOLDER = 'assets/audio/uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

# DeepSeek AI API 設定
DEEPSEEK_API_KEY = "sk-xmwxrtsxgsjwuyeceydoyuopezzlqresdjyvlzrbbjeejiff"
BASE_URL = "https://api.siliconflow.cn"
#MODEL_NAME = "deepseek-ai/DeepSeek-V3"
MODEL_NAME = "deepseek-ai/DeepSeek-V3"

# 中央氣象署 API 設定
CWA_API_KEY = os.getenv('CWA_API_KEY', '')
CWA_API_ENABLED = bool(CWA_API_KEY)

# 確保必要的目錄存在
def ensure_directories():
    directories = [
        'assets/audio/mockvoice', 
        'assets/audio/genvoice', 
        'static/audio', 
        AUDIO_UPLOAD_FOLDER,
        'genvoice'  # TTS 輸出目錄
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ 已創建目錄: {directory}")

# 檢查檔案副檔名是否允許
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
