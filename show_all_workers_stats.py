"""
顯示所有社工的完整統計資訊
"""

import sqlite3

def show_statistics():
    """顯示完整統計"""
    
    conn = sqlite3.connect('carbon_tracking.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("  碳排放追蹤系統 - 社工統計報表")
    print("=" * 80)
    print()
    
    # 1. 總體統計
    cursor.execute("SELECT COUNT(*) FROM visit_records")
    total_records = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT social_worker_id) FROM visit_records")
    total_workers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT social_worker_name) FROM visit_records")
    unique_names = cursor.fetchone()[0]
    
    print(f"📊 總體統計")
    print("-" * 80)
    print(f"  總訪視記錄數：{total_records:,} 筆")
    print(f"  社工人數：{total_workers} 位")
    print(f"  不重複姓名：{unique_names} 個")
    print()
    
    # 2. 所有社工列表
    cursor.execute("""
        SELECT social_worker_id, social_worker_name, COUNT(*) as count
        FROM visit_records
        GROUP BY social_worker_id, social_worker_name
        ORDER BY social_worker_id
    """)
    
    workers = cursor.fetchall()
    
    print(f"👥 所有社工列表（共 {len(workers)} 位）")
    print("-" * 80)
    print(f"{'編號':<10} {'姓名':<15} {'記錄數':<10} {'百分比'}")
    print("-" * 80)
    
    for worker_id, name, count in workers:
        percentage = (count / total_records * 100) if total_records > 0 else 0
        print(f"{worker_id:<10} {name:<15} {count:<10,} {percentage:>6.2f}%")
    
    print("-" * 80)
    print()
    
    # 3. 按姓名統計
    cursor.execute("""
        SELECT social_worker_name, COUNT(*) as count, COUNT(DISTINCT social_worker_id) as worker_count
        FROM visit_records
        GROUP BY social_worker_name
        ORDER BY count DESC
    """)
    
    names_stats = cursor.fetchall()
    
    print(f"📝 按姓名統計（共 {len(names_stats)} 個姓名）")
    print("-" * 80)
    print(f"{'姓名':<15} {'記錄數':<10} {'社工數':<10} {'百分比'}")
    print("-" * 80)
    
    for name, count, worker_count in names_stats:
        percentage = (count / total_records * 100) if total_records > 0 else 0
        print(f"{name:<15} {count:<10,} {worker_count:<10} {percentage:>6.2f}%")
    
    print("-" * 80)
    print()
    
    # 4. 月度統計
    cursor.execute("""
        SELECT strftime('%Y-%m', visit_date) as month, COUNT(*) as count
        FROM visit_records
        GROUP BY month
        ORDER BY month
    """)
    
    monthly_stats = cursor.fetchall()
    
    print(f"📅 月度統計")
    print("-" * 80)
    print(f"{'月份':<15} {'記錄數':<10} {'百分比'}")
    print("-" * 80)
    
    for month, count in monthly_stats:
        percentage = (count / total_records * 100) if total_records > 0 else 0
        print(f"{month:<15} {count:<10,} {percentage:>6.2f}%")
    
    print("-" * 80)
    print()
    
    # 5. 交通工具統計
    cursor.execute("""
        SELECT transport_type, COUNT(*) as count, 
               SUM(distance) as total_distance,
               SUM(carbon_emission) as total_emission
        FROM visit_records
        GROUP BY transport_type
        ORDER BY count DESC
    """)
    
    transport_stats = cursor.fetchall()
    
    print(f"🚗 交通工具統計")
    print("-" * 80)
    print(f"{'交通工具':<15} {'使用次數':<10} {'總里程(km)':<15} {'總碳排(kg)'}")
    print("-" * 80)
    
    for transport, count, distance, emission in transport_stats:
        print(f"{transport:<15} {count:<10,} {distance:<15,.1f} {emission:,.2f}")
    
    print("-" * 80)
    print()
    
    # 6. 碳排放統計
    cursor.execute("""
        SELECT 
            SUM(carbon_emission) as total_emission,
            AVG(carbon_emission) as avg_emission,
            MIN(carbon_emission) as min_emission,
            MAX(carbon_emission) as max_emission
        FROM visit_records
    """)
    
    emission_stats = cursor.fetchone()
    total_emission, avg_emission, min_emission, max_emission = emission_stats
    
    print(f"🌍 碳排放統計")
    print("-" * 80)
    print(f"  總碳排放量：{total_emission:,.2f} kg CO2e ({total_emission/1000:.2f} 公噸)")
    print(f"  平均碳排放：{avg_emission:.3f} kg CO2e / 次")
    print(f"  最小碳排放：{min_emission:.3f} kg CO2e")
    print(f"  最大碳排放：{max_emission:.3f} kg CO2e")
    print()
    
    conn.close()
    
    print("=" * 80)
    print("  報表結束")
    print("=" * 80)

if __name__ == '__main__':
    show_statistics()
