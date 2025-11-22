#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成評分系統 Mock Data
生成從 2025-3-1 到 2025-10-30 的 180 筆評分記錄
展示從不好到好的進步趨勢
"""

import sys
import os
import random
from datetime import datetime, timedelta
import uuid

# 添加項目根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.score_database import score_db
from services.score_calculator import score_calculator

def generate_progressive_score(index, total):
    """
    生成漸進式評分
    index: 當前索引 (0 到 total-1)
    total: 總筆數
    返回: (emotion_score, voice_score, content_score)
    """
    # 計算進度百分比 (0.0 到 1.0)
    progress = index / (total - 1)
    
    # 初始分數範圍 (較低)
    initial_emotion = random.uniform(45, 60)
    initial_voice = random.uniform(50, 65)
    initial_content = random.uniform(40, 55)
    
    # 最終分數範圍 (較高)
    final_emotion = random.uniform(85, 95)
    final_voice = random.uniform(90, 98)
    final_content = random.uniform(80, 92)
    
    # 線性插值 + 隨機波動
    emotion_score = initial_emotion + (final_emotion - initial_emotion) * progress
    voice_score = initial_voice + (final_voice - initial_voice) * progress
    content_score = initial_content + (final_content - initial_content) * progress
    
    # 添加隨機波動 (±5分)
    emotion_score += random.uniform(-5, 5)
    voice_score += random.uniform(-5, 5)
    content_score += random.uniform(-5, 5)
    
    # 確保分數在合理範圍內
    emotion_score = max(30, min(100, emotion_score))
    voice_score = max(30, min(100, voice_score))
    content_score = max(30, min(100, content_score))
    
    return round(emotion_score, 1), round(voice_score, 1), round(content_score, 1)

def generate_conversation_history(emotion_score, voice_score, content_score):
    """
    根據評分生成對話歷史
    """
    # 根據評分決定對話輪數 (分數越高，對話越多)
    overall = (emotion_score * 0.35 + voice_score * 0.35 + content_score * 0.3)
    if overall < 60:
        num_rounds = random.randint(2, 4)
    elif overall < 75:
        num_rounds = random.randint(4, 6)
    elif overall < 85:
        num_rounds = random.randint(6, 8)
    else:
        num_rounds = random.randint(8, 12)
    
    # 情緒類型池
    sentiments = ['positive', 'neutral', 'negative', 'happy', 'sad', 'excited', 'calm']
    
    # 對話內容模板
    user_templates = [
        "你好，今天天氣很好",
        "我想問一下關於情緒的問題",
        "最近感覺壓力有點大",
        "謝謝你的幫助",
        "我覺得這個建議很有用",
        "能再詳細說明一下嗎",
        "我明白了，謝謝",
        "這讓我感覺好多了",
        "我會試著這樣做",
        "你說得很有道理",
        "我想分享一下我的感受",
        "這對我很有幫助"
    ]
    
    ai_templates = [
        "您好！很高興為您服務",
        "當然可以！我很樂意幫助您",
        "我理解您的感受，讓我們一起來看看",
        "不客氣！這是我應該做的",
        "很高興能幫到您",
        "讓我為您詳細解釋一下",
        "您做得很好！",
        "我很高興聽到這個消息",
        "這是一個很好的想法",
        "您的進步讓我很欣慰",
        "請繼續保持這樣的態度",
        "我會一直支持您的"
    ]
    
    conversations = []
    for i in range(num_rounds):
        # 用戶對話
        user_text = random.choice(user_templates)
        user_sentiment = random.choice(sentiments)
        conversations.append({
            'speaker': 'user',
            'text': user_text,
            'sentiment': user_sentiment,
            'audio_quality': voice_score / 100.0,
            'word_count': len(user_text)
        })
        
        # AI 回應
        ai_text = random.choice(ai_templates)
        ai_sentiment = 'positive' if random.random() > 0.2 else 'neutral'
        conversations.append({
            'speaker': 'ai',
            'text': ai_text,
            'sentiment': ai_sentiment,
            'audio_quality': 0.95,
            'word_count': len(ai_text)
        })
    
    return conversations

def generate_mock_data():
    """生成 Mock Data"""
    print("=" * 60)
    print("🎲 開始生成評分系統 Mock Data")
    print("=" * 60)
    print()
    
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
    try:
        score_db.create_or_get_user(user_id, "示範用戶", "demo@example.com")
        print(f"✅ 用戶創建成功: {user_id}")
    except Exception as e:
        print(f"⚠️  用戶可能已存在: {e}")
    
    print()
    print("開始生成評分記錄...")
    print()
    
    success_count = 0
    error_count = 0
    
    for i in range(total_records):
        try:
            # 計算當前日期
            current_date = start_date + timedelta(days=i * date_interval)
            
            # 生成漸進式評分
            emotion_score, voice_score, content_score = generate_progressive_score(i, total_records)
            
            # 計算綜合評分
            overall_score = round(
                emotion_score * 0.35 + voice_score * 0.35 + content_score * 0.3,
                1
            )
            
            # 創建會話（會自動生成 session_id）
            session_id = score_db.create_session(
                user_id=user_id,
                device_type="Desktop",
                browser="Chrome",
                ip_address="127.0.0.1"
            )
            
            # 生成對話歷史
            conversations = generate_conversation_history(emotion_score, voice_score, content_score)
            
            # 添加對話記錄
            for conv in conversations:
                score_db.add_conversation(
                    session_id=session_id,
                    speaker=conv['speaker'],
                    text=conv['text'],
                    sentiment=conv['sentiment']
                )
            
            # 計算持續時間 (根據對話輪數)
            duration = len(conversations) * random.randint(15, 30)
            
            # 結束會話
            score_db.end_session(session_id)
            
            # 準備評分數據
            scores = {
                'emotion': emotion_score,
                'voice': voice_score,
                'content': content_score,
                'overall': overall_score,
                'details': {
                    'emotion': {
                        'diversity': round(emotion_score + random.uniform(-5, 5), 1),
                        'appropriateness': round(emotion_score + random.uniform(-5, 5), 1),
                        'intensity': round(emotion_score + random.uniform(-5, 5), 1),
                        'consistency': round(emotion_score + random.uniform(-5, 5), 1)
                    },
                    'voice': {
                        'clarity': round(voice_score + random.uniform(-5, 5), 1),
                        'volume': round(voice_score + random.uniform(-5, 5), 1),
                        'speed': round(voice_score + random.uniform(-5, 5), 1),
                        'fluency': round(voice_score + random.uniform(-5, 5), 1)
                    },
                    'content': {
                        'length': round(content_score + random.uniform(-5, 5), 1),
                        'richness': round(content_score + random.uniform(-5, 5), 1),
                        'coherence': round(content_score + random.uniform(-5, 5), 1),
                        'engagement': round(content_score + random.uniform(-5, 5), 1)
                    }
                },
                'suggestions': []
            }
            
            # 根據評分生成建議
            if emotion_score < 80:
                scores['suggestions'].append({
                    'category': '情緒表達',
                    'icon': '💪',
                    'text': '可以更明確地表達你的感受和情緒',
                    'priority': 'medium'
                })
            if voice_score < 80:
                scores['suggestions'].append({
                    'category': '語音品質',
                    'icon': '🎤',
                    'text': '建議放慢語速，咬字更清晰',
                    'priority': 'medium'
                })
            if content_score < 80:
                scores['suggestions'].append({
                    'category': '文字內容',
                    'icon': '📝',
                    'text': '可以說得更詳細一些，豐富對話內容',
                    'priority': 'medium'
                })
            
            # 統計資訊
            statistics = {
                'conversation_count': len(conversations),
                'total_words': sum(c.get('word_count', 0) for c in conversations),
                'duration': duration
            }
            
            # 保存評分記錄
            record_id = score_db.save_score_record(
                session_id=session_id,
                user_id=user_id,
                scores=scores,
                statistics=statistics
            )
            
            # 更新記錄的創建時間（使用 SQL 直接更新）
            conn = score_db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE score_records SET created_at = ? WHERE id = ?",
                (current_date.strftime('%Y-%m-%d %H:%M:%S'), record_id)
            )
            cursor.execute(
                "UPDATE sessions SET start_time = ?, end_time = ? WHERE session_id = ?",
                (
                    current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    (current_date + timedelta(seconds=duration)).strftime('%Y-%m-%d %H:%M:%S'),
                    session_id
                )
            )
            conn.commit()
            conn.close()
            
            success_count += 1
            
            # 每 20 筆顯示一次進度
            if (i + 1) % 20 == 0 or i == 0 or i == total_records - 1:
                progress = (i + 1) / total_records * 100
                print(f"  [{i+1:3d}/{total_records}] {progress:5.1f}% | "
                      f"日期: {current_date.strftime('%Y-%m-%d')} | "
                      f"評分: {overall_score:5.1f} | "
                      f"情緒: {emotion_score:5.1f} | "
                      f"語音: {voice_score:5.1f} | "
                      f"文字: {content_score:5.1f}")
            
        except Exception as e:
            error_count += 1
            print(f"  ❌ 第 {i+1} 筆記錄生成失敗: {e}")
    
    print()
    print("=" * 60)
    print("📊 生成結果統計")
    print("=" * 60)
    print(f"✅ 成功: {success_count} 筆")
    print(f"❌ 失敗: {error_count} 筆")
    print(f"📈 成功率: {success_count/total_records*100:.1f}%")
    print()
    
    # 查詢統計資訊
    stats = score_db.get_user_statistics(user_id)
    print("=" * 60)
    print("📈 用戶統計資訊")
    print("=" * 60)
    print(f"總會話數: {stats['total_sessions'] or 0}")
    print(f"平均評分: {stats['avg_score'] or 0:.1f}")
    print(f"最佳評分: {stats['best_score'] or 0:.1f}")
    print(f"最差評分: {stats['worst_score'] or 0:.1f}")
    print(f"平均情緒評分: {stats['avg_emotion'] or 0:.1f}")
    print(f"平均語音評分: {stats['avg_voice'] or 0:.1f}")
    print(f"平均文字評分: {stats['avg_content'] or 0:.1f}")
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
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
