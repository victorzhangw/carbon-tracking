"""
資料庫擴展 - 情緒分析結果儲存
執行此腳本來為現有資料庫添加情緒分析相關欄位
"""

import sqlite3
from config import DATABASE

def add_emotion_columns():
    """為 audio 表添加情緒分析相關欄位"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 檢查是否已存在情緒相關欄位
        cursor.execute("PRAGMA table_info(audio)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # 添加情緒分析欄位
        if 'emotion' not in columns:
            cursor.execute('''
                ALTER TABLE audio 
                ADD COLUMN emotion TEXT DEFAULT NULL
            ''')
            print("✅ 添加 emotion 欄位成功")
        
        if 'emotion_confidence' not in columns:
            cursor.execute('''
                ALTER TABLE audio 
                ADD COLUMN emotion_confidence REAL DEFAULT NULL
            ''')
            print("✅ 添加 emotion_confidence 欄位成功")
        
        if 'emotion_analysis_data' not in columns:
            cursor.execute('''
                ALTER TABLE audio 
                ADD COLUMN emotion_analysis_data TEXT DEFAULT NULL
            ''')
            print("✅ 添加 emotion_analysis_data 欄位成功")
        
        if 'emotion_analyzed_at' not in columns:
            cursor.execute('''
                ALTER TABLE audio 
                ADD COLUMN emotion_analyzed_at TIMESTAMP DEFAULT NULL
            ''')
            print("✅ 添加 emotion_analyzed_at 欄位成功")
        
        conn.commit()
        conn.close()
        
        print("🎉 資料庫擴展完成！")
        
    except Exception as e:
        print(f"❌ 資料庫擴展失敗: {e}")

def create_emotion_analysis_table():
    """創建專門的情緒分析結果表"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotion_analysis (
                id TEXT PRIMARY KEY,
                audio_id TEXT NOT NULL,
                method TEXT NOT NULL,
                predicted_emotion TEXT NOT NULL,
                confidence REAL NOT NULL,
                all_emotions_json TEXT,
                features_json TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (audio_id) REFERENCES audio (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ emotion_analysis 表創建成功")
        
    except Exception as e:
        print(f"❌ 創建情緒分析表失敗: {e}")

if __name__ == "__main__":
    print("=== 資料庫情緒分析擴展 ===")
    add_emotion_columns()
    create_emotion_analysis_table()
    print("=== 擴展完成 ===")