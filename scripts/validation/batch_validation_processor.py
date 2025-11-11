"""
批量驗證處理器
Batch Validation Processor for Voice Dataset
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import os
import json
import logging
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict, Tuple
import pandas as pd
from tqdm import tqdm
import librosa
import hashlib
from datetime import datetime

from voice_dataset_validation_system import VoiceDataSample, VoiceDatasetValidator

class BatchValidationProcessor:
    """批量驗證處理器"""
    
    def __init__(self, validator: VoiceDatasetValidator, max_workers: int = None):
        self.validator = validator
        self.max_workers = max_workers or mp.cpu_count()
        self.logger = logging.getLogger(__name__)
        
    def process_annotation_file(self, annotation_file: str) -> List[VoiceDataSample]:
        """處理標註檔案，轉換為 VoiceDataSample 列表"""
        samples = []
        
        try:
            # 支援多種格式的標註檔案
            if annotation_file.endswith('.csv'):
                df = pd.read_csv(annotation_file, encoding='utf-8')
            elif annotation_file.endswith('.json'):
                with open(annotation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            elif annotation_file.endswith('.xlsx'):
                df = pd.read_excel(annotation_file)
            else:
                raise ValueError(f"不支援的檔案格式: {annotation_file}")
            
            # 驗證必要欄位
            required_columns = [
                'file_path', 'transcript', 'speaker_id', 'speaker_type',
                'emotion', 'intent', 'age_group', 'gender'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"缺少必要欄位: {missing_columns}")
            
            # 轉換為 VoiceDataSample
            for _, row in df.iterrows():
                try:
                    # 生成檔案 ID
                    file_id = self.generate_file_id(row['file_path'])
                    
                    # 提取音頻資訊
                    audio_info = self.extract_audio_info(row['file_path'])
                    
                    # 解析槽位資訊
                    slots = {}
                    if 'slots' in row and pd.notna(row['slots']):
                        try:
                            slots = json.loads(row['slots']) if isinstance(row['slots'], str) else row['slots']
                        except:
                            slots = {}
                    
                    # 創建樣本
                    sample = VoiceDataSample(
                        file_id=file_id,
                        file_path=row['file_path'],
                        transcript=str(row['transcript']),
                        speaker_id=str(row['speaker_id']),
                        speaker_type=str(row['speaker_type']),
                        emotion=str(row['emotion']),
                        intent=str(row['intent']),
                        slots=slots,
                        duration=audio_info['duration'],
                        sample_rate=audio_info['sample_rate'],
                        file_size=audio_info['file_size'],
                        age_group=str(row['age_group']),
                        gender=str(row['gender']),
                        quality_score=float(row.get('quality_score', 0.8)),
                        created_at=datetime.now().isoformat()
                    )
                    
                    samples.append(sample)
                    
                except Exception as e:
                    self.logger.error(f"處理樣本失敗 {row.get('file_path', 'unknown')}: {str(e)}")
                    continue
            
            self.logger.info(f"成功處理 {len(samples)} 個樣本")
            return samples
            
        except Exception as e:
            self.logger.error(f"處理標註檔案失敗: {str(e)}")
            return []
    
    def generate_file_id(self, file_path: str) -> str:
        """生成檔案 ID"""
        # 使用檔案路徑的 MD5 雜湊作為 ID
        return hashlib.md5(file_path.encode('utf-8')).hexdigest()[:16]
    
    def extract_audio_info(self, file_path: str) -> Dict:
        """提取音頻資訊"""
        try:
            if not os.path.exists(file_path):
                return {
                    'duration': 0.0,
                    'sample_rate': 16000,
                    'file_size': 0
                }
            
            # 獲取檔案大小
            file_size = os.path.getsize(file_path)
            
            # 載入音頻獲取基本資訊
            duration = librosa.get_duration(filename=file_path)
            sample_rate = librosa.get_samplerate(file_path)
            
            return {
                'duration': duration,
                'sample_rate': sample_rate,
                'file_size': file_size
            }
            
        except Exception as e:
            self.logger.warning(f"提取音頻資訊失敗 {file_path}: {str(e)}")
            return {
                'duration': 0.0,
                'sample_rate': 16000,
                'file_size': 0
            }
    
    def validate_sample_batch(self, samples: List[VoiceDataSample]) -> List[Tuple[bool, VoiceDataSample]]:
        """批量驗證樣本"""
        results = []
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交驗證任務
            future_to_sample = {
                executor.submit(self.validate_single_sample, sample): sample 
                for sample in samples
            }
            
            # 收集結果
            for future in tqdm(as_completed(future_to_sample), total=len(samples), desc="驗證樣本"):
                sample = future_to_sample[future]
                try:
                    success = future.result()
                    results.append((success, sample))
                except Exception as e:
                    self.logger.error(f"驗證樣本失敗 {sample.file_id}: {str(e)}")
                    results.append((False, sample))
        
        return results
    
    def validate_single_sample(self, sample: VoiceDataSample) -> bool:
        """驗證單個樣本（用於多進程）"""
        try:
            # 創建新的驗證器實例（避免多進程問題）
            validator = VoiceDatasetValidator()
            return validator.add_sample(sample)
        except Exception as e:
            logging.error(f"驗證樣本失敗 {sample.file_id}: {str(e)}")
            return False
    
    def process_directory(self, audio_dir: str, annotation_file: str) -> Dict:
        """處理整個目錄的音頻檔案"""
        self.logger.info(f"開始處理目錄: {audio_dir}")
        self.logger.info(f"標註檔案: {annotation_file}")
        
        # 載入標註資料
        samples = self.process_annotation_file(annotation_file)
        
        if not samples:
            return {
                'status': 'failed',
                'message': '無有效樣本',
                'total_samples': 0,
                'processed_samples': 0,
                'success_samples': 0
            }
        
        # 批量驗證
        self.logger.info(f"開始批量驗證 {len(samples)} 個樣本")
        results = self.validate_sample_batch(samples)
        
        # 統計結果
        success_count = sum(1 for success, _ in results if success)
        
        result_summary = {
            'status': 'completed',
            'total_samples': len(samples),
            'processed_samples': len(results),
            'success_samples': success_count,
            'success_rate': success_count / len(results) if results else 0,
            'processed_at': datetime.now().isoformat()
        }
        
        self.logger.info(f"批量處理完成: {result_summary}")
        return result_summary
    
    def generate_processing_report(self, output_path: str) -> bool:
        """生成處理報告"""
        try:
            report = self.validator.get_validation_report()
            
            # 添加處理統計
            report['processing_info'] = {
                'max_workers': self.max_workers,
                'processing_time': datetime.now().isoformat()
            }
            
            # 儲存報告
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"處理報告已儲存至: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"生成處理報告失敗: {str(e)}")
            return False

class DatasetSplitter:
    """資料集分割器"""
    
    def __init__(self, validator: VoiceDatasetValidator):
        self.validator = validator
        self.logger = logging.getLogger(__name__)
    
    def split_dataset(self, train_ratio: float = 0.8, val_ratio: float = 0.1, test_ratio: float = 0.1) -> Dict:
        """分割資料集"""
        if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-6:
            raise ValueError("分割比例總和必須等於 1.0")
        
        try:
            # 載入所有通過驗證的樣本
            conn = sqlite3.connect(self.validator.db_path)
            df = pd.read_sql_query('''
            SELECT * FROM voice_samples 
            WHERE validation_status = "passed"
            ORDER BY file_id
            ''', conn)
            conn.close()
            
            if df.empty:
                return {'status': 'failed', 'message': '無有效樣本'}
            
            # 按照情緒和年齡群組進行分層抽樣
            splits = {'train': [], 'val': [], 'test': []}
            
            for emotion in df['emotion'].unique():
                for age_group in df['age_group'].unique():
                    subset = df[(df['emotion'] == emotion) & (df['age_group'] == age_group)]
                    
                    if len(subset) == 0:
                        continue
                    
                    # 計算分割點
                    n_samples = len(subset)
                    n_train = int(n_samples * train_ratio)
                    n_val = int(n_samples * val_ratio)
                    
                    # 隨機打亂
                    subset = subset.sample(frac=1, random_state=42).reset_index(drop=True)
                    
                    # 分割
                    splits['train'].extend(subset.iloc[:n_train]['file_id'].tolist())
                    splits['val'].extend(subset.iloc[n_train:n_train+n_val]['file_id'].tolist())
                    splits['test'].extend(subset.iloc[n_train+n_val:]['file_id'].tolist())
            
            # 儲存分割結果
            split_info = {
                'train': {
                    'file_ids': splits['train'],
                    'count': len(splits['train']),
                    'duration': self.calculate_split_duration(splits['train'])
                },
                'val': {
                    'file_ids': splits['val'],
                    'count': len(splits['val']),
                    'duration': self.calculate_split_duration(splits['val'])
                },
                'test': {
                    'file_ids': splits['test'],
                    'count': len(splits['test']),
                    'duration': self.calculate_split_duration(splits['test'])
                },
                'split_at': datetime.now().isoformat()
            }
            
            # 儲存到檔案
            with open('dataset_splits.json', 'w', encoding='utf-8') as f:
                json.dump(split_info, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"資料集分割完成: 訓練集 {len(splits['train'])}, 驗證集 {len(splits['val'])}, 測試集 {len(splits['test'])}")
            
            return {
                'status': 'success',
                'splits': split_info
            }
            
        except Exception as e:
            self.logger.error(f"資料集分割失敗: {str(e)}")
            return {'status': 'failed', 'message': str(e)}
    
    def calculate_split_duration(self, file_ids: List[str]) -> float:
        """計算分割的總時長"""
        try:
            conn = sqlite3.connect(self.validator.db_path)
            cursor = conn.cursor()
            
            placeholders = ','.join(['?' for _ in file_ids])
            cursor.execute(f'SELECT SUM(duration) FROM voice_samples WHERE file_id IN ({placeholders})', file_ids)
            
            total_duration = cursor.fetchone()[0] or 0.0
            conn.close()
            
            return total_duration
            
        except Exception as e:
            self.logger.error(f"計算分割時長失敗: {str(e)}")
            return 0.0

# 使用範例和命令列介面
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='批量驗證語音資料集')
    parser.add_argument('--audio_dir', required=True, help='音頻檔案目錄')
    parser.add_argument('--annotation_file', required=True, help='標註檔案路徑')
    parser.add_argument('--workers', type=int, default=4, help='並行處理數量')
    parser.add_argument('--output_report', default='validation_report.json', help='輸出報告路徑')
    parser.add_argument('--split_dataset', action='store_true', help='是否分割資料集')
    
    args = parser.parse_args()
    
    # 初始化處理器
    validator = VoiceDatasetValidator()
    processor = BatchValidationProcessor(validator, max_workers=args.workers)
    
    # 批量處理
    result = processor.process_directory(args.audio_dir, args.annotation_file)
    print(f"處理結果: {result}")
    
    # 生成報告
    processor.generate_processing_report(args.output_report)
    
    # 分割資料集
    if args.split_dataset:
        splitter = DatasetSplitter(validator)
        split_result = splitter.split_dataset()
        print(f"分割結果: {split_result}")
    
    print("批量處理完成！")