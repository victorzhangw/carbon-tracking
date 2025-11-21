from flask import Blueprint, render_template, request, jsonify
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """主頁面 - 重定向到 Portal"""
    from flask import redirect, url_for
    return redirect('/portal')

@main.route('/voice-clone')
def voice_clone():
    """語音克隆示範頁面"""
    return render_template('voice_clone_demo.html')

@main.route('/voice-chat')
def voice_chat():
    """語音聊天示範頁面"""
    return render_template('voice_interaction_enhanced.html')

@main.route('/realtime-voice')
def realtime_voice():
    """即時語音互動示範頁面"""
    return render_template('voice_interaction_realtime.html')

@main.route('/audiobook-player')
def audiobook_player():
    """AI廣播劇播放器頁面"""
    return render_template('audiobook_player.html')

@main.route('/bilingual-audiobook-player')
def bilingual_audiobook_player():
    """雙語AI廣播劇播放器頁面"""
    return render_template('bilingual_audiobook_player.html')

@main.route('/voice-care')
def voice_care():
    """智慧語音關懷頁面"""
    return render_template('voice_care_dashboard.html')

@main.route('/voice-testing')
def voice_testing():
    """語音測試訓練模組入口頁面"""
    return render_template('voice_testing_hub.html')

@main.route('/emotion-analysis')
def emotion_analysis():
    """情緒識別系統頁面"""
    return render_template('emotion_analysis.html')

@main.route('/process_audio', methods=['POST'])
def process_audio():
    """處理上傳的音頻檔案進行情緒分析"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "未上傳檔案"}), 400

        file = request.files['file']
        audio_data = file.read()
        
        # 導入服務
        from services.speech import transcribe_audio
        from services.ai import analyze_and_respond
        
        # 進行語音轉文字
        transcript = transcribe_audio(audio_data)
        if not transcript:
            return jsonify({"error": "無法轉錄音頻"}), 500

        # 分析並生成回應
        analysis_result = analyze_and_respond(transcript)
        
        # 檢查是否有音訊URL
        audio_url = analysis_result.get("audio_url", None)
            
        return jsonify({
            "transcript": transcript,
            "sentiment": analysis_result.get("sentiment", "neutral"),
            "response": analysis_result.get("response", ""),
            "audio_url": audio_url
        })
        
    except Exception as e:
        print(f"處理音頻錯誤: {e}")
        return jsonify({"error": f"處理音頻時發生錯誤: {str(e)}"}), 500

@main.route('/health')
def health_check():
    """健康檢查端點"""
    return {'status': 'healthy', 'service': 'AICares'}, 200