#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中央氣象署天氣服務模組
提供通用的天氣查詢功能，可供所有模組使用

使用範例:
    from services.weather_service import weather_service
    
    # 根據地址查詢
    weather = weather_service.get_weather_by_address("台北市大安區信義路100號")
    
    # 根據縣市查詢
    weather = weather_service.get_weather_by_city("臺北市")
    
    # 取得天氣建議
    advice = weather_service.get_weather_advice(weather)
"""

import requests
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from config import CWA_API_KEY, CWA_API_ENABLED


class WeatherCache:
    """天氣資料快取類別"""
    
    def __init__(self, cache_duration_minutes: int = 60):
        """
        初始化快取
        
        Args:
            cache_duration_minutes: 快取有效時間（分鐘）
        """
        self.cache = {}
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
    
    def get(self, city: str) -> Optional[Dict]:
        """
        取得快取資料
        
        Args:
            city: 縣市名稱
            
        Returns:
            快取的天氣資料，如果過期或不存在則返回 None
        """
        if city in self.cache:
            data, timestamp = self.cache[city]
            if datetime.now() - timestamp < self.cache_duration:
                return data
        return None
    
    def set(self, city: str, data: Dict):
        """
        設定快取資料
        
        Args:
            city: 縣市名稱
            data: 天氣資料
        """
        self.cache[city] = (data, datetime.now())
    
    def clear(self):
        """清除所有快取"""
        self.cache.clear()
    
    def get_cache_info(self) -> Dict:
        """取得快取資訊"""
        return {
            'total_cached': len(self.cache),
            'cities': list(self.cache.keys()),
            'cache_duration_minutes': self.cache_duration.total_seconds() / 60
        }


class CWAWeatherService:
    """中央氣象署天氣服務類別"""
    
    # 縣市名稱對應表（支援台/臺轉換）
    CITY_MAPPING = {
        # 直轄市
        '台北市': '臺北市', '臺北市': '臺北市',
        '新北市': '新北市',
        '桃園市': '桃園市',
        '台中市': '臺中市', '臺中市': '臺中市',
        '台南市': '臺南市', '臺南市': '臺南市',
        '高雄市': '高雄市',
        
        # 縣市
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
    
    # 天氣狀況對應建議
    WEATHER_ADVICE = {
        '晴': '天氣晴朗，適合外出散步，記得戴帽子防曬喔',
        '多雲': '天氣還不錯，可以出門走走',
        '陰': '天氣陰陰的，出門記得帶件外套',
        '雨': '今天有雨，如果要出門記得帶雨傘',
        '大雨': '今天雨勢較大，建議在家休息比較安全',
        '雷': '有雷陣雨，盡量不要外出，注意安全',
        '颱風': '颱風天氣，請待在室內，注意安全',
    }
    
    def __init__(self, api_key: str = CWA_API_KEY, cache_duration: int = 60):
        """
        初始化天氣服務
        
        Args:
            api_key: 中央氣象署 API 金鑰
            cache_duration: 快取有效時間（分鐘）
        """
        self.api_key = api_key
        self.base_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore"
        self.dataset_id = "F-C0032-001"  # 36小時天氣預報
        self.enabled = bool(api_key)
        self.cache = WeatherCache(cache_duration)
        
        if not self.enabled:
            print("⚠️ 天氣服務未啟用：缺少 API Key")
    
    def extract_city_from_address(self, address: str) -> str:
        """
        從地址中提取縣市名稱
        
        Args:
            address: 完整地址，如 "台北市大安區信義路100號"
            
        Returns:
            標準縣市名稱，如 "臺北市"
        """
        for city_variant, standard_city in self.CITY_MAPPING.items():
            if city_variant in address:
                return standard_city
        
        # 預設返回台北市
        return '臺北市'
    
    def get_weather_by_city(self, city: str, use_cache: bool = True) -> Dict:
        """
        根據縣市取得天氣預報
        
        Args:
            city: 縣市名稱（會自動轉換為標準名稱）
            use_cache: 是否使用快取
            
        Returns:
            標準化的天氣資料
        """
        # 標準化縣市名稱
        standard_city = self.CITY_MAPPING.get(city, city)
        
        # 檢查快取
        if use_cache:
            cached_data = self.cache.get(standard_city)
            if cached_data:
                cached_data['from_cache'] = True
                return cached_data
        
        # 如果 API 未啟用，返回模擬數據
        if not self.enabled:
            return self._get_mock_weather(standard_city)
        
        try:
            # 調用 API
            weather_data = self._call_weather_api(standard_city)
            
            # 快取結果
            if use_cache:
                self.cache.set(standard_city, weather_data)
            
            weather_data['from_cache'] = False
            return weather_data
            
        except Exception as e:
            print(f"天氣 API 調用失敗: {e}")
            return self._get_mock_weather(standard_city)
    
    def get_weather_by_address(self, address: str, use_cache: bool = True) -> Dict:
        """
        根據地址取得天氣預報
        
        Args:
            address: 完整地址
            use_cache: 是否使用快取
            
        Returns:
            標準化的天氣資料
        """
        city = self.extract_city_from_address(address)
        return self.get_weather_by_city(city, use_cache)
    
    def _call_weather_api(self, city: str) -> Dict:
        """
        調用中央氣象署 API
        
        Args:
            city: 標準縣市名稱
            
        Returns:
            標準化的天氣資料
        """
        # 時間參數：從當下開始的一天
        time_from = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        time_to = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
        
        # 請求參數
        params = {
            'Authorization': self.api_key,
            'locationName': city,
            'elementName': 'Wx,PoP,MinT,MaxT,CI',
            'timeFrom': time_from,
            'timeTo': time_to
        }
        
        # 發送請求
        response = requests.get(
            f"{self.base_url}/{self.dataset_id}",
            params=params,
            timeout=10
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP 錯誤: {response.status_code}")
        
        data = response.json()
        
        if data.get('success') != 'true':
            raise Exception("API 回應失敗")
        
        # 解析資料
        return self._parse_weather_data(data, city)
    
    def _parse_weather_data(self, raw_data: Dict, city: str) -> Dict:
        """
        解析 API 回應資料
        
        Args:
            raw_data: API 原始回應
            city: 縣市名稱
            
        Returns:
            標準化的天氣資料
        """
        records = raw_data.get('records', {})
        locations = records.get('location', [])
        
        if not locations:
            raise Exception("無天氣資料")
        
        location = locations[0]
        weather_elements = location.get('weatherElement', [])
        
        # 提取各項氣象要素
        weather_data = {}
        for element in weather_elements:
            element_name = element.get('elementName')
            times = element.get('time', [])
            
            if times:
                param = times[0].get('parameter', {})
                weather_data[element_name] = param.get('parameterName')
        
        # 標準化格式
        condition = weather_data.get('Wx', '晴天')
        min_temp = int(weather_data.get('MinT', 20))
        max_temp = int(weather_data.get('MaxT', 25))
        rain_prob = int(weather_data.get('PoP', 0))
        comfort = weather_data.get('CI', '舒適')
        
        return {
            'city': city,
            'temperature': (min_temp + max_temp) // 2,  # 平均溫度
            'min_temperature': min_temp,
            'max_temperature': max_temp,
            'condition': condition,
            'rain_probability': rain_prob,
            'comfort': comfort,
            'forecast': self._generate_forecast(condition, min_temp, max_temp, rain_prob),
            'update_time': datetime.now().isoformat(),
            'data_source': '中央氣象署'
        }
    
    def _generate_forecast(self, condition: str, min_temp: int, max_temp: int, rain_prob: int) -> str:
        """
        生成天氣預報描述
        
        Args:
            condition: 天氣狀況
            min_temp: 最低溫度
            max_temp: 最高溫度
            rain_prob: 降雨機率
            
        Returns:
            天氣預報文字描述
        """
        forecast = f"今天天氣{condition}，溫度約 {min_temp}-{max_temp} 度"
        
        if rain_prob > 70:
            forecast += f"，降雨機率 {rain_prob}%，很可能會下雨"
        elif rain_prob > 30:
            forecast += f"，降雨機率 {rain_prob}%，可能會下雨"
        else:
            forecast += f"，降雨機率 {rain_prob}%"
        
        return forecast + "。"
    
    def get_weather_advice(self, weather_data: Dict) -> str:
        """
        根據天氣狀況生成建議
        
        Args:
            weather_data: 天氣資料
            
        Returns:
            天氣建議文字
        """
        condition = weather_data.get('condition', '')
        rain_prob = weather_data.get('rain_probability', 0)
        
        # 根據天氣狀況匹配建議
        for key, advice in self.WEATHER_ADVICE.items():
            if key in condition:
                return advice
        
        # 根據降雨機率給建議
        if rain_prob > 70:
            return "降雨機率高，記得帶雨具"
        elif rain_prob > 30:
            return "可能會下雨，建議帶把傘"
        
        return "天氣還不錯，祝您有美好的一天"
    
    def _get_mock_weather(self, city: str) -> Dict:
        """
        取得模擬天氣資料（降級方案）
        
        Args:
            city: 縣市名稱
            
        Returns:
            模擬的天氣資料
        """
        return {
            'city': city,
            'temperature': 25,
            'min_temperature': 20,
            'max_temperature': 28,
            'condition': '晴天',
            'rain_probability': 20,
            'comfort': '舒適',
            'forecast': '今天天氣晴朗，溫度約 20-28 度，降雨機率 20%。',
            'update_time': datetime.now().isoformat(),
            'data_source': '模擬資料',
            'from_cache': False
        }
    
    def get_cache_info(self) -> Dict:
        """取得快取資訊"""
        return self.cache.get_cache_info()
    
    def clear_cache(self):
        """清除快取"""
        self.cache.clear()


# 創建全域服務實例（單例模式）
weather_service = CWAWeatherService()


# 便捷函數
def get_weather(location: str, use_cache: bool = True) -> Dict:
    """
    便捷函數：根據地址或縣市取得天氣
    
    Args:
        location: 地址或縣市名稱
        use_cache: 是否使用快取
        
    Returns:
        天氣資料
    """
    return weather_service.get_weather_by_address(location, use_cache)


def get_weather_advice(weather_data: Dict) -> str:
    """
    便捷函數：取得天氣建議
    
    Args:
        weather_data: 天氣資料
        
    Returns:
        天氣建議
    """
    return weather_service.get_weather_advice(weather_data)
