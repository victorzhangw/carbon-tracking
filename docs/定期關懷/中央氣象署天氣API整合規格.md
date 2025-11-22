# 中央氣象署天氣 API 整合規格

**文檔版本**: 1.0  
**發布日期**: 2025-11-21  
**API 來源**: 中央氣象署開放資料平台  
**API 文檔**: https://opendata.cwa.gov.tw/dist/opendata-swagger.html

---

## 1. 整合目標

將中央氣象署的天氣預報 API 整合到定期關懷系統中，為長者提供即時、準確的天氣資訊，生成更貼心的關懷訊息。

---

## 2. API 基本資訊

### 2.1 API 端點

```
GET https://opendata.cwa.gov.tw/api/v1/rest/datastore/{dataid}
```

### 2.2 主要資料集

| 資料集 ID     | 說明                               | 更新頻率   | 適用場景     |
| ------------- | ---------------------------------- | ---------- | ------------ |
| `F-C0032-001` | 一般天氣預報-今明 36 小時天氣預報  | 每 3 小時  | **推薦使用** |
| `F-D0047-089` | 鄉鎮天氣預報-臺灣未來 1 週天氣預報 | 每日 2 次  | 詳細預報     |
| `O-A0003-001` | 自動氣象站-氣象觀測資料            | 每 10 分鐘 | 即時觀測     |

**本系統採用**: `F-C0032-001` (36 小時天氣預報)

### 2.3 認證方式

```
Authorization: CWA-{API_KEY}
```

- 需要至中央氣象署開放資料平台註冊取得 API Key
- 註冊網址: https://opendata.cwa.gov.tw/userLogin
- 免費額度: 無限制（但建議合理使用）

---

## 3. API 請求規格

### 3.1 請求參數

| 參數名稱        | 類型   | 必填 | 說明     | 範例                  |
| --------------- | ------ | ---- | -------- | --------------------- |
| `Authorization` | Header | ✅   | API 金鑰 | `CWA-XXXXXXXX`        |
| `locationName`  | Query  | ❌   | 縣市名稱 | `臺北市`, `新北市`    |
| `elementName`   | Query  | ❌   | 氣象要素 | `Wx,PoP,MinT,MaxT`    |
| `timeFrom`      | Query  | ❌   | 起始時間 | `2025-11-21T00:00:00` |
| `timeTo`        | Query  | ❌   | 結束時間 | `2025-11-22T00:00:00` |

### 3.2 時間參數設定

```python
from datetime import datetime, timedelta

# 從當下開始的一天
time_from = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
time_to = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
```

### 3.3 氣象要素說明

| 要素代碼             | 中文名稱         | 說明                     | 單位 |
| -------------------- | ---------------- | ------------------------ | ---- |
| `Wx`                 | 天氣現象         | 晴天、多雲、陰天、雨天等 | 文字 |
| `PoP`                | 降雨機率         | 0-100                    | %    |
| `MinT`               | 最低溫度         | 當日最低溫               | °C   |
| `MaxT`               | 最高溫度         | 當日最高溫               | °C   |
| `CI`                 | 舒適度           | 舒適、悶熱等             | 文字 |
| `WeatherDescription` | 天氣預報綜合描述 | 詳細天氣描述             | 文字 |

---

## 4. API 回應格式

### 4.1 成功回應範例

```json
{
  "success": "true",
  "result": {
    "resource_id": "F-C0032-001",
    "fields": [...],
  },
  "records": {
    "datasetDescription": "三十六小時天氣預報",
    "location": [
      {
        "locationName": "臺北市",
        "weatherElement": [
          {
            "elementName": "Wx",
            "time": [
              {
                "startTime": "2025-11-21T06:00:00",
                "endTime": "2025-11-21T18:00:00",
                "parameter": {
                  "parameterName": "多雲時晴",
                  "parameterValue": "3"
                }
              }
            ]
          },
          {
            "elementName": "PoP",
            "time": [
              {
                "startTime": "2025-11-21T06:00:00",
                "endTime": "2025-11-21T18:00:00",
                "parameter": {
                  "parameterName": "20",
                  "parameterUnit": "百分比"
                }
              }
            ]
          },
          {
            "elementName": "MinT",
            "time": [
              {
                "startTime": "2025-11-21T06:00:00",
                "endTime": "2025-11-21T18:00:00",
                "parameter": {
                  "parameterName": "18",
                  "parameterUnit": "C"
                }
              }
            ]
          },
          {
            "elementName": "MaxT",
            "time": [
              {
                "startTime": "2025-11-21T06:00:00",
                "endTime": "2025-11-21T18:00:00",
                "parameter": {
                  "parameterName": "25",
                  "parameterUnit": "C"
                }
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### 4.2 錯誤回應

```json
{
  "success": "false",
  "result": {
    "resource_id": "F-C0032-001",
    "fields": []
  },
  "records": {}
}
```

---

## 5. 地址解析策略

### 5.1 縣市對應表

由於 API 需要標準縣市名稱，需要從長者地址中提取縣市資訊：

```python
CITY_MAPPING = {
    # 直轄市
    '台北市': '臺北市', '臺北市': '臺北市',
    '新北市': '新北市',
    '桃園市': '桃園市',
    '台中市': '臺中市', '臺中市': '臺中市',
    '台南市': '臺南市', '臺南市': '臺南市',
    '高雄市': '高雄市',

    # 縣
    '基隆市': '基隆市',
    '新竹市': '新竹市',
    '新竹縣': '新竹縣',
    '苗栗縣': '苗栗縣',
    '彰化縣': '彰化縣',
    '南投縣': '南投縣',
    '雲林縣': '雲林縣',
    '嘉義市': '嘉義市',
    '嘉義縣': '嘉義縣',
    '屏東縣': '屏東縣',
    '宜蘭縣': '宜蘭縣',
    '花蓮縣': '花蓮縣',
    '台東縣': '臺東縣', '臺東縣': '臺東縣',
    '澎湖縣': '澎湖縣',
    '金門縣': '金門縣',
    '連江縣': '連江縣'
}
```

### 5.2 地址解析函數

```python
import re

def extract_city_from_address(address: str) -> str:
    """
    從地址中提取縣市名稱

    Args:
        address: 完整地址，如 "台北市大安區信義路100號"

    Returns:
        標準縣市名稱，如 "臺北市"
    """
    for city_variant, standard_city in CITY_MAPPING.items():
        if city_variant in address:
            return standard_city

    # 預設返回台北市
    return '臺北市'
```

---

## 6. 資料轉換規格

### 6.1 標準化天氣資料格式

系統內部使用的標準格式：

```python
{
    "city": "臺北市",              # 縣市名稱
    "temperature": 22,             # 當前溫度（取平均）
    "min_temperature": 18,         # 最低溫度
    "max_temperature": 25,         # 最高溫度
    "condition": "多雲時晴",        # 天氣狀況
    "rain_probability": 20,        # 降雨機率 (%)
    "comfort": "舒適",             # 舒適度
    "forecast": "今天天氣多雲時晴，溫度約 18-25 度，降雨機率 20%，天氣舒適。",
    "update_time": "2025-11-21T08:00:00",
    "data_source": "中央氣象署"
}
```

### 6.2 天氣狀況對應建議

根據天氣狀況生成關懷建議：

```python
WEATHER_ADVICE = {
    "晴天": "天氣晴朗，適合外出散步，記得戴帽子防曬喔",
    "多雲": "天氣還不錯，可以出門走走",
    "陰天": "天氣陰陰的，出門記得帶件外套",
    "雨天": "今天有雨，如果要出門記得帶雨傘",
    "大雨": "今天雨勢較大，建議在家休息比較安全",
    "雷雨": "有雷陣雨，盡量不要外出，注意安全",
}

def get_weather_advice(condition: str, rain_prob: int) -> str:
    """根據天氣狀況生成建議"""
    for key, advice in WEATHER_ADVICE.items():
        if key in condition:
            return advice

    if rain_prob > 70:
        return "降雨機率高，記得帶雨具"
    elif rain_prob > 30:
        return "可能會下雨，建議帶把傘"

    return "天氣還不錯，祝您有美好的一天"
```

---

## 7. 實作架構

### 7.1 新增服務模組

建立 `services/weather_service.py`：

```python
class CWAWeatherService:
    """中央氣象署天氣服務"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore"
        self.dataset_id = "F-C0032-001"

    def get_weather_by_city(self, city: str) -> dict:
        """根據縣市取得天氣預報"""
        pass

    def get_weather_by_address(self, address: str) -> dict:
        """根據地址取得天氣預報"""
        pass

    def parse_weather_data(self, raw_data: dict) -> dict:
        """解析 API 回應資料"""
        pass
```

### 7.2 整合到關懷服務

修改 `modules/voice_processing/voice_care_service.py`：

```python
from services.weather_service import CWAWeatherService

class VoiceCareService:
    def __init__(self):
        # 初始化天氣服務
        api_key = os.getenv('CWA_API_KEY')
        if api_key:
            self.weather_service = CWAWeatherService(api_key)
            self.use_real_weather = True
        else:
            self.weather_service = None
            self.use_real_weather = False

    def get_weather_info(self, latitude: float, longitude: float,
                        address: str = "") -> Dict:
        """獲取天氣資訊（優先使用真實 API）"""
        if self.use_real_weather and address:
            try:
                return self.weather_service.get_weather_by_address(address)
            except Exception as e:
                print(f"天氣 API 調用失敗，使用模擬數據: {e}")

        # 降級到模擬數據
        return self._get_mock_weather()
```

### 7.3 配置管理

在 `config.py` 中新增：

```python
# 中央氣象署 API 設定
CWA_API_KEY = os.getenv('CWA_API_KEY', '')
CWA_API_ENABLED = bool(CWA_API_KEY)
```

在 `.env` 中新增：

```bash
# 中央氣象署開放資料 API
CWA_API_KEY=your_api_key_here
```

---

## 8. 快取策略

### 8.1 快取需求

- 天氣資料每 3 小時更新一次
- 同一縣市的資料可以快取 1 小時
- 減少 API 調用次數

### 8.2 快取實作

```python
from datetime import datetime, timedelta
from typing import Optional

class WeatherCache:
    """天氣資料快取"""

    def __init__(self, cache_duration_minutes: int = 60):
        self.cache = {}
        self.cache_duration = timedelta(minutes=cache_duration_minutes)

    def get(self, city: str) -> Optional[dict]:
        """取得快取資料"""
        if city in self.cache:
            data, timestamp = self.cache[city]
            if datetime.now() - timestamp < self.cache_duration:
                return data
        return None

    def set(self, city: str, data: dict):
        """設定快取資料"""
        self.cache[city] = (data, datetime.now())

    def clear(self):
        """清除快取"""
        self.cache.clear()
```

---

## 9. 錯誤處理

### 9.1 錯誤類型

| 錯誤情況     | 處理方式                      |
| ------------ | ----------------------------- |
| API Key 無效 | 降級到模擬數據                |
| 網路連線失敗 | 重試 3 次，失敗後使用模擬數據 |
| 縣市名稱錯誤 | 使用預設縣市（台北市）        |
| 回應格式錯誤 | 記錄錯誤，使用模擬數據        |
| API 限流     | 使用快取資料或模擬數據        |

### 9.2 降級機制

```python
def get_weather_with_fallback(self, address: str) -> dict:
    """帶降級機制的天氣查詢"""
    try:
        # 1. 嘗試使用真實 API
        if self.use_real_weather:
            return self.weather_service.get_weather_by_address(address)
    except Exception as e:
        print(f"天氣 API 失敗: {e}")

    try:
        # 2. 嘗試使用快取
        city = extract_city_from_address(address)
        cached = self.weather_cache.get(city)
        if cached:
            return cached
    except Exception as e:
        print(f"快取讀取失敗: {e}")

    # 3. 使用模擬數據
    return self._get_mock_weather()
```

---

## 10. 測試計畫

### 10.1 單元測試

```python
def test_extract_city_from_address():
    """測試地址解析"""
    assert extract_city_from_address("台北市大安區") == "臺北市"
    assert extract_city_from_address("新北市板橋區") == "新北市"
    assert extract_city_from_address("高雄市前金區") == "高雄市"

def test_weather_api_call():
    """測試 API 調用"""
    service = CWAWeatherService(api_key="test_key")
    weather = service.get_weather_by_city("臺北市")
    assert "temperature" in weather
    assert "condition" in weather

def test_weather_cache():
    """測試快取機制"""
    cache = WeatherCache(cache_duration_minutes=1)
    cache.set("臺北市", {"temperature": 25})
    assert cache.get("臺北市") is not None
```

### 10.2 整合測試

1. 測試不同縣市的天氣查詢
2. 測試時間區間參數
3. 測試錯誤處理和降級機制
4. 測試快取功能
5. 測試與關懷訊息生成的整合

---

## 11. 上線檢查清單

- [ ] 註冊中央氣象署 API 帳號
- [ ] 取得 API Key 並設定環境變數
- [ ] 實作 `CWAWeatherService` 類別
- [ ] 實作地址解析功能
- [ ] 實作快取機制
- [ ] 實作錯誤處理和降級機制
- [ ] 更新 `VoiceCareService` 整合天氣服務
- [ ] 撰寫單元測試
- [ ] 執行整合測試
- [ ] 更新系統文檔
- [ ] 監控 API 調用狀況

---

## 12. 參考資源

- 中央氣象署開放資料平台: https://opendata.cwa.gov.tw/
- API 文檔: https://opendata.cwa.gov.tw/dist/opendata-swagger.html
- 使用者註冊: https://opendata.cwa.gov.tw/userLogin
- 資料集說明: https://opendata.cwa.gov.tw/opendatadoc/Observation/O-A0001-001.pdf

---

**文檔結束**
