"""
即時語音互動路由
整合 Qwen-ASR-Realtime + DeepSeek LLM + Qwen TTS Realtime
"""

import os
import json
import uuid
from flask import Blueprint, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from services.realtime_interaction_service import RealtimeInteractionService

voice_interaction_realtime_bp = Blueprint('voice_interaction_realtime', __name__, url_prefix='/voice_interaction_realtime')

# 儲存活躍的會話
active_sessions = {}


@voice_interaction_realtime_bp.route('/')
def index_page():
    """索引頁面 - 選擇語言版本"""
    return render_template('voice_interaction_realtime_index.html')


@voice_interaction_realtime_bp.route('/roy')
def roy_page():
    """閩南語版本（Roy）"""
    return render_template('voice_interaction_realtime_roy.html')


@voice_interaction_realtime_bp.route('/nofish')
def nofish_page():
    """國語版本（Nofish）"""
    return render_template('voice_interaction_realtime_nofish.html')


@voice_interaction_realtime_bp.route('/session/start', methods=['POST'])
def start_session():
    """啟動新的即時互動會話"""
    try:
        data = request.get_json()
        voice = data.get('voice', 'Nofish')
        enable_vad = data.get('enable_vad', True)
        
        # 生成會話 ID
        session_id = str(uuid.uuid4())
        
        # 獲取 API 密鑰
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            return jsonify({
                'status': 'error',
                'message': 'DASHSCOPE_API_KEY 未設置'
            }), 500
        
        # 創建服務實例
        service = RealtimeInteractionService(api_key=api_key, voice=voice)
        
        # 啟動 ASR 連接
        if not service.start_asr_session():
            return jsonify({
                'status': 'error',
                'message': 'ASR 連接失敗'
            }), 500
        
        # 儲存會話
        active_sessions[session_id] = service
        
        print(f"✅ 會話已啟動: {session_id} (語音: {voice})")
        
        return jsonify({
            'status': 'success',
            'session_id': session_id,
            'voice': voice,
            'message': '會話已啟動'
        })
    
    except Exception as e:
        print(f"❌ 啟動會話失敗: {e}")
        return jsonify({
            'status': 'error',
            'message': f'啟動會話失敗: {str(e)}'
        }), 500


@voice_interaction_realtime_bp.route('/session/stop', methods=['POST'])
def stop_session():
    """結束會話並清理資源"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id or session_id not in active_sessions:
            return jsonify({
                'status': 'error',
                'message': '會話不存在'
            }), 404
        
        # 關閉服務
        service = active_sessions[session_id]
        service.close_sessions()
        
        # 移除會話
        del active_sessions[session_id]
        
        print(f"✅ 會話已結束: {session_id}")
        
        return jsonify({
            'status': 'success',
            'message': '會話已結束'
        })
    
    except Exception as e:
        print(f"❌ 結束會話失敗: {e}")
        return jsonify({
            'status': 'error',
            'message': f'結束會話失敗: {str(e)}'
        }), 500


# SocketIO 事件處理（需要在 app.py 中初始化 SocketIO）
def init_socketio_events(socketio: SocketIO):
    """初始化 SocketIO 事件處理"""
    
    @socketio.on('connect', namespace='/voice_interaction_realtime')
    def handle_connect():
        """客戶端連接"""
        print(f"🔌 客戶端已連接: {request.sid}")
        emit('connected', {'status': 'success'})
    
    @socketio.on('disconnect', namespace='/voice_interaction_realtime')
    def handle_disconnect():
        """客戶端斷開"""
        print(f"🔌 客戶端已斷開: {request.sid}")
    
    @socketio.on('join_session', namespace='/voice_interaction_realtime')
    def handle_join_session(data):
        """加入會話"""
        session_id = data.get('session_id')
        
        if not session_id or session_id not in active_sessions:
            emit('error', {'message': '會話不存在'})
            return
        
        join_room(session_id)
        
        # 設置回調函數
        service = active_sessions[session_id]
        
        def on_transcript_partial(text, stash):
            socketio.emit('transcript_partial', {
                'text': text,
                'stash': stash
            }, room=session_id, namespace='/voice_interaction_realtime')
        
        def on_transcript_final(text):
            socketio.emit('transcript_final', {
                'text': text
            }, room=session_id, namespace='/voice_interaction_realtime')
        
        def on_llm_response(text, sentiment, confidence):
            socketio.emit('llm_response', {
                'text': text,
                'sentiment': sentiment,
                'confidence': confidence
            }, room=session_id, namespace='/voice_interaction_realtime')
        
        def on_audio_output(audio_data, is_final):
            socketio.emit('audio_output', {
                'audio': audio_data,
                'is_final': is_final
            }, room=session_id, namespace='/voice_interaction_realtime')
        
        def on_error(error_msg):
            socketio.emit('error', {
                'message': error_msg
            }, room=session_id, namespace='/voice_interaction_realtime')
        
        service.on_transcript_partial = on_transcript_partial
        service.on_transcript_final = on_transcript_final
        service.on_llm_response = on_llm_response
        service.on_audio_output = on_audio_output
        service.on_error = on_error
        
        emit('joined', {'session_id': session_id})
        print(f"✅ 客戶端已加入會話: {session_id}")
    
    @socketio.on('audio_input', namespace='/voice_interaction_realtime')
    def handle_audio_input(data):
        """處理音頻輸入"""
        session_id = data.get('session_id')
        audio_base64 = data.get('audio')
        
        if not session_id or session_id not in active_sessions:
            emit('error', {'message': '會話不存在'})
            return
        
        service = active_sessions[session_id]
        service.process_audio_input(audio_base64)
    
    @socketio.on('leave_session', namespace='/voice_interaction_realtime')
    def handle_leave_session(data):
        """離開會話"""
        session_id = data.get('session_id')
        leave_room(session_id)
        emit('left', {'session_id': session_id})
        print(f"✅ 客戶端已離開會話: {session_id}")
    
    @socketio.on('quick_message', namespace='/voice_interaction_realtime')
    def handle_quick_message(data):
        """處理快速訊息（文字輸入）"""
        session_id = data.get('session_id')
        text = data.get('text')
        
        if not session_id or session_id not in active_sessions:
            emit('error', {'message': '會話不存在'})
            return
        
        if not text:
            emit('error', {'message': '訊息內容為空'})
            return
        
        try:
            service = active_sessions[session_id]
            # 直接處理文字輸入，跳過 ASR
            service.process_text_input(text)
            print(f"📝 快速訊息: {text}")
        except Exception as e:
            print(f"❌ 處理快速訊息失敗: {e}")
            emit('error', {'message': f'處理失敗: {str(e)}'})
