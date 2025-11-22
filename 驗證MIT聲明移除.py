#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驗證 MIT 聲明是否已成功移除
"""

import os
import sys

def check_file_modification(filepath, search_text, should_be_commented=False):
    """檢查文件是否已修改"""
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if should_be_commented:
        # 檢查是否被註釋
        lines = content.split('\n')
        found_commented = False
        for i, line in enumerate(lines):
            if search_text in line and line.strip().startswith('#'):
                found_commented = True
                break
        
        if found_commented:
            print(f"✅ {filepath}: 聲明已被註釋")
            return True
        else:
            print(f"❌ {filepath}: 聲明未被註釋")
            return False
    else:
        # 檢查是否不包含搜尋文本
        if search_text not in content:
            print(f"✅ {filepath}: 不包含搜尋文本")
            return True
        else:
            print(f"❌ {filepath}: 仍包含搜尋文本")
            return False

def check_backup_exists(filepath):
    """檢查備份文件是否存在"""
    backup_path = filepath + '.backup'
    if os.path.exists(backup_path):
        print(f"✅ 備份存在: {backup_path}")
        return True
    else:
        print(f"❌ 備份不存在: {backup_path}")
        return False

def main():
    print("=" * 60)
    print("🔍 驗證 MIT 聲明移除")
    print("=" * 60)
    print()
    
    results = {}
    
    # 檢查 webui.py
    print("📄 檢查 webui.py...")
    webui_path = "GPT-SoVITS-v2pro-20250604/webui.py"
    results['webui.py 修改'] = check_file_modification(
        webui_path, 
        "本软件以MIT协议开源",
        should_be_commented=True
    )
    results['webui.py 備份'] = check_backup_exists(webui_path)
    print()
    
    # 檢查 assets.py
    print("📄 檢查 assets.py...")
    assets_path = "GPT-SoVITS-v2pro-20250604/tools/assets.py"
    
    # 檢查是否簡化了 top_html
    with open(assets_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'GitHub-GPT--SoVITS' not in content:
        print(f"✅ {assets_path}: top_html 已簡化")
        results['assets.py 修改'] = True
    else:
        print(f"❌ {assets_path}: top_html 未簡化")
        results['assets.py 修改'] = False
    
    results['assets.py 備份'] = check_backup_exists(assets_path)
    print()
    
    # 檢查 Python 緩存
    print("📄 檢查 Python 緩存...")
    cache_dirs = [
        "GPT-SoVITS-v2pro-20250604/__pycache__",
        "GPT-SoVITS-v2pro-20250604/tools/__pycache__"
    ]
    
    cache_exists = False
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            cache_exists = True
            print(f"⚠️ 緩存目錄存在: {cache_dir}")
    
    if not cache_exists:
        print("✅ 沒有 Python 緩存")
        results['緩存清理'] = True
    else:
        print("❌ 存在 Python 緩存，建議清理")
        results['緩存清理'] = False
    print()
    
    # 總結
    print("=" * 60)
    print("📊 檢查結果總結")
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
        print("   1. 執行: 清理並重啟GPT-SoVITS.bat")
        print("   2. 或手動執行:")
        print("      - 停止現有的 GPT-SoVITS 進程")
        print("      - 刪除 __pycache__ 目錄")
        print("      - 重新啟動 go-webui.bat")
        print("   3. 訪問: http://localhost:9874")
        print("   4. 檢查頂部是否還有 MIT 聲明")
        return 0
    else:
        print("❌ 部分檢查失敗")
        print()
        print("💡 建議:")
        if not results.get('緩存清理', True):
            print("   - 執行: 清理並重啟GPT-SoVITS.bat")
        if not results.get('webui.py 修改', True):
            print("   - 重新修改 webui.py")
        if not results.get('assets.py 修改', True):
            print("   - 重新修改 assets.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
