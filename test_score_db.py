"""測試評分系統資料庫"""
from services.score_database import score_db
from services.score_calculator import score_calculator

print("=" * 60)
print("🧪 測試評分系統資料庫")
print("=" * 60)

# 測試 1: 創建用戶
print("\n[測試 1] 創建用戶...")
user = score_db.create_or_get_user('test_user_001', '測試用戶', 'test@example.com')
print(f"✅ 用戶創建成功: {user['user_id']}")

# 測試 2: 創建會話
print("\n[測試 2] 創建會話...")
session_id = score_db.create_session('test_user_001', 'desktop', 'Chrome', '127.0.0.1')
print(f"✅ 會話創建成功: {session_id}")

# 測試 3: 添加對話
print("\n[測試 3] 添加對話...")
conversations_data = [
    ('user', '你好，今天天氣很好', 'positive', 0.8),
    ('ai', '您好！今天確實是個好天氣呢', 'positive', 0.9),
    ('user', '我想問一下關於情緒的問題', 'neutral', 0.6),
    ('ai', '當然可以！我很樂意幫助您', 'positive', 0.85),
    ('user', '謝謝你的幫助', 'positive', 0.9),
]

for speaker, text, sentiment, score in conversations_data:
    seq = score_db.add_conversation(
        session_id, speaker, text, sentiment, score
    )
    print(f"  ✅ 添加對話 #{seq}: {speaker} - {text[:20]}...")

# 測試 4: 獲取對話記錄
print("\n[測試 4] 獲取對話記錄...")
conversations = score_db.get_conversations(session_id)
print(f"✅ 獲取到 {len(conversations)} 條對話記錄")

# 測試 5: 計算評分
print("\n[測試 5] 計算評分...")
scores = score_calculator.calculate_all_scores(conversations)
print(f"  情緒評分: {scores['emotion']}")
print(f"  語音評分: {scores['voice']}")
print(f"  文字評分: {scores['content']}")
print(f"  綜合評分: {scores['overall']}")
print(f"  改進建議: {len(scores['suggestions'])} 條")

# 測試 6: 結束會話
print("\n[測試 6] 結束會話...")
duration = score_db.end_session(session_id)
print(f"✅ 會話已結束，持續時間: {duration} 秒")

# 測試 7: 保存評分記錄
print("\n[測試 7] 保存評分記錄...")
record_id = score_db.save_score_record(
    session_id, 
    'test_user_001',
    scores,
    {
        'conversation_count': len(conversations),
        'total_words': sum([c['word_count'] for c in conversations]),
        'duration': duration
    }
)
print(f"✅ 評分記錄已保存，ID: {record_id}")

# 測試 8: 獲取評分記錄
print("\n[測試 8] 獲取評分記錄...")
record = score_db.get_score_record(session_id)
print(f"✅ 評分記錄:")
print(f"  等級: {record['grade']} ({record['stars']} 星)")
print(f"  稱號: {record['title']}")
print(f"  詳情: {len(record['details'])} 項")
print(f"  建議: {len(record['suggestions'])} 條")

# 測試 9: 獲取用戶統計
print("\n[測試 9] 獲取用戶統計...")
stats = score_db.get_user_statistics('test_user_001')
print(f"✅ 用戶統計:")
print(f"  總會話數: {stats['total_sessions']}")
print(f"  平均評分: {stats['avg_score']:.1f}")
print(f"  最佳評分: {stats['best_score']:.1f}")

print("\n" + "=" * 60)
print("✅ 所有測試通過！")
print("=" * 60)
