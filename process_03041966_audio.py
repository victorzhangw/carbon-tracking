#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
專門處理 03041966.m4a 檔案的人聲分離腳本
"""

import os
import sys
from audio_voice_separation import VoiceSeparator

def main():
    # 指定的音頻檔案路徑
    input_file = r"D:\python\Flask-AICares\TTS\03041966.m4a"
    
    print("🎵 音頻人聲分離工具")
    print("=" * 50)
    print(f"處理檔案: {input_file}")
    
    # 檢查檔案是否存在
    if not os.path.exists(input_file):
        print(f"❌ 檔案不存在: {input_file}")
        print("請確認檔案路徑是否正確")
        return False
    
    try:
        # 創建處理器
        separator = VoiceSeparator(input_file)
        
        # 處理音頻
        success = separator.process_audio()
        
        if success:
            print("\n🎉 處理完成！")
            print(f"輸出目錄: {separator.output_dir}")
            print("\n📁 生成的檔案說明:")
            print("  • 05_vocals_final_enhanced.wav - 最終人聲（推薦使用）")
            print("  • 03_vocals_noise_reduced.wav - 去噪後人聲")
            print("  • 06_background_music.wav - 背景音樂/噪音")
            print("  • 其他檔案為處理過程中的中間結果")
            
            return True
        else:
            print("\n❌ 處理失敗")
            return False
            
    except ImportError as e:
        print(f"\n❌ 缺少必要的套件: {e}")
        print("\n請先安裝所需套件:")
        print("pip install -r requirements_audio_separation.txt")
        return False
        
    except Exception as e:
        print(f"\n❌ 處理過程中發生錯誤: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)