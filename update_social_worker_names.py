"""
更新資料庫中的社工姓名
將原本的姓名替換為真實姓名
"""

import sqlite3
import random

# 新的社工姓名列表
NEW_NAMES = [
    "陳冠宇",
    "曾柏睿",
    "林怡君",
    "吳宜靜",
    "方琬婷"
]

def update_social_worker_names():
    """更新資料庫中的社工姓名"""
    
    # 連接資料庫
    conn = sqlite3.connect('carbon_tracking.db')
    cursor = conn.cursor()
    
    try:
        # 1. 獲取所有不重複的社工編號和姓名
        cursor.execute("""
            SELECT DISTINCT social_worker_id, social_worker_name 
            FROM visit_records 
            ORDER BY social_worker_id
        """)
        
        old_workers = cursor.fetchall()
        print(f"找到 {len(old_workers)} 位社工")
        print("\n原始社工資料：")
        for worker_id, worker_name in old_workers:
            print(f"  {worker_id}: {worker_name}")
        
        # 2. 建立對應關係（隨機分配新姓名）
        name_mapping = {}
        available_names = NEW_NAMES.copy()
        
        for worker_id, old_name in old_workers:
            if available_names:
                # 隨機選擇一個新姓名
                new_name = random.choice(available_names)
                available_names.remove(new_name)
            else:
                # 如果姓名用完了，重新使用
                new_name = random.choice(NEW_NAMES)
            
            name_mapping[worker_id] = new_name
        
        print("\n\n新的對應關係：")
        for worker_id, new_name in name_mapping.items():
            print(f"  {worker_id}: {new_name}")
        
        # 3. 更新資料庫
        print("\n\n開始更新資料庫...")
        update_count = 0
        
        for worker_id, new_name in name_mapping.items():
            cursor.execute("""
                UPDATE visit_records 
                SET social_worker_name = ? 
                WHERE social_worker_id = ?
            """, (new_name, worker_id))
            
            affected_rows = cursor.rowcount
            update_count += affected_rows
            print(f"  更新 {worker_id} -> {new_name}: {affected_rows} 筆記錄")
        
        # 4. 提交變更
        conn.commit()
        
        # 5. 驗證更新結果
        print("\n\n驗證更新結果：")
        cursor.execute("""
            SELECT DISTINCT social_worker_id, social_worker_name 
            FROM visit_records 
            ORDER BY social_worker_id
        """)
        
        updated_workers = cursor.fetchall()
        for worker_id, worker_name in updated_workers:
            print(f"  {worker_id}: {worker_name}")
        
        # 6. 統計資訊
        cursor.execute("SELECT COUNT(*) FROM visit_records")
        total_records = cursor.fetchone()[0]
        
        print(f"\n\n✅ 更新完成！")
        print(f"   總記錄數：{total_records}")
        print(f"   更新記錄數：{update_count}")
        print(f"   社工人數：{len(name_mapping)}")
        
        # 7. 顯示每位社工的記錄數
        print("\n\n各社工的記錄數：")
        cursor.execute("""
            SELECT social_worker_name, COUNT(*) as count
            FROM visit_records
            GROUP BY social_worker_name
            ORDER BY count DESC
        """)
        
        for name, count in cursor.fetchall():
            print(f"  {name}: {count} 筆")
        
    except Exception as e:
        print(f"\n❌ 錯誤：{e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()

def backup_database():
    """備份資料庫"""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"carbon_tracking_backup_{timestamp}.db"
    
    try:
        shutil.copy2('carbon_tracking.db', backup_file)
        print(f"✅ 資料庫已備份：{backup_file}")
        return True
    except Exception as e:
        print(f"❌ 備份失敗：{e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("  更新社工姓名工具")
    print("=" * 60)
    print()
    print("新姓名列表：")
    for i, name in enumerate(NEW_NAMES, 1):
        print(f"  {i}. {name}")
    print()
    
    # 詢問是否繼續
    response = input("是否要更新資料庫中的社工姓名？(y/n): ")
    
    if response.lower() == 'y':
        # 先備份
        print("\n正在備份資料庫...")
        if backup_database():
            print("\n開始更新...")
            update_social_worker_names()
        else:
            print("\n❌ 備份失敗，取消更新")
    else:
        print("\n已取消更新")
