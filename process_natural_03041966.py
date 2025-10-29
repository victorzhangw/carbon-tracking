#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
專門處理 03041966.m4a 檔案的自然人聲分離腳本
保持語音自然度，避免音調變高和不連續問題
"""

import os
import sys
from natural_voice_separation import NaturalVoiceSeparator

def main():
    input_file = r"D:\python\Flask-AICares\TTS\03041966.m4a"
    
    print("🎵 自然音頻人聲分離工具")
    print("=" * 60)
    print("🌟 專門解決的問題:")
    print("  • 避免人聲音調變高")
    print("  • 保持語音連續性")
    print("  • 溫和的噪音處理")
    print("  • 保持自然語音特性")
    print("=" * 60)
    print(f"處理檔案: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"❌ 檔案不存在: {input_file}")
        print("請確認檔案路徑是否正確")
        return False
    
    try:
        # 創建自然處理器
        separator = NaturalVoiceSeparator(input_file)
        
        # 處理音頻，優先保持自然度
        success = separator.process_audio(n_speakers=2)
        
        if success:
            print("\n🎉 自然處理完成！")
            print(f"📁 輸出目錄: {separator.output_dir}")
            print("\n📋 檔案說明:")
            print("  🎯 03_naturally_enhanced.wav - 整體自然增強版（推薦）")
            print("  🎯 04_speaker_1_natural.wav - 說話者1自然版")
            print("  🎯 04_speaker_2_natural.wav - 說話者2自然版")
            print("  🔧 02_gentle_noise_reduced.wav - 溫和去噪版")
            print("  📄 01_original.wav - 原始檔案")
            
            print("\n💡 特點:")
            print("  • 保持原始音調，不會變高")
            print("  • 語音連續流暢，無突兀切斷")
            print("  • 溫和去除鈴聲，保護語音")
            print("  • 自然的語音增強效果")
            
            print("\n🎯 建議優先試聽: 03_naturally_enhanced.wav")
            
            return True
        else:
            print("\n❌ 處理失敗")
            return False
            
    except ImportError as e:
        print(f"\n❌ 缺少必要的套件: {e}")
        print("\n請確認已安裝所需套件")
        return False
        
    except Exception as e:
        print(f"\n❌ 處理過程中發生錯誤: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)