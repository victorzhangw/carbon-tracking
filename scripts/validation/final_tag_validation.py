#!/usr/bin/env python3
"""
最終的 Tag 組件驗證
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import re

def validate_tag_components():
    """驗證 Tag 組件的使用是否正確"""
    
    file_path = 'webpage/ai-customer-service-frontend/src/components/voice/VoiceInteractionContainer.vue'
    
    # iView Tag 組件支援的顏色值
    valid_tag_colors = [
        'default', 'primary', 'success', 'info', 'warning', 'error',
        'blue', 'green', 'red', 'yellow', 'pink', 'magenta', 'volcano',
        'orange', 'gold', 'lime', 'cyan', 'geekblue', 'purple'
    ]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🏷️ Tag 組件最終驗證")
        print("=" * 50)
        
        # 查找所有 Tag 組件的使用
        tag_pattern = r'<Tag[^>]*>'
        tag_matches = re.findall(tag_pattern, content)
        
        print(f"📋 找到 {len(tag_matches)} 個 Tag 組件:")
        
        issues = []
        
        for i, tag in enumerate(tag_matches, 1):
            print(f"\n{i}. {tag}")
            
            # 檢查是否有 size 屬性
            if 'size=' in tag:
                print("   ❌ 包含不支援的 size 屬性")
                issues.append(f"Tag {i} 包含 size 屬性")
            else:
                print("   ✅ 沒有 size 屬性")
            
            # 檢查顏色屬性
            color_match = re.search(r'color="([^"]*)"', tag)
            if color_match:
                color = color_match.group(1)
                if color in valid_tag_colors:
                    print(f"   ✅ 顏色 '{color}' 有效")
                else:
                    print(f"   ❌ 顏色 '{color}' 無效")
                    issues.append(f"Tag {i} 使用無效顏色 '{color}'")
            
            # 檢查動態顏色綁定
            dynamic_color_match = re.search(r':color="([^"]*)"', tag)
            if dynamic_color_match:
                method = dynamic_color_match.group(1)
                print(f"   ✅ 使用動態顏色綁定: {method}")
        
        print("\n" + "=" * 50)
        
        if not issues:
            print("🎉 所有 Tag 組件都正確配置！")
            print("✅ 沒有 size 屬性")
            print("✅ 所有顏色值都有效")
            print("✅ 不應該再有 Vue 警告")
        else:
            print("❌ 發現以下問題:")
            for issue in issues:
                print(f"   - {issue}")
        
        # 檢查情緒方法的顏色返回值
        print(f"\n📚 情緒顏色方法檢查:")
        
        emotion_colors = re.findall(r'(happy|sad|angry|neutral|fear|surprise|calm|disgust|fearful|surprised|excited|bored|confused|confident|frustrated|relaxed):\s*"([^"]+)"', content)
        
        for emotion, color in emotion_colors:
            if color in valid_tag_colors:
                print(f"   ✅ {emotion}: {color}")
            else:
                print(f"   ❌ {emotion}: {color} (無效)")
                issues.append(f"情緒 {emotion} 使用無效顏色 {color}")
        
        return len(issues) == 0
        
    except FileNotFoundError:
        print(f"❌ 找不到檔案: {file_path}")
        return False
    except Exception as e:
        print(f"❌ 驗證失敗: {e}")
        return False

if __name__ == "__main__":
    success = validate_tag_components()
    print(f"\n{'🎉 驗證通過' if success else '❌ 驗證失敗'}")
    exit(0 if success else 1)