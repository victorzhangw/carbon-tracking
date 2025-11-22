"""
評分系統資料庫服務
提供資料庫初始化、CRUD 操作等功能
"""
import sqlite3
import os
from datetime import datetime
import json
import uuid

class ScoreDatabase:
    def __init__(self, db_path='data/databases/emotion_analysis.db'):
        self.db_path = db_path
        self._ensure_directory()
        self._init_database()
    
    def _ensure_directory(self):
        """確保資料庫目錄存在"""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"✅ 已創建目錄: {db_dir}")
    
    def _init_database(self):
        """初始化資料庫表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. users 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                username TEXT,
                email TEXT,
                avatar_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login_at TIMESTAMP,
                total_sessions INTEGER DEFAULT 0,
                total_conversations INTEGER DEFAULT 0,
                average_score REAL DEFAULT 0.0,
                best_score REAL DEFAULT 0.0
            )
        """)
        
        # 2. sessions 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP,
                duration INTEGER,
                status TEXT DEFAULT 'active',
                conversation_count INTEGER DEFAULT 0,
                total_words INTEGER DEFAULT 0,
                device_type TEXT,
                browser TEXT,
                ip_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        
        # 3. conversations 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                sequence_number INTEGER NOT NULL,
                speaker TEXT NOT NULL,
                text TEXT NOT NULL,
                sentiment TEXT,
                sentiment_score REAL,
                sentiment_confidence REAL,
                audio_duration REAL,
                audio_volume REAL,
                audio_clarity REAL,
                words_per_minute INTEGER,
                pause_count INTEGER,
                word_count INTEGER,
                unique_words INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
            )
        """)
        
        # 4. score_records 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS score_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                emotion_score REAL NOT NULL,
                voice_score REAL NOT NULL,
                content_score REAL NOT NULL,
                overall_score REAL NOT NULL,
                grade TEXT NOT NULL,
                stars INTEGER NOT NULL,
                title TEXT,
                conversation_count INTEGER NOT NULL,
                total_words INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        
        # 5. score_details 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS score_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                sub_category TEXT NOT NULL,
                score REAL NOT NULL,
                weight REAL NOT NULL,
                description TEXT,
                data TEXT,
                FOREIGN KEY (record_id) REFERENCES score_records(id) ON DELETE CASCADE
            )
        """)
        
        # 6. suggestions 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                icon TEXT,
                text TEXT NOT NULL,
                priority TEXT NOT NULL,
                display_order INTEGER,
                FOREIGN KEY (record_id) REFERENCES score_records(id) ON DELETE CASCADE
            )
        """)
        
        # 創建索引
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON sessions(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_score_records_session_id ON score_records(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_score_records_user_id ON score_records(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_score_details_record_id ON score_details(record_id)",
            "CREATE INDEX IF NOT EXISTS idx_suggestions_record_id ON suggestions(record_id)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        conn.commit()
        conn.close()
        print("✅ 資料庫初始化完成")
    
    def get_connection(self):
        """獲取資料庫連接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使用 Row 工廠，可以通過列名訪問
        return conn
    
    # ==================== User 操作 ====================
    
    def create_or_get_user(self, user_id='default', username=None, email=None):
        """創建或獲取用戶"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 檢查用戶是否存在
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        if user:
            # 更新最後登入時間
            cursor.execute(
                "UPDATE users SET last_login_at = ? WHERE user_id = ?",
                (datetime.now(), user_id)
            )
            conn.commit()
            conn.close()
            return dict(user)
        else:
            # 創建新用戶
            cursor.execute("""
                INSERT INTO users (user_id, username, email, last_login_at)
                VALUES (?, ?, ?, ?)
            """, (user_id, username, email, datetime.now()))
            conn.commit()
            
            # 獲取創建的用戶
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            conn.close()
            return dict(user)
    
    # ==================== Session 操作 ====================
    
    def create_session(self, user_id='default', device_type=None, browser=None, ip_address=None):
        """創建新會話"""
        session_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sessions (
                session_id, user_id, start_time, 
                device_type, browser, ip_address
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (session_id, user_id, datetime.now(), device_type, browser, ip_address))
        
        conn.commit()
        conn.close()
        
        print(f"✅ 創建會話: {session_id}")
        return session_id
    
    def end_session(self, session_id):
        """結束會話"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 獲取會話開始時間
        cursor.execute("SELECT start_time FROM sessions WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()
        
        if result:
            start_time = datetime.fromisoformat(result['start_time'])
            end_time = datetime.now()
            duration = int((end_time - start_time).total_seconds())
            
            cursor.execute("""
                UPDATE sessions 
                SET end_time = ?, duration = ?, status = 'ended'
                WHERE session_id = ?
            """, (end_time, duration, session_id))
            
            conn.commit()
            conn.close()
            print(f"✅ 結束會話: {session_id}, 持續時間: {duration}秒")
            return duration
        else:
            conn.close()
            print(f"⚠️ 會話不存在: {session_id}")
            return 0
    
    # ==================== Conversation 操作 ====================
    
    def add_conversation(self, session_id, speaker, text, sentiment=None, 
                        sentiment_score=None, audio_features=None):
        """添加對話記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 獲取當前序號
        cursor.execute(
            "SELECT MAX(sequence_number) as max_seq FROM conversations WHERE session_id = ?",
            (session_id,)
        )
        result = cursor.fetchone()
        sequence_number = (result['max_seq'] or 0) + 1
        
        # 計算字數
        word_count = len(text)
        unique_words = len(set(text))
        
        # 準備音頻特徵
        audio_duration = None
        audio_volume = None
        audio_clarity = None
        words_per_minute = None
        pause_count = None
        
        if audio_features:
            audio_duration = audio_features.get('duration')
            audio_volume = audio_features.get('volume')
            audio_clarity = audio_features.get('clarity')
            words_per_minute = audio_features.get('words_per_minute')
            pause_count = audio_features.get('pause_count')
        
        cursor.execute("""
            INSERT INTO conversations (
                session_id, sequence_number, speaker, text,
                sentiment, sentiment_score,
                audio_duration, audio_volume, audio_clarity,
                words_per_minute, pause_count,
                word_count, unique_words
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id, sequence_number, speaker, text,
            sentiment, sentiment_score,
            audio_duration, audio_volume, audio_clarity,
            words_per_minute, pause_count,
            word_count, unique_words
        ))
        
        # 更新會話統計
        cursor.execute("""
            UPDATE sessions 
            SET conversation_count = conversation_count + 1,
                total_words = total_words + ?
            WHERE session_id = ?
        """, (word_count, session_id))
        
        conn.commit()
        conn.close()
        
        return sequence_number
    
    def get_conversations(self, session_id):
        """獲取會話的所有對話"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE session_id = ? 
            ORDER BY sequence_number
        """, (session_id,))
        
        conversations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return conversations
    
    # ==================== Score 操作 ====================
    
    def save_score_record(self, session_id, user_id, scores, statistics):
        """保存評分記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 計算等級和星級
        overall_score = scores['overall']
        grade, stars, title = self._calculate_grade(overall_score)
        
        # 插入評分記錄
        cursor.execute("""
            INSERT INTO score_records (
                session_id, user_id,
                emotion_score, voice_score, content_score, overall_score,
                grade, stars, title,
                conversation_count, total_words, duration
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id, user_id,
            scores['emotion'], scores['voice'], scores['content'], overall_score,
            grade, stars, title,
            statistics['conversation_count'], statistics['total_words'], statistics['duration']
        ))
        
        record_id = cursor.lastrowid
        
        # 保存評分詳情
        if 'details' in scores:
            for detail in scores['details']:
                cursor.execute("""
                    INSERT INTO score_details (
                        record_id, category, sub_category, score, weight, description
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    record_id, detail['category'], detail['sub_category'],
                    detail['score'], detail['weight'], detail.get('description', '')
                ))
        
        # 保存改進建議
        if 'suggestions' in scores:
            for i, suggestion in enumerate(scores['suggestions']):
                cursor.execute("""
                    INSERT INTO suggestions (
                        record_id, category, icon, text, priority, display_order
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    record_id, suggestion['category'], suggestion['icon'],
                    suggestion['text'], suggestion['priority'], i + 1
                ))
        
        # 更新用戶統計
        cursor.execute("""
            UPDATE users 
            SET total_sessions = total_sessions + 1,
                total_conversations = total_conversations + ?,
                average_score = (
                    SELECT AVG(overall_score) FROM score_records WHERE user_id = ?
                ),
                best_score = (
                    SELECT MAX(overall_score) FROM score_records WHERE user_id = ?
                )
            WHERE user_id = ?
        """, (statistics['conversation_count'], user_id, user_id, user_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ 保存評分記錄: {session_id}, 綜合評分: {overall_score}")
        return record_id
    
    def get_score_record(self, session_id):
        """獲取評分記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 獲取主記錄
        cursor.execute("""
            SELECT * FROM score_records WHERE session_id = ?
        """, (session_id,))
        record = cursor.fetchone()
        
        if not record:
            conn.close()
            return None
        
        record_dict = dict(record)
        record_id = record_dict['id']
        
        # 獲取詳情
        cursor.execute("""
            SELECT * FROM score_details WHERE record_id = ?
        """, (record_id,))
        record_dict['details'] = [dict(row) for row in cursor.fetchall()]
        
        # 獲取建議
        cursor.execute("""
            SELECT * FROM suggestions WHERE record_id = ? ORDER BY display_order
        """, (record_id,))
        record_dict['suggestions'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return record_dict
    
    def get_user_score_history(self, user_id='default', limit=10):
        """獲取用戶評分歷史"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                sr.*,
                s.start_time,
                s.end_time
            FROM score_records sr
            JOIN sessions s ON sr.session_id = s.session_id
            WHERE sr.user_id = ?
            ORDER BY sr.created_at DESC
            LIMIT ?
        """, (user_id, limit))
        
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return records
    
    def _calculate_grade(self, score):
        """計算等級、星級和稱號"""
        if score >= 95:
            return 'S', 5, '大師級'
        elif score >= 85:
            return 'A', 4, '優秀'
        elif score >= 75:
            return 'B', 3, '良好'
        elif score >= 60:
            return 'C', 2, '及格'
        else:
            return 'D', 1, '待改進'
    
    # ==================== 統計查詢 ====================
    
    def get_user_statistics(self, user_id='default'):
        """獲取用戶統計資訊"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_sessions,
                AVG(overall_score) as avg_score,
                MAX(overall_score) as best_score,
                MIN(overall_score) as worst_score,
                AVG(emotion_score) as avg_emotion,
                AVG(voice_score) as avg_voice,
                AVG(content_score) as avg_content
            FROM score_records
            WHERE user_id = ?
        """, (user_id,))
        
        stats = dict(cursor.fetchone())
        conn.close()
        
        return stats

# 創建全局實例
score_db = ScoreDatabase()
