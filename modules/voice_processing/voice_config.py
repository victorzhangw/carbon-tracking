"""
語音克隆服務配置文件
"""

# GPT-SoVITS 配置
GPT_SOVITS_PATH = "./GPT-SoVITS-v4-20250422fix"
GPT_SOVITS_API_URL = "http://localhost:9874"  # 使用您提供的URL
GPT_SOVITS_CONFIG_PATH = "./GPT-SoVITS-v4-20250422fix/GPT_SoVITS/configs/tts_infer.yaml"

# 服務配置
VOICE_CLONE_SERVICE_PORT = 5002
VOICE_CLONE_SERVICE_HOST = "0.0.0.0"

# 目錄配置
UPLOAD_DIR = "./assets/audio/uploads"
OUTPUT_DIR = "./assets/audio/genvoice"  # 改為genvoice目錄，與路由一致
TEMP_DIR = "./temp"

# 音頻配置
SUPPORTED_FORMATS = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MIN_DURATION = 1.0  # 最小時長 1 秒
MAX_DURATION = 300.0  # 最大時長 5 分鐘

# 質量評估閾值
QUALITY_THRESHOLDS = {
    'excellent': 0.8,
    'good': 0.6,
    'fair': 0.4,
    'poor': 0.0
}

# 語言支持
SUPPORTED_LANGUAGES = {
    'zh': '中文',
    'en': 'English',
    'ja': '日本語',
    'ko': '한국어',
    'yue': '粵語'
}

# 預設參考文字
DEFAULT_PROMPT_TEXTS = {
    'zh': '這是一段參考語音，用於語音克隆。',
    'en': 'This is a reference audio for voice cloning.',
    'ja': 'これは音声クローニングのための参考音声です。',
    'ko': '이것은 음성 복제를 위한 참조 오디오입니다。',
    'yue': '呢個係用嚟做語音克隆嘅參考語音。'
}