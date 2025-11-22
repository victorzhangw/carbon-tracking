#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整系統測試腳本
測試評分系統的所有功能
"""

import sys
import os

# 添加項目根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """測試所有必要的模組是否能正常導入"""
    print("=" * 60)
    print("🧪 測試模組導入")
    print("=" * 60)
    
    try:
        from services.score_database import score_db
        print("✅ score_database 導入成功")
    except Exception as e:
        print(f"❌ score_database 導入失敗: {e}")
        return False
    
    try:
        from services.score_calculator import score_calculator
        print("✅ score_calculator 導入成功")
    except Exception as e:
        print(f"❌ score_calculator 導入失敗: {e}")
        return False
    
    try:
        from routes.main import main
        print("✅ routes.main 導入成功")
    except Exception as e:
        print(f"❌ routes.main 導入失敗: {e}")
        return False
    
    print()
    return True

def test_database():
    """測試資料庫功能"""
    print("=" * 60)
    print("🧪 測試資料庫功能")
    print("=" * 60)
    
    try:
        from services.score_database import score_db
        import uuid
        
        # 創建測試用戶
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        score_db.create_user(user_id, "測試用戶")
        print(f"✅ 創建用戶成功: {user_id}")
        
        # 創建測試會話
        session_id = str(uuid.uuid4())
        score_db.create_session(session_id, user_id)
        print(f"✅ 創建會話成功: {session_id}")
        
        # 添加測試對話
        conversations = [
            {"speaker": "user", "text": "你好，今天天氣很好", "sentiment": "positive"},
            {"speaker": "ai", "text": "您好！今天確實是個好天氣呢", "sentiment": "positive"},
            {"speaker": "user", "text": "我想問一下關於情緒的問題", "sentiment": "neutral"},
            {"speaker": "ai", "text": "當然可以！我很樂意幫助您", "sentiment": "positive"},
        ]
        
        for conv in conversations:
            score_db.add_conversation(
                session_id,
                conv['speaker'],
                conv['text'],
                conv['sentiment']
            )
        print(f"✅ 添加 {len(conversations)} 條對話記錄")
        
        # 獲取對話記錄
        records = score_db.get_conversations(session_id)
        print(f"✅ 獲取對話記錄: {len(records)} 條")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ 資料庫測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_calculator():
    """測試評分計算功能"""
    print("=" * 60)
    print("🧪 測試評分計算功能")
    print("=" * 60)
    
    try:
        from services.score_calculator import score_calculator
        
        # 測試對話數據
        conversations = [
            {
                "speaker": "user",
                "text": "你好，今天天氣很好，我感覺心情不錯",
                "sentiment": "positive",
                "audio_quality": 0.9
            },
            {
                "speaker": "ai",
                "text": "您好！今天確實是個好天氣呢，很高興聽到您心情不錯",
                "sentiment": "positive",
                "audio_quality": 0.95
            },
            {
                "speaker": "user",
                "text": "我想問一下關於情緒管理的問題",
                "sentiment": "neutral",
                "audio_quality": 0.85
            },
            {
                "speaker": "ai",
                "text": "當然可以！我很樂意幫助您了解情緒管理的相關知識",
                "sentiment": "positive",
                "audio_quality": 0.9
            },
        ]
        
        # 計算評分
        scores = score_calculator.calculate_all_scores(conversations)
        
        print(f"✅ 情緒評分: {scores['emotion']:.1f}")
        print(f"✅ 語音評分: {scores['voice']:.1f}")
        print(f"✅ 文字評分: {scores['content']:.1f}")
        print(f"✅ 綜合評分: {scores['overall']:.1f}")
        print(f"✅ 改進建議: {len(scores['suggestions'])} 條")
        
        # 顯示建議
        if scores['suggestions']:
            print("\n💡 改進建議:")
            for i, suggestion in enumerate(scores['suggestions'], 1):
                print(f"   {i}. {suggestion}")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ 評分計算測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_routes():
    """測試路由配置"""
    print("=" * 60)
    print("🧪 測試路由配置")
    print("=" * 60)
    
    try:
        from routes.main import main
        
        # 檢查路由是否存在
        routes = []
        for rule in main.url_map.iter_rules():
            if rule.endpoint.startswith('main.'):
                routes.append(str(rule))
        
        required_routes = [
            '/emotion-analysis',
            '/score-analysis',
            '/api/end-session',
            '/api/score-history'
        ]
        
        for route in required_routes:
            if any(route in r for r in routes):
                print(f"✅ 路由存在: {route}")
            else:
                print(f"⚠️  路由可能缺失: {route}")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ 路由測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主測試函數"""
    print("\n" + "=" * 60)
    print("🚀 開始完整系統測試")
    print("=" * 60)
    print()
    
    results = []
    
    # 執行所有測試
    results.append(("模組導入", test_imports()))
    results.append(("資料庫功能", test_database()))
    results.append(("評分計算", test_calculator()))
    results.append(("路由配置", test_routes()))
    
    # 顯示測試結果
    print("=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {name}")
    
    print()
    print(f"總計: {passed}/{total} 測試通過")
    
    if passed == total:
        print("\n🎉 所有測試通過！系統運行正常！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 個測試失敗，請檢查錯誤訊息")
        return 1

if __name__ == "__main__":
    sys.exit(main())
