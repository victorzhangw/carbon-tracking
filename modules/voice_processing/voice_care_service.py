#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧語音關懷服務模組
提供基於排程、用戶地址和天氣資訊的語音關懷提醒功能
"""

import sqlite3
import datetime
import uuid
import requests
import json
import os
from typing import Dict, List, Optional, Union
from config import DATABASE
from services.ai import generate_care_message
from modules.voice_processing.qwen_tts_service import QwenTTSService

class VoiceCareService:
    """智慧語音關懷服務類"""
    
    def __init__(self):
        """初始化智慧語音關懷服務"""
        self.audio_output_dir = "voice_care_audio"
        
        # 初始化 Qwen TTS 服務
        try:
            self.qwen_tts = QwenTTSService()
            self.use_qwen_tts = True
            print("✅ Qwen TTS 服務已啟用")
        except Exception as e:
            self.qwen_tts = None
            self.use_qwen_tts = False
            print(f"⚠️ Qwen TTS 服務未啟用: {e}")
        
        # 確保音頻輸出目錄存在
        os.makedirs(self.audio_output_dir, exist_ok=True)
    
    def create_schedule(self, user_id: str, title: str, scheduled_time: str, 
                       address: str = "", latitude: float = 0.0, longitude: float = 0.0,
                       staff_id: Optional[str] = None, description: str = "") -> str:
        """
        創建語音關懷排程
        
        Args:
            user_id (str): 用戶ID
            title (str): 排程標題
            scheduled_time (str): 排程時間 (ISO格式)
            address (str): 地址
            latitude (float): 緯度
            longitude (float): 經度
            staff_id (str): 客服專員ID
            description (str): 描述
            
        Returns:
            str: 排程ID
        """
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            schedule_id = str(uuid.uuid4())
            now = datetime.datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO voice_care_schedules 
                (id, user_id, staff_id, title, description, scheduled_time, address, latitude, longitude, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', [schedule_id, user_id, staff_id, title, description, scheduled_time, address, latitude, longitude, now, now])
            
            conn.commit()
            return schedule_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_schedule(self, schedule_id: str) -> Optional[Dict]:
        """
        獲取排程資訊
        
        Args:
            schedule_id (str): 排程ID
            
        Returns:
            Dict: 排程資訊
        """
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT vcs.*, u.full_name as user_name, s.name as staff_name
                FROM voice_care_schedules vcs
                LEFT JOIN users u ON vcs.user_id = u.id
                LEFT JOIN staff s ON vcs.staff_id = s.id
                WHERE vcs.id = ?
            ''', [schedule_id])
            
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def get_user_schedules(self, user_id: str, status: Optional[str] = None) -> List[Dict]:
        """
        獲取用戶的所有排程
        
        Args:
            user_id (str): 用戶ID
            status (str): 狀態過濾
            
        Returns:
            List[Dict]: 排程列表
        """
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            if status:
                cursor.execute('''
                    SELECT vcs.*, u.full_name as user_name, s.name as staff_name
                    FROM voice_care_schedules vcs
                    LEFT JOIN users u ON vcs.user_id = u.id
                    LEFT JOIN staff s ON vcs.staff_id = s.id
                    WHERE vcs.user_id = ? AND vcs.status = ?
                    ORDER BY vcs.scheduled_time
                ''', [user_id, status])
            else:
                cursor.execute('''
                    SELECT vcs.*, u.full_name as user_name, s.name as staff_name
                    FROM voice_care_schedules vcs
                    LEFT JOIN users u ON vcs.user_id = u.id
                    LEFT JOIN staff s ON vcs.staff_id = s.id
                    WHERE vcs.user_id = ?
                    ORDER BY vcs.scheduled_time
                ''', [user_id])
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def update_schedule_status(self, schedule_id: str, status: str) -> bool:
        """
        更新排程狀態
        
        Args:
            schedule_id (str): 排程ID
            status (str): 新狀態
            
        Returns:
            bool: 是否更新成功
        """
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            now = datetime.datetime.now().isoformat()
            cursor.execute('''
                UPDATE voice_care_schedules 
                SET status = ?, updated_at = ?
                WHERE id = ?
            ''', [status, now, schedule_id])
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_weather_info(self, latitude: float, longitude: float, address: str = "") -> Dict:
        """
        獲取天氣資訊（整合中央氣象署 API）
        
        Args:
            latitude (float): 緯度（保留參數以保持向後相容）
            longitude (float): 經度（保留參數以保持向後相容）
            address (str): 地址（優先使用）
            
        Returns:
            Dict: 天氣資訊
        """
        try:
            # 使用真實天氣服務
            from services.weather_service import weather_service
            
            if address:
                # 優先使用地址查詢
                weather_data = weather_service.get_weather_by_address(address)
            else:
                # 降級：使用預設縣市
                weather_data = weather_service.get_weather_by_city('臺北市')
            
            # 轉換為舊格式以保持相容性
            return {
                "temperature": weather_data['temperature'],
                "condition": weather_data['condition'],
                "humidity": 60,  # API 未提供，使用預設值
                "wind_speed": 3.5,  # API 未提供，使用預設值
                "forecast": weather_data['forecast'],
                "min_temperature": weather_data['min_temperature'],
                "max_temperature": weather_data['max_temperature'],
                "rain_probability": weather_data['rain_probability'],
                "comfort": weather_data['comfort'],
                "data_source": weather_data['data_source']
            }
        except Exception as e:
            print(f"⚠️ 天氣服務調用失敗，使用模擬數據: {e}")
            # 降級到模擬數據
            return {
                "temperature": 25,
                "condition": "晴天",
                "humidity": 60,
                "wind_speed": 3.5,
                "forecast": "今天天氣晴朗，適合外出活動"
            }
    
    def get_user_profile(self, user_id: str) -> Dict:
        """
        獲取用戶資料
        
        Args:
            user_id (str): 用戶ID
            
        Returns:
            Dict: 用戶資料
        """
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users WHERE id = ?', [user_id])
            row = cursor.fetchone()
            return dict(row) if row else {}
        finally:
            conn.close()
    
    def generate_care_message(self, schedule: Dict) -> str:
        """
        生成關懷訊息（使用 DeepSeek LLM）
        
        Args:
            schedule (Dict): 排程資訊
            
        Returns:
            str: 關懷訊息
        """
        # 獲取用戶資料
        user_profile = self.get_user_profile(schedule['user_id'])
        
        # 獲取天氣資訊（優先使用地址）
        weather_info = {}
        address = schedule.get('address', '')
        if address or (schedule.get('latitude') and schedule.get('longitude')):
            weather_info = self.get_weather_info(
                schedule.get('latitude', 0.0),
                schedule.get('longitude', 0.0),
                address
            )
        
        # 使用 DeepSeek LLM 生成訊息
        try:
            message = generate_care_message(schedule, weather_info, user_profile)
            print(f"✅ 使用 DeepSeek LLM 生成關懷訊息")
            return message
        except Exception as e:
            print(f"⚠️ LLM 生成失敗，使用預設模板: {e}")
            # 降級：使用預設模板
            return self._generate_default_message(schedule, weather_info, user_profile)
    
    def _generate_default_message(self, schedule: Dict, weather_info: Dict, user_profile: Dict) -> str:
        """生成預設關懷訊息（降級方案）"""
        user_name = user_profile.get('full_name', '用戶')
        message = f"親愛的{user_name}您好，"
        
        # 添加時間信息
        try:
            scheduled_time = datetime.datetime.fromisoformat(schedule['scheduled_time'])
            message += f"現在是{scheduled_time.strftime('%Y年%m月%d日 %H:%M')}，"
        except:
            message += "這是一個溫馨提醒，"
        
        # 添加天氣信息
        if weather_info:
            message += f"今天的天氣是{weather_info.get('condition', '晴朗')}，"
            message += f"溫度約{weather_info.get('temperature', 25)}度，"
            message += f"{weather_info.get('forecast', '適合外出活動')}。"
        
        # 添加自定義描述
        if schedule.get('description'):
            message += f"特別提醒：{schedule['description']}"
        
        message += "祝您有美好的一天！"
        
        return message
    
    def send_voice_care(self, schedule_id: str, language: str = 'mandarin') -> Dict:
        """
        發送語音關懷（支援雙語）
        
        Args:
            schedule_id (str): 排程ID
            language (str): 'mandarin', 'minan', 或 'both'
            
        Returns:
            Dict: 發送結果
        """
        # 獲取排程資訊
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            raise ValueError("排程不存在")
        
        if schedule['status'] != 'pending':
            raise ValueError("排程狀態不正確")
        
        # 生成關懷訊息（使用 DeepSeek LLM）
        message = self.generate_care_message(schedule)
        
        # 獲取天氣資訊（優先使用地址）
        weather_info = {}
        address = schedule.get('address', '')
        if address or (schedule.get('latitude') and schedule.get('longitude')):
            weather_info = self.get_weather_info(
                schedule.get('latitude', 0.0),
                schedule.get('longitude', 0.0),
                address
            )
        
        # 生成語音文件
        audio_dir = os.path.join(
            self.audio_output_dir,
            f"care_{schedule_id}_{int(datetime.datetime.now().timestamp())}"
        )
        os.makedirs(audio_dir, exist_ok=True)
        
        audio_files = {}
        
        try:
            # 使用 Qwen TTS 生成語音
            if self.use_qwen_tts and self.qwen_tts:
                print(f"使用 Qwen TTS 生成語音：{language}")
                
                if language == 'both':
                    audio_files = self.qwen_tts.synthesize_bilingual(message, audio_dir)
                else:
                    audio_file = os.path.join(audio_dir, f"{language}.wav")
                    result = self.qwen_tts.synthesize(message, language, audio_file)
                    audio_files[language] = result
            else:
                # 降級：使用 F5-TTS
                print("使用 F5-TTS 生成語音（降級方案）")
                from services.tts import f5_tts
                audio_data = f5_tts(message)
                if audio_data:
                    audio_file = os.path.join(audio_dir, "mandarin.wav")
                    with open(audio_file, 'wb') as f:
                        f.write(audio_data)
                    audio_files['mandarin'] = audio_file
            
            # 創建關懷記錄
            record_id = self.create_care_record(
                schedule_id=schedule_id,
                audio_file_path=json.dumps(audio_files),
                message=message,
                weather_info=json.dumps(weather_info) if weather_info else None
            )
            
            # 更新排程狀態
            self.update_schedule_status(schedule_id, 'completed')
            
            return {
                'success': True,
                'record_id': record_id,
                'audio_files': audio_files,
                'message': message
            }
        except Exception as e:
            # 更新排程狀態為失敗
            self.update_schedule_status(schedule_id, 'failed')
            raise e
    
    def create_care_record(self, schedule_id: str, audio_file_path: str, 
                          message: str, weather_info: Union[str, None] = None) -> str:
        """
        創建關懷記錄
        
        Args:
            schedule_id (str): 排程ID
            audio_file_path (str): 音頻文件路徑
            message (str): 訊息內容
            weather_info (str): 天氣資訊
            
        Returns:
            str: 記錄ID
        """
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            record_id = str(uuid.uuid4())
            now = datetime.datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO voice_care_records 
                (id, schedule_id, audio_file_path, message, weather_info, sent_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', [record_id, schedule_id, audio_file_path, message, weather_info, now, now])
            
            conn.commit()
            return record_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_care_records(self, schedule_id: Optional[str] = None) -> List[Dict]:
        """
        獲取關懷記錄
        
        Args:
            schedule_id (str): 排程ID（可選）
            
        Returns:
            List[Dict]: 關懷記錄列表
        """
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            if schedule_id:
                cursor.execute('''
                    SELECT vcr.*, vcs.title as schedule_title
                    FROM voice_care_records vcr
                    JOIN voice_care_schedules vcs ON vcr.schedule_id = vcs.id
                    WHERE vcr.schedule_id = ?
                    ORDER BY vcr.sent_at DESC
                ''', [schedule_id])
            else:
                cursor.execute('''
                    SELECT vcr.*, vcs.title as schedule_title
                    FROM voice_care_records vcr
                    JOIN voice_care_schedules vcs ON vcr.schedule_id = vcs.id
                    ORDER BY vcr.sent_at DESC
                ''')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def get_pending_schedules(self) -> List[Dict]:
        """
        獲取所有待處理的排程
        
        Returns:
            List[Dict]: 待處理排程列表
        """
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # 獲取當前時間前後5分鐘內的待處理排程
            now = datetime.datetime.now()
            start_time = (now - datetime.timedelta(minutes=5)).isoformat()
            end_time = (now + datetime.timedelta(minutes=5)).isoformat()
            
            cursor.execute('''
                SELECT *
                FROM voice_care_schedules
                WHERE status = 'pending'
                AND scheduled_time BETWEEN ? AND ?
                ORDER BY scheduled_time
            ''', [start_time, end_time])
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def process_pending_schedules(self) -> Dict:
        """
        處理所有待處理的排程
        
        Returns:
            Dict: 處理結果
        """
        pending_schedules = self.get_pending_schedules()
        results = {
            'total': len(pending_schedules),
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        for schedule in pending_schedules:
            try:
                result = self.send_voice_care(schedule['id'])
                results['success'] += 1
                results['details'].append({
                    'schedule_id': schedule['id'],
                    'status': 'success',
                    'record_id': result['record_id']
                })
            except Exception as e:
                results['failed'] += 1
                results['details'].append({
                    'schedule_id': schedule['id'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results

# 創建服務實例
voice_care_service = VoiceCareService()