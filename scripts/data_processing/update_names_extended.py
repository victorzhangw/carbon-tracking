"""
擴充更新資料庫中的社工姓名
保留原有姓名，並加入新的男女姓名
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import sqlite3
import random

# 原有的姓名（保留）
EXISTING_NAMES = [
    "陳冠宇",
    "曾柏睿",
    "林怡君",
    "吳宜靜",
    "方琬婷"
]

# 新增的男性姓名
MALE_NAMES = [
    "王建宏",
    "劉俊傑",
    "張志偉",
    "陳冠廷",
    "林哲瑋",
    "李承翰",
    "黃文博",
    "吳家豪",
    "郭俊宏",
    "鄭宇辰"
]

# 新增的女性姓名
FEMALE_NAMES = [
    "陳怡靜",
    "林欣怡",
    "黃詩涵",
    "張雅雯",
    "許慧君",
    "許嘉玲",
    "許家瑜",
    "蔡依璇",
    "曾珮瑜",
    "董婉婷"
]

# 合併所有姓名
ALL_NAMES = EXISTING_NAMES + MALE_NAMES + FEMALE_NAMES

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
        print("\n目前社工資料：")
        for worker_id, worker_name in old_workers:
            print(f"  {worker_id}: {worker_name}")
        
        # 2. 建立對應關係
        name_mapping = {}
        available_names = ALL_NAMES.copy()
        random.shuffle(available_names)  # 隨機打亂順序
        
        for i, (worker_id, old_name) in enumerate(old_workers):
            # 如果是原有的 5 個姓名之一，保留
            if old_name in EXISTING_NAMES:
                name_mapping[worker_id] = old_name
                print(f"  保留 {worker_id}: {old_name}")
            else:
                # 使用新姓名
                if available_names:
                    new_name = available_names.pop(0)
                else:
                    # 如果姓名用完了，重新使用
                    new_name = random.choice(ALL_NAMES)
                name_mapping[worker_id] = new_name
        
        print("\n\n新的對應關係：")
        print("-" * 60)
        print(f"{'社工編號':<15} {'新姓名':<15} {'類型'}")
        print("-" * 60)
        
        for worker_id, new_name in sorted(name_mapping.items()):
            if new_name in EXISTING_NAMES:
                name_type = "原有"
            elif new_name in MALE_NAMES:
                name_type = "男性"
            elif new_name in FEMALE_NAMES:
                name_type = "女性"
            else:
                name_type = "其他"
            print(f"{worker_id:<15} {new_name:<15} {name_type}")
        
        print("-" * 60)
        
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
        print("-" * 60)
        print(f"{'社工編號':<15} {'姓名':<15} {'類型'}")
        print("-" * 60)
        
        for worker_id, worker_name in updated_workers:
            if worker_name in EXISTING_NAMES:
                name_type = "原有"
            elif worker_name in MALE_NAMES:
                name_type = "男性"
            elif worker_name in FEMALE_NAMES:
                name_type = "女性"
            else:
                name_type = "其他"
            print(f"{worker_id:<15} {worker_name:<15} {name_type}")
        
        print("-" * 60)
        
        # 6. 統計資訊
        cursor.execute("SELECT COUNT(*) FROM visit_records")
        total_records = cursor.fetchone()[0]
        
        print(f"\n\n✅ 更新完成！")
        print(f"   總記錄數：{total_records:,}")
        print(f"   更新記錄數：{update_count:,}")
        print(f"   社工人數：{len(name_mapping)}")
        
        # 7. 顯示每位社工的記錄數
        print("\n\n各社工的記錄數：")
        cursor.execute("""
            SELECT social_worker_name, COUNT(*) as count
            FROM visit_records
            GROUP BY social_worker_name
            ORDER BY count DESC
        """)
        
        print("-" * 60)
        print(f"{'姓名':<15} {'記錄數':<10} {'類型'}")
        print("-" * 60)
        
        for name, count in cursor.fetchall():
            if name in EXISTING_NAMES:
                name_type = "原有"
            elif name in MALE_NAMES:
                name_type = "男性"
            elif name in FEMALE_NAMES:
                name_type = "女性"
            else:
                name_type = "其他"
            print(f"{name:<15} {count:<10,} {name_type}")
        
        print("-" * 60)
        
        # 8. 統計姓名類型分布
        print("\n\n姓名類型統計：")
        cursor.execute("""
            SELECT social_worker_name, COUNT(*) as count
            FROM visit_records
            GROUP BY social_worker_name
        """)
        
        existing_count = 0
        male_count = 0
        female_count = 0
        
        for name, count in cursor.fetchall():
            if name in EXISTING_NAMES:
                existing_count += count
            elif name in MALE_NAMES:
                male_count += count
            elif name in FEMALE_NAMES:
                female_count += count
        
        print(f"  原有姓名：{existing_count:,} 筆 ({existing_count/total_records*100:.1f}%)")
        print(f"  男性姓名：{male_count:,} 筆 ({male_count/total_records*100:.1f}%)")
        print(f"  女性姓名：{female_count:,} 筆 ({female_count/total_records*100:.1f}%)")
        
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
    print("=" * 70)
    print("  擴充更新社工姓名工具")
    print("=" * 70)
    print()
    print("原有姓名（保留）：")
    for i, name in enumerate(EXISTING_NAMES, 1):
        print(f"  {i}. {name}")
    
    print("\n新增男性姓名：")
    for i, name in enumerate(MALE_NAMES, 1):
        print(f"  {i}. {name}")
    
    print("\n新增女性姓名：")
    for i, name in enumerate(FEMALE_NAMES, 1):
        print(f"  {i}. {name}")
    
    print(f"\n總計：{len(ALL_NAMES)} 個姓名")
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
