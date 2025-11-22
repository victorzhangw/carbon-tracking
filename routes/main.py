from flask import Blueprint, render_template, request, jsonify
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """主頁面 - 重定向到登入頁面"""
    from flask import redirect, url_for
    return redirect('/login')

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

@main.route('/login')
def login_page():
    """登入頁面"""
    return render_template('login.html')

@main.route('/emotion-analysis')
def emotion_analysis():
    """情緒識別系統頁面"""
    return render_template('emotion_analysis.html')

@main.route('/process_audio', methods=['POST'])
def process_audio():
    """處理上傳的音頻檔案進行情緒分析（支援多輪對話）"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "未上傳檔案"}), 400

        file = request.files['file']
        audio_data = file.read()
        
        # 獲取對話上下文（從表單數據）
        conversation_context_json = request.form.get('conversation_context', '[]')
        try:
            conversation_context = json.loads(conversation_context_json)
        except:
            conversation_context = []
        
        # 獲取對話輪次
        try:
            conversation_round = int(request.form.get('conversation_round', 0))
        except:
            conversation_round = 0
        
        # 導入服務
        from services.speech import transcribe_audio
        from services.ai import analyze_and_respond_with_context
        from services.tts import f5_tts
        import threading
        import uuid
        
        # 進行語音轉文字
        transcript = transcribe_audio(audio_data)
        if not transcript:
            return jsonify({"error": "無法轉錄音頻"}), 500

        # 使用帶上下文的 AI 分析
        print(f"🔄 對話輪次: {conversation_round}, 歷史記錄: {len(conversation_context)} 條")
        analysis_result = analyze_and_respond_with_context(
            user_input=transcript,
            conversation_context=conversation_context,
            response_style='friendly',
            conversation_mode='continuous',
            conversation_round=conversation_round
        )
        response_text = analysis_result.get("response", "")
        
        # 生成唯一的任務 ID
        task_id = str(uuid.uuid4())
        
        # 異步生成 TTS 語音（不阻塞響應）
        def generate_tts_async():
            try:
                print(f"🎵 開始異步生成 TTS (任務 {task_id[:8]}...)")
                output_file = f5_tts(response_text)
                if output_file:
                    filename = os.path.basename(output_file)
                    audio_url = f"/genvoice/{filename}"
                    # 儲存結果到全局字典（簡單實現）
                    if not hasattr(main, 'tts_cache'):
                        main.tts_cache = {}
                    main.tts_cache[task_id] = audio_url
                    print(f"✅ TTS 異步生成成功 (任務 {task_id[:8]}...): {audio_url}")
                else:
                    print(f"⚠️ TTS 異步生成失敗 (任務 {task_id[:8]}...)")
            except Exception as e:
                print(f"❌ TTS 異步生成錯誤 (任務 {task_id[:8]}...): {e}")
        
        # 啟動後台線程生成 TTS
        if response_text:
            thread = threading.Thread(target=generate_tts_async, daemon=True)
            thread.start()
        
        # 立即返回文字響應（不等待 TTS）
        return jsonify({
            "transcript": transcript,
            "sentiment": analysis_result.get("sentiment", "neutral"),
            "response": response_text,
            "confidence": analysis_result.get("confidence", 0.8),
            "audio_url": None,  # 初始為 None
            "task_id": task_id,  # 返回任務 ID 供前端輪詢
            "tts_status": "generating",  # TTS 生成中
            "conversation_round": conversation_round + 1  # 返回下一輪次
        })
        
    except Exception as e:
        print(f"處理音頻錯誤: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"處理音頻時發生錯誤: {str(e)}"}), 500

@main.route('/api/check-tts/<task_id>', methods=['GET'])
def check_tts_status(task_id):
    """檢查 TTS 生成狀態"""
    if not hasattr(main, 'tts_cache'):
        main.tts_cache = {}
    
    if task_id in main.tts_cache:
        return jsonify({
            "status": "ready",
            "audio_url": main.tts_cache[task_id]
        })
    else:
        return jsonify({
            "status": "generating"
        })

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

@main.route('/score-analysis')
def score_analysis():
    """評分分析頁面（增強版）"""
    return render_template('score_analysis_enhanced.html')

@main.route('/score-analysis-simple')
def score_analysis_simple():
    """評分分析頁面（簡單版）"""
    return render_template('score_analysis.html')

# ==================== 評分系統 API ====================

@main.route('/api/end-session', methods=['POST'])
def end_session():
    """結束對話並生成評分報告"""
    try:
        from services.score_database import score_db
        from services.score_calculator import score_calculator
        from datetime import datetime
        
        data = request.get_json()
        session_id = data.get('session_id')
        user_id = data.get('user_id', 'default')
        conversation_history = data.get('conversation_history', [])
        
        if not session_id:
            return jsonify({'status': 'error', 'message': '缺少 session_id'}), 400
        
        if not conversation_history:
            return jsonify({'status': 'error', 'message': '沒有對話記錄'}), 400
        
        print(f"📊 開始生成評分報告: {session_id}")
        print(f"   對話輪數: {len(conversation_history)}")
        
        # 計算各維度評分
        scores = score_calculator.calculate_all_scores(conversation_history)
        
        # 計算統計資訊
        total_words = sum([c.get('word_count', len(c.get('text', ''))) for c in conversation_history])
        duration = data.get('duration', 0)
        
        statistics = {
            'conversation_count': len(conversation_history),
            'total_words': total_words,
            'duration': duration
        }
        
        # 保存評分記錄
        record_id = score_db.save_score_record(
            session_id, 
            user_id,
            scores,
            statistics
        )
        
        # 獲取完整記錄（包含等級、星級等）
        record = score_db.get_score_record(session_id)
        
        print(f"✅ 評分報告生成完成: 綜合評分 {scores['overall']}, 等級 {record['grade']}")
        
        return jsonify({
            'status': 'success',
            'scores': {
                'emotion': scores['emotion'],
                'voice': scores['voice'],
                'content': scores['content'],
                'overall': scores['overall']
            },
            'grade': record['grade'],
            'stars': record['stars'],
            'title': record['title'],
            'suggestions': scores['suggestions'],
            'statistics': statistics,
            'details': scores['details']
        })
        
    except Exception as e:
        print(f"❌ 生成評分報告失敗: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main.route('/api/score-history', methods=['GET'])
def get_score_history():
    """獲取歷史評分記錄"""
    try:
        from services.score_database import score_db
        
        user_id = request.args.get('user_id', 'default')
        limit = int(request.args.get('limit', 200))  # 增加預設限制以支援更多記錄
        
        records = score_db.get_user_score_history(user_id, limit)
        stats = score_db.get_user_statistics(user_id)
        
        return jsonify({
            'status': 'success',
            'records': records,
            'statistics': {
                'total_sessions': int(stats['total_sessions'] or 0),
                'average_score': round(stats['avg_score'] or 0, 1),
                'best_score': round(stats['best_score'] or 0, 1),
                'worst_score': round(stats['worst_score'] or 0, 1),
                'avg_emotion': round(stats['avg_emotion'] or 0, 1),
                'avg_voice': round(stats['avg_voice'] or 0, 1),
                'avg_content': round(stats['avg_content'] or 0, 1)
            }
        })
        
    except Exception as e:
        print(f"❌ 獲取評分歷史失敗: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main.route('/api/login', methods=['POST'])
def api_login():
    """用戶登入 API"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'status': 'error', 'message': '請輸入用戶名稱和密碼'}), 400
        
        # 這裡應該查詢資料庫驗證用戶
        # 暫時使用簡單的驗證邏輯
        from database import get_user_by_username
        
        user = get_user_by_username(username)
        
        if user and verify_password(password, user.get('password_hash', '')):
            return jsonify({
                'status': 'success',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'full_name': user.get('full_name', username),
                    'email': user.get('email', '')
                }
            })
        else:
            return jsonify({'status': 'error', 'message': '用戶名稱或密碼錯誤'}), 401
        
    except Exception as e:
        print(f"❌ 登入失敗: {e}")
        return jsonify({'status': 'error', 'message': '登入失敗'}), 500

@main.route('/api/submit-user-score', methods=['POST'])
def submit_user_score():
    """提交用戶評分"""
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        user_id = data.get('user_id')
        user_name = data.get('user_name')
        scores = data.get('scores', {})
        feedback = data.get('feedback', '')
        conversation_history = data.get('conversation_history', [])
        statistics = data.get('statistics', {})
        
        if not session_id or not user_id:
            return jsonify({'status': 'error', 'message': '缺少必要參數'}), 400
        
        # 保存評分到資料庫
        from services.score_database import score_db
        
        # 計算等級和星級
        overall_score = scores.get('overall', 0)
        if overall_score >= 90:
            grade, title, stars = 'A+', '優秀', 5
        elif overall_score >= 80:
            grade, title, stars = 'A', '良好', 4
        elif overall_score >= 70:
            grade, title, stars = 'B', '中上', 3
        elif overall_score >= 60:
            grade, title, stars = 'C', '尚可', 2
        else:
            grade, title, stars = 'D', '待改進', 1
        
        # 保存記錄
        record_id = score_db.save_score_record(
            session_id=session_id,
            user_id=user_id,
            scores=scores,
            statistics=statistics,
            grade=grade,
            title=title,
            stars=stars,
            feedback=feedback,
            user_name=user_name
        )
        
        print(f"✅ 用戶評分已保存: {user_name} - {overall_score}分")
        
        return jsonify({
            'status': 'success',
            'record_id': record_id,
            'message': '評分提交成功'
        })
        
    except Exception as e:
        print(f"❌ 提交評分失敗: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

def verify_password(password, password_hash):
    """驗證密碼"""
    try:
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except:
        # 簡單比對（測試用）
        return password == password_hash
