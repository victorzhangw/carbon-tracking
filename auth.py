from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from database import get_user_by_id, get_user_permissions

def token_required(f):
    """JWT Token 驗證裝飾器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': '無效的認證令牌'}), 401
    return decorated

def permission_required(permission_name):
    """權限驗證裝飾器"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                
                # 獲取用戶權限
                user_permissions = get_user_permissions(user_id)
                permission_names = [perm['name'] for perm in user_permissions]
                
                if permission_name not in permission_names:
                    return jsonify({'error': '權限不足'}), 403
                    
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': '認證失敗'}), 401
        return decorated
    return decorator

def role_required(role_name):
    """角色驗證裝飾器"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                
                # 獲取用戶角色
                from database import get_user_roles
                user_roles = get_user_roles(user_id)
                role_names = [role['name'] for role in user_roles]
                
                if role_name not in role_names:
                    return jsonify({'error': '角色權限不足'}), 403
                    
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': '認證失敗'}), 401
        return decorated
    return decorator

def get_current_user():
    """獲取當前登入用戶"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return get_user_by_id(user_id)
    except:
        return None