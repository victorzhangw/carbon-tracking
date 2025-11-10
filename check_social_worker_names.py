"""
檢查資料庫中的社工姓名
"""

import sqlite3

# 目標姓名列表
TARGET_NAMES = [
    "陳冠宇",
    "曾柏睿",
    "林怡君",
    "吳宜靜",
    "方琬婷"
]

def check_social_worker_names():
    """檢查資料庫中的社工姓名"""
    
    try:
        # 連接資料庫
        conn = sqlite3.connect('carbon_tracking.db')
        cursor = conn.cursor()
        
        print("=" * 70)
        print("  資料庫社工姓名檢查")
        print("=" * 70)
        print()
        
        # 1. 獲取所有不重複的社工
        cursor.execute("""
            SELECT DISTINCT social_worker_id, social_worker_name 
            FROM visit_records 
            ORDER BY social_worker_id
        """)
        
        workers = cursor.fetchall()
        
        print(f"📊 資料庫中共有 {len(workers)} 位社工\n")
        print("-" * 70)
        print(f"{'社工編號':<15} {'姓名':<15} {'狀態'}")
        print("-" * 70)
        
        # 檢查每位社工的姓名
        all_updated = True
        for worker_id, worker_name in workers:
            if worker_name in TARGET_NAMES:
                status = "✅ 已更新"
            else:
                status = "❌ 未更新"
                all_updated = False
            
            print(f"{worker_id:<15} {worker_name:<15} {status}")
        
        print("-" * 70)
        print()
        
        # 2. 統計各姓名的記錄數
        print("📈 各社工的記錄數統計：\n")
        cursor.execute("""
            SELECT social_worker_name, COUNT(*) as count
            FROM visit_records
            GROUP BY social_worker_name
            ORDER BY count DESC
        """)
        
        print("-" * 70)
        print(f"{'姓名':<15} {'記錄數':<10} {'百分比'}")
        print("-" * 70)
        
        # 獲取總記錄數
        cursor.execute("SELECT COUNT(*) FROM visit_records")
        total_records = cursor.fetchone()[0]
        
        for name, count in cursor.fetchall():
            percentage = (count / total_records * 100) if total_records > 0 else 0
            status = "✅" if name in TARGET_NAMES else "❌"
            print(f"{status} {name:<13} {count:<10} {percentage:>5.1f}%")
        
        print("-" * 70)
        print(f"{'總計':<15} {total_records:<10} 100.0%")
        print("-" * 70)
        print()
        
        # 3. 檢查目標姓名是否都存在
        print("🎯 目標姓名檢查：\n")
        cursor.execute("""
            SELECT DISTINCT social_worker_name 
            FROM visit_records
        """)
        
        current_names = [row[0] for row in cursor.fetchall()]
        
        print("-" * 70)
        print(f"{'目標姓名':<15} {'狀態'}")
        print("-" * 70)
        
        for target_name in TARGET_NAMES:
            if target_name in current_names:
                print(f"{target_name:<15} ✅ 已存在")
            else:
                print(f"{target_name:<15} ❌ 不存在")
        
        print("-" * 70)
        print()
        
        # 4. 最終結論
        print("=" * 70)
        if all_updated:
            print("✅ 結論：所有社工姓名已更新為目標姓名")
        else:
            print("❌ 結論：尚未完成姓名更新")
            print("\n💡 執行以下命令進行更新：")
            print("   python update_social_worker_names.py")
        print("=" * 70)
        
        conn.close()
        
        return all_updated
        
    except sqlite3.Error as e:
        print(f"\n❌ 資料庫錯誤：{e}")
        return False
    except FileNotFoundError:
        print(f"\n❌ 找不到資料庫檔案：carbon_tracking.db")
        print("💡 請確認資料庫檔案是否存在")
        return False
    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
        return False

if __name__ == '__main__':
    check_social_worker_names()
