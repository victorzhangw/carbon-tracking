"""
碳排放追蹤系統 - 資料庫模型
"""

import sqlite3
from datetime import datetime
from pathlib import Path

class CarbonTrackingDB:
    def __init__(self, db_path='data/databases/carbon_tracking.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """取得資料庫連線"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """初始化資料庫表格"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 1. 社工訪視記錄表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS visit_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visit_date DATE NOT NULL,
            social_worker_id TEXT NOT NULL,
            social_worker_name TEXT NOT NULL,
            elder_id TEXT NOT NULL,
            elder_name TEXT,
            visit_type TEXT NOT NULL,
            transport_type TEXT NOT NULL,
            distance REAL NOT NULL,
            travel_time INTEGER,
            start_location TEXT,
            end_location TEXT,
            carbon_emission REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 2. 長者基本資料表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS elders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            elder_id TEXT UNIQUE NOT NULL,
            elder_name TEXT NOT NULL,
            region_type TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 3. 社工基本資料表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS social_workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id TEXT UNIQUE NOT NULL,
            worker_name TEXT NOT NULL,
            department TEXT,
            phone TEXT,
            email TEXT,
            primary_transport TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 4. AI關懷記錄表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_care_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            care_date DATE NOT NULL,
            elder_id TEXT NOT NULL,
            care_type TEXT NOT NULL,
            duration INTEGER,
            result TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 5. 月度統計表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            total_elders INTEGER,
            physical_visits INTEGER,
            ai_care_count INTEGER,
            total_distance REAL,
            total_carbon_emission REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(year, month)
        )
        ''')
        
        # 6. 排放係數設定表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emission_coefficients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transport_type TEXT UNIQUE NOT NULL,
            coefficient REAL NOT NULL,
            unit TEXT NOT NULL,
            source TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 插入預設排放係數
        cursor.execute('''
        INSERT OR IGNORE INTO emission_coefficients 
        (transport_type, coefficient, unit, source) VALUES
        ('機車', 0.0695, 'kg CO2e/km', '環保署排放係數管理表6.0.4版'),
        ('汽車', 0.1850, 'kg CO2e/km', '環保署排放係數管理表6.0.4版'),
        ('大眾運輸', 0.0295, 'kg CO2e/km', '環保署排放係數管理表6.0.4版')
        ''')
        
        conn.commit()
        conn.close()
        
        print("✓ 資料庫初始化完成")
    
    def add_visit_record(self, data):
        """新增訪視記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 計算碳排放
        carbon_emission = self.calculate_carbon_emission(
            data['transport_type'], 
            data['distance']
        )
        
        cursor.execute('''
        INSERT INTO visit_records 
        (visit_date, social_worker_id, social_worker_name, elder_id, elder_name,
         visit_type, transport_type, distance, travel_time, start_location, 
         end_location, carbon_emission, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['visit_date'],
            data['social_worker_id'],
            data['social_worker_name'],
            data['elder_id'],
            data.get('elder_name', ''),
            data['visit_type'],
            data['transport_type'],
            data['distance'],
            data.get('travel_time'),
            data.get('start_location', ''),
            data.get('end_location', ''),
            carbon_emission,
            data.get('notes', '')
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        return record_id
    
    def get_visit_record_by_id(self, record_id):
        """取得單筆訪視記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, visit_date, social_worker_id, social_worker_name, 
               elder_id, elder_name, visit_type, transport_type, distance,
               travel_time, start_location, end_location, carbon_emission, notes
        FROM visit_records
        WHERE id = ?
        ''', (record_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = ['id', 'visit_date', 'social_worker_id', 'social_worker_name',
                      'elder_id', 'elder_name', 'visit_type', 'transport_type', 'distance',
                      'travel_time', 'start_location', 'end_location', 'carbon_emission', 'notes']
            return dict(zip(columns, row))
        return None
    
    def update_visit_record(self, record_id, data):
        """更新訪視記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 重新計算碳排放
        carbon_emission = self.calculate_carbon_emission(
            data['transport_type'], 
            data['distance']
        )
        
        cursor.execute('''
        UPDATE visit_records
        SET visit_date = ?, social_worker_id = ?, social_worker_name = ?,
            elder_id = ?, elder_name = ?, visit_type = ?, transport_type = ?,
            distance = ?, travel_time = ?, start_location = ?, end_location = ?,
            carbon_emission = ?, notes = ?
        WHERE id = ?
        ''', (
            data['visit_date'],
            data['social_worker_id'],
            data['social_worker_name'],
            data['elder_id'],
            data.get('elder_name', ''),
            data['visit_type'],
            data['transport_type'],
            data['distance'],
            data.get('travel_time'),
            data.get('start_location', ''),
            data.get('end_location', ''),
            carbon_emission,
            data.get('notes', ''),
            record_id
        ))
        
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        
        return affected_rows > 0
    
    def delete_visit_record(self, record_id):
        """刪除訪視記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM visit_records WHERE id = ?', (record_id,))
        
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        
        return affected_rows > 0
    
    def search_visit_records(self, keyword='', worker_id='', start_date='', end_date='', transport_type='', limit=1000):
        """搜尋和篩選訪視記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 建立 SQL 查詢
        query = '''
        SELECT id, visit_date, social_worker_id, social_worker_name, 
               elder_id, elder_name, visit_type, transport_type, distance,
               travel_time, start_location, end_location, carbon_emission, notes
        FROM visit_records
        WHERE 1=1
        '''
        
        params = []
        
        # 關鍵字搜尋（社工姓名、工號、長者編號）
        if keyword:
            query += ''' AND (
                social_worker_name LIKE ? OR 
                social_worker_id LIKE ? OR 
                elder_id LIKE ? OR
                elder_name LIKE ?
            )'''
            keyword_param = f'%{keyword}%'
            params.extend([keyword_param, keyword_param, keyword_param, keyword_param])
        
        # 社工篩選
        if worker_id:
            query += ' AND social_worker_id = ?'
            params.append(worker_id)
        
        # 日期範圍篩選
        if start_date:
            query += ' AND visit_date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND visit_date <= ?'
            params.append(end_date)
        
        # 交通工具篩選
        if transport_type:
            query += ' AND transport_type = ?'
            params.append(transport_type)
        
        # 排序和限制
        query += ' ORDER BY visit_date DESC, id DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        
        columns = ['id', 'visit_date', 'social_worker_id', 'social_worker_name',
                  'elder_id', 'elder_name', 'visit_type', 'transport_type', 'distance',
                  'travel_time', 'start_location', 'end_location', 'carbon_emission', 'notes']
        
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        
        return results
    
    def add_ai_care_record(self, data):
        """新增AI關懷記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO ai_care_records 
        (care_date, elder_id, care_type, duration, result, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['care_date'],
            data['elder_id'],
            data['care_type'],
            data.get('duration'),
            data.get('result', ''),
            data.get('notes', '')
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        return record_id
    
    def calculate_carbon_emission(self, transport_type, distance):
        """計算碳排放量"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT coefficient FROM emission_coefficients WHERE transport_type = ?',
            (transport_type,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            coefficient = result[0]
            return distance * coefficient
        return 0
    
    def get_monthly_statistics(self, year, month):
        """取得月度統計"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 訪視統計
        cursor.execute('''
        SELECT 
            COUNT(*) as visit_count,
            SUM(distance) as total_distance,
            SUM(carbon_emission) as total_emission
        FROM visit_records
        WHERE strftime('%Y', visit_date) = ? 
        AND strftime('%m', visit_date) = ?
        ''', (str(year), f'{month:02d}'))
        
        visit_stats = cursor.fetchone()
        
        # AI關懷統計
        cursor.execute('''
        SELECT COUNT(*) as ai_care_count
        FROM ai_care_records
        WHERE strftime('%Y', care_date) = ? 
        AND strftime('%m', care_date) = ?
        ''', (str(year), f'{month:02d}'))
        
        ai_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'year': year,
            'month': month,
            'physical_visits': visit_stats[0] or 0,
            'total_distance': visit_stats[1] or 0,
            'total_carbon_emission': visit_stats[2] or 0,
            'ai_care_count': ai_stats[0] or 0
        }
    
    def get_all_visit_records(self, limit=100):
        """取得所有訪視記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM visit_records 
        ORDER BY visit_date DESC 
        LIMIT ?
        ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return records
    
    def get_statistics_summary(self, start_date, end_date):
        """取得統計摘要"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT 
            COUNT(*) as total_visits,
            COUNT(DISTINCT elder_id) as unique_elders,
            SUM(distance) as total_distance,
            SUM(carbon_emission) as total_emission,
            AVG(distance) as avg_distance
        FROM visit_records
        WHERE visit_date BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total_visits': result[0] or 0,
            'unique_elders': result[1] or 0,
            'total_distance': result[2] or 0,
            'total_emission': result[3] or 0,
            'avg_distance': result[4] or 0
        }

if __name__ == '__main__':
    # 測試資料庫
    db = CarbonTrackingDB()
    print("資料庫測試完成")
