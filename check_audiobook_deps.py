#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 廣播劇系統 - 依賴套件檢查工具
檢查所有必要和可選的依賴套件是否已安裝
"""

import sys
import subprocess

def check_package(package_name, import_name=None, version_check=None):
    """
    檢查套件是否已安裝
    
    Args:
        package_name: 套件名稱（用於顯示）
        import_name: 導入名稱（如果與套件名不同）
        version_check: 版本檢查函數
    
    Returns:
        bool: 是否已安裝
    """
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        
        # 檢查版本
        if version_check and version != 'unknown':
            if not version_check(version):
                print(f"⚠️  {package_name} - 已安裝但版本過舊 (v{version})")
                return False
        
        print(f"✅ {package_name} - 已安裝 (v{version})")
        return True
    except ImportError:
        print(f"❌ {package_name} - 未安裝")
        return False
    except Exception as e:
        print(f"⚠️  {package_name} - 檢查時發生錯誤: {e}")
        return False

def check_system_command(command, name):
    """
    檢查系統命令是否可用
    
    Args:
        command: 命令名稱
        name: 顯示名稱
    
    Returns:
        bool: 是否可用
    """
    try:
        result = subprocess.run(
            [command, '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # 嘗試提取版本號
            version_line = result.stdout.split('\n')[0] if result.stdout else result.stderr.split('\n')[0]
            print(f"✅ {name} - 已安裝 ({version_line[:50]}...)")
            return True
        else:
            print(f"❌ {name} - 未安裝或無法執行")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print(f"❌ {name} - 未安裝")
        return False
    except Exception as e:
        print(f"⚠️  {name} - 檢查時發生錯誤: {e}")
        return False

def print_section(title):
    """打印區段標題"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)

def print_summary(required_ok, optional_count, system_ok):
    """打印總結"""
    print_section("檢查總結")
    
    if required_ok:
        print("✅ 基礎功能可用")
        print("   - EPUB 解析功能正常")
        print("   - 文字處理功能正常")
        print("   - 可以開始使用基礎版本")
    else:
        print("❌ 基礎功能不可用")
        print("   - 缺少必要套件")
        print("   - 請先安裝必要套件")
    
    print(f"\n可選功能: {optional_count}/3 可用")
    
    if optional_count == 3:
        print("   ✅ 所有進階功能可用")
    elif optional_count > 0:
        print("   ⚠️  部分進階功能可用")
    else:
        print("   ❌ 進階功能不可用")
    
    if system_ok:
        print("\n✅ 系統級依賴正常")
    else:
        print("\n⚠️  系統級依賴未完整安裝")

def print_installation_guide(missing_required, missing_optional, missing_system):
    """打印安裝指南"""
    print_section("安裝指南")
    
    if missing_required:
        print("\n【必要套件安裝】")
        print(f"pip install {' '.join(missing_required)}")
    
    if missing_optional:
        print("\n【可選套件安裝】")
        print(f"pip install {' '.join(missing_optional)}")
    
    if missing_system:
        print("\n【系統級依賴安裝】")
        if sys.platform == 'win32':
            print("Windows:")
            print("  1. 下載 FFmpeg: https://ffmpeg.org/download.html")
            print("  2. 解壓到 C:\\ffmpeg")
            print("  3. 添加到系統 PATH: C:\\ffmpeg\\bin")
        elif sys.platform == 'darwin':
            print("macOS:")
            print("  brew install ffmpeg")
        else:
            print("Linux:")
            print("  sudo apt-get install ffmpeg")
    
    if not missing_required and not missing_optional and not missing_system:
        print("\n🎉 所有依賴已安裝完成！")
        print("   可以開始使用 AI 廣播劇系統")

def main():
    """主函數"""
    print_section("AI 廣播劇系統 - 依賴套件檢查")
    print(f"Python 版本: {sys.version}")
    print(f"平台: {sys.platform}")
    
    # 檢查必要套件
    print_section("必要套件檢查")
    required_packages = [
        ('ebooklib', 'ebooklib'),
        ('beautifulsoup4', 'bs4'),
        ('lxml', 'lxml'),
    ]
    
    missing_required = []
    required_results = []
    
    for pkg_name, import_name in required_packages:
        result = check_package(pkg_name, import_name)
        required_results.append(result)
        if not result:
            missing_required.append(pkg_name)
    
    required_ok = all(required_results)
    
    # 檢查可選套件
    print_section("可選套件檢查")
    optional_packages = [
        ('dashscope', 'dashscope', 'Qwen TTS API 支援'),
        ('pydub', 'pydub', '音頻合併功能'),
        ('requests', 'requests', 'HTTP 請求功能'),
    ]
    
    missing_optional = []
    optional_count = 0
    
    for pkg_name, import_name, description in optional_packages:
        result = check_package(pkg_name, import_name)
        if result:
            optional_count += 1
            print(f"   → {description}")
        else:
            missing_optional.append(pkg_name)
    
    # 檢查系統級依賴
    print_section("系統級依賴檢查")
    system_commands = [
        ('ffmpeg', 'FFmpeg (音頻處理)'),
    ]
    
    missing_system = []
    system_results = []
    
    for cmd, name in system_commands:
        result = check_system_command(cmd, name)
        system_results.append(result)
        if not result:
            missing_system.append(cmd)
    
    system_ok = all(system_results)
    
    # 檢查 Flask 相關套件
    print_section("Flask 相關套件檢查")
    flask_packages = [
        ('Flask', 'flask'),
        ('Flask-CORS', 'flask_cors'),
        ('Werkzeug', 'werkzeug'),
    ]
    
    for pkg_name, import_name in flask_packages:
        check_package(pkg_name, import_name)
    
    # 打印總結
    print_summary(required_ok, optional_count, system_ok)
    
    # 打印安裝指南
    if missing_required or missing_optional or missing_system:
        print_installation_guide(missing_required, missing_optional, missing_system)
    
    # 打印額外資訊
    print_section("額外資訊")
    print("📚 完整文檔: docs/AI廣播劇系統文檔.md")
    print("🔧 安裝指南: docs/AI廣播劇系統-安裝指南.md")
    print("🌐 API 文檔: docs/API端點總覽.md")
    
    print("\n" + "=" * 60)
    
    # 返回狀態碼
    if required_ok:
        return 0
    else:
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n檢查已中斷")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 檢查過程發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
