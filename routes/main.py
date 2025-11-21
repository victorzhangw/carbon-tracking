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
        from services.tts import f5_tts
        
        # 進行語音轉文字
        transcript = transcribe_audio(audio_data)
        if not transcript:
            return jsonify({"error": "無法轉錄音頻"}), 500

        # 分析並生成回應
        analysis_result = analyze_and_respond(transcript)
        response_text = analysis_result.get("response", "")
        
        # 生成 TTS 語音
        audio_url = None
        if response_text:
            try:
                output_file = f5_tts(response_text)
                if output_file:
                    # 獲取文件名用於URL
                    filename = os.path.basename(output_file)
                    audio_url = f"/genvoice/{filename}"
                    print(f"✅ TTS 生成成功: {audio_url}")
                else:
                    print("⚠️ TTS 生成失敗")
            except Exception as tts_error:
                print(f"❌ TTS 生成錯誤: {tts_error}")
            
        return jsonify({
            "transcript": transcript,
            "sentiment": analysis_result.get("sentiment", "neutral"),
            "response": response_text,
            "audio_url": audio_url
        })
        
    except Exception as e:
        print(f"處理音頻錯誤: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"處理音頻時發生錯誤: {str(e)}"}), 500

@main.route('/api/generate-tts', methods=['POST'])
def generate_tts():
    """生成 TTS 語音"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "缺少文字內容"}), 400
        
        # 導入 TTS 服務
        from services.tts import f5_tts
        
        # 生成語音
        output_file = f5_tts(text)
        if output_file:
            filename = os.path.basename(output_file)
            audio_url = f"/genvoice/{filename}"
            print(f"✅ TTS 生成成功: {audio_url}")
            return jsonify({"audio_url": audio_url})
        else:
            print("⚠️ TTS 生成失敗")
            return jsonify({"error": "TTS 生成失敗"}), 500
            
    except Exception as e:
        print(f"❌ TTS 生成錯誤: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"TTS 生成錯誤: {str(e)}"}), 500

@main.route('/api/weather/by-location', methods=['POST'])
def get_weather_by_location():
    """根據地理位置取得天氣資訊"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not latitude or not longitude:
            return jsonify({"error": "缺少位置資訊"}), 400
        
        # 導入天氣服務
        from services.weather_service import weather_service
        
        # 根據經緯度判斷縣市（簡化版，實際應使用反向地理編碼）
        # 這裡使用預設台北市，實際專案中應該整合地理編碼服務
        city = _get_city_from_coordinates(latitude, longitude)
        
        # 取得天氣資料
        weather_data = weather_service.get_weather_by_city(city)
        
        return jsonify(weather_data)
        
    except Exception as e:
        print(f"取得天氣資訊錯誤: {e}")
        return jsonify({"error": f"取得天氣資訊時發生錯誤: {str(e)}"}), 500

def _get_city_from_coordinates(lat, lon):
    """根據經緯度判斷縣市（簡化版）"""
    # 台灣主要城市的大致經緯度範圍
    city_ranges = {
        '臺北市': {'lat': (24.9, 25.2), 'lon': (121.4, 121.7)},
        '新北市': {'lat': (24.6, 25.3), 'lon': (121.3, 122.0)},
        '桃園市': {'lat': (24.8, 25.1), 'lon': (121.0, 121.5)},
        '臺中市': {'lat': (24.0, 24.3), 'lon': (120.5, 121.0)},
        '臺南市': {'lat': (22.9, 23.2), 'lon': (120.1, 120.5)},
        '高雄市': {'lat': (22.5, 22.8), 'lon': (120.2, 120.5)},
    }
    
    for city, ranges in city_ranges.items():
        if (ranges['lat'][0] <= lat <= ranges['lat'][1] and 
            ranges['lon'][0] <= lon <= ranges['lon'][1]):
            return city
    
    # 預設返回台北市
    return '臺北市'

@main.route('/health')
def health_check():
    """健康檢查端點"""
    return {'status': 'healthy', 'service': 'AICares'}, 200