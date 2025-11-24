#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI廣播劇路由模組
處理AI廣播劇相關服務的API請求
"""

from flask import Blueprint, request, jsonify, current_app, send_file, abort, render_template
import os
import uuid
from werkzeug.utils import secure_filename
import logging

# 條件式導入 audiobook_service
try:
    from modules.voice_processing.audiobook_service import AudiobookService
    AUDIOBOOK_SERVICE_AVAILABLE = True
except ImportError:
    AUDIOBOOK_SERVICE_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("AudiobookService 未載入，部分功能將不可用")

# 導入資料庫管理
try:
    from modules.voice_processing.audiobook_database import audiobook_db
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("AudiobookDatabase 未載入，進度記錄功能將不可用")

# 創建藍圖
audiobook_bp = Blueprint('audiobook', __name__, url_prefix='/api/audiobook')

# 配置允許的文件擴展名
ALLOWED_EXTENSIONS = {'epub'}
UPLOAD_FOLDER = 'uploads/audiobooks'

# 設置日誌
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """檢查文件擴展名是否允許"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@audiobook_bp.route('/')
def audiobook_home():
    """AI廣播劇首頁"""
    return render_template('audiobook_player.html')

@audiobook_bp.route('/bilingual')
def bilingual_player():
    """雙語AI廣播劇播放器"""
    return render_template('bilingual_audiobook_player.html')

@audiobook_bp.route('/test')
def test_page():
    """測試頁面 - 顯示詳細錯誤訊息"""
    return render_template('audiobook_test.html')

@audiobook_bp.route('/qwen-test')
def qwen_test_page():
    """Qwen 雙語測試頁面"""
    return render_template('qwen_bilingual_test.html')

@audiobook_bp.route('/test-enhanced')
def test_enhanced_page():
    """Phase 1 功能測試頁面"""
    return render_template('audiobook_test_enhanced.html')

@audiobook_bp.route('/library')
def library_page():
    """AI 廣播劇書庫 - 原始版本"""
    return render_template('audiobook_library.html')

@audiobook_bp.route('/library-enhanced')
def library_enhanced_page():
    """AI 廣播劇書庫 - 增強版 (搜尋、篩選、分頁)"""
    return render_template('audiobook_library_enhanced.html')

@audiobook_bp.route('/upload', methods=['POST'])
def upload_epub():
    """
    上傳EPUB文件
    
    Returns:
        JSON: 上傳結果
    """
    try:
        # 檢查服務是否可用
        if not AUDIOBOOK_SERVICE_AVAILABLE:
            return jsonify({
                'success': False,
                'error': '系統依賴套件未安裝',
                'details': '請先安裝必要套件: pip install ebooklib beautifulsoup4 lxml',
                'solution': '執行安裝命令後重新啟動系統'
            }), 500
        
        # 檢查是否有文件在請求中
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '沒有文件被上傳'}), 400
        
        file = request.files['file']
        
        # 檢查文件名
        if file.filename == '':
            return jsonify({'success': False, 'error': '沒有選擇文件'}), 400
        
        if file and allowed_file(file.filename):
            # 確保上傳目錄存在
            upload_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            os.makedirs(upload_dir, exist_ok=True)
            
            # 生成安全的文件名
            filename = secure_filename(file.filename)
            # 添加唯一標識符避免文件名衝突
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # 保存文件
            file.save(file_path)
            logger.info(f"文件已保存: {file_path}")
            
            try:
                # 初始化AI廣播劇服務
                audiobook_service = AudiobookService(
                    output_dir=os.path.join(current_app.root_path, 'audiobooks')
                )
                
                # 生成AI廣播劇
                logger.info(f"開始處理 EPUB: {filename}")
                book_info = audiobook_service.generate_audiobook(file_path)
                
                return jsonify({
                    'success': True,
                    'message': 'EPUB文件上傳並處理成功',
                    'book_id': book_info['id'],
                    'book_title': book_info['title'],
                    'chapter_count': book_info['chapter_count']
                }), 200
                
            except ImportError as ie:
                logger.error(f"導入錯誤: {str(ie)}")
                return jsonify({
                    'success': False,
                    'error': '缺少必要的 Python 套件',
                    'details': str(ie),
                    'solution': '請執行: pip install ebooklib beautifulsoup4 lxml'
                }), 500
                
        else:
            return jsonify({'success': False, 'error': '不支持的文件格式，請上傳EPUB文件'}), 400
            
    except Exception as e:
        logger.error(f"上傳EPUB文件時出錯: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'處理文件時發生錯誤: {str(e)}',
            'type': type(e).__name__
        }), 500
        return jsonify({'error': f'處理文件時發生錯誤: {str(e)}'}), 500

@audiobook_bp.route('/books', methods=['GET'])
def list_books():
    """
    獲取已生成的廣播劇列表
    
    Returns:
        JSON: 廣播劇列表
    """
    try:
        import json
        from datetime import datetime
        from services.book_cover_service import book_cover_service
        
        audiobooks_dir = os.path.join(current_app.root_path, 'static', 'audiobooks')
        books = []
        
        if os.path.exists(audiobooks_dir):
            for book_id in os.listdir(audiobooks_dir):
                book_dir = os.path.join(audiobooks_dir, book_id)
                if not os.path.isdir(book_dir):
                    continue
                
                metadata_file = os.path.join(book_dir, 'metadata.json')
                if os.path.exists(metadata_file):
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        created_time = datetime.fromtimestamp(os.path.getctime(book_dir))
                        
                        # 檢查是否已有封面，沒有則嘗試獲取
                        cover_url = metadata.get('cover_url')
                        if not cover_url:
                            title = metadata.get('title', '未命名')
                            author = metadata.get('author')
                            cover_url = book_cover_service.fetch_cover_url(title, author)
                            
                            # 儲存封面 URL 到 metadata
                            if cover_url:
                                metadata['cover_url'] = cover_url
                                with open(metadata_file, 'w', encoding='utf-8') as f:
                                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                        
                        books.append({
                            'id': metadata.get('id', book_id),
                            'title': metadata.get('title', '未命名'),
                            'chapter_count': metadata.get('chapter_count', 0),
                            'created_at': created_time.isoformat(),
                            'cover_url': cover_url
                        })
                    except Exception as e:
                        logger.error(f"讀取書籍 {book_id} 失敗: {str(e)}")
                        continue
        
        # 按創建時間排序
        books.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'books': books
        }), 200
        
    except Exception as e:
        logger.error(f"獲取廣播劇列表時出錯: {str(e)}")
        return jsonify({'error': f'獲取廣播劇列表時發生錯誤: {str(e)}'}), 500

@audiobook_bp.route('/book/<book_id>', methods=['GET'])
def get_book_info(book_id):
    """
    獲取特定廣播劇的詳細信息
    
    Args:
        book_id (str): 書籍ID
        
    Returns:
        JSON: 書籍詳細信息
    """
    try:
        audiobooks_dir = os.path.join(current_app.root_path, 'static', 'audiobooks')
        book_dir = os.path.join(audiobooks_dir, book_id)
        
        if not os.path.exists(book_dir):
            return jsonify({'error': '找不到指定的廣播劇'}), 404
        
        # 這裏需要實現讀取書籍詳細信息的邏輯
        # 暫時返回基本結構
        book_info = {
            'id': book_id,
            'title': book_id,  # 需要從元數據中讀取
            'chapters': []  # 需要從實際文件中讀取章節信息
        }
        
        # 讀取章節文件
        for filename in os.listdir(book_dir):
            if filename.endswith('.mp3'):
                chapter_id = filename.replace('.mp3', '')
                book_info['chapters'].append({
                    'id': chapter_id,
                    'title': chapter_id,  # 需要從元數據中讀取
                    'audio_url': f'/api/audiobook/book/{book_id}/chapter/{chapter_id}/audio'
                })
        
        return jsonify({
            'success': True,
            'book': book_info
        }), 200
        
    except Exception as e:
        logger.error(f"獲取廣播劇信息時出錯: {str(e)}")
        return jsonify({'error': f'獲取廣播劇信息時發生錯誤: {str(e)}'}), 500

@audiobook_bp.route('/book/<book_id>/chapter/<chapter_id>/audio', methods=['GET'])
def get_chapter_audio(book_id, chapter_id):
    """
    獲取章節音頻文件
    
    Args:
        book_id (str): 書籍ID
        chapter_id (str): 章節ID
        
    Returns:
        File: 音頻文件
    """
    try:
        audiobooks_dir = os.path.join(current_app.root_path, 'static', 'audiobooks')
        audio_file_path = os.path.join(audiobooks_dir, book_id, f"{chapter_id}.mp3")
        
        if not os.path.exists(audio_file_path):
            return jsonify({'error': '找不到指定的音頻文件'}), 404
        
        return send_file(audio_file_path, as_attachment=True)
        
    except Exception as e:
        logger.error(f"獲取音頻文件時出錯: {str(e)}")
        return jsonify({'error': f'獲取音頻文件時發生錯誤: {str(e)}'}), 500

@audiobook_bp.route('/book/<book_id>/chapter/<chapter_id>/content', methods=['GET'])
def get_chapter_content(book_id, chapter_id):
    """
    獲取章節文字內容
    
    Args:
        book_id (str): 書籍ID
        chapter_id (str): 章節ID
        
    Returns:
        JSON: 章節文字內容
    """
    try:
        # 嘗試從文字檔案中讀取章節內容
        audiobooks_dir = os.path.join(current_app.root_path, 'static', 'audiobooks')
        content_file_path = os.path.join(audiobooks_dir, book_id, f"{chapter_id}.txt")
        
        if os.path.exists(content_file_path):
            with open(content_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return jsonify({
                'status': 'success',
                'data': {
                    'book_id': book_id,
                    'chapter_id': chapter_id,
                    'content': content
                }
            }), 200
        else:
            # 如果沒有文字檔案，返回提示訊息
            return jsonify({
                'status': 'success',
                'data': {
                    'book_id': book_id,
                    'chapter_id': chapter_id,
                    'content': None
                }
            }), 200
        
    except Exception as e:
        logger.error(f"獲取章節內容時出錯: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'獲取章節內容時發生錯誤: {str(e)}'
        }), 500

@audiobook_bp.route('/book/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    刪除廣播劇
    
    Args:
        book_id (str): 書籍ID
        
    Returns:
        JSON: 刪除結果
    """
    try:
        audiobooks_dir = os.path.join(current_app.root_path, 'audiobooks')
        book_dir = os.path.join(audiobooks_dir, book_id)
        
        if not os.path.exists(book_dir):
            return jsonify({'error': '找不到指定的廣播劇'}), 404
        
        # 刪除書籍目錄
        import shutil
        shutil.rmtree(book_dir)
        
        return jsonify({
            'success': True,
            'message': '廣播劇已成功刪除'
        }), 200
        
    except Exception as e:
        logger.error(f"刪除廣播劇時出錯: {str(e)}")
        return jsonify({'error': f'刪除廣播劇時發生錯誤: {str(e)}'}), 500


# ==================== 進度管理 API ====================

@audiobook_bp.route('/progress/save', methods=['POST'])
def save_progress():
    """儲存播放進度"""
    if not DATABASE_AVAILABLE:
        return jsonify({'success': False, 'error': '資料庫服務不可用'}), 503
    
    try:
        data = request.json
        book_id = data.get('book_id')
        chapter_id = data.get('chapter_id')
        position = data.get('position')
        total_duration = data.get('total_duration')
        
        if not all([book_id, chapter_id, position is not None]):
            return jsonify({'success': False, 'error': '缺少必要參數'}), 400
        
        success = audiobook_db.save_progress(book_id, chapter_id, position, total_duration)
        
        if success:
            return jsonify({'success': True, 'message': '進度已儲存'})
        else:
            return jsonify({'success': False, 'error': '儲存失敗'}), 500
            
    except Exception as e:
        logger.error(f"儲存進度錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@audiobook_bp.route('/progress/<book_id>', methods=['GET'])
def get_progress(book_id):
    """獲取播放進度"""
    if not DATABASE_AVAILABLE:
        return jsonify({'success': False, 'error': '資料庫服務不可用'}), 503
    
    try:
        progress = audiobook_db.get_progress(book_id)
        
        if progress:
            return jsonify({'success': True, 'progress': progress})
        else:
            return jsonify({'success': True, 'progress': None})
            
    except Exception as e:
        logger.error(f"獲取進度錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 書籤管理 API ====================

@audiobook_bp.route('/bookmark/add', methods=['POST'])
def add_bookmark():
    """添加書籤"""
    if not DATABASE_AVAILABLE:
        return jsonify({'success': False, 'error': '資料庫服務不可用'}), 503
    
    try:
        data = request.json
        book_id = data.get('book_id')
        chapter_id = data.get('chapter_id')
        chapter_title = data.get('chapter_title')
        position = data.get('position')
        note = data.get('note', '')
        
        if not all([book_id, chapter_id, chapter_title, position is not None]):
            return jsonify({'success': False, 'error': '缺少必要參數'}), 400
        
        bookmark_id = audiobook_db.add_bookmark(
            book_id, chapter_id, chapter_title, position, note
        )
        
        if bookmark_id:
            return jsonify({
                'success': True, 
                'bookmark_id': bookmark_id,
                'message': '書籤已添加'
            })
        else:
            return jsonify({'success': False, 'error': '添加失敗'}), 500
            
    except Exception as e:
        logger.error(f"添加書籤錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@audiobook_bp.route('/bookmarks/<book_id>', methods=['GET'])
def get_bookmarks(book_id):
    """獲取書籤列表"""
    if not DATABASE_AVAILABLE:
        return jsonify({'success': False, 'error': '資料庫服務不可用'}), 503
    
    try:
        bookmarks = audiobook_db.get_bookmarks(book_id)
        return jsonify({'success': True, 'bookmarks': bookmarks})
            
    except Exception as e:
        logger.error(f"獲取書籤錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@audiobook_bp.route('/bookmark/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    """刪除書籤"""
    if not DATABASE_AVAILABLE:
        return jsonify({'success': False, 'error': '資料庫服務不可用'}), 503
    
    try:
        success = audiobook_db.delete_bookmark(bookmark_id)
        
        if success:
            return jsonify({'success': True, 'message': '書籤已刪除'})
        else:
            return jsonify({'success': False, 'error': '刪除失敗'}), 500
            
    except Exception as e:
        logger.error(f"刪除書籤錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 偏好設定 API ====================

@audiobook_bp.route('/preferences/save', methods=['POST'])
def save_preferences():
    """儲存使用者偏好設定"""
    if not DATABASE_AVAILABLE:
        return jsonify({'success': False, 'error': '資料庫服務不可用'}), 503
    
    try:
        data = request.json
        
        for key, value in data.items():
            audiobook_db.save_preference(key, value)
        
        return jsonify({'success': True, 'message': '設定已儲存'})
            
    except Exception as e:
        logger.error(f"儲存設定錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@audiobook_bp.route('/preferences', methods=['GET'])
def get_preferences():
    """獲取使用者偏好設定"""
    if not DATABASE_AVAILABLE:
        return jsonify({'success': False, 'error': '資料庫服務不可用'}), 503
    
    try:
        preferences = audiobook_db.get_all_preferences()
        
        # 設定預設值
        defaults = {
            'playbackSpeed': 0.8,
            'volume': 1.0,
            'autoPlay': True,
            'theme': 'light'
        }
        
        # 合併預設值和使用者設定
        for key, value in defaults.items():
            if key not in preferences:
                preferences[key] = value
        
        return jsonify({'success': True, 'preferences': preferences})
            
    except Exception as e:
        logger.error(f"獲取設定錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500