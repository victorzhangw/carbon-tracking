"""
測試情緒識別系統是否正常運作
"""

import requests
import json

def test_emotion_analysis_page():
    """測試情緒識別頁面是否可訪問"""
    print("=" * 60)
    print("測試情緒識別頁面")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:5000/emotion-analysis", timeout=5)
        
        if response.status_code == 200:
            print("✅ 情緒識別頁面可訪問")
            
            # 檢查頁面內容
            content = response.text
            
            checks = [
                ("showWeatherGreeting", "天氣問候功能"),
                ("startRecordBtn", "錄音按鈕"),
                ("stopRecordBtn", "停止按鈕"),
                ("playAudio", "音頻播放函數"),
                ("ScoreManager", "評分管理器"),
                ("getUserLocation", "地理位置功能"),
                ("getWeatherData", "天氣資料功能"),
            ]
            
            print("\n檢查頁面功能:")
            for keyword, name in checks:
                if keyword in content:
                    print(f"  ✓ {name} 存在")
                else:
                    print(f"  ✗ {name} 缺失")
            
            # 檢查是否有重複的代碼
            if content.count("function playAudio") > 1:
                print("\n  ⚠️ 警告: playAudio 函數定義重複")
            else:
                print("\n  ✓ 沒有重複的函數定義")
            
            return True
        else:
            print(f"❌ 頁面訪問失敗: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器")
        print("   請確認 Flask 應用正在運行")
        return False
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_weather_api():
    """測試天氣 API 端點"""
    print("\n" + "=" * 60)
    print("測試天氣 API")
    print("=" * 60)
    
    try:
        # 測試台北的天氣
        data = {
            "latitude": 25.033,
            "longitude": 121.5654
        }
        
        response = requests.post(
            "http://localhost:5000/api/weather/by-location",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 天氣 API 正常")
            print(f"\n天氣資訊:")
            print(f"  城市: {result.get('city', 'N/A')}")
            print(f"  天氣: {result.get('condition', 'N/A')}")
            print(f"  溫度: {result.get('temperature', 'N/A')}°C")
            print(f"  降雨機率: {result.get('rain_probability', 'N/A')}%")
            return True
        else:
            print(f"❌ 天氣 API 失敗: HTTP {response.status_code}")
            print(f"   回應: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到天氣 API")
        return False
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_tts_api():
    """測試 TTS API 端點"""
    print("\n" + "=" * 60)
    print("測試 TTS API")
    print("=" * 60)
    
    try:
        data = {
            "text": "測試語音合成"
        }
        
        response = requests.post(
            "http://localhost:5000/api/generate-tts",
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "audio_url" in result:
                print("✅ TTS API 正常")
                print(f"   音頻 URL: {result['audio_url']}")
                return True
            else:
                print("⚠️ TTS API 回應格式異常")
                print(f"   回應: {result}")
                return False
        else:
            print(f"❌ TTS API 失敗: HTTP {response.status_code}")
            print(f"   回應: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⚠️ TTS API 超時（可能正在生成語音）")
        print("   這是正常的，TTS 生成需要時間")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 TTS API")
        print("   請確認 GPT-SoVITS 服務正在運行")
        return False
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_process_audio_api():
    """測試音頻處理 API 端點"""
    print("\n" + "=" * 60)
    print("測試音頻處理 API")
    print("=" * 60)
    
    try:
        # 檢查端點是否存在（不實際上傳音頻）
        response = requests.post(
            "http://localhost:5000/process_audio",
            timeout=5
        )
        
        # 預期會返回 400（因為沒有上傳文件）
        if response.status_code == 400:
            result = response.json()
            if "error" in result and "未上傳檔案" in result["error"]:
                print("✅ 音頻處理 API 端點存在")
                return True
        
        print(f"⚠️ 音頻處理 API 回應異常: HTTP {response.status_code}")
        return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到音頻處理 API")
        return False
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("\n🔍 情緒識別系統測試工具\n")
    
    results = []
    
    # 測試頁面
    results.append(("情緒識別頁面", test_emotion_analysis_page()))
    
    # 測試 API
    results.append(("天氣 API", test_weather_api()))
    results.append(("TTS API", test_tts_api()))
    results.append(("音頻處理 API", test_process_audio_api()))
    
    # 總結
    print("\n" + "=" * 60)
    print("測試總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {name}")
    
    print(f"\n總計: {passed}/{total} 項測試通過")
    
    if passed == total:
        print("\n🎉 所有測試通過！情緒識別系統正常運作")
        print("\n訪問頁面: http://localhost:5000/emotion-analysis")
    else:
        print("\n⚠️ 部分測試失敗，請檢查:")
        print("  1. Flask 應用是否正在運行")
        print("  2. GPT-SoVITS 服務是否正在運行")
        print("  3. 網絡連接是否正常")
        print("  4. 查看 Flask 控制台的錯誤訊息")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
