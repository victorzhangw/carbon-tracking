from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from database import get_user_by_username, verify_password, get_user_permissions, get_user_roles
import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """用戶登入"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '用戶名和密碼為必填項'}), 400
        
        # 驗證用戶
        user = get_user_by_username(username)
        if not user:
            return jsonify({'error': '用戶名或密碼錯誤'}), 401
        
        if not user['is_active']:
            return jsonify({'error': '帳號已被停用'}), 401
        
        if not verify_password(password, user['password_hash']):
            return jsonify({'error': '用戶名或密碼錯誤'}), 401
        
        # 創建 JWT Token
        access_token = create_access_token(
            identity=user['id'],
            expires_delta=datetime.timedelta(hours=8)
        )
        refresh_token = create_refresh_token(
            identity=user['id'],
            expires_delta=datetime.timedelta(days=30)
        )
        
        # 獲取用戶權限和角色
        permissions = get_user_permissions(user['id'])
        roles = get_user_roles(user['id'])
        
        return jsonify({
            'message': '登入成功',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'permissions': [perm['name'] for perm in permissions],
                'roles': [role['name'] for role in roles]
            }
        }), 200
        
    except Exception as e:
        print(f"登入錯誤: {e}")
        return jsonify({'error': '登入失敗'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """刷新 Token"""
    try:
        current_user_id = get_jwt_identity()
        
        # 創建新的 access token
        new_token = create_access_token(
            identity=current_user_id,
            expires_delta=datetime.timedelta(hours=8)
        )
        
        return jsonify({
            'access_token': new_token
        }), 200
        
    except Exception as e:
        print(f"刷新 Token 錯誤: {e}")
        return jsonify({'error': '刷新 Token 失敗'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """獲取用戶資料"""
    try:
        user_id = get_jwt_identity()
        
        from database import get_user_by_id
        user = get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': '用戶不存在'}), 404
        
        # 獲取用戶權限和角色
        permissions = get_user_permissions(user_id)
        roles = get_user_roles(user_id)
        
        return jsonify({
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'permissions': [perm['name'] for perm in permissions],
                'roles': [role['name'] for role in roles]
            }
        }), 200
        
    except Exception as e:
        print(f"獲取用戶資料錯誤: {e}")
        return jsonify({'error': '獲取用戶資料失敗'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用戶登出"""
    # JWT 是無狀態的，登出主要在前端處理（刪除 token）
    return jsonify({'message': '登出成功'}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """用戶註冊（僅限管理員使用）"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        role_name = data.get('role', 'staff')
        
        if not username or not email or not password:
            return jsonify({'error': '用戶名、郵箱和密碼為必填項'}), 400
        
        # 創建用戶
        from database import create_user
        user_id, error = create_user(username, email, password, full_name, role_name)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': '用戶創建成功',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        print(f"註冊錯誤: {e}")
        return jsonify({'error': '註冊失敗'}), 500