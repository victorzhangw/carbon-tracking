# 高齡語音資料集驗證與日誌系統使用指南

## 📋 系統概述

本系統專為高齡語音資料集的建構、驗證與品質控管而設計，提供完整的資料處理流程、多層次驗證機制、即時監控儀表板和詳細的日誌記錄功能。

### 🎯 核心功能

1. **語音資料驗證**: 音頻品質、逐字稿準確性、標註完整性驗證
2. **品質控管**: 多輪審核機制、標註一致性檢查、資料平衡性分析
3. **即時監控**: Web 儀表板、品質警告、趨勢分析
4. **批量處理**: 多進程並行驗證、大規模資料集處理
5. **資料分割**: 訓練/驗證/測試集智能分割
6. **日誌系統**: 完整的操作記錄、錯誤追蹤、統計報告

---

## 🚀 快速開始

### 1. 環境準備

```bash
# 安裝依賴套件
pip install librosa pandas numpy sqlite3 streamlit plotly tqdm

# 創建工作目錄
mkdir voice_dataset_validation
cd voice_dataset_validation

# 複製系統檔案
cp voice_dataset_validation_system.py .
cp dataset_validation_dashboard.py .
cp batch_validation_processor.py .
```

### 2. 初始化系統

```python
from voice_dataset_validation_system import VoiceDatasetValidator, DatasetQualityMonitor

# 初始化驗證器
validator = VoiceDatasetValidator()
monitor = DatasetQualityMonitor(validator)

print("✅ 系統初始化完成")
```

### 3. 啟動監控儀表板

```bash
# 啟動 Streamlit 儀表板
streamlit run dataset_validation_dashboard.py

# 瀏覽器開啟 http://localhost:8501
```

---

## 📊 資料格式規範

### 標註檔案格式

支援 CSV、JSON、Excel 三種格式，必須包含以下欄位：

#### CSV 格式範例

```csv
file_path,transcript,speaker_id,speaker_type,emotion,intent,age_group,gender,quality_score,slots
./audio/sample_001.wav,您好請問有什麼可以幫助您的嗎,agent_001,agent,neutral,greeting,middle,female,0.85,"{""greeting_type"": ""formal""}"
./audio/sample_002.wav,我想查詢我的訂單狀態,customer_001,customer,neutral,query,elderly,male,0.78,"{""query_type"": ""order_status""}"
```

#### JSON 格式範例

```json
[
  {
    "file_path": "./audio/sample_001.wav",
    "transcript": "您好，請問有什麼可以幫助您的嗎？",
    "speaker_id": "agent_001",
    "speaker_type": "agent",
    "emotion": "neutral",
    "intent": "greeting",
    "age_group": "middle",
    "gender": "female",
    "quality_score": 0.85,
    "slots": {
      "greeting_type": "formal"
    }
  }
]
```

### 必要欄位說明

| 欄位名稱      | 資料類型 | 說明         | 可選值                                                   |
| ------------- | -------- | ------------ | -------------------------------------------------------- |
| file_path     | string   | 音頻檔案路徑 | 相對或絕對路徑                                           |
| transcript    | string   | 逐字稿內容   | 2-500 字中文                                             |
| speaker_id    | string   | 語者識別碼   | 唯一識別碼                                               |
| speaker_type  | string   | 語者類型     | agent, customer                                          |
| emotion       | string   | 情緒標註     | neutral, happy, sad, angry, anxious, frustrated          |
| intent        | string   | 意圖標註     | query, complaint, consultation, booking, thanks, goodbye |
| age_group     | string   | 年齡群組     | young, middle, elderly                                   |
| gender        | string   | 性別         | male, female                                             |
| quality_score | float    | 品質分數     | 0.0-1.0                                                  |
| slots         | object   | 槽位資訊     | JSON 格式的鍵值對                                        |

---

## 🔧 系統使用方法

### 1. 單個樣本驗證

```python
from voice_dataset_validation_system import VoiceDataSample, VoiceDatasetValidator
from datetime import datetime

# 創建語音樣本
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

# 驗證並添加樣本
validator = VoiceDatasetValidator()
success = validator.add_sample(sample)

if success:
    print("✅ 樣本驗證通過並已添加")
else:
    print("❌ 樣本驗證失敗")
```

### 2. 批量處理

```python
from batch_validation_processor import BatchValidationProcessor

# 初始化批量處理器
validator = VoiceDatasetValidator()
processor = BatchValidationProcessor(validator, max_workers=4)

# 處理整個目錄
result = processor.process_directory(
    audio_dir="./audio_files",
    annotation_file="./annotations.csv"
)

print(f"處理結果: {result}")
```

### 3. 命令列批量處理

```bash
# 批量驗證語音資料集
python batch_validation_processor.py \
    --audio_dir ./audio_files \
    --annotation_file ./annotations.csv \
    --workers 8 \
    --output_report validation_report.json \
    --split_dataset

# 參數說明:
# --audio_dir: 音頻檔案目錄
# --annotation_file: 標註檔案路徑
# --workers: 並行處理數量
# --output_report: 輸出報告路徑
# --split_dataset: 是否自動分割資料集
```

### 4. 資料集分割

```python
from batch_validation_processor import DatasetSplitter

# 初始化分割器
splitter = DatasetSplitter(validator)

# 分割資料集 (80% 訓練, 10% 驗證, 10% 測試)
result = splitter.split_dataset(
    train_ratio=0.8,
    val_ratio=0.1,
    test_ratio=0.1
)

if result['status'] == 'success':
    splits = result['splits']
    print(f"訓練集: {splits['train']['count']} 樣本, {splits['train']['duration']:.1f} 小時")
    print(f"驗證集: {splits['val']['count']} 樣本, {splits['val']['duration']:.1f} 小時")
    print(f"測試集: {splits['test']['count']} 樣本, {splits['test']['duration']:.1f} 小時")
```

---

## 📈 監控儀表板使用

### 1. 概覽頁面

- **基本統計**: 總樣本數、通過驗證數、通過率、有效時長
- **驗證狀態分佈**: 通過/失敗/待處理的比例
- **品質分數分佈**: 樣本品質分數的直方圖

### 2. 分佈分析頁面

- **多維度分佈**: 情緒、意圖、年齡、性別的分佈圓餅圖
- **平衡性分析**: 各維度的平衡比例和建議
- **詳細分佈圖**: 各類別的樣本數量柱狀圖

### 3. 品質監控頁面

- **品質警告**: 自動檢測的品質問題和改進建議
- **驗證趨勢**: 每日驗證通過/失敗的趨勢圖
- **常見錯誤**: 最常出現的驗證錯誤類型統計

### 4. 樣本詳情頁面

- **篩選功能**: 按驗證狀態、情緒類型、年齡群組篩選
- **樣本列表**: 詳細的樣本資訊表格
- **匯出功能**: 將篩選結果匯出為 CSV 檔案

### 5. 驗證日誌頁面

- **日誌統計**: 總日誌數、成功/失敗驗證數
- **日誌類型分佈**: 不同驗證類型的分佈
- **最近日誌**: 最新的驗證操作記錄

---

## 🔍 驗證標準與規則

### 音頻檔案驗證

```python
validation_criteria = {
    'min_duration': 0.5,      # 最短 0.5 秒
    'max_duration': 60.0,     # 最長 60 秒
    'min_sample_rate': 16000, # 最低採樣率 16kHz
    'max_file_size': 50 * 1024 * 1024,  # 最大 50MB
    'min_quality_score': 0.7  # 最低品質分數 0.7
}
```

### 逐字稿驗證

- **長度限制**: 2-500 字
- **中文字符**: 至少包含 2 個中文字符
- **特殊字符**: 特殊字符比例不超過 30%
- **內容檢查**: 不能為空或只包含空白字符

### 標註驗證

- **情緒標註**: 必須在預定義的情緒類別中
- **意圖標註**: 必須在預定義的意圖類別中
- **槽位資訊**: 必須為有效的 JSON 格式
- **必要欄位**: 語者 ID、語者類型、年齡群組、性別不能為空

---

## 📊 品質控管機制

### 1. 多輪審核機制

```python
class QualityControlSystem:
    def __init__(self):
        self.cross_annotation_ratio = 0.10    # 10% 交叉標註
        self.expert_review_ratio = 0.05       # 5% 專家審核
        self.quality_thresholds = {
            'werr': 0.05,    # 字錯率 < 5%
            'kappa': 0.85,   # Kappa 系數 > 0.85
            'f1': 0.90       # F1 分數 > 0.90
        }
```

### 2. 標註一致性評估

- **字錯率 (WERR)**: 逐字稿標註的錯誤率
- **Kappa 系數**: 標註人員間的一致性
- **F1 分數**: 意圖和槽位標註的準確性

### 3. 資料平衡性檢查

- **情緒平衡**: 各情緒類別的樣本比例
- **年齡平衡**: 不同年齡群組的分佈
- **性別平衡**: 男女語者的比例
- **意圖平衡**: 各意圖類別的覆蓋度

### 4. 品質警告系統

```python
# 自動生成的品質警告類型
alert_types = {
    'low_pass_rate': '驗證通過率過低',
    'low_quality_score': '平均品質分數偏低',
    'data_imbalance': '資料分佈不平衡',
    'annotation_inconsistency': '標註一致性不足'
}
```

---

## 📝 日誌系統

### 1. 驗證日誌

每次驗證操作都會記錄：

- **檔案 ID**: 被驗證的樣本識別碼
- **驗證類型**: sample_validation, audio_validation 等
- **驗證狀態**: passed, failed
- **錯誤訊息**: 詳細的錯誤描述
- **時間戳記**: 驗證執行時間

### 2. 操作日誌

系統操作記錄包括：

- **樣本添加**: 新樣本的添加記錄
- **批量處理**: 批量驗證的進度和結果
- **資料分割**: 資料集分割的執行記錄
- **報告生成**: 各種報告的生成時間

### 3. 日誌查詢

```python
# 查詢特定樣本的驗證日誌
def get_sample_logs(file_id: str):
    conn = sqlite3.connect('voice_dataset.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM validation_logs
    WHERE file_id = ?
    ORDER BY timestamp DESC
    ''', [file_id])

    logs = cursor.fetchall()
    conn.close()

    return logs
```

---

## 📈 統計報告

### 1. 驗證報告

```python
# 生成完整的驗證報告
report = validator.get_validation_report()

# 報告內容包括:
{
    'summary': {
        'total_samples': 1000,
        'passed_samples': 950,
        'failed_samples': 50,
        'pass_rate': 0.95,
        'total_duration_hours': 12.5,
        'avg_quality_score': 0.82
    },
    'distributions': {
        'emotion': {'neutral': 400, 'happy': 200, ...},
        'intent': {'query': 300, 'complaint': 150, ...},
        'age_group': {'elderly': 600, 'middle': 300, ...},
        'gender': {'female': 520, 'male': 480}
    },
    'common_errors': [
        ('音頻過短: 0.3 秒', 15),
        ('逐字稿為空', 12),
        ...
    ]
}
```

### 2. 品質監控報告

```python
# 生成品質監控報告
alerts = monitor.generate_quality_alerts()
balance_report = monitor.check_data_balance()

# 品質警告範例:
[
    {
        'type': 'low_pass_rate',
        'severity': 'high',
        'message': '驗證通過率過低: 85%',
        'recommendation': '檢查資料品質和標註流程'
    }
]
```

---

## 🛠️ 進階配置

### 1. 自定義驗證標準

```python
# 修改驗證標準
validator.validation_criteria.update({
    'min_duration': 1.0,      # 提高最短時長要求
    'max_duration': 30.0,     # 降低最長時長限制
    'min_quality_score': 0.8  # 提高品質分數要求
})
```

### 2. 擴展情緒和意圖類別

```python
# 添加新的情緒類別
validator.validation_criteria['required_emotions'].extend([
    'confused', 'satisfied', 'impatient'
])

# 添加新的意圖類別
validator.validation_criteria['required_intents'].extend([
    'cancel', 'refund', 'upgrade'
])
```

### 3. 自定義品質檢查

```python
def custom_quality_check(sample: VoiceDataSample) -> Tuple[bool, List[str]]:
    """自定義品質檢查函數"""
    errors = []

    # 檢查高齡語音特殊要求
    if sample.age_group == 'elderly':
        if sample.duration < 2.0:
            errors.append("高齡語音樣本時長應不少於 2 秒")

        if sample.quality_score < 0.75:
            errors.append("高齡語音樣本品質分數應不低於 0.75")

    return len(errors) == 0, errors

# 整合自定義檢查
validator.custom_checks.append(custom_quality_check)
```

---

## 🚨 故障排除

### 常見問題與解決方案

#### 1. 音頻載入失敗

**問題**: `音頻載入失敗: No such file or directory`

**解決方案**:

- 檢查音頻檔案路徑是否正確
- 確認檔案格式是否支援 (WAV, MP3, M4A, FLAC)
- 檢查檔案是否損壞

#### 2. 資料庫連接錯誤

**問題**: `database is locked`

**解決方案**:

```python
# 確保正確關閉資料庫連接
try:
    conn = sqlite3.connect('voice_dataset.db')
    # 執行操作
finally:
    conn.close()
```

#### 3. 記憶體不足

**問題**: 批量處理時記憶體不足

**解決方案**:

```python
# 減少並行處理數量
processor = BatchValidationProcessor(validator, max_workers=2)

# 或分批處理
def process_in_batches(samples, batch_size=100):
    for i in range(0, len(samples), batch_size):
        batch = samples[i:i+batch_size]
        processor.validate_sample_batch(batch)
```

#### 4. 儀表板無法啟動

**問題**: Streamlit 儀表板啟動失敗

**解決方案**:

```bash
# 檢查依賴套件
pip install streamlit plotly pandas

# 檢查埠號是否被佔用
streamlit run dataset_validation_dashboard.py --server.port 8502
```

---

## 📚 API 參考

### VoiceDatasetValidator 類別

#### 主要方法

```python
class VoiceDatasetValidator:
    def __init__(self, db_path: str = "voice_dataset.db")
    def validate_sample(self, sample: VoiceDataSample) -> Tuple[bool, List[str]]
    def add_sample(self, sample: VoiceDataSample) -> bool
    def get_validation_report(self) -> Dict
    def export_failed_samples(self, output_path: str) -> bool
```

### DatasetQualityMonitor 類別

#### 主要方法

```python
class DatasetQualityMonitor:
    def __init__(self, validator: VoiceDatasetValidator)
    def check_data_balance(self) -> Dict
    def generate_quality_alerts(self) -> List[Dict]
```

### BatchValidationProcessor 類別

#### 主要方法

```python
class BatchValidationProcessor:
    def __init__(self, validator: VoiceDatasetValidator, max_workers: int = None)
    def process_annotation_file(self, annotation_file: str) -> List[VoiceDataSample]
    def process_directory(self, audio_dir: str, annotation_file: str) -> Dict
    def generate_processing_report(self, output_path: str) -> bool
```

---

## 📞 技術支援

如有任何問題或建議，請聯繫開發團隊：

- **技術文檔**: 參考本指南和程式碼註釋
- **問題回報**: 提供詳細的錯誤訊息和重現步驟
- **功能建議**: 歡迎提出改進建議和新功能需求

---

**系統版本**: v1.0  
**最後更新**: 2024 年 12 月 5 日  
**維護團隊**: AI 語音資料處理小組
