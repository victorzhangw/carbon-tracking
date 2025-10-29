#!/usr/bin/env python3
"""
檢查 Vue 組件中的情緒相關方法
"""

import re

def check_emotion_methods():
    """檢查情緒相關方法是否正確定義"""
    
    file_path = 'webpage/ai-customer-service-frontend/src/components/voice/VoiceInteractionContainer.vue'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔍 檢查情緒相關方法定義")
        print("=" * 50)
        
        # 檢查的方法列表
        methods_to_check = [
            'getEmotionColor',
            'getEmotionLabel', 
            'getEmotionEmoji'
        ]
        
        all_good = True
        
        for method in methods_to_check:
            # 查找方法定義
            pattern = rf'^\s*{method}\s*\('
            matches = re.findall(pattern, content, re.MULTILINE)
            
            print(f"📋 {method}:")
            print(f"   定義次數: {len(matches)}")
            
            if len(matches) == 1:
                print(f"   ✅ 正確 - 只定義一次")
            elif len(matches) == 0:
                print(f"   ❌ 錯誤 - 未找到定義")
                all_good = False
            else:
                print(f"   ❌ 錯誤 - 重複定義 {len(matches)} 次")
                all_good = False
            
            # 查找方法使用
            usage_pattern = rf'{method}\s*\('
            usage_matches = re.findall(usage_pattern, content)
            usage_count = len(usage_matches) - len(matches)  # 扣除定義本身
            print(f"   使用次數: {usage_count}")
            print()
        
        # 檢查模板中的使用
        print("📱 模板中的使用檢查:")
        template_match = re.search(r'<template>(.*?)</template>', content, re.DOTALL)
        if template_match:
            template_content = template_match.group(1)
            
            for method in methods_to_check:
                if method in template_content:
                    print(f"   ✅ {method} 在模板中被使用")
                else:
                    print(f"   ⚠️ {method} 在模板中未被使用")
        
        print("\n" + "=" * 50)
        if all_good:
            print("🎉 所有情緒方法檢查通過！")
            print("✅ 沒有重複定義的問題")
            print("✅ 所有必要的方法都已定義")
        else:
            print("❌ 發現問題，請檢查上述錯誤")
        
        return all_good
        
    except FileNotFoundError:
        print(f"❌ 找不到檔案: {file_path}")
        return False
    except Exception as e:
        print(f"❌ 檢查失敗: {e}")
        return False

if __name__ == "__main__":
    success = check_emotion_methods()
    exit(0 if success else 1)