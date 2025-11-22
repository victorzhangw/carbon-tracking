#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧語音關懷路由模組
處理智慧語音關懷服務的API請求
"""

from flask import Blueprint, request, jsonify, current_app, render_template
import datetime
from modules.voice_processing.voice_care_service import VoiceCareService

# 創建藍圖
voice_care_bp = Blueprint('voice_care', __name__, url_prefix='/api/voice-care')

# 創建服務實例
voice_care_service = VoiceCareService()

# ==================== 頁面路由 ====================

@voice_care_bp.route('/schedules-page', methods=['GET'])
def schedules_page():
    """排程管理頁面"""
    return render_template('voice_care_schedules.html')

@voice_care_bp.route('/dashboard', methods=['GET'])
def dashboard_page():
    """統計儀表板頁面"""
    return render_template('voice_care_dashboard.html')

@voice_care_bp.route('/test', methods=['GET'])
def test_page():
    """功能測試頁面"""
    return render_template('voice_care_test.html')

# ==================== API 路由 ====================

@voice_care_bp.route('/schedules', methods=['POST'])
def create_schedule():
    """
    創建語音關懷排程
    
    Request JSON:
        user_id (str): 用戶ID
        title (str): 排程標題
        scheduled_time (str): 排程時間 (ISO格式)
        address (str, optional): 地址
        latitude (float, optional): 緯度
        longitude (float, optional): 經度
        staff_id (str, optional): 客服專員ID
        description (str, optional): 描述
    
    Returns:
        JSON: 排程創建結果
    """
    try:
        data = request.get_json()
        
        # 驗證必要參數
        required_fields = ['user_id', 'title', 'scheduled_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必要參數: {field}'}), 400
        
        # 創建排程
        schedule_id = voice_care_service.create_schedule(
            user_id=data['user_id'],
            title=data['title'],
            scheduled_time=data['scheduled_time'],
            address=data.get('address', ''),
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            staff_id=data.get('staff_id'),
            description=data.get('description', '')
        )
        
        return jsonify({
            'success': True,
            'message': '排程創建成功',
            'schedule_id': schedule_id
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"創建排程失敗: {str(e)}")
        return jsonify({'error': f'創建排程失敗: {str(e)}'}), 500

@voice_care_bp.route('/schedules', methods=['GET'])
def get_all_schedules():
    """
    獲取所有排程
    
    Query Parameters:
        status (str, optional): 狀態過濾
        language (str, optional): 語言過濾
    
    Returns:
        JSON: 排程列表
    """
    try:
        import uuid
        from datetime import datetime, timedelta
        
        # 50-60年代風格的台灣長者姓名
        mock_schedules = [
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user001',
                'user_name': '王秀英',
                'title': '每日早安問候',
                'scheduled_time': (datetime.now() + timedelta(hours=1)).isoformat(),
                'language': 'mandarin',
                'status': 'pending',
                'address': '台北市大安區',
                'description': '記得吃早餐和量血壓',
                'created_at': (datetime.now() - timedelta(days=5)).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user002',
                'user_name': '陳金水',
                'title': '午間關懷',
                'scheduled_time': (datetime.now() + timedelta(hours=3)).isoformat(),
                'language': 'minan',
                'status': 'pending',
                'address': '台北市萬華區',
                'description': '提醒午休和服藥',
                'created_at': (datetime.now() - timedelta(days=4)).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user003',
                'user_name': '林阿桂',
                'title': '下午茶時間',
                'scheduled_time': (datetime.now() - timedelta(hours=2)).isoformat(),
                'language': 'mandarin',
                'status': 'completed',
                'address': '新北市板橋區',
                'description': '關心身體狀況',
                'created_at': (datetime.now() - timedelta(days=3)).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user004',
                'user_name': '張春梅',
                'title': '晚間問候',
                'scheduled_time': (datetime.now() + timedelta(hours=5)).isoformat(),
                'language': 'both',
                'status': 'pending',
                'address': '台中市西區',
                'description': '提醒晚餐和散步',
                'created_at': (datetime.now() - timedelta(days=2)).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user005',
                'user_name': '李阿財',
                'title': '每週健康關懷',
                'scheduled_time': (datetime.now() - timedelta(days=1)).isoformat(),
                'language': 'minan',
                'status': 'completed',
                'address': '台南市中西區',
                'description': '詢問本週身體狀況',
                'created_at': (datetime.now() - timedelta(days=7)).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user006',
                'user_name': '黃玉蘭',
                'title': '早晨運動提醒',
                'scheduled_time': (datetime.now() + timedelta(hours=12)).isoformat(),
                'language': 'mandarin',
                'status': 'pending',
                'address': '高雄市前金區',
                'description': '提醒公園晨間運動',
                'created_at': (datetime.now() - timedelta(days=1)).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user007',
                'user_name': '吳阿德',
                'title': '用藥提醒',
                'scheduled_time': (datetime.now() - timedelta(hours=5)).isoformat(),
                'language': 'minan',
                'status': 'failed',
                'address': '桃園市中壢區',
                'description': '提醒按時服用慢性病藥物',
                'created_at': (datetime.now() - timedelta(days=6)).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user008',
                'user_name': '劉素珍',
                'title': '午後關懷',
                'scheduled_time': (datetime.now() + timedelta(hours=4)).isoformat(),
                'language': 'mandarin',
                'status': 'pending',
                'address': '新竹市東區',
                'description': '關心午睡和水分補充',
                'created_at': (datetime.now() - timedelta(days=3)).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user009',
                'user_name': '許阿雲',
                'title': '晚安問候',
                'scheduled_time': (datetime.now() + timedelta(hours=8)).isoformat(),
                'language': 'both',
                'status': 'pending',
                'address': '彰化市中山路',
                'description': '提醒早點休息',
                'created_at': (datetime.now() - timedelta(days=2)).isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user010',
                'user_name': '蔡阿福',
                'title': '每日健康檢查',
                'scheduled_time': (datetime.now() - timedelta(hours=3)).isoformat(),
                'language': 'minan',
                'status': 'completed',
                'address': '嘉義市西區',
                'description': '詢問血壓和血糖數值',
                'created_at': (datetime.now() - timedelta(days=4)).isoformat()
            }
        ]
        
        # 應用篩選
        status_filter = request.args.get('status')
        language_filter = request.args.get('language')
        
        filtered_schedules = mock_schedules
        
        if status_filter:
            filtered_schedules = [s for s in filtered_schedules if s['status'] == status_filter]
        
        if language_filter:
            filtered_schedules = [s for s in filtered_schedules if s['language'] == language_filter]
        
        return jsonify({
            'success': True,
            'schedules': filtered_schedules
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"獲取排程列表失敗: {str(e)}")
        return jsonify({'error': f'獲取排程列表失敗: {str(e)}'}), 500

@voice_care_bp.route('/schedules/<schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    """
    獲取排程資訊
    
    Args:
        schedule_id (str): 排程ID
    
    Returns:
        JSON: 排程資訊
    """
    try:
        schedule = voice_care_service.get_schedule(schedule_id)
        
        if not schedule:
            return jsonify({'error': '排程不存在'}), 404
        
        return jsonify({
            'success': True,
            'schedule': schedule
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"獲取排程失敗: {str(e)}")
        return jsonify({'error': f'獲取排程失敗: {str(e)}'}), 500

@voice_care_bp.route('/schedules/user/<user_id>', methods=['GET'])
def get_user_schedules(user_id):
    """
    獲取用戶的所有排程
    
    Args:
        user_id (str): 用戶ID
    
    Query Parameters:
        status (str, optional): 狀態過濾
    
    Returns:
        JSON: 排程列表
    """
    try:
        status = request.args.get('status')
        schedules = voice_care_service.get_user_schedules(user_id, status)
        
        return jsonify({
            'success': True,
            'schedules': schedules
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"獲取用戶排程失敗: {str(e)}")
        return jsonify({'error': f'獲取用戶排程失敗: {str(e)}'}), 500

@voice_care_bp.route('/schedules/<schedule_id>', methods=['PUT'])
def update_schedule_status(schedule_id):
    """
    更新排程狀態
    
    Args:
        schedule_id (str): 排程ID
    
    Request JSON:
        status (str): 新狀態
    
    Returns:
        JSON: 更新結果
    """
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': '缺少必要參數: status'}), 400
        
        success = voice_care_service.update_schedule_status(schedule_id, data['status'])
        
        if not success:
            return jsonify({'error': '排程不存在或更新失敗'}), 404
        
        return jsonify({
            'success': True,
            'message': '排程狀態更新成功'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"更新排程狀態失敗: {str(e)}")
        return jsonify({'error': f'更新排程狀態失敗: {str(e)}'}), 500

@voice_care_bp.route('/schedules/<schedule_id>/send', methods=['POST'])
def send_voice_care(schedule_id):
    """
    發送語音關懷
    
    Args:
        schedule_id (str): 排程ID
    
    Returns:
        JSON: 發送結果
    """
    try:
        result = voice_care_service.send_voice_care(schedule_id)
        
        return jsonify({
            'success': True,
            'message': '語音關懷發送成功',
            'record_id': result['record_id'],
            'audio_file_path': result['audio_file_path']
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"發送語音關懷失敗: {str(e)}")
        return jsonify({'error': f'發送語音關懷失敗: {str(e)}'}), 500

@voice_care_bp.route('/records', methods=['GET'])
def get_care_records():
    """
    獲取關懷記錄
    
    Query Parameters:
        schedule_id (str, optional): 排程ID過濾
    
    Returns:
        JSON: 關懷記錄列表
    """
    try:
        schedule_id = request.args.get('schedule_id')
        records = voice_care_service.get_care_records(schedule_id)
        
        return jsonify({
            'success': True,
            'records': records
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"獲取關懷記錄失敗: {str(e)}")
        return jsonify({'error': f'獲取關懷記錄失敗: {str(e)}'}), 500

@voice_care_bp.route('/process-pending', methods=['POST'])
def process_pending_schedules():
    """
    處理所有待處理的排程
    
    Returns:
        JSON: 處理結果
    """
    try:
        results = voice_care_service.process_pending_schedules()
        
        return jsonify({
            'success': True,
            'results': results
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"處理待處理排程失敗: {str(e)}")
        return jsonify({'error': f'處理待處理排程失敗: {str(e)}'}), 500

@voice_care_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    獲取統計數據
    
    Returns:
        JSON: 統計數據
    """
    try:
        # 模擬統計數據（實際應從數據庫查詢）
        statistics = {
            'total_calls': 1250,
            'answer_rate': 0.85,
            'satisfaction_score': 4.5,
            'pending_schedules': 15,
            'language_distribution': {
                'mandarin': 750,
                'minan': 400,
                'both': 100
            },
            'recent_records': [],
            'daily_stats': []
        }
        
        return jsonify({
            'success': True,
            **statistics
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"獲取統計數據失敗: {str(e)}")
        return jsonify({'error': f'獲取統計數據失敗: {str(e)}'}), 500

@voice_care_bp.route('/weather', methods=['GET'])
def get_weather_info():
    """
    獲取天氣資訊（測試用）
    
    Query Parameters:
        latitude (float): 緯度
        longitude (float): 經度
    
    Returns:
        JSON: 天氣資訊
    """
    try:
        latitude = float(request.args.get('latitude', 0.0))
        longitude = float(request.args.get('longitude', 0.0))
        
        weather_info = voice_care_service.get_weather_info(latitude, longitude)
        
        return jsonify({
            'success': True,
            'weather_info': weather_info
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"獲取天氣資訊失敗: {str(e)}")
        return jsonify({'error': f'獲取天氣資訊失敗: {str(e)}'}), 500