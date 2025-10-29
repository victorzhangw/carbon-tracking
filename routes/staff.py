import os
from flask import Blueprint, request, jsonify
from config import AUDIO_UPLOAD_FOLDER
from auth import token_required, permission_required
from database import (
    get_paginated_results, 
    get_staff_by_id, 
    create_staff, 
    update_staff, 
    delete_staff
)

staff_bp = Blueprint('staff', __name__, url_prefix='/api/staff')

# 獲取客服專員列表
@staff_bp.route('', methods=['GET'])
@token_required
@permission_required('perm_staff_read')
def get_staff_list():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        keyword = request.args.get('keyword', '')
        
        query = '''
        SELECT * FROM staff
        WHERE (name LIKE ? OR code LIKE ? OR phone LIKE ? OR email LIKE ?)
        ORDER BY created_at DESC
        '''
        
        params = [f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%']
        
        result = get_paginated_results(query, params, page, size)
        return jsonify(result), 200
    
    except Exception as e:
        print(f"獲取客服專員列表失敗: {e}")
        return jsonify({"error": "獲取客服專員列表失敗"}), 500

# 獲取單個客服專員
@staff_bp.route('/<staff_id>', methods=['GET'])
def get_staff(staff_id):
    try:
        staff = get_staff_by_id(staff_id)
        
        if staff:
            return jsonify(staff), 200
        else:
            return jsonify({"error": "找不到該客服專員"}), 404
    
    except Exception as e:
        print(f"獲取客服專員失敗: {e}")
        return jsonify({"error": "獲取客服專員失敗"}), 500

# 新增客服專員
@staff_bp.route('', methods=['POST'])
@token_required
@permission_required('perm_staff_create')
def add_staff():
    try:
        data = request.json
        
        if not data.get('name') or not data.get('code'):
            return jsonify({"error": "姓名和代號為必填項"}), 400
        
        staff_id, error = create_staff(
            name=data.get('name'),
            code=data.get('code'),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            description=data.get('description', '')
        )
        
        if error:
            return jsonify({"error": error}), 400
        
        # 創建該客服專員的音頻上傳目錄
        code_dir = os.path.join(AUDIO_UPLOAD_FOLDER, data.get('code'))
        if not os.path.exists(code_dir):
            os.makedirs(code_dir)
        
        return jsonify({
            "message": "新增客服專員成功",
            "id": staff_id
        }), 201
    
    except Exception as e:
        print(f"新增客服專員失敗: {e}")
        return jsonify({"error": "新增客服專員失敗"}), 500

# 更新客服專員
@staff_bp.route('/<staff_id>', methods=['PUT'])
@token_required
@permission_required('perm_staff_update')
def update_staff_info(staff_id):
    try:
        data = request.json
        
        if not data.get('name') or not data.get('code'):
            return jsonify({"error": "姓名和代號為必填項"}), 400
        
        success, old_code = update_staff(
            staff_id=staff_id,
            name=data.get('name'),
            code=data.get('code'),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            status=data.get('status', 'active'),
            description=data.get('description', '')
        )
        
        if not success:
            return jsonify({"error": old_code}), 400
        
        # 如果代號有變更，處理目錄和檔案
        if old_code:
            old_code_dir = os.path.join(AUDIO_UPLOAD_FOLDER, old_code)
            new_code_dir = os.path.join(AUDIO_UPLOAD_FOLDER, data.get('code'))
            
            # 創建新代號的目錄
            if not os.path.exists(new_code_dir):
                os.makedirs(new_code_dir)
            
            # 移動檔案
            import shutil
            from database import get_paginated_results, update_audio_file_path
            
            # 獲取需要移動的檔案
            query = "SELECT id, file_path FROM audio WHERE staff_id = ?"
            results = get_paginated_results(query, [staff_id], 1, 1000)
            
            for item in results['items']:
                old_path = item['file_path']
                if old_path.startswith(old_code_dir):
                    # 構建新路徑
                    filename = os.path.basename(old_path)
                    new_path = os.path.join(new_code_dir, filename)
                    
                    # 移動檔案
                    if os.path.exists(old_path):
                        shutil.move(old_path, new_path)
                    
                    # 更新資料庫中的路徑
                    update_audio_file_path(item['id'], new_path)
        
        return jsonify({
            "message": "更新客服專員成功",
            "id": staff_id
        }), 200
    
    except Exception as e:
        print(f"更新客服專員失敗: {e}")
        return jsonify({"error": f"更新客服專員失敗: {str(e)}"}), 500

# 刪除客服專員
@staff_bp.route('/<staff_id>', methods=['DELETE'])
@token_required
@permission_required('perm_staff_delete')
def delete_staff_record(staff_id):
    try:
        success, message = delete_staff(staff_id)
        
        if not success:
            return jsonify({"error": message}), 404
        
        return jsonify({
            "message": "刪除客服專員成功"
        }), 200
    
    except Exception as e:
        print(f"刪除客服專員失敗: {e}")
        return jsonify({"error": "刪除客服專員失敗"}), 500
