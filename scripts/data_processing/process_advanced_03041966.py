#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
專門處理 03041966.m4a 檔案的進階人聲分離腳本
保持語音清晰度並分離不同說話者
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import os
import sys
from advanced_voice_separation import AdvancedVoiceSeparator

def main():
    # 指定的音頻檔案路徑
    input_file = r"D:\python\Flask-AICares\TTS\03041966.m4a"
    
    print("🎵 進階音頻人聲分離工具")
    print("=" * 60)
    print("✨ 特色功能:")
    print("  • 保持人聲清晰度，避免模糊")
    print("  • 智能分離不同說話者")
    print("  • 溫和的噪音去除")
    print("  • 語音增強處理")
    print("=" * 60)
    print(f"處理檔案: {input_file}")
    
    # 檢查檔案是否存在
    if not os.path.exists(input_file):
        print(f"❌ 檔案不存在: {input_file}")
        print("請確認檔案路徑是否正確")
        return False
    
    try:
        # 創建進階處理器
        separator = AdvancedVoiceSeparator(input_file)
        
        # 處理音頻，分離2個說話者
        success = separator.process_audio(n_speakers=2)
        
        if success:
            print("\n🎉 處理完成！")
            print(f"📁 輸出目錄: {separator.output_dir}")
            print("\n📋 檔案說明:")
            print("  🎯 04_speaker_1_enhanced.wav - 說話者1（清晰版）")
            print("  🎯 04_speaker_2_enhanced.wav - 說話者2（清晰版）")
            print("  🎯 05_all_speakers_enhanced.wav - 整體增強版")
            print("  📊 03_speaker_X_raw.wav - 原始分離版本")
            print("  🔧 02_noise_reduced.wav - 去噪版本")
            print("  📄 01_original.wav - 原始檔案")
            
            print("\n💡 使用建議:")
            print("  • 如需單獨的說話者音頻，使用 04_speaker_X_enhanced.wav")
            print("  • 如需整體對話，使用 05_all_speakers_enhanced.wav")
            print("  • 所有檔案都保持了語音的自然清晰度")
            
            return True
        else:
            print("\n❌ 處理失敗")
            return False
            
    except ImportError as e:
        print(f"\n❌ 缺少必要的套件: {e}")
        print("\n請先安裝所需套件:")
        print("pip install scikit-learn")
        print("pip install matplotlib")
        print("pip install -r requirements_audio_separation.txt")
        return False
        
    except Exception as e:
        print(f"\n❌ 處理過程中發生錯誤: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)