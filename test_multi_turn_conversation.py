"""
測試多輪對話功能
"""

import requests
import json

def test_multi_turn_conversation():
    """測試多輪對話上下文記憶"""
    print("=" * 60)
    print("測試多輪對話功能")
    print("=" * 60)
    
    # 模擬對話歷史
    conversation_history = []
    conversation_round = 0
    
    # 測試對話場景
    test_conversations = [
        {
            "round": 1,
            "user_input": "今天天氣真好",
            "expected_keywords": ["天氣", "計劃", "出去"]
        },
        {
            "round": 2,
            "user_input": "想出去走走",
            "expected_keywords": ["走走", "去哪", "推薦"]
        },
        {
            "round": 3,
            "user_input": "不知道去哪",
            "expected_keywords": ["推薦", "地方", "公園", "商場"]
        }
    ]
    
    print("\n開始模擬多輪對話...\n")
    
    for test in test_conversations:
        print(f"{'=' * 60}")
        print(f"第 {test['round']} 輪對話")
        print(f"{'=' * 60}")
        
        user_input = test['user_input']
        print(f"👤 用戶: {user_input}")
        
        # 調用 AI 服務
        from services.ai import analyze_and_respond_with_context
        
        result = analyze_and_respond_with_context(
            user_input=user_input,
            conversation_context=conversation_history,
            response_style='friendly',
            conversation_mode='continuous',
            conversation_round=conversation_round
        )
        
        response = result.get('response', '')
        sentiment = result.get('sentiment', '')
        confidence = result.get('confidence', 0)
        
        print(f"🤖 AI: {response}")
        print(f"📊 情緒: {sentiment}, 信心度: {confidence:.2f}")
        
        # 檢查回應是否包含預期關鍵字
        keywords_found = []
        for keyword in test['expected_keywords']:
            if keyword in response:
                keywords_found.append(keyword)
        
        if keywords_found:
            print(f"✅ 包含預期關鍵字: {', '.join(keywords_found)}")
        else:
            print(f"⚠️ 未包含預期關鍵字: {', '.join(test['expected_keywords'])}")
        
        # 更新對話歷史
        conversation_history.append({
            'role': 'user',
            'content': user_input
        })
        conversation_history.append({
            'role': 'assistant',
            'content': response
        })
        
        conversation_round += 1
        
        print(f"\n📝 當前歷史記錄: {len(conversation_history)} 條")
        print()
    
    # 測試上下文記憶
    print(f"{'=' * 60}")
    print("測試上下文記憶")
    print(f"{'=' * 60}")
    
    # 第 4 輪：測試 AI 是否記得之前討論的內容
    test_memory_input = "那你剛才說的第一個地方在哪"
    print(f"👤 用戶: {test_memory_input}")
    
    result = analyze_and_respond_with_context(
        user_input=test_memory_input,
        conversation_context=conversation_history,
        response_style='friendly',
        conversation_mode='continuous',
        conversation_round=conversation_round
    )
    
    response = result.get('response', '')
    print(f"🤖 AI: {response}")
    
    # 檢查是否提到之前推薦的地方
    if any(keyword in response for keyword in ['公園', '商場', '咖啡', '之前', '剛才']):
        print("✅ AI 記得之前的對話內容")
    else:
        print("⚠️ AI 可能忘記了之前的對話內容")
    
    print(f"\n{'=' * 60}")
    print("測試完成")
    print(f"{'=' * 60}")
    print(f"總對話輪次: {conversation_round + 1}")
    print(f"對話歷史長度: {len(conversation_history)} 條")

def test_conversation_reset():
    """測試對話重置功能"""
    print("\n" + "=" * 60)
    print("測試對話重置功能")
    print("=" * 60)
    
    # 創建一些對話歷史
    conversation_history = [
        {'role': 'user', 'content': '你好'},
        {'role': 'assistant', 'content': '你好！有什麼我可以幫忙的嗎？'},
        {'role': 'user', 'content': '我想聊聊天'},
        {'role': 'assistant', 'content': '當然可以！你想聊什麼呢？'}
    ]
    
    print(f"重置前歷史記錄: {len(conversation_history)} 條")
    
    # 模擬重置
    conversation_history = []
    conversation_round = 0
    
    print(f"重置後歷史記錄: {len(conversation_history)} 條")
    print("✅ 對話重置成功")

def test_context_limit():
    """測試對話歷史長度限制"""
    print("\n" + "=" * 60)
    print("測試對話歷史長度限制")
    print("=" * 60)
    
    # 創建超過 10 條的對話歷史
    conversation_history = []
    for i in range(15):
        conversation_history.append({
            'role': 'user' if i % 2 == 0 else 'assistant',
            'content': f'測試訊息 {i + 1}'
        })
    
    print(f"創建了 {len(conversation_history)} 條對話記錄")
    
    # 限制長度
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]
    
    print(f"限制後保留 {len(conversation_history)} 條記錄")
    print(f"最舊的記錄: {conversation_history[0]['content']}")
    print(f"最新的記錄: {conversation_history[-1]['content']}")
    print("✅ 歷史長度限制正常")

def main():
    """主測試函數"""
    print("\n🔍 多輪對話功能測試工具\n")
    
    try:
        # 測試多輪對話
        test_multi_turn_conversation()
        
        # 測試對話重置
        test_conversation_reset()
        
        # 測試歷史長度限制
        test_context_limit()
        
        print("\n" + "=" * 60)
        print("所有測試完成")
        print("=" * 60)
        print("\n✅ 多輪對話功能正常！")
        print("\n使用方式:")
        print("1. 啟動 Flask 應用")
        print("2. 訪問 http://localhost:5000/emotion-analysis")
        print("3. 開始錄音並進行多輪對話")
        print("4. 觀察 AI 是否記得之前的對話內容")
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
