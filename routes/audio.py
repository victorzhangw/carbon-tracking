import os
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from config import AUDIO_UPLOAD_FOLDER, allowed_file
from database import (
    get_paginated_results, 
    get_audio_by_id, 
    create_audio, 
    update_audio, 
    delete_audio,
    get_staff_by_id,
    update_audio_file_info 
)
from utils import format_file_size
from services.speech import get_audio_duration
from services.emotion_recognition import emotion_recognizer
from services.emotion_recognition_advanced import advanced_emotion_recognizer

audio_bp = Blueprint('audio', __name__, url_prefix='/api/audio')

# 獲取錄音記錄列表
@audio_bp.route('', methods=['GET'])
def get_audio_list():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        keyword = request.args.get('keyword', '')
        staff_id = request.args.get('staff_id', '')
        
        query_params = []
        conditions = []
        
        if keyword:
            conditions.append('(a.name LIKE ? OR s.name LIKE ? OR s.code LIKE ?)')
            query_params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
        
        if staff_id:
            conditions.append('a.staff_id = ?')
            query_params.append(staff_id)
        
        where_clause = ''
        if conditions:
            where_clause = 'WHERE ' + ' AND '.join(conditions)
        
        query = f'''
        SELECT a.*, s.name as staff_name, s.code as staff_code
        FROM audio a
        LEFT JOIN staff s ON a.staff_id = s.id
        {where_clause}
        ORDER BY a.created_at DESC
        '''
        
        result = get_paginated_results(query, query_params, page, size)
        return jsonify(result), 200
    
    except Exception as e:
        print(f"獲取錄音記錄列表失敗: {e}")
        return jsonify({"error": "獲取錄音記錄列表失敗"}), 500

# 獲取單個錄音記錄
@audio_bp.route('/<audio_id>', methods=['GET'])
def get_audio(audio_id):
    try:
        audio = get_audio_by_id(audio_id)
        
        if audio:
            return jsonify(audio), 200
        else:
            return jsonify({"error": "找不到該錄音記錄"}), 404
    
    except Exception as e:
        print(f"獲取錄音記錄失敗: {e}")
        return jsonify({"error": "獲取錄音記錄失敗"}), 500

# 上傳錄音
@audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "未上傳檔案"}), 400
        
        file = request.files['file']
        name = request.form.get('name', '')
        staff_id = request.form.get('staff_id', None)
        description = request.form.get('description', '')
        
        if file.filename == '':
            return jsonify({"error": "未選擇檔案"}), 400
        
        if not name:
            return jsonify({"error": "錄音名稱為必填項"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "不支援的檔案格式"}), 400
        
        # 檢查 staff_id 是否有效，並獲取客服專員代號
        staff_code = None
        if staff_id:
            staff = get_staff_by_id(staff_id)
            if not staff:
                return jsonify({"error": "無效的客服專員 ID"}), 400
            staff_code = staff['code']
        
        # 生成新 ID
        import uuid
        audio_id = str(uuid.uuid4())
        
        # 根據客服專員代號確定儲存路徑
        if staff_code:
            # 確保客服專員的目錄存在
            staff_dir = os.path.join(AUDIO_UPLOAD_FOLDER, staff_code)
            if not os.path.exists(staff_dir):
                os.makedirs(staff_dir)
            
            filename = secure_filename(f"{audio_id}_{file.filename}")
            file_path = os.path.join(staff_dir, filename)
        else:
            # 如果沒有客服專員，則放入主目錄
            filename = secure_filename(f"{audio_id}_{file.filename}")
            file_path = os.path.join(AUDIO_UPLOAD_FOLDER, filename)
        
        # 保存檔案
        file.save(file_path)
        
        # 獲取檔案資訊
        file_size = os.path.getsize(file_path)
        formatted_size = format_file_size(file_size)
        
        # 獲取音頻時長
        duration_seconds = get_audio_duration(file_path)
        
        # 進行情緒識別（可選）
        emotion_result = None
        try:
            # 使用基礎版本的情緒識別
            emotion_result = emotion_recognizer.predict_emotion(file_path)
        except Exception as e:
            print(f"情緒識別失敗: {e}")
        
        # 儲存記錄到資料庫
        audio_id = create_audio(
            name=name,
            file_path=file_path,
            staff_id=staff_id,
            duration=duration_seconds,
            file_size=formatted_size,
            description=description
        )
        
        response_data = {
            "message": "上傳錄音成功",
            "id": audio_id
        }
        
        # 如果情緒識別成功，加入結果
        if emotion_result and "error" not in emotion_result:
            response_data["emotion_analysis"] = emotion_result
        
        return jsonify(response_data), 201
    
    except Exception as e:
        print(f"上傳錄音失敗: {e}")
        return jsonify({"error": f"上傳錄音失敗: {str(e)}"}), 500

# 串流音頻
@audio_bp.route('/stream/<audio_id>', methods=['GET'])
def stream_audio(audio_id):
    try:
        audio = get_audio_by_id(audio_id)
        
        if not audio:
            return jsonify({"error": "找不到該錄音記錄"}), 404
        
        # 檢查檔案是否存在
        file_path = audio['file_path']
        if not os.path.exists(file_path):
            return jsonify({"error": "音頻檔案不存在"}), 404
        
        # 串流音頻檔案
        return send_file(file_path, as_attachment=False, mimetype='audio/wav')
    
    except Exception as e:
        print(f"串流音頻失敗: {e}")
        return jsonify({"error": "串流音頻失敗"}), 500

# 下載音頻
@audio_bp.route('/download/<audio_id>', methods=['GET'])
def download_audio(audio_id):
    try:
        audio = get_audio_by_id(audio_id)
        
        if not audio:
            return jsonify({"error": "找不到該錄音記錄"}), 404
        
        # 檢查檔案是否存在
        file_path = audio['file_path']
        if not os.path.exists(file_path):
            return jsonify({"error": "音頻檔案不存在"}), 404
        
        # 獲取檔案副檔名
        _, ext = os.path.splitext(file_path)
        if not ext:
            ext = '.wav'  # 預設為 .wav 格式
        
        # 設置下載檔案名稱
        download_name = f"{audio['name']}{ext}"
        
        # 下載音頻檔案
        return send_file(file_path, as_attachment=True, download_name=download_name)
    
    except Exception as e:
        print(f"下載音頻失敗: {e}")
        return jsonify({"error": "下載音頻失敗"}), 500

# 更新錄音記錄
@audio_bp.route('/<audio_id>', methods=['PUT'])
def update_audio_record(audio_id):
    try:
        data = request.json
        
        if not data.get('name'):
            return jsonify({"error": "錄音名稱為必填項"}), 400
        
        staff_id = data.get('staff_id')
        
        # 如果提供了 staff_id，檢查其有效性
        if staff_id:
            staff = get_staff_by_id(staff_id)
            if not staff:
                return jsonify({"error": "無效的客服專員 ID"}), 400
        
        # 更新錄音記錄
        success, error = update_audio(
            audio_id=audio_id,
            name=data.get('name'),
            staff_id=staff_id,
            status=data.get('status', 'active'),
            description=data.get('description', '')
        )
        
        if not success:
            return jsonify({"error": error}), 404
        
        return jsonify({
            "message": "更新錄音記錄成功",
            "id": audio_id
        }), 200
    
    except Exception as e:
        print(f"更新錄音記錄失敗: {e}")
        return jsonify({"error": "更新錄音記錄失敗"}), 500

# 刪除錄音記錄
@audio_bp.route('/<audio_id>', methods=['DELETE'])
def delete_audio_record(audio_id):
    try:
        success, file_path = delete_audio(audio_id)
        
        if not success:
            return jsonify({"error": file_path}), 404
        
        # 刪除檔案
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as file_error:
            print(f"刪除檔案失敗: {file_error}")
            # 即使刪除檔案失敗，依然返回成功，因為資料庫記錄已刪除
        
        return jsonify({
            "message": "刪除錄音記錄成功"
        }), 200
    
    except Exception as e:
        print(f"刪除錄音記錄失敗: {e}")
        return jsonify({"error": "刪除錄音記錄失敗"}), 500
# 音頻編輯 API
@audio_bp.route('/edit/<audio_id>', methods=['POST'])
def edit_audio(audio_id):
    """
    編輯現有的音頻文件
    - 可以替換整個文件
    - 或者更新音頻的元數據
    """
    try:
        # 獲取現有的音頻記錄
        audio = get_audio_by_id(audio_id)
        if not audio:
            return jsonify({"error": "找不到該錄音記錄"}), 404
        
        # 檢查是否有新的音頻文件
        new_file = None
        if 'file' in request.files:
            new_file = request.files['file']
            if new_file.filename == '':
                new_file = None
        
        # 獲取更新的元數據
        name = request.form.get('name', audio['name'])
        staff_id = request.form.get('staff_id', audio['staff_id'])
        description = request.form.get('description', audio['description'])
        
        # 如果沒有更新，直接返回成功
        if new_file is None and name == audio['name'] and staff_id == audio['staff_id'] and description == audio['description']:
            return jsonify({"message": "無更新變更"}), 200
        
        # 處理文件更新
        file_path = audio['file_path']
        if new_file and allowed_file(new_file.filename):
            # 如果是相同的路徑，先刪除原文件
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # 保存新文件到相同的路徑
            new_file.save(file_path)
            
            # 更新文件大小
            file_size = os.path.getsize(file_path)
            formatted_size = format_file_size(file_size)
            
            # 更新音頻時長
            duration_seconds = get_audio_duration(file_path)
            
            # 更新資料庫中的文件大小和時長
            update_audio_file_info(audio_id, duration_seconds, formatted_size)
        
        # 更新元數據
        success, error = update_audio(
            audio_id=audio_id,
            name=name,
            staff_id=staff_id,
            status=audio['status'],
            description=description
        )
        
        if not success:
            return jsonify({"error": error}), 400
        
        return jsonify({
            "message": "更新錄音成功",
            "id": audio_id
        }), 200
    
    except Exception as e:
        print(f"編輯音頻失敗: {e}")
        return jsonify({"error": f"編輯音頻失敗: {str(e)}"}), 500