"""
增加更多社工記錄，使用新的男女姓名
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import sqlite3
import random
from datetime import datetime, timedelta

# 原有的姓名
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

# 合併新姓名
NEW_NAMES = MALE_NAMES + FEMALE_NAMES

def add_new_social_workers():
    """增加新的社工記錄"""
    
    conn = sqlite3.connect('carbon_tracking.db')
    cursor = conn.cursor()
    
    try:
        # 1. 獲取現有的最大社工編號
        cursor.execute("""
            SELECT social_worker_id 
            FROM visit_records 
            WHERE social_worker_id LIKE 'SW%'
            ORDER BY social_worker_id DESC 
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        if result:
            last_id = int(result[0].replace('SW', ''))
        else:
            last_id = 10
        
        print(f"目前最大社工編號：SW{last_id:03d}")
        
        # 2. 為每個新姓名建立社工編號和記錄
        new_workers = []
        for i, name in enumerate(NEW_NAMES, 1):
            worker_id = f"SW{last_id + i:03d}"
            gender = "男" if name in MALE_NAMES else "女"
            new_workers.append((worker_id, name, gender))
        
        print(f"\n將新增 {len(new_workers)} 位社工：")
        print("-" * 70)
        print(f"{'社工編號':<15} {'姓名':<15} {'性別':<10} {'類型'}")
        print("-" * 70)
        
        for worker_id, name, gender in new_workers:
            name_type = "男性" if name in MALE_NAMES else "女性"
            print(f"{worker_id:<15} {name:<15} {gender:<10} {name_type}")
        
        print("-" * 70)
        
        # 3. 為每位新社工生成訪視記錄
        print("\n\n開始生成訪視記錄...")
        
        # 交通工具選項
        transport_types = ["機車", "汽車", "大眾運輸"]
        transport_coefficients = {
            "機車": 0.0695,
            "汽車": 0.1850,
            "大眾運輸": 0.0295
        }
        
        # 訪視類型
        visit_types = ["定期關懷", "健康檢查", "緊急訪視", "例行訪視"]
        
        # 日期範圍：2024/06/01 - 2024/09/30
        start_date = datetime(2024, 6, 1)
        end_date = datetime(2024, 9, 30)
        total_days = (end_date - start_date).days
        
        total_new_records = 0
        
        for worker_id, name, gender in new_workers:
            # 每位社工生成 800-1000 筆記錄
            num_records = random.randint(800, 1000)
            
            for _ in range(num_records):
                # 隨機日期
                random_days = random.randint(0, total_days)
                visit_date = start_date + timedelta(days=random_days)
                
                # 隨機交通工具和里程
                transport_type = random.choice(transport_types)
                distance = round(random.uniform(5, 50), 1)
                
                # 計算碳排放
                coefficient = transport_coefficients[transport_type]
                carbon_emission = round(distance * coefficient, 3)
                
                # 隨機訪視類型
                visit_type = random.choice(visit_types)
                
                # 隨機長者編號
                elder_id = f"E{random.randint(10001, 10100):05d}"
                
                # 插入記錄
                cursor.execute("""
                    INSERT INTO visit_records (
                        visit_date, social_worker_id, social_worker_name,
                        elder_id, visit_type, transport_type,
                        distance, carbon_emission
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    visit_date.strftime('%Y-%m-%d'),
                    worker_id,
                    name,
                    elder_id,
                    visit_type,
                    transport_type,
                    distance,
                    carbon_emission
                ))
            
            total_new_records += num_records
            print(f"  {worker_id} ({name}): 已生成 {num_records} 筆記錄")
        
        # 4. 提交變更
        conn.commit()
        
        # 5. 統計資訊
        cursor.execute("SELECT COUNT(*) FROM visit_records")
        total_records = cursor.fetchone()[0]
        
        print(f"\n\n✅ 新增完成！")
        print(f"   新增社工數：{len(new_workers)}")
        print(f"   新增記錄數：{total_new_records:,}")
        print(f"   資料庫總記錄數：{total_records:,}")
        
        # 6. 顯示所有社工統計
        print("\n\n所有社工統計：")
        cursor.execute("""
            SELECT social_worker_name, COUNT(*) as count
            FROM visit_records
            GROUP BY social_worker_name
            ORDER BY count DESC
        """)
        
        print("-" * 70)
        print(f"{'姓名':<15} {'記錄數':<10} {'類型'}")
        print("-" * 70)
        
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
        
        print("-" * 70)
        
        # 7. 類型統計
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
    print("  增加新社工記錄工具")
    print("=" * 70)
    print()
    print("將新增以下社工：")
    print("\n男性社工（10位）：")
    for i, name in enumerate(MALE_NAMES, 1):
        print(f"  {i}. {name}")
    
    print("\n女性社工（10位）：")
    for i, name in enumerate(FEMALE_NAMES, 1):
        print(f"  {i}. {name}")
    
    print(f"\n總計：{len(NEW_NAMES)} 位新社工")
    print("每位社工將生成 800-1000 筆訪視記錄")
    print()
    
    # 詢問是否繼續
    response = input("是否要新增這些社工記錄？(y/n): ")
    
    if response.lower() == 'y':
        # 先備份
        print("\n正在備份資料庫...")
        if backup_database():
            print("\n開始新增...")
            add_new_social_workers()
        else:
            print("\n❌ 備份失敗，取消新增")
    else:
        print("\n已取消新增")
