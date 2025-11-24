#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 廣播劇資料庫管理
支援進度記錄、書籤、播放列表等功能
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class AudiobookDatabase:
    """AI 廣播劇資料庫管理類"""
    
    def __init__(self, db_path: str = "audiobook.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化資料庫表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 書籍資訊表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                description TEXT,
                cover_image TEXT,
                category TEXT,
                language TEXT,
                total_duration REAL,
                chapter_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 播放進度表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playback_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT NOT NULL,
                chapter_id TEXT NOT NULL,
                position REAL NOT NULL,
                total_duration REAL,
                progress_percent REAL,
                last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(book_id)
            )
        ''')
        
        # 書籤表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT NOT NULL,
                chapter_id TEXT NOT NULL,
                chapter_title TEXT,
                position REAL NOT NULL,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 播放列表表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                cover_image TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 播放列表項目表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_id INTEGER NOT NULL,
                book_id TEXT NOT NULL,
                chapter_id TEXT,
                sort_order INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE
            )
        ''')
        
        # 播放歷史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playback_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT NOT NULL,
                chapter_id TEXT NOT NULL,
                chapter_title TEXT,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 使用者偏好設定表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ 資料庫初始化完成")
    
    # ==================== 播放進度管理 ====================
    
    def save_progress(self, book_id: str, chapter_id: str, position: float, 
                     total_duration: float = None) -> bool:
        """儲存播放進度"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            progress_percent = (position / total_duration * 100) if total_duration else 0
            
            cursor.execute('''
                INSERT OR REPLACE INTO playback_progress 
                (book_id, chapter_id, position, total_duration, progress_percent, last_played)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (book_id, chapter_id, position, total_duration, progress_percent, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 儲存進度失敗: {e}")
            return False
    
    def get_progress(self, book_id: str) -> Optional[Dict]:
        """獲取播放進度"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM playback_progress WHERE book_id = ?
            ''', (book_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            print(f"❌ 獲取進度失敗: {e}")
            return None
    
    def get_all_progress(self) -> List[Dict]:
        """獲取所有播放進度"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM playback_progress ORDER BY last_played DESC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ 獲取進度列表失敗: {e}")
            return []
    
    # ==================== 書籤管理 ====================
    
    def add_bookmark(self, book_id: str, chapter_id: str, chapter_title: str,
                    position: float, note: str = None) -> Optional[int]:
        """添加書籤"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO bookmarks (book_id, chapter_id, chapter_title, position, note)
                VALUES (?, ?, ?, ?, ?)
            ''', (book_id, chapter_id, chapter_title, position, note))
            
            bookmark_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return bookmark_id
        except Exception as e:
            print(f"❌ 添加書籤失敗: {e}")
            return None
    
    def get_bookmarks(self, book_id: str) -> List[Dict]:
        """獲取書籤列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM bookmarks WHERE book_id = ? ORDER BY created_at DESC
            ''', (book_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ 獲取書籤失敗: {e}")
            return []
    
    def delete_bookmark(self, bookmark_id: int) -> bool:
        """刪除書籤"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM bookmarks WHERE id = ?', (bookmark_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 刪除書籤失敗: {e}")
            return False
    
    # ==================== 播放列表管理 ====================
    
    def create_playlist(self, name: str, description: str = None) -> Optional[int]:
        """創建播放列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO playlists (name, description)
                VALUES (?, ?)
            ''', (name, description))
            
            playlist_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return playlist_id
        except Exception as e:
            print(f"❌ 創建播放列表失敗: {e}")
            return None
    
    def get_playlists(self) -> List[Dict]:
        """獲取所有播放列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.*, COUNT(pi.id) as item_count
                FROM playlists p
                LEFT JOIN playlist_items pi ON p.id = pi.playlist_id
                GROUP BY p.id
                ORDER BY p.updated_at DESC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ 獲取播放列表失敗: {e}")
            return []
    
    def add_to_playlist(self, playlist_id: int, book_id: str, chapter_id: str = None) -> bool:
        """添加到播放列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 獲取當前最大排序號
            cursor.execute('''
                SELECT MAX(sort_order) FROM playlist_items WHERE playlist_id = ?
            ''', (playlist_id,))
            max_order = cursor.fetchone()[0] or 0
            
            cursor.execute('''
                INSERT INTO playlist_items (playlist_id, book_id, chapter_id, sort_order)
                VALUES (?, ?, ?, ?)
            ''', (playlist_id, book_id, chapter_id, max_order + 1))
            
            # 更新播放列表的更新時間
            cursor.execute('''
                UPDATE playlists SET updated_at = ? WHERE id = ?
            ''', (datetime.now(), playlist_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 添加到播放列表失敗: {e}")
            return False
    
    def get_playlist_items(self, playlist_id: int) -> List[Dict]:
        """獲取播放列表項目"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM playlist_items 
                WHERE playlist_id = ? 
                ORDER BY sort_order
            ''', (playlist_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ 獲取播放列表項目失敗: {e}")
            return []
    
    def delete_playlist(self, playlist_id: int) -> bool:
        """刪除播放列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM playlists WHERE id = ?', (playlist_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 刪除播放列表失敗: {e}")
            return False
    
    # ==================== 播放歷史 ====================
    
    def add_to_history(self, book_id: str, chapter_id: str, chapter_title: str) -> bool:
        """添加到播放歷史"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO playback_history (book_id, chapter_id, chapter_title)
                VALUES (?, ?, ?)
            ''', (book_id, chapter_id, chapter_title))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 添加播放歷史失敗: {e}")
            return False
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """獲取播放歷史"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM playback_history 
                ORDER BY played_at DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ 獲取播放歷史失敗: {e}")
            return []
    
    # ==================== 使用者偏好設定 ====================
    
    def save_preference(self, key: str, value: any) -> bool:
        """儲存使用者偏好設定"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 將值轉換為 JSON 字串
            value_str = json.dumps(value)
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
                VALUES (?, ?, ?)
            ''', (key, value_str, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 儲存偏好設定失敗: {e}")
            return False
    
    def get_preference(self, key: str, default: any = None) -> any:
        """獲取使用者偏好設定"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM user_preferences WHERE key = ?', (key,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return json.loads(row[0])
            return default
        except Exception as e:
            print(f"❌ 獲取偏好設定失敗: {e}")
            return default
    
    def get_all_preferences(self) -> Dict:
        """獲取所有使用者偏好設定"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT key, value FROM user_preferences')
            rows = cursor.fetchall()
            conn.close()
            
            preferences = {}
            for row in rows:
                preferences[row['key']] = json.loads(row['value'])
            
            return preferences
        except Exception as e:
            print(f"❌ 獲取偏好設定列表失敗: {e}")
            return {}


# 創建全域實例
audiobook_db = AudiobookDatabase()
