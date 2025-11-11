"""
測試 ASR API 端點
需要先啟動 Flask 應用: python app.py
"""

import requests
import json
import os
import sys

# Add parent directory to path to import from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def test_health_check():
    """測試健康檢查端點（無需認證）"""
    print("=" * 60)
    print("測試 1: 健康檢查")
    print("=" * 60)
    
    url = "http://localhost:5000/api/asr/health"
    
    try:
        response = requests.get(url)
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"錯誤: {e}")
        print()
        return False


def test_login():
    """登入獲取 Token"""
    print("=" * 60)
    print("測試 2: 用戶登入")
    print("=" * 60)
    
    url = "http://localhost:5000/api/auth/login"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            print(f"✓ 登入成功")
            print(f"Token: {token[:50]}...")
            print()
            return token
        else:
            print(f"登入失敗: {response.json()}")
            print()
            return None
    except Exception as e:
        print(f"錯誤: {e}")
        print()
        return None


def test_recognize_audio(token):
    """測試單個音頻識別"""
    print("=" * 60)
    print("測試 3: 單個音頻識別")
    print("=" * 60)
    
    url = "http://localhost:5000/api/asr/recognize"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 查找測試音頻
    test_audio_paths = [
        "TTS/vc.wav",
        "mockvoice/vc.wav"
    ]
    
    test_audio = None
    for path in test_audio_paths:
        if os.path.exists(path):
            test_audio = path
            break
    
    if not test_audio:
        print("未找到測試音頻文件")
        print()
        return False
    
    print(f"使用測試音頻: {test_audio}")
    
    try:
        with open(test_audio, 'rb') as f:
            files = {'file': f}
            data = {
                'language_hint': 'zh',
                'return_details': 'true'
            }
            
            response = requests.post(url, headers=headers, files=files, data=data)
        
        print(f"狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 識別成功")
            print(f"文本: {result.get('text', '')}")
            print(f"置信度: {result.get('confidence', 0):.3f}")
            print(f"處理時間: {result.get('processing_time', 0):.3f}秒")
            print()
            return True
        else:
            print(f"識別失敗: {response.json()}")
            print()
            return False
            
    except Exception as e:
        print(f"錯誤: {e}")
        print()
        return False


def test_get_status(token):
    """測試獲取系統狀態"""
    print("=" * 60)
    print("測試 4: 獲取系統狀態")
    print("=" * 60)
    
    url = "http://localhost:5000/api/asr/status"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"系統狀態: {result.get('status')}")
            print(f"系統信息:")
            print(json.dumps(result.get('system_info', {}), indent=2, ensure_ascii=False))
            print()
            return True
        else:
            print(f"獲取狀態失敗: {response.json()}")
            print()
            return False
            
    except Exception as e:
        print(f"錯誤: {e}")
        print()
        return False


def main():
    """主測試函數"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 20 + "ASR API 測試" + " " * 26 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    print("請確保 Flask 應用正在運行: python app.py")
    print()
    
    results = []
    
    # 測試 1: 健康檢查
    results.append(("健康檢查", test_health_check()))
    
    # 測試 2: 登入
    token = test_login()
    if not token:
        print("❌ 無法獲取 Token，後續測試將跳過")
        return
    
    results.append(("用戶登入", True))
    
    # 測試 3: 單個音頻識別
    results.append(("單個音頻識別", test_recognize_audio(token)))
    
    # 測試 4: 獲取系統狀態
    results.append(("獲取系統狀態", test_get_status(token)))
    
    # 總結
    print("=" * 60)
    print("測試總結")
    print("=" * 60)
    print()
    
    for test_name, success in results:
        status = "✓ 通過" if success else "✗ 失敗"
        print(f"  {test_name}: {status}")
    
    print()
    total = len(results)
    passed = sum(1 for _, s in results if s)
    print(f"總計: {passed}/{total} 通過")
    print()


if __name__ == "__main__":
    main()
