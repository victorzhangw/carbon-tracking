import os
import json
import shutil
from werkzeug.utils import secure_filename

def format_file_size(size_in_bytes):
    """轉換檔案大小為人類可讀格式"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0 or unit == 'GB':
            break
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} {unit}"

def fix_incomplete_json(json_str):
    """修復可能不完整或包含多餘標記的 JSON 字符串"""
    if isinstance(json_str, dict):
        return json.dumps(json_str)

    # 移除多餘的標記，例如 "```json" 和 "```"
    json_str = json_str.replace("```json", "").replace("```", "").strip()

    # 移除可能的多餘字符，例如 "json" 開頭
    if json_str.startswith("json"):
        json_str = json_str[4:].strip()

    # 確保 JSON 結構正確
    try:
        json.loads(json_str)  # 如果是有效 JSON，直接返回
        return json_str
    except json.JSONDecodeError:
        # 嘗試補全結尾
        if not json_str.endswith('}'):
            json_str += '}'
        return json_str

def move_file_with_staff_code(old_path, new_code, audio_upload_folder):
    """根據客服專員代號移動檔案"""
    # 創建新代號的目錄
    new_code_dir = os.path.join(audio_upload_folder, new_code)
    if not os.path.exists(new_code_dir):
        os.makedirs(new_code_dir)
    
    # 構建新路徑
    filename = os.path.basename(old_path)
    new_path = os.path.join(new_code_dir, filename)
    
    # 移動檔案
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)
    
    return new_path

def generate_unique_filename(file, prefix=''):
    """生成唯一的檔案名"""
    from uuid import uuid4
    filename = secure_filename(file.filename)
    unique_id = str(uuid4())
    if prefix:
        return f"{prefix}_{unique_id}_{filename}"
    return f"{unique_id}_{filename}"

def save_uploaded_file(file, directory):
    """保存上傳的檔案"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = generate_unique_filename(file)
    file_path = os.path.join(directory, filename)
    file.save(file_path)
    
    return file_path, filename