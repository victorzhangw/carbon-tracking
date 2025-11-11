"""
檢查音頻文件和語音模型的腳本
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import os
import sqlite3
from database import get_all_voice_models, get_voice_model_by_staff
from config import DATABASE

def check_audio_files():
    """檢查音頻文件和語音模型"""
    print("🔍 檢查音頻文件和語音模型...")
    print("=" * 60)
    
    # 1. 檢查目錄結構
    directories = [
        './audio_uploads',
        './genvoice', 
        './voice_output',
        './mockvoice',
        './temp'
    ]
    
    print("📁 檢查目錄結構:")
    for directory in directories:
        if os.path.exists(directory):
            files = os.listdir(directory)
            print(f"  ✅ {directory}: {len(files)} 個文件")
            for file in files[:3]:  # 只顯示前3個文件
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    print(f"     - {file} ({size} bytes)")
        else:
            print(f"  ❌ {directory}: 目錄不存在")
    
    # 2. 檢查數據庫中的語音模型
    print(f"\n🗄️ 檢查數據庫中的語音模型:")
    try:
        all_models = get_all_voice_models()
        print(f"  📊 總共 {len(all_models)} 個語音模型")
        
        for i, model in enumerate(all_models):
            print(f"\n  📋 模型 {i+1}:")
            print(f"     客服代號: {model.get('staff_code', 'Unknown')}")
            print(f"     狀態: {model.get('model_status', 'Unknown')}")
            print(f"     原始音頻: {model.get('original_audio_path', 'Unknown')}")
            print(f"     處理音頻: {model.get('processed_audio_path', 'Unknown')}")
            print(f"     參考文字: {model.get('reference_text', 'Unknown')[:50]}...")
            
            # 檢查音頻文件是否存在
            original_path = model.get('original_audio_path', '')
            processed_path = model.get('processed_audio_path', '')
            
            if original_path and os.path.exists(original_path):
                size = os.path.getsize(original_path)
                print(f"     ✅ 原始音頻存在 ({size} bytes)")
            else:
                print(f"     ❌ 原始音頻不存在: {original_path}")
            
            if processed_path and os.path.exists(processed_path):
                size = os.path.getsize(processed_path)
                print(f"     ✅ 處理音頻存在 ({size} bytes)")
            else:
                print(f"     ❌ 處理音頻不存在: {processed_path}")
                
    except Exception as e:
        print(f"  ❌ 數據庫錯誤: {e}")
    
    # 3. 檢查genvoice目錄中的生成文件
    print(f"\n🎵 檢查genvoice目錄:")
    genvoice_dir = './genvoice'
    if os.path.exists(genvoice_dir):
        wav_files = [f for f in os.listdir(genvoice_dir) if f.endswith('.wav')]
        print(f"  📊 WAV文件數量: {len(wav_files)}")
        
        for wav_file in wav_files:
            file_path = os.path.join(genvoice_dir, wav_file)
            size = os.path.getsize(file_path)
            print(f"     - {wav_file} ({size} bytes)")
            
            # 檢查文件是否可讀
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(12)
                    if header.startswith(b'RIFF') and b'WAVE' in header:
                        print(f"       ✅ 有效的WAV文件")
                    else:
                        print(f"       ❌ 無效的WAV文件格式")
            except Exception as e:
                print(f"       ❌ 無法讀取文件: {e}")
    else:
        print(f"  ❌ genvoice目錄不存在")
    
    # 4. 測試特定客服代號
    print(f"\n🧪 測試特定客服代號:")
    test_codes = ['admin', 'CS001', 'test']
    
    for code in test_codes:
        model = get_voice_model_by_staff(code)
        if model:
            print(f"  ✅ {code}: 找到語音模型")
            print(f"     狀態: {model.get('model_status')}")
            print(f"     音頻路徑: {model.get('processed_audio_path')}")
        else:
            print(f"  ❌ {code}: 未找到語音模型")

def check_wav_file_validity(file_path):
    """檢查WAV文件的有效性"""
    try:
        with open(file_path, 'rb') as f:
            # 讀取WAV文件頭
            header = f.read(44)  # WAV文件頭通常是44字節
            
            if len(header) < 44:
                return False, "文件太小，不是有效的WAV文件"
            
            # 檢查RIFF標識
            if not header.startswith(b'RIFF'):
                return False, "缺少RIFF標識"
            
            # 檢查WAVE標識
            if b'WAVE' not in header[:12]:
                return False, "缺少WAVE標識"
            
            # 檢查fmt chunk
            if b'fmt ' not in header[:20]:
                return False, "缺少fmt chunk"
            
            return True, "有效的WAV文件"
            
    except Exception as e:
        return False, f"讀取錯誤: {e}"

if __name__ == "__main__":
    check_audio_files()
    
    print(f"\n🔧 修復建議:")
    print(f"1. 確保上傳的WAV文件保存到正確位置")
    print(f"2. 檢查語音模型是否正確保存到數據庫")
    print(f"3. 確保genvoice目錄存在且可寫")
    print(f"4. 檢查生成的音頻文件是否有效")
    print(f"5. 確保Flask路由能正確提供音頻文件")