"""
生成碳排放追蹤系統的模擬資料
日期範圍：2024/06/01 ~ 2024/09/30
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import random
from datetime import datetime, timedelta
from modules.carbon_tracking.database_carbon_tracking import CarbonTrackingDB

def generate_mock_data():
    """生成模擬資料"""
    print("\n" + "="*60)
    print("開始生成碳排放追蹤系統模擬資料")
    print("="*60 + "\n")
    
    db = CarbonTrackingDB()
    
    # 社工資料
    social_workers = [
        {'worker_id': 'SW001', 'name': '王小明', 'transport': '機車'},
        {'worker_id': 'SW002', 'name': '李小華', 'transport': '汽車'},
        {'worker_id': 'SW003', 'name': '張小美', 'transport': '機車'},
        {'worker_id': 'SW004', 'name': '陳小強', 'transport': '機車'},
        {'worker_id': 'SW005', 'name': '林小芳', 'transport': '汽車'},
        {'worker_id': 'SW006', 'name': '黃小玲', 'transport': '機車'},
        {'worker_id': 'SW007', 'name': '吳小文', 'transport': '大眾運輸'},
        {'worker_id': 'SW008', 'name': '劉小雯', 'transport': '機車'},
        {'worker_id': 'SW009', 'name': '鄭小傑', 'transport': '汽車'},
        {'worker_id': 'SW010', 'name': '謝小慧', 'transport': '機車'},
    ]
    
    # 長者資料（3300人，生成部分代表性資料）
    elder_regions = {
        '都會區': 1650,
        '郊區': 1320,
        '偏鄉': 330
    }
    
    # 距離範圍（根據區域）
    distance_ranges = {
        '都會區': (5, 10),
        '郊區': (12, 25),
        '偏鄉': (20, 35)
    }
    
    # 生成日期範圍：2024/06/01 ~ 2024/09/30
    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 9, 30)
    
    print("📊 生成訪視記錄...")
    
    total_visits = 0
    total_ai_care = 0
    
    # 按月生成資料
    current_date = start_date
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        
        print(f"\n生成 {year}年{month}月 資料...")
        
        # 每月每位長者平均訪視2次（導入AI後）
        monthly_visits = 0
        monthly_ai_care = 0
        
        # 生成該月的訪視記錄
        days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31
        
        for day in range(1, days_in_month + 1):
            visit_date = datetime(year, month, day)
            
            # 工作日才有訪視（週一到週五）
            if visit_date.weekday() < 5:
                # 每天約220次訪視（3300人 * 2次/月 / 30天 * 工作日比例）
                daily_visits = random.randint(200, 240)
                
                for _ in range(daily_visits):
                    # 隨機選擇社工
                    worker = random.choice(social_workers)
                    
                    # 隨機選擇區域
                    region = random.choices(
                        list(elder_regions.keys()),
                        weights=[1650, 1320, 330]
                    )[0]
                    
                    # 生成長者ID
                    elder_id = f"E{random.randint(10000, 13300):05d}"
                    
                    # 根據區域生成距離
                    min_dist, max_dist = distance_ranges[region]
                    distance = round(random.uniform(min_dist, max_dist), 1)
                    
                    # 生成訪視記錄
                    visit_data = {
                        'visit_date': visit_date.strftime('%Y-%m-%d'),
                        'social_worker_id': worker['worker_id'],
                        'social_worker_name': worker['name'],
                        'elder_id': elder_id,
                        'elder_name': f'長者{elder_id}',
                        'visit_type': random.choice(['定期關懷', '健康檢查', '緊急訪視', '例行訪視']),
                        'transport_type': worker['transport'],
                        'distance': distance,
                        'travel_time': int(distance * random.uniform(2, 4)),
                        'start_location': f'{region}社工站',
                        'end_location': f'{region}長者住所',
                        'notes': random.choice(['順利完成', '長者狀況良好', '需要後續追蹤', ''])
                    }
                    
                    db.add_visit_record(visit_data)
                    monthly_visits += 1
                
                # 生成AI關懷記錄（每天約440次，是訪視的2倍）
                daily_ai_care = random.randint(400, 480)
                
                for _ in range(daily_ai_care):
                    elder_id = f"E{random.randint(10000, 13300):05d}"
                    
                    ai_care_data = {
                        'care_date': visit_date.strftime('%Y-%m-%d'),
                        'elder_id': elder_id,
                        'care_type': random.choice(['語音關懷', '健康提醒', '用藥提醒', '情緒關懷']),
                        'duration': random.randint(3, 10),
                        'result': random.choice(['正常', '需關注', '良好']),
                        'notes': ''
                    }
                    
                    db.add_ai_care_record(ai_care_data)
                    monthly_ai_care += 1
        
        total_visits += monthly_visits
        total_ai_care += monthly_ai_care
        
        print(f"  ✓ 實地訪視：{monthly_visits:,} 次")
        print(f"  ✓ AI關懷：{monthly_ai_care:,} 次")
        
        # 移到下個月
        if month == 12:
            current_date = datetime(year + 1, 1, 1)
        else:
            current_date = datetime(year, month + 1, 1)
    
    print("\n" + "="*60)
    print("✓ 模擬資料生成完成！")
    print("="*60)
    print(f"\n📊 統計摘要：")
    print(f"  期間：2024/06/01 ~ 2024/09/30")
    print(f"  總實地訪視：{total_visits:,} 次")
    print(f"  總AI關懷：{total_ai_care:,} 次")
    print(f"  服務長者：約 3,300 人")
    
    # 計算碳排放統計
    stats = db.get_statistics_summary('2024-06-01', '2024-09-30')
    print(f"\n🌍 碳排放統計：")
    print(f"  總行駛里程：{stats['total_distance']:,.1f} 公里")
    print(f"  總碳排放：{stats['total_emission']:,.2f} kg CO2e")
    print(f"  總碳排放：{stats['total_emission']/1000:.2f} 公噸 CO2e")
    print(f"  平均每次訪視：{stats['avg_distance']:.1f} 公里")
    
    print("\n✅ 資料已儲存到資料庫：carbon_tracking.db")
    print("\n💡 提示：可以使用後台頁面查看和管理這些資料\n")

if __name__ == '__main__':
    generate_mock_data()
