import sqlite3
import datetime
import uuid
import bcrypt
from config import DATABASE

def init_db():
    """初始化資料庫結構"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 建立用戶表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at TEXT,
        updated_at TEXT
    )
    ''')
    
    # 建立角色表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS roles (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TEXT
    )
    ''')
    
    # 建立權限表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS permissions (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        resource TEXT,
        action TEXT,
        created_at TEXT
    )
    ''')
    
    # 建立用戶角色關聯表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_roles (
        user_id TEXT,
        role_id TEXT,
        assigned_at TEXT,
        PRIMARY KEY (user_id, role_id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
    )
    ''')
    
    # 建立角色權限關聯表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS role_permissions (
        role_id TEXT,
        permission_id TEXT,
        assigned_at TEXT,
        PRIMARY KEY (role_id, permission_id),
        FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE,
        FOREIGN KEY (permission_id) REFERENCES permissions (id) ON DELETE CASCADE
    )
    ''')
    
    # 建立客服專員表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        code TEXT NOT NULL UNIQUE,
        phone TEXT,
        email TEXT,
        status TEXT DEFAULT 'active',
        description TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    ''')
    
    # 建立音頻記錄表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audio (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        staff_id TEXT,
        file_path TEXT NOT NULL,
        duration INTEGER,
        file_size TEXT,
        status TEXT DEFAULT 'active',
        description TEXT,
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (staff_id) REFERENCES staff (id)
    )
    ''')
    
    conn.commit()
    
    # 初始化基本角色和權限
    init_default_roles_and_permissions(cursor)
    
    conn.commit()
    conn.close()

def init_default_roles_and_permissions(cursor):
    """初始化預設角色和權限"""
    now = datetime.datetime.now().isoformat()
    
    # 建立預設權限
    permissions = [
        ('perm_staff_read', '查看客服專員', 'staff', 'read'),
        ('perm_staff_create', '新增客服專員', 'staff', 'create'),
        ('perm_staff_update', '編輯客服專員', 'staff', 'update'),
        ('perm_staff_delete', '刪除客服專員', 'staff', 'delete'),
        ('perm_audio_read', '查看音頻記錄', 'audio', 'read'),
        ('perm_audio_create', '上傳音頻', 'audio', 'create'),
        ('perm_audio_update', '編輯音頻', 'audio', 'update'),
        ('perm_audio_delete', '刪除音頻', 'audio', 'delete'),
        ('perm_user_manage', '用戶管理', 'user', 'manage'),
        ('perm_role_manage', '角色管理', 'role', 'manage'),
        ('perm_system_admin', '系統管理', 'system', 'admin')
    ]
    
    for perm_name, description, resource, action in permissions:
        perm_id = str(uuid.uuid4())
        cursor.execute('''
        INSERT OR IGNORE INTO permissions (id, name, description, resource, action, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', [perm_id, perm_name, description, resource, action, now])
    
    # 建立預設角色
    roles = [
        ('admin', '系統管理員', [
            'perm_staff_read', 'perm_staff_create', 'perm_staff_update', 'perm_staff_delete',
            'perm_audio_read', 'perm_audio_create', 'perm_audio_update', 'perm_audio_delete',
            'perm_user_manage', 'perm_role_manage', 'perm_system_admin'
        ]),
        ('manager', '管理者', [
            'perm_staff_read', 'perm_staff_create', 'perm_staff_update',
            'perm_audio_read', 'perm_audio_create', 'perm_audio_update'
        ]),
        ('staff', '一般員工', [
            'perm_audio_read', 'perm_audio_create'
        ]),
        ('viewer', '訪客', [
            'perm_staff_read', 'perm_audio_read'
        ])
    ]
    
    for role_name, description, permission_names in roles:
        role_id = str(uuid.uuid4())
        cursor.execute('''
        INSERT OR IGNORE INTO roles (id, name, description, created_at)
        VALUES (?, ?, ?, ?)
        ''', [role_id, role_name, description, now])
        
        # 獲取角色ID
        cursor.execute('SELECT id FROM roles WHERE name = ?', [role_name])
        role_result = cursor.fetchone()
        if role_result:
            actual_role_id = role_result[0]
            
            # 為角色分配權限
            for perm_name in permission_names:
                cursor.execute('SELECT id FROM permissions WHERE name = ?', [perm_name])
                perm_result = cursor.fetchone()
                if perm_result:
                    perm_id = perm_result[0]
                    cursor.execute('''
                    INSERT OR IGNORE INTO role_permissions (role_id, permission_id, assigned_at)
                    VALUES (?, ?, ?)
                    ''', [actual_role_id, perm_id, now])
    
    # 建立預設管理員用戶
    admin_id = str(uuid.uuid4())
    password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
   
    cursor.execute('''
    INSERT OR IGNORE INTO users (id, username, email, password_hash, full_name, is_active, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', [admin_id, 'admin', 'admin@example.com', password_hash, '系統管理員', 1, now, now])
    
    # 為管理員分配角色
    cursor.execute('SELECT id FROM roles WHERE name = ?', ['admin'])
    admin_role = cursor.fetchone()
    if admin_role:
        cursor.execute('''
        INSERT OR IGNORE INTO user_roles (user_id, role_id, assigned_at)
        VALUES (?, ?, ?)
        ''', [admin_id, admin_role[0], now])

# 用戶管理相關函數
def get_user_by_username(username):
    """根據用戶名獲取用戶"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', [username])
    user = cursor.fetchone()
    
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    """根據ID獲取用戶"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', [user_id])
    user = cursor.fetchone()
    
    conn.close()
    return dict(user) if user else None

def get_user_permissions(user_id):
    """獲取用戶的所有權限"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT DISTINCT p.name, p.description
    FROM permissions p
    JOIN role_permissions rp ON p.id = rp.permission_id
    JOIN user_roles ur ON rp.role_id = ur.role_id
    WHERE ur.user_id = ?
    ''', [user_id])
    
    permissions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return permissions

def get_user_roles(user_id):
    """獲取用戶的所有角色"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT r.name, r.description
    FROM roles r
    JOIN user_roles ur ON r.id = ur.role_id
    WHERE ur.user_id = ?
    ''', [user_id])
    
    roles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return roles

def verify_password(password, password_hash):
    """驗證密碼"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_user(username, email, password, full_name='', role_name='staff'):
    """創建新用戶"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # 檢查用戶名是否已存在
        cursor.execute('SELECT id FROM users WHERE username = ?', [username])
        if cursor.fetchone():
            return None, '用戶名已存在'
        
        # 檢查郵箱是否已存在
        cursor.execute('SELECT id FROM users WHERE email = ?', [email])
        if cursor.fetchone():
            return None, '郵箱已存在'
        
        # 生成新用戶ID和時間戳
        user_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()
        
        # 加密密碼
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # 插入新用戶
        cursor.execute('''
        INSERT INTO users (id, username, email, password_hash, full_name, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', [user_id, username, email, password_hash, full_name, 1, now, now])
        
        # 分配角色
        cursor.execute('SELECT id FROM roles WHERE name = ?', [role_name])
        role_result = cursor.fetchone()
        if role_result:
            cursor.execute('''
            INSERT INTO user_roles (user_id, role_id, assigned_at)
            VALUES (?, ?, ?)
            ''', [user_id, role_result[0], now])
        
        conn.commit()
        return user_id, None
        
    except sqlite3.Error as e:
        print(f"創建用戶錯誤: {e}")
        conn.rollback()
        return None, f"創建用戶失敗: {e}"
    finally:
        conn.close()

def get_paginated_results(query, params, page, size):
    """分頁查詢結果輔助函數"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 計算總筆數
    count_query = f"SELECT COUNT(*) as count FROM ({query})"
    cursor.execute(count_query, params)
    total = cursor.fetchone()['count']
    
    # 添加分頁
    paginated_query = f"{query} LIMIT ? OFFSET ?"
    offset = (page - 1) * size
    paginated_params = params + [size, offset]
    
    cursor.execute(paginated_query, paginated_params)
    items = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'size': size,
        'total_pages': (total + size - 1) // size
    }

# 客服專員資料庫操作
def get_staff_by_id(staff_id):
    """根據ID獲取客服專員信息"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM staff WHERE id = ?', [staff_id])
    staff = cursor.fetchone()
    
    conn.close()
    
    return dict(staff) if staff else None

def get_staff_by_code(code):
    """根據代號獲取客服專員信息"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM staff WHERE code = ?', [code])
    staff = cursor.fetchone()
    
    conn.close()
    
    return dict(staff) if staff else None

def create_staff(name, code, phone='', email='', description=''):
    """創建新客服專員"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 檢查代號是否已存在
    cursor.execute('SELECT id FROM staff WHERE code = ?', [code])
    existing = cursor.fetchone()
    
    if existing:
        conn.close()
        return None, "該代號已存在"
    
    # 生成新 ID 和時間戳
    staff_id = str(uuid.uuid4())
    now = datetime.datetime.now().isoformat()
   
    cursor.execute('''
    INSERT INTO staff (id, name, code, phone, email, status, description, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [
        staff_id,
        name,
        code,
        phone,
        email,
        'active',
        description,
        now,
        now
    ])
    
    conn.commit()
    conn.close()
    
    return staff_id, None

def update_staff(staff_id, name, code, phone='', email='', status='active', description=''):
    """更新客服專員信息"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 檢查要更新的專員是否存在
    cursor.execute('SELECT code FROM staff WHERE id = ?', [staff_id])
    current_staff = cursor.fetchone()
    
    if not current_staff:
        conn.close()
        return False, "找不到該客服專員"
        
    old_code = current_staff[0]
    
    # 檢查新代號是否已被其他專員使用
    cursor.execute('SELECT id FROM staff WHERE code = ? AND id != ?', [code, staff_id])
    existing = cursor.fetchone()
    
    if existing:
        conn.close()
        return False, "該代號已被其他專員使用"
    
    # 更新時間戳
    now = datetime.datetime.now().isoformat()
    
    cursor.execute('''
    UPDATE staff 
    SET name = ?, code = ?, phone = ?, email = ?, status = ?, description = ?, updated_at = ?
    WHERE id = ?
    ''', [
        name,
        code,
        phone,
        email,
        status,
        description,
        now,
        staff_id
    ])
    
    conn.commit()
    conn.close()
    
    return True, old_code

def delete_staff(staff_id):
    """刪除客服專員"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 檢查要刪除的專員是否存在
    cursor.execute('SELECT code FROM staff WHERE id = ?', [staff_id])
    target = cursor.fetchone()
    
    if not target:
        conn.close()
        return False, "找不到該客服專員"
    
    code = target[0]
    
    # 檢查是否有關聯的錄音記錄
    cursor.execute('SELECT COUNT(*) as count FROM audio WHERE staff_id = ?', [staff_id])
    audio_count = cursor.fetchone()[0]
    
    if audio_count > 0:
        # 將關聯的錄音記錄的 staff_id 設為 NULL
        cursor.execute('UPDATE audio SET staff_id = NULL WHERE staff_id = ?', [staff_id])
    
    # 刪除專員
    cursor.execute('DELETE FROM staff WHERE id = ?', [staff_id])
    
    conn.commit()
    conn.close()
    
    return True, code

# 音頻記錄資料庫操作
def get_audio_by_id(audio_id):
    """根據 ID 獲取音頻記錄"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT a.*, s.name as staff_name, s.code as staff_code
    FROM audio a
    LEFT JOIN staff s ON a.staff_id = s.id
    WHERE a.id = ?
    ''', [audio_id])
    
    audio = cursor.fetchone()
    
    conn.close()
    
    return dict(audio) if audio else None

def create_audio(name, staff_id, file_path, duration=0, file_size='', description=''):
    """創建音頻記錄"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 生成新 ID 和時間戳
    audio_id = str(uuid.uuid4())
    now = datetime.datetime.now().isoformat()
    
    cursor.execute('''
    INSERT INTO audio (id, name, staff_id, file_path, duration, file_size, description, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [audio_id, name, staff_id, file_path, duration, file_size, description, now, now])
    
    conn.commit()
    conn.close()
    
    return audio_id, None

def delete_audio(audio_id):
    """刪除音頻記錄"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 獲取檔案路徑以便刪除實際檔案
    cursor.execute('SELECT file_path FROM audio WHERE id = ?', [audio_id])
    target = cursor.fetchone()
    
    if not target:
        conn.close()
        return False, "找不到該音頻記錄"
    
    file_path = target[0]
    
    # 刪除記錄
    cursor.execute('DELETE FROM audio WHERE id = ?', [audio_id])
    conn.commit()
    conn.close()
    
    return True, file_path

def update_audio(audio_id, name, staff_id=None, status='active', description=''):
    """更新音頻記錄"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 檢查音頻記錄是否存在
    cursor.execute('SELECT id FROM audio WHERE id = ?', [audio_id])
    existing = cursor.fetchone()
    
    if not existing:
        conn.close()
        return False, "找不到該音頻記錄"
    
    # 更新時間戳
    now = datetime.datetime.now().isoformat()
    
    cursor.execute('''
    UPDATE audio 
    SET name = ?, staff_id = ?, status = ?, description = ?, updated_at = ?
    WHERE id = ?
    ''', [name, staff_id, status, description, now, audio_id])
    
    conn.commit()
    conn.close()
    
    return True, None

def update_audio_file_path(audio_id, new_path):
    """更新音頻檔案路徑"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE audio SET file_path = ? WHERE id = ?', [new_path, audio_id])
    
    conn.commit()
    conn.close()
    
    return True
def update_audio_file_info(audio_id, duration, file_size):
    """更新音頻文件的時長和大小信息"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 更新時間戳
        now = datetime.datetime.now().isoformat()
        
        cursor.execute(
            "UPDATE audio SET duration = ?, file_size = ?, updated_at = ? WHERE id = ?",
            [duration, file_size, now, audio_id]
        )
        
        conn.commit()
        conn.close()
        
        return True, None
    except Exception as e:
        print(f"更新音頻文件信息錯誤: {e}")
        return False, str(e)

# 語音模型相關函數
def save_voice_model_info(staff_code, original_audio_path, processed_audio_path, reference_text, model_status='processing', quality_score=None):
    """保存語音模型信息"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        model_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()
        
        cursor.execute('''
            INSERT OR REPLACE INTO voice_models 
            (id, staff_code, original_audio_path, processed_audio_path, reference_text, model_status, quality_score, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (model_id, staff_code, original_audio_path, processed_audio_path, reference_text, model_status, quality_score, now, now))
        
        conn.commit()
        return model_id
        
    except sqlite3.Error as e:
        print(f"保存語音模型信息錯誤: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_voice_model_by_staff(staff_code):
    """根據客服代號獲取語音模型"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM voice_models WHERE staff_code = ?
        ''', (staff_code,))
        
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
        
    except sqlite3.Error as e:
        print(f"獲取語音模型錯誤: {e}")
        return None
    finally:
        conn.close()

def get_all_voice_models():
    """獲取所有語音模型"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT vm.*, s.name as staff_name
            FROM voice_models vm
            LEFT JOIN staff s ON vm.staff_code = s.code
            ORDER BY vm.created_at DESC
        ''')
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
        
    except sqlite3.Error as e:
        print(f"獲取語音模型列表錯誤: {e}")
        return []
    finally:
        conn.close()

def save_voice_generation_record(staff_code, input_text, generated_audio_path, sentiment=None):
    """保存語音生成記錄"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        generation_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO voice_generations 
            (id, staff_code, input_text, generated_audio_path, sentiment, generation_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (generation_id, staff_code, input_text, generated_audio_path, sentiment, now))
        
        conn.commit()
        return generation_id
        
    except sqlite3.Error as e:
        print(f"保存語音生成記錄錯誤: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()
