"""
自動替換 Emoji 為 Material Icons 的腳本
"""

import os
import re

# Emoji 到 Material Icon 的映射
EMOJI_TO_ICON = {
    # 語音相關
    '🎤': '<span class="material-icons">mic</span>',
    '🎙️': '<span class="material-icons">record_voice_over</span>',
    '🗣️': '<span class="material-icons">hearing</span>',
    '🎵': '<span class="material-icons">music_note</span>',
    '🔊': '<span class="material-icons">volume_up</span>',
    
    # 數據分析
    '📊': '<span class="material-icons">bar_chart</span>',
    '📈': '<span class="material-icons">trending_up</span>',
    '📉': '<span class="material-icons">trending_down</span>',
    
    # 情緒（保留 emoji 或替換為 icon）
    '😊': '<span class="material-icons">sentiment_satisfied</span>',
    '😢': '<span class="material-icons">sentiment_dissatisfied</span>',
    '😠': '<span class="material-icons">sentiment_very_dissatisfied</span>',
    '😐': '<span class="material-icons">sentiment_neutral</span>',
    '😨': '<span class="material-icons">sentiment_stressed</span>',
    '😲': '<span class="material-icons">sentiment_excited</span>',
    
    # 用戶
    '👤': '<span class="material-icons">person</span>',
    '👨‍💼': '<span class="material-icons">admin_panel_settings</span>',
    '👥': '<span class="material-icons">group</span>',
    '🤖': '<span class="material-icons">smart_toy</span>',
    
    # 操作
    '📝': '<span class="material-icons">edit_note</span>',
    '💬': '<span class="material-icons">chat</span>',
    '⏱️': '<span class="material-icons">schedule</span>',
    '🏁': '<span class="material-icons">flag</span>',
    '🎯': '<span class="material-icons">gps_fixed</span>',
    '⏹️': '<span class="material-icons">stop</span>',
    '▶️': '<span class="material-icons">play_arrow</span>',
    '⏸️': '<span class="material-icons">pause</span>',
    
    # 文件
    '📁': '<span class="material-icons">folder</span>',
    '📄': '<span class="material-icons">description</span>',
    '📚': '<span class="material-icons">library_books</span>',
    
    # 其他
    '💡': '<span class="material-icons">lightbulb</span>',
    '⭐': '<span class="material-icons">star</span>',
    '🔬': '<span class="material-icons">science</span>',
    '✅': '<span class="material-icons">check_circle</span>',
    '❌': '<span class="material-icons">cancel</span>',
    '⚠️': '<span class="material-icons">warning</span>',
    'ℹ️': '<span class="material-icons">info</span>',
    '🔄': '<span class="material-icons">refresh</span>',
    '🔍': '<span class="material-icons">search</span>',
    '⚙️': '<span class="material-icons">settings</span>',
    '🗑️': '<span class="material-icons">delete</span>',
    '✏️': '<span class="material-icons">edit</span>',
    '💾': '<span class="material-icons">save</span>',
    '📤': '<span class="material-icons">upload</span>',
    '📥': '<span class="material-icons">download</span>',
    '🌍': '<span class="material-icons">public</span>',
    '☁️': '<span class="material-icons">cloud</span>',
    '🌤️': '<span class="material-icons">wb_sunny</span>',
    '🌆': '<span class="material-icons">location_city</span>',
    '🌙': '<span class="material-icons">nightlight</span>',
    '🌅': '<span class="material-icons">wb_twilight</span>',
    '☀️': '<span class="material-icons">wb_sunny</span>',
}

def replace_emojis_in_file(file_path, dry_run=True):
    """替換文件中的 emoji"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements = []
        
        # 替換所有 emoji
        for emoji, icon_html in EMOJI_TO_ICON.items():
            if emoji in content:
                count = content.count(emoji)
                content = content.replace(emoji, icon_html)
                replacements.append((emoji, icon_html, count))
        
        if replacements:
            print(f"\n📄 {file_path}")
            print(f"   找到 {len(replacements)} 種 emoji:")
            for emoji, icon, count in replacements:
                print(f"   - {emoji} → {icon[:50]}... (x{count})")
            
            if not dry_run:
                # 備份原文件
                backup_path = file_path + '.emoji_backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 寫入新內容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ 已替換並備份到 {backup_path}")
            else:
                print(f"   ℹ️ 預覽模式，未實際修改")
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ 處理 {file_path} 時發生錯誤: {e}")
        return False

def add_material_icons_link(file_path, dry_run=True):
    """在 HTML 文件中添加 Material Icons CSS 連結"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已經有 Material Icons
        if 'material-icons.css' in content or 'Material Icons' in content:
            return False
        
        # 在 </head> 之前添加
        material_icons_link = '''    <!-- Material Icons -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/material-icons.css') }}">
  </head>'''
        
        if '</head>' in content:
            content = content.replace('  </head>', material_icons_link)
            
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ 已添加 Material Icons CSS 連結")
            else:
                print(f"   ℹ️ 需要添加 Material Icons CSS 連結")
            
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ 添加 CSS 連結時發生錯誤: {e}")
        return False

def process_templates(dry_run=True, files=None):
    """處理所有模板文件"""
    templates_dir = 'templates'
    
    if files is None:
        # 處理所有 HTML 文件
        files = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
    
    print("=" * 60)
    print(f"{'預覽' if dry_run else '執行'} Emoji 替換")
    print("=" * 60)
    
    processed_files = []
    
    for filename in files:
        file_path = os.path.join(templates_dir, filename)
        
        # 添加 Material Icons CSS
        add_material_icons_link(file_path, dry_run)
        
        # 替換 emoji
        if replace_emojis_in_file(file_path, dry_run):
            processed_files.append(filename)
    
    print("\n" + "=" * 60)
    print("總結")
    print("=" * 60)
    print(f"處理了 {len(processed_files)} 個文件:")
    for filename in processed_files:
        print(f"  - {filename}")
    
    if dry_run:
        print("\n⚠️ 這是預覽模式，未實際修改文件")
        print("要執行實際替換，請運行:")
        print("  python replace_emojis_with_icons.py --execute")
    else:
        print("\n✅ 替換完成！")
        print("原文件已備份為 .emoji_backup")

def main():
    """主函數"""
    import sys
    
    # 檢查命令行參數
    dry_run = '--execute' not in sys.argv
    
    # 優先處理的文件
    priority_files = [
        'portal.html',
        'emotion_analysis.html',
        'voice_testing_hub.html',
        'score_report_modal_v2.html',
        'asr_test.html',
    ]
    
    if '--all' in sys.argv:
        # 處理所有文件
        process_templates(dry_run=dry_run)
    elif '--priority' in sys.argv:
        # 只處理優先文件
        process_templates(dry_run=dry_run, files=priority_files)
    else:
        # 預覽模式
        print("\n🔍 Emoji 替換工具\n")
        print("使用方式:")
        print("  python replace_emojis_with_icons.py              # 預覽所有文件")
        print("  python replace_emojis_with_icons.py --priority   # 預覽優先文件")
        print("  python replace_emojis_with_icons.py --execute    # 執行替換（所有文件）")
        print("  python replace_emojis_with_icons.py --priority --execute  # 執行替換（優先文件）")
        print()
        
        process_templates(dry_run=True, files=priority_files)

if __name__ == "__main__":
    main()
