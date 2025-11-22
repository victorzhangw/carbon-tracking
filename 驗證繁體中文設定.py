#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驗證 GPT-SoVITS 繁體中文語言設定
"""

import os
import sys
import json

def check_language_file():
    """檢查繁體中文語言文件是否存在"""
    print("=" * 60)
    print("🔍 檢查繁體中文語言文件")
    print("=" * 60)
    
    zh_tw_path = "GPT-SoVITS-v2pro-20250604/tools/i18n/locale/zh_TW.json"
    
    if not os.path.exists(zh_tw_path):
        print(f"❌ 繁體中文語言文件不存在: {zh_tw_path}")
        return False
    
    print(f"✅ 繁體中文語言文件存在: {zh_tw_path}")
    
    # 檢查文件內容
    try:
        with open(zh_tw_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
        
        count = len(translations)
        print(f"✅ 翻譯條目數量: {count}")
        
        # 顯示一些範例翻譯
        print("\n📝 翻譯範例:")
        sample_keys = [
            "前置数据集获取工具",
            "UVR5人声伴奏分离&去混响去延迟工具",
            "音频切分工具",
            "语音识别",
            "文本标注"
        ]
        
        for key in sample_keys:
            if key in translations:
                print(f"   {key} → {translations[key]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 讀取語言文件失敗: {e}")
        return False

def check_startup_script():
    """檢查啟動腳本的語言設定"""
    print("\n" + "=" * 60)
    print("🔍 檢查啟動腳本語言設定")
    print("=" * 60)
    
    bat_path = "GPT-SoVITS-v2pro-20250604/go-webui.bat"
    backup_path = bat_path + ".backup"
    
    # 檢查備份
    if os.path.exists(backup_path):
        print(f"✅ 備份文件存在: {backup_path}")
    else:
        print(f"⚠️ 備份文件不存在: {backup_path}")
    
    # 檢查當前設定
    if not os.path.exists(bat_path):
        print(f"❌ 啟動腳本不存在: {bat_path}")
        return False
    
    with open(bat_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'webui.py zh_TW' in content:
        print(f"✅ 語言設定: zh_TW (繁體中文)")
        return True
    elif 'webui.py zh_CN' in content:
        print(f"❌ 語言設定: zh_CN (簡體中文) - 需要修改")
        return False
    elif 'webui.py en_US' in content:
        print(f"❌ 語言設定: en_US (英文) - 需要修改")
        return False
    else:
        print(f"⚠️ 無法識別語言設定")
        print(f"   內容: {content}")
        return False

def check_i18n_system():
    """檢查 i18n 系統"""
    print("\n" + "=" * 60)
    print("🔍 檢查 i18n 系統")
    print("=" * 60)
    
    i18n_path = "GPT-SoVITS-v2pro-20250604/tools/i18n/i18n.py"
    
    if not os.path.exists(i18n_path):
        print(f"❌ i18n 系統文件不存在: {i18n_path}")
        return False
    
    print(f"✅ i18n 系統文件存在: {i18n_path}")
    
    # 列出所有可用語言
    locale_dir = "GPT-SoVITS-v2pro-20250604/tools/i18n/locale"
    if os.path.exists(locale_dir):
        languages = [f.replace('.json', '') for f in os.listdir(locale_dir) if f.endswith('.json')]
        print(f"✅ 可用語言數量: {len(languages)}")
        print(f"   語言列表: {', '.join(sorted(languages))}")
        
        if 'zh_TW' in languages:
            print(f"✅ zh_TW 在可用語言列表中")
            return True
        else:
            print(f"❌ zh_TW 不在可用語言列表中")
            return False
    else:
        print(f"❌ locale 目錄不存在: {locale_dir}")
        return False

def main():
    """主函數"""
    print("\n" + "=" * 60)
    print("🚀 GPT-SoVITS 繁體中文設定驗證")
    print("=" * 60)
    print()
    
    results = {
        "繁體中文語言文件": check_language_file(),
        "啟動腳本設定": check_startup_script(),
        "i18n 系統": check_i18n_system()
    }
    
    print("\n" + "=" * 60)
    print("📊 驗證結果總結")
    print("=" * 60)
    
    for check_name, result in results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {check_name}")
    
    passed = sum(results.values())
    total = len(results)
    
    print()
    print(f"總計: {passed}/{total} 檢查通過")
    print()
    
    if passed == total:
        print("🎉 所有檢查通過！")
        print()
        print("💡 下一步:")
        print("   1. 啟動 GPT-SoVITS:")
        print("      cd GPT-SoVITS-v2pro-20250604")
        print("      go-webui.bat")
        print()
        print("   2. 訪問: http://localhost:9874")
        print()
        print("   3. 確認界面文字為繁體中文:")
        print("      - 前置資料集獲取工具")
        print("      - UVR5人聲伴奏分離")
        print("      - 音頻切分工具")
        print("      - 語音識別")
        print()
        return 0
    else:
        print("❌ 部分檢查失敗")
        print()
        print("💡 建議:")
        if not results.get('繁體中文語言文件', True):
            print("   - 檢查 zh_TW.json 文件是否存在")
        if not results.get('啟動腳本設定', True):
            print("   - 修改 go-webui.bat，將 zh_CN 改為 zh_TW")
        if not results.get('i18n 系統', True):
            print("   - 檢查 i18n 系統文件是否完整")
        return 1

if __name__ == "__main__":
    sys.exit(main())
