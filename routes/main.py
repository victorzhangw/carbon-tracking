import os
from flask import Blueprint, request, jsonify, render_template, send_from_directory
from services.speech import transcribe_audio
from services.ai import analyze_and_respond
from services.tts import f5_tts

main_bp = Blueprint('main', __name__)

# API 端點 - 首頁
@main_bp.route("/")
def index():
    """提供主要的 HTML 頁面"""
    return render_template("index.html")

# API 端點 - 語音互動增強版頁面
@main_bp.route("/voice_interaction")
def voice_interaction():
    """提供語音互動增強版頁面"""
    return render_template("voice_interaction_enhanced.html")

# API 端點 - 語音互動即時版頁面
@main_bp.route("/voice_interaction_realtime")
def voice_interaction_realtime():
    """提供語音互動即時版頁面"""
    return render_template("voice_interaction_realtime.html")

# API 端點 - 處理上傳音頻
@main_bp.route("/process_audio", methods=["POST"])
def process_audio():
    """處理上傳的音頻檔案"""
    if "file" not in request.files:
        return jsonify({"error": "未上傳檔案"}), 400

    file = request.files["file"]
    audio_data = file.read()
    
    # 進行語音轉文字
    transcript = transcribe_audio(audio_data)
    if not transcript:
        return jsonify({"error": "無法轉錄音頻"}), 500

    # 分析並生成回應
    analysis_result = analyze_and_respond(transcript)
    
    # 檢查是否有音訊URL
    if "audio_url" in analysis_result:
        audio_url = analysis_result["audio_url"]
    else:
        audio_url = None  # Or handle the error as needed
        
    return jsonify({
        "transcript": transcript,
        "sentiment": analysis_result["sentiment"],
        "response": analysis_result["response"],
        "audio_url": audio_url  # This will be None if TTS failed
    })

# API 端點 - TTS
@main_bp.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # 調用新的GPT-SoVITS TTS生成音訊檔案
        output_file = f5_tts(text)
        if output_file:
            # 獲取文件名用於URL
            filename = os.path.basename(output_file)
            return jsonify({"audio_url": f"/genvoice/{filename}"})
        else:
            return jsonify({"error": "Failed to generate audio"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API 端點 - 上傳模擬聲音
@main_bp.route('/upload_mockvoice', methods=['POST'])
def upload_mockvoice():
    """處理服務聲音模擬的音檔上傳"""
    if 'file' not in request.files:
        return jsonify({"error": "未找到音檔"}), 400

    file = request.files['file']
    if not os.path.exists('mockvoice'):
        os.makedirs('mockvoice')

    file_path = os.path.join('mockvoice', file.filename)
    try:
        file.save(file_path)
        return jsonify({"message": "音檔已成功儲存！"}), 200
    except Exception as e:
        return jsonify({"error": f"無法儲存音檔：{e}"}), 500

# API 端點 - 提供模擬聲音檔案
@main_bp.route('/mockvoice/<filename>')
def serve_mockvoice(filename):
    """提供 mockvoice 資料夾中的音頻文件"""
    try:
        # 安全檢查：確保文件名只包含安全的字符
        if '..' in filename or filename.startswith('/'):
            return jsonify({"error": "Invalid filename"}), 400
            
        # 確保文件是 .wav 格式
        if not filename.endswith('.wav'):
            return jsonify({"error": "Only .wav files are allowed"}), 400
            
        # 從 mockvoice 目錄提供文件
        return send_from_directory('mockvoice', filename)
        
    except Exception as e:
        return jsonify({"error": f"Error serving file: {str(e)}"}), 500

# API 端點 - 提供生成的聲音檔案
@main_bp.route('/genvoice/<filename>')
def serve_genvoice(filename):
    """提供 genvoice 資料夾中的音頻文件"""
    try:
        # 確保安全文件名
        if '..' in filename or filename.startswith('/'):
            return jsonify({"error": "Invalid filename"}), 400
        
        # 提供 .wav 文件
        if not filename.endswith('.wav'):
            return jsonify({"error": "Only .wav files are allowed"}), 400
        
        # 檢查文件是否存在
        file_path = os.path.join('genvoice', filename)
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return jsonify({"error": f"File not found: {filename}"}), 404
        
        print(f"📁 提供音頻文件: {file_path}")
        return send_from_directory('genvoice', filename)
    except Exception as e:
        print(f"❌ 提供文件錯誤: {e}")
        return jsonify({"error": f"Error serving file: {str(e)}"}), 500