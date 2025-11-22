#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
簡化版 Mock Data 生成腳本
直接使用 SQL 插入數據，更快更可靠
"""

import sqlite3
from datetime import datetime, timedelta
import random
import uuid

def generate_mock_data():
    """生成 Mock Data"""
    print("=" * 60)
    print("🎲 開始生成評分系統 Mock Data (簡化版)")
    print("=" * 60)
    print()
    
    # 連接資料庫
    conn = sqlite3.connect('data/databases/emotion_analysis.db')
    cursor = conn.cursor()
    
    # 參數設定
    start_date = datetime(2025, 3, 1)
    end_date = datetime(2025, 10, 30)
    total_records = 180
    user_id = "demo_user"
    
    # 計算日期間隔
    date_range = (end_date - start_date).days
    date_interval = date_range / (total_records - 1)
    
    print(f"📅 時間範圍: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
    print(f"📊 總筆數: {total_records}")
    print(f"👤 用戶ID: {user_id}")
    print()
    
    # 創建用戶
    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, username, email, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, "示範用戶", "demo@example.com", datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    print("開始生成評分記錄...")
    print()
    
    success_count = 0
    
    for i in range(total_records):
        try:
            # 計算當前日期
            current_date = start_date + timedelta(days=i * date_interval)
            
            # 計算進度百分比 (0.0 到 1.0)
            progress = i / (total_records - 1)
            
            # 生成漸進式評分（從低到高）
            initial_emotion = random.uniform(45, 60)
            initial_voice = random.uniform(50, 65)
            initial_content = random.uniform(40, 55)
            
            final_emotion = random.uniform(85, 95)
            final_voice = random.uniform(90, 98)
            final_content = random.uniform(80, 92)
            
            emotion_score = initial_emotion + (final_emotion - initial_emotion) * progress + random.uniform(-5, 5)
            voice_score = initial_voice + (final_voice - initial_voice) * progress + random.uniform(-5, 5)
            content_score = initial_content + (final_content - initial_content) * progress + random.uniform(-5, 5)
            
            # 確保分數在合理範圍內
            emotion_score = max(30, min(100, emotion_score))
            voice_score = max(30, min(100, voice_score))
            content_score = max(30, min(100, content_score))
            
            # 計算綜合評分
            overall_score = emotion_score * 0.35 + voice_score * 0.35 + content_score * 0.30
            
            # 計算等級
            if overall_score >= 95:
                grade, stars, title = 'S', 5, '大師級'
            elif overall_score >= 85:
                grade, stars, title = 'A', 4, '優秀'
            elif overall_score >= 75:
                grade, stars, title = 'B', 3, '良好'
            elif overall_score >= 60:
                grade, stars, title = 'C', 2, '及格'
            else:
                grade, stars, title = 'D', 1, '待改進'
            
            # 生成會話ID
            session_id = str(uuid.uuid4())
            
            # 計算對話輪數和持續時間
            if overall_score < 60:
                conversation_count = random.randint(2, 4)
            elif overall_score < 75:
                conversation_count = random.randint(4, 6)
            elif overall_score < 85:
                conversation_count = random.randint(6, 8)
            else:
                conversation_count = random.randint(8, 12)
            
            total_words = conversation_count * random.randint(10, 20)
            duration = conversation_count * random.randint(15, 30)
            
            # 插入會話記錄
            cursor.execute("""
                INSERT INTO sessions (session_id, user_id, start_time, end_time, duration, device_type, browser, ip_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                user_id,
                current_date.strftime('%Y-%m-%d %H:%M:%S'),
                (current_date + timedelta(seconds=duration)).strftime('%Y-%m-%d %H:%M:%S'),
                duration,
                'Desktop',
                'Chrome',
                '127.0.0.1'
            ))
            
            # 插入評分記錄
            cursor.execute("""
                INSERT INTO score_records (
                    session_id, user_id, overall_score, emotion_score, voice_score, content_score,
                    grade, stars, title, conversation_count, total_words, duration, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                user_id,
                round(overall_score, 1),
                round(emotion_score, 1),
                round(voice_score, 1),
                round(content_score, 1),
                grade,
                stars,
                title,
                conversation_count,
                total_words,
                duration,
                current_date.strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            success_count += 1
            
            # 每 20 筆顯示一次進度
            if (i + 1) % 20 == 0 or i == 0 or i == total_records - 1:
                progress_pct = (i + 1) / total_records * 100
                print(f"  [{i+1:3d}/{total_records}] {progress_pct:5.1f}% | "
                      f"日期: {current_date.strftime('%Y-%m-%d')} | "
                      f"評分: {overall_score:5.1f} | "
                      f"等級: {grade}")
            
        except Exception as e:
            print(f"  ❌ 第 {i+1} 筆記錄生成失敗: {e}")
    
    # 提交事務
    conn.commit()
    conn.close()
    
    print()
    print("=" * 60)
    print("📊 生成結果統計")
    print("=" * 60)
    print(f"✅ 成功: {success_count} 筆")
    print(f"❌ 失敗: {total_records - success_count} 筆")
    print(f"📈 成功率: {success_count/total_records*100:.1f}%")
    print()
    
    print("=" * 60)
    print("🎉 Mock Data 生成完成！")
    print("=" * 60)
    print()
    print("💡 下一步:")
    print("   1. 啟動 Flask 應用: bStart.bat")
    print("   2. 訪問評分分析頁面: http://localhost:5000/score-analysis")
    print("   3. 查看進步趨勢圖表")
    print()

if __name__ == "__main__":
    try:
        generate_mock_data()
    except KeyboardInterrupt:
        print("\n\n⚠️  用戶中斷操作")
    except Exception as e:
        print(f"\n\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
