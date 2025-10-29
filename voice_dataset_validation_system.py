"""
高齡語音資料集驗證與日誌系統
Voice Dataset Validation and Logging System for Elderly Speech Data
"""

import os
import json
import logging
import sqlite3
import hashlib
import librosa
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import pandas as pd

# 配置日誌系統
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_dataset_validation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

@dataclass
class VoiceDataSample:
    """語音資料樣本結構"""
    file_id: str
    file_path: str
    transcript: str
    speaker_id: str
    speaker_type: str  # 'agent' or 'customer'
    emotion: str
    intent: str
    slots: Dict[str, str]
    duration: float
    sample_rate: int
    file_size: int
    age_group: str  # 'young', 'middle', 'elderly'
    gender: str  # 'male', 'female'
    quality_score: float
    created_at: str
    validated_at: Optional[str] = None
    validation_status: str = 'pending'  # 'pending', 'passed', 'failed'
    validation_errors: List[str] = None

class VoiceDatasetValidator:
    """語音資料集驗證器"""
    
    def __init__(self, db_path: str = "voice_dataset.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.init_database()
        
        # 驗證標準
        self.validation_criteria = {
            'min_duration': 0.5,  # 最短 0.5 秒
            'max_duration': 60.0,  # 最長 60 秒
            'min_sample_rate': 16000,  # 最低採樣率
            'max_file_size': 50 * 1024 * 1024,  # 最大 50MB
            'required_emotions': ['neutral', 'happy', 'sad', 'angry', 'anxious', 'frustrated'],
            'required_intents': ['query', 'complaint', 'consultation', 'booking', 'thanks', 'goodbye'],
            'min_quality_score': 0.7,  # 最低品質分數
            'transcript_min_length': 2,  # 逐字稿最短字數
            'transcript_max_length': 500  # 逐字稿最長字數
        }
    
    def init_database(self):
        """初始化資料庫"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 創建語音資料表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS voice_samples (
            file_id TEXT PRIMARY KEY,
            file_path TEXT NOT NULL,
            transcript TEXT NOT NULL,
            speaker_id TEXT NOT NULL,
            speaker_type TEXT NOT NULL,
            emotion TEXT NOT NULL,
            intent TEXT NOT NULL,
            slots TEXT,  -- JSON 格式
            duration REAL NOT NULL,
            sample_rate INTEGER NOT NULL,
            file_size INTEGER NOT NULL,
            age_group TEXT NOT NULL,
            gender TEXT NOT NULL,
            quality_score REAL NOT NULL,
            created_at TEXT NOT NULL,
            validated_at TEXT,
            validation_status TEXT DEFAULT 'pending',
            validation_errors TEXT  -- JSON 格式
        )
        ''')
        
        # 創建驗證日誌表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS validation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT NOT NULL,
            validation_type TEXT NOT NULL,
            status TEXT NOT NULL,
            message TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (file_id) REFERENCES voice_samples (file_id)
        )
        ''')
        
        # 創建統計表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dataset_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_samples INTEGER,
            validated_samples INTEGER,
            passed_samples INTEGER,
            failed_samples INTEGER,
            total_duration REAL,
            avg_quality_score REAL,
            emotion_distribution TEXT,  -- JSON 格式
            intent_distribution TEXT,   -- JSON 格式
            age_distribution TEXT,      -- JSON 格式
            gender_distribution TEXT,   -- JSON 格式
            updated_at TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
        self.logger.info("資料庫初始化完成")
    
    def validate_audio_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """驗證音頻檔案"""
        errors = []
        
        try:
            # 檢查檔案是否存在
            if not os.path.exists(file_path):
                errors.append(f"檔案不存在: {file_path}")
                return False, errors
            
            # 檢查檔案大小
            file_size = os.path.getsize(file_path)
            if file_size > self.validation_criteria['max_file_size']:
                errors.append(f"檔案過大: {file_size} bytes")
            
            # 載入音頻並檢查基本屬性
            try:
                y, sr = librosa.load(file_path, sr=None)
                duration = librosa.get_duration(y=y, sr=sr)
                
                # 檢查時長
                if duration < self.validation_criteria['min_duration']:
                    errors.append(f"音頻過短: {duration:.2f} 秒")
                elif duration > self.validation_criteria['max_duration']:
                    errors.append(f"音頻過長: {duration:.2f} 秒")
                
                # 檢查採樣率
                if sr < self.validation_criteria['min_sample_rate']:
                    errors.append(f"採樣率過低: {sr} Hz")
                
                # 檢查音頻品質
                if np.max(np.abs(y)) < 0.01:
                    errors.append("音頻音量過低")
                
                # 檢查是否有音頻內容
                if np.all(y == 0):
                    errors.append("音頻檔案無內容")
                    
            except Exception as e:
                errors.append(f"音頻載入失敗: {str(e)}")
        
        except Exception as e:
            errors.append(f"檔案驗證異常: {str(e)}")
        
        return len(errors) == 0, errors
    
    def validate_transcript(self, transcript: str) -> Tuple[bool, List[str]]:
        """驗證逐字稿"""
        errors = []
        
        if not transcript or not transcript.strip():
            errors.append("逐字稿為空")
            return False, errors
        
        transcript = transcript.strip()
        
        # 檢查長度
        if len(transcript) < self.validation_criteria['transcript_min_length']:
            errors.append(f"逐字稿過短: {len(transcript)} 字")
        elif len(transcript) > self.validation_criteria['transcript_max_length']:
            errors.append(f"逐字稿過長: {len(transcript)} 字")
        
        # 檢查是否包含有效中文字符
        chinese_chars = sum(1 for char in transcript if '\u4e00' <= char <= '\u9fff')
        if chinese_chars < 2:
            errors.append("逐字稿中文字符過少")
        
        # 檢查特殊字符比例
        special_chars = sum(1 for char in transcript if not char.isalnum() and char not in '，。！？；：「」『』（）')
        if special_chars / len(transcript) > 0.3:
            errors.append("逐字稿特殊字符比例過高")
        
        return len(errors) == 0, errors
    
    def validate_annotations(self, emotion: str, intent: str, slots: Dict[str, str]) -> Tuple[bool, List[str]]:
        """驗證標註資訊"""
        errors = []
        
        # 驗證情緒標註
        if emotion not in self.validation_criteria['required_emotions']:
            errors.append(f"無效的情緒標註: {emotion}")
        
        # 驗證意圖標註
        if intent not in self.validation_criteria['required_intents']:
            errors.append(f"無效的意圖標註: {intent}")
        
        # 驗證槽位資訊
        if not isinstance(slots, dict):
            errors.append("槽位資訊格式錯誤")
        else:
            for key, value in slots.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    errors.append(f"槽位資訊格式錯誤: {key}={value}")
        
        return len(errors) == 0, errors
    
    def validate_sample(self, sample: VoiceDataSample) -> Tuple[bool, List[str]]:
        """驗證單個語音樣本"""
        all_errors = []
        
        # 驗證音頻檔案
        audio_valid, audio_errors = self.validate_audio_file(sample.file_path)
        all_errors.extend(audio_errors)
        
        # 驗證逐字稿
        transcript_valid, transcript_errors = self.validate_transcript(sample.transcript)
        all_errors.extend(transcript_errors)
        
        # 驗證標註
        annotation_valid, annotation_errors = self.validate_annotations(
            sample.emotion, sample.intent, sample.slots
        )
        all_errors.extend(annotation_errors)
        
        # 驗證品質分數
        if sample.quality_score < self.validation_criteria['min_quality_score']:
            all_errors.append(f"品質分數過低: {sample.quality_score}")
        
        # 驗證必要欄位
        required_fields = ['speaker_id', 'speaker_type', 'age_group', 'gender']
        for field in required_fields:
            if not getattr(sample, field):
                all_errors.append(f"必要欄位缺失: {field}")
        
        is_valid = len(all_errors) == 0
        
        # 記錄驗證日誌
        self.log_validation(sample.file_id, 'sample_validation', 
                          'passed' if is_valid else 'failed', 
                          '; '.join(all_errors) if all_errors else 'All checks passed')
        
        return is_valid, all_errors
    
    def add_sample(self, sample: VoiceDataSample) -> bool:
        """添加語音樣本到資料庫"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 驗證樣本
            is_valid, errors = self.validate_sample(sample)
            sample.validation_status = 'passed' if is_valid else 'failed'
            sample.validation_errors = errors
            sample.validated_at = datetime.now().isoformat()
            
            # 插入資料
            cursor.execute('''
            INSERT OR REPLACE INTO voice_samples VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            ''', (
                sample.file_id, sample.file_path, sample.transcript,
                sample.speaker_id, sample.speaker_type, sample.emotion,
                sample.intent, json.dumps(sample.slots, ensure_ascii=False),
                sample.duration, sample.sample_rate, sample.file_size,
                sample.age_group, sample.gender, sample.quality_score,
                sample.created_at, sample.validated_at, sample.validation_status,
                json.dumps(sample.validation_errors, ensure_ascii=False) if sample.validation_errors else None
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"樣本 {sample.file_id} 添加成功，驗證狀態: {sample.validation_status}")
            return True
            
        except Exception as e:
            self.logger.error(f"添加樣本失敗: {str(e)}")
            return False
    
    def log_validation(self, file_id: str, validation_type: str, status: str, message: str = ""):
        """記錄驗證日誌"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO validation_logs (file_id, validation_type, status, message, timestamp)
            VALUES (?, ?, ?, ?, ?)
            ''', (file_id, validation_type, status, message, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"記錄驗證日誌失敗: {str(e)}")
    
    def get_validation_report(self) -> Dict:
        """生成驗證報告"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 基本統計
            cursor.execute('SELECT COUNT(*) FROM voice_samples')
            total_samples = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM voice_samples WHERE validation_status = "passed"')
            passed_samples = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM voice_samples WHERE validation_status = "failed"')
            failed_samples = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(duration) FROM voice_samples WHERE validation_status = "passed"')
            total_duration = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT AVG(quality_score) FROM voice_samples WHERE validation_status = "passed"')
            avg_quality = cursor.fetchone()[0] or 0
            
            # 分佈統計
            cursor.execute('SELECT emotion, COUNT(*) FROM voice_samples WHERE validation_status = "passed" GROUP BY emotion')
            emotion_dist = dict(cursor.fetchall())
            
            cursor.execute('SELECT intent, COUNT(*) FROM voice_samples WHERE validation_status = "passed" GROUP BY intent')
            intent_dist = dict(cursor.fetchall())
            
            cursor.execute('SELECT age_group, COUNT(*) FROM voice_samples WHERE validation_status = "passed" GROUP BY age_group')
            age_dist = dict(cursor.fetchall())
            
            cursor.execute('SELECT gender, COUNT(*) FROM voice_samples WHERE validation_status = "passed" GROUP BY gender')
            gender_dist = dict(cursor.fetchall())
            
            # 常見錯誤統計
            cursor.execute('''
            SELECT validation_errors, COUNT(*) 
            FROM voice_samples 
            WHERE validation_status = "failed" AND validation_errors IS NOT NULL
            GROUP BY validation_errors
            ORDER BY COUNT(*) DESC
            LIMIT 10
            ''')
            common_errors = cursor.fetchall()
            
            conn.close()
            
            report = {
                'summary': {
                    'total_samples': total_samples,
                    'passed_samples': passed_samples,
                    'failed_samples': failed_samples,
                    'pass_rate': passed_samples / total_samples if total_samples > 0 else 0,
                    'total_duration_hours': total_duration / 3600,
                    'avg_quality_score': avg_quality
                },
                'distributions': {
                    'emotion': emotion_dist,
                    'intent': intent_dist,
                    'age_group': age_dist,
                    'gender': gender_dist
                },
                'common_errors': common_errors,
                'generated_at': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"生成驗證報告失敗: {str(e)}")
            return {}
    
    def export_failed_samples(self, output_path: str) -> bool:
        """匯出驗證失敗的樣本"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
            SELECT file_id, file_path, transcript, emotion, intent, 
                   validation_errors, quality_score
            FROM voice_samples 
            WHERE validation_status = "failed"
            ORDER BY file_id
            '''
            
            df = pd.read_sql_query(query, conn)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            conn.close()
            
            self.logger.info(f"驗證失敗樣本已匯出至: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"匯出失敗樣本錯誤: {str(e)}")
            return False

class DatasetQualityMonitor:
    """資料集品質監控器"""
    
    def __init__(self, validator: VoiceDatasetValidator):
        self.validator = validator
        self.logger = logging.getLogger(__name__)
    
    def check_data_balance(self) -> Dict:
        """檢查資料平衡性"""
        try:
            conn = sqlite3.connect(self.validator.db_path)
            cursor = conn.cursor()
            
            # 檢查各維度的平衡性
            balance_report = {}
            
            # 情緒分佈平衡
            cursor.execute('''
            SELECT emotion, COUNT(*) as count 
            FROM voice_samples 
            WHERE validation_status = "passed" 
            GROUP BY emotion
            ''')
            emotion_counts = dict(cursor.fetchall())
            if emotion_counts:
                max_count = max(emotion_counts.values())
                min_count = min(emotion_counts.values())
                balance_report['emotion_balance'] = {
                    'ratio': min_count / max_count if max_count > 0 else 0,
                    'distribution': emotion_counts,
                    'recommendation': 'balanced' if min_count / max_count > 0.5 else 'imbalanced'
                }
            
            # 年齡分佈平衡
            cursor.execute('''
            SELECT age_group, COUNT(*) as count 
            FROM voice_samples 
            WHERE validation_status = "passed" 
            GROUP BY age_group
            ''')
            age_counts = dict(cursor.fetchall())
            if age_counts:
                max_count = max(age_counts.values())
                min_count = min(age_counts.values())
                balance_report['age_balance'] = {
                    'ratio': min_count / max_count if max_count > 0 else 0,
                    'distribution': age_counts,
                    'recommendation': 'balanced' if min_count / max_count > 0.3 else 'imbalanced'
                }
            
            # 性別分佈平衡
            cursor.execute('''
            SELECT gender, COUNT(*) as count 
            FROM voice_samples 
            WHERE validation_status = "passed" 
            GROUP BY gender
            ''')
            gender_counts = dict(cursor.fetchall())
            if gender_counts:
                max_count = max(gender_counts.values())
                min_count = min(gender_counts.values())
                balance_report['gender_balance'] = {
                    'ratio': min_count / max_count if max_count > 0 else 0,
                    'distribution': gender_counts,
                    'recommendation': 'balanced' if min_count / max_count > 0.4 else 'imbalanced'
                }
            
            conn.close()
            return balance_report
            
        except Exception as e:
            self.logger.error(f"檢查資料平衡性失敗: {str(e)}")
            return {}
    
    def generate_quality_alerts(self) -> List[Dict]:
        """生成品質警告"""
        alerts = []
        
        try:
            conn = sqlite3.connect(self.validator.db_path)
            cursor = conn.cursor()
            
            # 檢查通過率
            cursor.execute('SELECT COUNT(*) FROM voice_samples')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM voice_samples WHERE validation_status = "passed"')
            passed = cursor.fetchone()[0]
            
            if total > 0:
                pass_rate = passed / total
                if pass_rate < 0.9:
                    alerts.append({
                        'type': 'low_pass_rate',
                        'severity': 'high' if pass_rate < 0.8 else 'medium',
                        'message': f'驗證通過率過低: {pass_rate:.2%}',
                        'recommendation': '檢查資料品質和標註流程'
                    })
            
            # 檢查平均品質分數
            cursor.execute('SELECT AVG(quality_score) FROM voice_samples WHERE validation_status = "passed"')
            avg_quality = cursor.fetchone()[0]
            
            if avg_quality and avg_quality < 0.8:
                alerts.append({
                    'type': 'low_quality_score',
                    'severity': 'medium',
                    'message': f'平均品質分數偏低: {avg_quality:.2f}',
                    'recommendation': '提升音頻錄製品質和標註準確度'
                })
            
            # 檢查資料不平衡
            balance_report = self.check_data_balance()
            for dimension, info in balance_report.items():
                if info['recommendation'] == 'imbalanced':
                    alerts.append({
                        'type': 'data_imbalance',
                        'severity': 'medium',
                        'message': f'{dimension} 資料分佈不平衡: 比例 {info["ratio"]:.2f}',
                        'recommendation': f'增加 {dimension} 中樣本數較少類別的資料'
                    })
            
            conn.close()
            
        except Exception as e:
            self.logger.error(f"生成品質警告失敗: {str(e)}")
        
        return alerts

# 使用範例
if __name__ == "__main__":
    # 初始化驗證器
    validator = VoiceDatasetValidator()
    monitor = DatasetQualityMonitor(validator)
    
    # 範例：添加語音樣本
    sample = VoiceDataSample(
        file_id="sample_001",
        file_path="./audio/sample_001.wav",
        transcript="您好，請問有什麼可以幫助您的嗎？",
        speaker_id="agent_001",
        speaker_type="agent",
        emotion="neutral",
        intent="greeting",
        slots={"greeting_type": "formal"},
        duration=3.5,
        sample_rate=16000,
        file_size=112000,
        age_group="middle",
        gender="female",
        quality_score=0.85,
        created_at=datetime.now().isoformat()
    )
    
    # 添加並驗證樣本
    success = validator.add_sample(sample)
    print(f"樣本添加結果: {success}")
    
    # 生成驗證報告
    report = validator.get_validation_report()
    print("驗證報告:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 檢查品質警告
    alerts = monitor.generate_quality_alerts()
    if alerts:
        print("\n品質警告:")
        for alert in alerts:
            print(f"- {alert['message']} (建議: {alert['recommendation']})")