"""
調試語音模型數據庫的腳本
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import sqlite3
from database import get_all_voice_models, get_voice_model_by_staff, save_voice_model_info
from config import DATABASE

def debug_voice_models():
    """調試語音模型數據庫"""
    print("🔍 調試語音模型數據庫...")
    print("=" * 50)
    
    # 1. 檢查數據庫連接
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 檢查voice_models表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='voice_models'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ voice_models表存在")
            
            # 查看表結構
            cursor.execute("PRAGMA table_info(voice_models)")
            columns = cursor.fetchall()
            print(f"📋 表結構: {[col[1] for col in columns]}")
            
            # 查看所有記錄
            cursor.execute("SELECT * FROM voice_models")
            records = cursor.fetchall()
            print(f"📊 記錄數量: {len(records)}")
            
            if records:
                print("\n🗂️ 現有記錄:")
                for i, record in enumerate(records):
                    print(f"  {i+1}. ID: {record[0]}, 客服代號: {record[1]}, 狀態: {record[5]}")
            else:
                print("⚠️ 沒有找到任何語音模型記錄")
                
        else:
            print("❌ voice_models表不存在")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ 數據庫錯誤: {e}")
    
    # 2. 測試API函數
    print("\n🧪 測試API函數...")
    
    try:
        all_models = get_all_voice_models()
        print(f"📋 get_all_voice_models() 返回: {len(all_models)} 個模型")
        
        if all_models:
            for model in all_models:
                print(f"  - {model.get('staff_code', 'Unknown')}: {model.get('model_status', 'Unknown')}")
        
        # 測試特定客服代號
        test_codes = ['admin', 'CS001', 'test']
        for code in test_codes:
            model = get_voice_model_by_staff(code)
            if model:
                print(f"✅ 找到 {code} 的語音模型")
            else:
                print(f"❌ 未找到 {code} 的語音模型")
                
    except Exception as e:
        print(f"❌ API測試錯誤: {e}")
    
    # 3. 創建測試模型
    print("\n🛠️ 創建測試語音模型...")
    
    try:
        test_model_id = save_voice_model_info(
            staff_code="admin",
            original_audio_path="./test/admin_original.wav",
            processed_audio_path="./test/admin_processed.wav",
            reference_text="這是管理員的測試語音模型",
            model_status="ready"
        )
        
        if test_model_id:
            print(f"✅ 成功創建測試模型，ID: {test_model_id}")
            
            # 驗證創建結果
            admin_model = get_voice_model_by_staff("admin")
            if admin_model:
                print(f"✅ 驗證成功，admin模型已創建")
                print(f"   狀態: {admin_model.get('model_status')}")
                print(f"   參考文字: {admin_model.get('reference_text')}")
            else:
                print(f"❌ 驗證失敗，無法找到admin模型")
        else:
            print(f"❌ 創建測試模型失敗")
            
    except Exception as e:
        print(f"❌ 創建測試模型錯誤: {e}")

if __name__ == "__main__":
    debug_voice_models()