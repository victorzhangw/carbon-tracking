# AI 客服系統 - 模型儲存與部署完整指南

## 📋 文件概述

本指南提供 AI 客服語音克隆系統的完整模型儲存與部署解決方案，涵蓋本地端部署、雲端部署、混合架構等多種方案。

## 🎯 目標讀者

- **系統管理員**: 負責系統部署和維護
- **DevOps 工程師**: 負責自動化部署和監控
- **技術主管**: 需要了解技術架構和決策依據
- **IT 決策者**: 需要評估不同部署方案的成本效益

---

## 🏗️ 模型儲存架構設計

### 模型分類與特性

#### 1. 情緒識別模型

- **基礎版本**: scikit-learn 模型，檔案大小 ~50MB
- **進階版本**: Wav2Vec2 模型，檔案大小 ~1.2GB
- **更新頻率**: 每月一次模型優化
- **載入時間**: 基礎版 2 秒，進階版 15 秒

#### 2. 語音克隆模型

- **GPT 模型**: 語義理解，檔案大小 ~800MB
- **SoVITS 模型**: 聲學合成，檔案大小 ~600MB
- **參考音頻**: 每位客服 20-50 個樣本，總計 ~100MB
- **更新頻率**: 新增客服時訓練，每季度微調

#### 3. 預訓練模型

- **基礎預訓練模型**: 3 個檔案，總計 ~2.5GB
- **更新頻率**: 每半年更新一次
- **共享性**: 所有客服共用基礎模型

#

## 儲存需求分析

```
總儲存需求估算 (10位客服專員):
├── 預訓練模型: 2.5GB (共用)
├── 情緒識別模型: 1.25GB (共用)
├── 個人化語音模型: 14GB (10 × 1.4GB)
├── 訓練資料: 5GB (音頻樣本)
├── 快取和日誌: 2GB
└── 總計: ~25GB
```

---

## 💻 本地端部署方案

### 架構優勢

- **完全控制**: 數據和模型完全在本地
- **低延遲**: 無網路傳輸延遲
- **成本可控**: 無雲端服務費用
- **隱私保護**: 敏感數據不離開本地環境

### 硬體需求

#### 最低配置

- **CPU**: Intel i5-8400 或 AMD Ryzen 5 2600
- **記憶體**: 16GB DDR4
- **儲存**: 500GB SSD
- **GPU**: NVIDIA GTX 1060 6GB (可選)

#### 推薦配置

- **CPU**: Intel i7-10700K 或 AMD Ryzen 7 3700X
- **記憶體**: 32GB DDR4
- **儲存**: 1TB NVMe SSD
- **GPU**: NVIDIA RTX 3070 8GB

#### 企業級配置

- **CPU**: Intel Xeon E-2288G 或 AMD EPYC 7302P
- **記憶體**: 64GB ECC DDR4
- **儲存**: 2TB NVMe SSD + 4TB HDD
- **GPU**: NVIDIA RTX A4000 16GB#

## 本地端儲存架構

````python
# 本地端模型管理系統
class LocalModelManager:
    def __init__(self, base_path="./models"):
        self.base_path = base_path
        self.config = {
            'model_storage': {
                'base_path': base_path,
                'max_model_size': '2GB',
                'backup_enabled': True,
                'backup_interval': '24h',
                'cleanup_old_models': True,
                'max_model_versions': 5
            },
            'cache': {
                'enabled': True,
                'max_size': '1GB',
                'ttl': 3600  # 1小時
            }
        }
        self.setup_directories()

    def setup_directories(self):
        """初始化目錄結構"""
        directories = [
            f"{self.base_path}/emotion_recognition/basic",
            f"{self.base_path}/emotion_recognition/advanced",
            f"{self.base_path}/gpt_sovits/pretrained",
            f"{self.base_path}/gpt_sovits/fine_tuned",
            f"{self.base_path}/cache/embeddings",
            f"{self.base_path}/cache/inference_cache",
            f"{self.base_path}/backups",
            "./audio_uploads",
            "./voice_output",
            "./logs"
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def save_emotion_model(self, model_type, model_data, metadata):
        """儲存情緒識別模型"""
        model_dir = f"{self.base_path}/emotion_recognition/{model_type}"

        # 創建版本化儲存
        version = metadata.get('version', '1.0.0')
        versioned_dir = f"{model_dir}/v{version}"
        os.makedirs(versioned_dir, exist_ok=True)

        if model_type == "basic":
            # 儲存 scikit-learn 模型
            joblib.dump(model_data['model'], f"{versioned_dir}/model.pkl")
            joblib.dump(model_data['scaler'], f"{versioned_dir}/scaler.pkl")
        elif model_type == "advanced":
            # 儲存 PyTorch 模型
            model_data['model'].save_pretrained(versioned_dir)
            model_data['tokenizer'].save_pretrained(versioned_dir)

        # 儲存元數據
        metadata['saved_at'] = datetime.now().isoformat()
        metadata['file_size'] = self._get_directory_size(versioned_dir)

        with open(f"{versioned_dir}/metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # 創建符號連結到最新版本
        latest_link = f"{model_dir}/latest"
        if os.path.exists(latest_link):
            os.remove(latest_link)
        os.symlink(versioned_dir, latest_link)

        # 清理舊版本
        self._cleanup_old_versions(model_dir)

        return versioned_dir
```    def
 save_voice_model(self, staff_code, model_data, metadata):
        """儲存語音克隆模型"""
        model_dir = f"{self.base_path}/gpt_sovits/fine_tuned/{staff_code}"

        # 創建版本化儲存
        version = metadata.get('version', '1.0.0')
        versioned_dir = f"{model_dir}/v{version}"
        os.makedirs(versioned_dir, exist_ok=True)

        # 儲存模型檔案
        model_files = {
            'gpt_model.ckpt': model_data['gpt_model'],
            'sovits_model.pth': model_data['sovits_model'],
            'reference_audio.wav': model_data['reference_audio']
        }

        for filename, source_path in model_files.items():
            target_path = f"{versioned_dir}/{filename}"
            shutil.copy2(source_path, target_path)

        # 儲存配置和元數據
        config_data = {
            'staff_code': staff_code,
            'model_config': model_data.get('config', {}),
            'training_params': model_data.get('training_params', {}),
            'performance_metrics': model_data.get('metrics', {})
        }

        with open(f"{versioned_dir}/config.json", 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        # 更新元數據
        metadata.update({
            'saved_at': datetime.now().isoformat(),
            'file_size': self._get_directory_size(versioned_dir),
            'model_files': list(model_files.keys())
        })

        with open(f"{versioned_dir}/metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # 創建符號連結到最新版本
        latest_link = f"{model_dir}/latest"
        if os.path.exists(latest_link):
            os.remove(latest_link)
        os.symlink(versioned_dir, latest_link)

        # 更新資料庫記錄
        self._update_model_database_record(staff_code, versioned_dir, metadata)

        return versioned_dir

    def load_voice_model(self, staff_code, version='latest'):
        """載入語音克隆模型"""
        if version == 'latest':
            model_dir = f"{self.base_path}/gpt_sovits/fine_tuned/{staff_code}/latest"
        else:
            model_dir = f"{self.base_path}/gpt_sovits/fine_tuned/{staff_code}/v{version}"

        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"找不到 {staff_code} 的語音模型版本 {version}")

        # 載入模型檔案路徑
        model_data = {
            'gpt_model': f"{model_dir}/gpt_model.ckpt",
            'sovits_model': f"{model_dir}/sovits_model.pth",
            'reference_audio': f"{model_dir}/reference_audio.wav"
        }

        # 載入配置和元數據
        with open(f"{model_dir}/config.json", 'r', encoding='utf-8') as f:
            model_data['config'] = json.load(f)

        with open(f"{model_dir}/metadata.json", 'r', encoding='utf-8') as f:
            model_data['metadata'] = json.load(f)

        return model_data
   def _cleanup_old_versions(self, model_dir):
        """清理舊版本模型"""
        max_versions = self.config['model_storage']['max_model_versions']

        # 獲取所有版本目錄
        version_dirs = []
        for item in os.listdir(model_dir):
            if item.startswith('v') and os.path.isdir(f"{model_dir}/{item}"):
                version_dirs.append(item)

        # 按版本號排序
        version_dirs.sort(key=lambda x: version.parse(x[1:]), reverse=True)

        # 刪除超出限制的舊版本
        for old_version in version_dirs[max_versions:]:
            old_path = f"{model_dir}/{old_version}"
            shutil.rmtree(old_path)
            print(f"已刪除舊版本: {old_path}")

    def _get_directory_size(self, directory):
        """計算目錄大小"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size

    def backup_models(self):
        """備份所有模型"""
        backup_dir = f"{self.base_path}/backups/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)

        # 備份模型目錄
        shutil.copytree(f"{self.base_path}/emotion_recognition",
                       f"{backup_dir}/emotion_recognition")
        shutil.copytree(f"{self.base_path}/gpt_sovits",
                       f"{backup_dir}/gpt_sovits")

        # 創建備份清單
        backup_info = {
            'backup_time': datetime.now().isoformat(),
            'backup_size': self._get_directory_size(backup_dir),
            'models_included': self.list_all_models()
        }

        with open(f"{backup_dir}/backup_info.json", 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)

        return backup_dir

    def restore_from_backup(self, backup_path):
        """從備份恢復模型"""
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"備份路徑不存在: {backup_path}")

        # 創建當前狀態的備份
        current_backup = self.backup_models()
        print(f"已創建當前狀態備份: {current_backup}")

        try:
            # 恢復模型
            if os.path.exists(f"{backup_path}/emotion_recognition"):
                shutil.rmtree(f"{self.base_path}/emotion_recognition")
                shutil.copytree(f"{backup_path}/emotion_recognition",
                               f"{self.base_path}/emotion_recognition")

            if os.path.exists(f"{backup_path}/gpt_sovits"):
                shutil.rmtree(f"{self.base_path}/gpt_sovits")
                shutil.copytree(f"{backup_path}/gpt_sovits",
                               f"{self.base_path}/gpt_sovits")

            print(f"已成功從備份恢復: {backup_path}")

        except Exception as e:
            print(f"恢復失敗，正在回滾: {e}")
            # 回滾到恢復前的狀態
            self.restore_from_backup(current_backup)
            raise###
 本地端部署配置

```python
# 本地部署配置管理
class LocalDeploymentConfig:
    def __init__(self):
        self.config = {
            # 模型儲存配置
            'model_storage': {
                'base_path': './models',
                'max_model_size': '2GB',
                'backup_enabled': True,
                'backup_interval': '24h',
                'cleanup_old_models': True,
                'max_model_versions': 5,
                'compression_enabled': True,
                'encryption_enabled': False
            },

            # 推理服務配置
            'inference': {
                'max_concurrent_requests': 4,
                'model_cache_size': '1GB',
                'gpu_memory_fraction': 0.8,
                'cpu_threads': 4,
                'timeout': 60,
                'batch_size': 1,
                'warm_up_enabled': True
            },

            # 檔案儲存配置
            'file_storage': {
                'audio_upload_path': './audio_uploads',
                'voice_output_path': './voice_output',
                'temp_path': './temp',
                'max_file_size': '50MB',
                'allowed_formats': ['wav', 'mp3', 'm4a', 'flac'],
                'auto_cleanup': True,
                'cleanup_interval': '7d'
            },

            # 監控配置
            'monitoring': {
                'enabled': True,
                'log_level': 'INFO',
                'metrics_collection': True,
                'performance_tracking': True,
                'error_reporting': True
            }
        }

    def get_model_path(self, model_type, staff_code=None, version='latest'):
        """獲取模型路徑"""
        base_path = self.config['model_storage']['base_path']

        if model_type == 'emotion':
            return f"{base_path}/emotion_recognition/{version}"
        elif model_type == 'voice' and staff_code:
            return f"{base_path}/gpt_sovits/fine_tuned/{staff_code}/{version}"
        elif model_type == 'pretrained':
            return f"{base_path}/gpt_sovits/pretrained"
        else:
            return base_path

    def validate_hardware_requirements(self):
        """驗證硬體需求"""
        import psutil
        import GPUtil

        requirements = {
            'cpu_cores': 4,
            'memory_gb': 16,
            'disk_space_gb': 100,
            'gpu_memory_gb': 6
        }

        # 檢查 CPU
        cpu_cores = psutil.cpu_count(logical=False)
        if cpu_cores < requirements['cpu_cores']:
            print(f"警告: CPU 核心數不足 ({cpu_cores} < {requirements['cpu_cores']})")

        # 檢查記憶體
        memory_gb = psutil.virtual_memory().total / (1024**3)
        if memory_gb < requirements['memory_gb']:
            print(f"警告: 記憶體不足 ({memory_gb:.1f}GB < {requirements['memory_gb']}GB)")

        # 檢查磁碟空間
        disk_space_gb = psutil.disk_usage('.').free / (1024**3)
        if disk_space_gb < requirements['disk_space_gb']:
            print(f"警告: 磁碟空間不足 ({disk_space_gb:.1f}GB < {requirements['disk_space_gb']}GB)")

        # 檢查 GPU
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_memory_gb = gpus[0].memoryTotal / 1024
                if gpu_memory_gb < requirements['gpu_memory_gb']:
                    print(f"警告: GPU 記憶體不足 ({gpu_memory_gb:.1f}GB < {requirements['gpu_memory_gb']}GB)")
            else:
                print("警告: 未檢測到 GPU，將使用 CPU 進行推理")
        except:
            print("無法檢測 GPU 狀態")

        return True
```###
本地端安裝部署步驟

#### 1. 環境準備

```bash
# 1. 檢查 Python 版本
python --version  # 需要 Python 3.10+

# 2. 創建虛擬環境
python -m venv ai_customer_service_env
source ai_customer_service_env/bin/activate  # Linux/Mac
# 或
ai_customer_service_env\Scripts\activate  # Windows

# 3. 升級 pip
python -m pip install --upgrade pip

# 4. 安裝 CUDA (如果有 NVIDIA GPU)
# 下載並安裝 CUDA 11.8 或 12.1
# https://developer.nvidia.com/cuda-downloads
````

#### 2. 系統安裝

```bash
# 1. 克隆專案
git clone https://github.com/your-repo/ai-customer-service.git
cd ai-customer-service

# 2. 安裝後端依賴
pip install -r requirements.txt

# 3. 安裝額外的 GPU 支援 (可選)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 4. 初始化資料庫
python database_emotion_extension.py

# 5. 下載預訓練模型
python scripts/download_pretrained_models.py

# 6. 安裝前端依賴
cd webpage/ai-customer-service-frontend
npm install
npm run build
cd ../..
```

#### 3. 配置設定

```python
# config/local_config.py
LOCAL_CONFIG = {
    'database': {
        'url': 'sqlite:///ai_customer_service.db',
        'echo': False
    },
    'models': {
        'base_path': './models',
        'cache_enabled': True,
        'gpu_enabled': True,
        'batch_size': 1
    },
    'storage': {
        'audio_upload_path': './audio_uploads',
        'voice_output_path': './voice_output',
        'max_file_size': 50 * 1024 * 1024  # 50MB
    },
    'security': {
        'jwt_secret_key': 'your-secret-key-here',
        'jwt_expiration_hours': 24
    }
}
```

#### 4. 啟動服務

```bash
# 1. 啟動後端服務
python app.py

# 2. 驗證服務狀態
curl http://localhost:5000/health

# 3. 測試 API 端點
curl -X POST http://localhost:5000/api/emotion/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "測試情緒分析"}'
```

#### 5. 系統驗證

````python
# scripts/system_validation.py
import requests
import json

def validate_system():
    """驗證系統各項功能"""
    base_url = "http://localhost:5000"

    # 1. 健康檢查
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    print("✓ 健康檢查通過")

    # 2. 情緒分析測試
    emotion_data = {"text": "我很開心今天的服務"}
    response = requests.post(f"{base_url}/api/emotion/analyze",
                           json=emotion_data)
    assert response.status_code == 200
    print("✓ 情緒分析功能正常")

    # 3. 模型列表測試
    response = requests.get(f"{base_url}/api/models/list")
    assert response.status_code == 200
    print("✓ 模型管理功能正常")

    print("系統驗證完成！")

if __name__ == "__main__":
    validate_system()
```---

##
 ☁️ 雲端部署方案 (Google Cloud Platform)

### 架構優勢
- **無限擴展**: 支援大量並發用戶
- **高可用性**: 99.9% 以上的服務可用性
- **自動化管理**: 減少維護工作量
- **企業級安全**: Google 的安全基礎設施
- **成本優化**: 按需付費，可搶占實例

### GCP 服務架構

```yaml
# GCP 服務組件
GCP_Services:
  Compute:
    - Google Kubernetes Engine (GKE)     # 容器編排平台
    - Compute Engine (GPU instances)     # GPU 運算實例
    - Cloud Run                          # 無伺服器容器服務
    - Cloud Functions                    # 事件驅動函數

  Storage:
    - Cloud Storage                      # 物件儲存 (模型檔案)
    - Cloud SQL (PostgreSQL)            # 關聯式資料庫
    - Cloud Firestore                   # NoSQL 文檔資料庫
    - Persistent Disk                    # 持久化區塊儲存
    - Cloud Memorystore                  # Redis 快取服務

  AI_ML:
    - Vertex AI                          # 統一機器學習平台
    - AI Platform Prediction            # 模型推理服務
    - AutoML                             # 自動機器學習
    - Speech-to-Text API                 # 語音識別服務
    - Text-to-Speech API                 # 語音合成服務

  Networking:
    - Cloud Load Balancer                # 負載均衡器
    - Cloud CDN                          # 內容分發網路
    - VPC                                # 虛擬私有雲
    - Cloud NAT                          # 網路位址轉換

  Security:
    - Identity and Access Management     # 身份和存取管理
    - Cloud KMS                          # 金鑰管理服務
    - Cloud Security Command Center     # 安全指揮中心
    - Cloud Armor                        # DDoS 防護

  Monitoring:
    - Cloud Monitoring                   # 系統監控
    - Cloud Logging                      # 日誌管理
    - Cloud Trace                        # 分散式追蹤
    - Cloud Profiler                     # 性能分析
````

### GCP 模型儲存架構

```python
# GCP 模型管理系統
from google.cloud import storage, aiplatform
from google.cloud.sql import connector
import json
import os

class GCPModelManager:
    def __init__(self, project_id, region="us-central1"):
        self.project_id = project_id
        self.region = region
        self.bucket_name = f"{project_id}-ai-models"

        # 初始化 GCP 客戶端
        self.storage_client = storage.Client(project=project_id)
        self.bucket = self._get_or_create_bucket()

        # 初始化 Vertex AI
        aiplatform.init(project=project_id, location=region)

    def _get_or_create_bucket(self):
        """獲取或創建 Cloud Storage bucket"""
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            bucket.reload()
            return bucket
        except:
            # 創建新的 bucket
            bucket = self.storage_client.create_bucket(
                self.bucket_name,
                location=self.region
            )

            # 設置生命週期規則
            lifecycle_rule = {
                'action': {'type': 'Delete'},
                'condition': {
                    'age': 365,  # 365天後刪除
                    'matchesPrefix': ['temp/', 'cache/']
                }
            }
            bucket.lifecycle_rules = [lifecycle_rule]
            bucket.patch()

            return bucket

    def upload_model_to_gcs(self, local_path, gcs_path, metadata=None):
        """上傳模型到 Google Cloud Storage"""
        blob = self.bucket.blob(gcs_path)

        # 設置元數據
        if metadata:
            blob.metadata = metadata

        # 設置快取控制
        blob.cache_control = "public, max-age=3600"

        # 上傳檔案
        blob.upload_from_filename(local_path)

        # 設置公開讀取權限 (如果需要)
        # blob.make_public()

        print(f"模型已上傳到 gs://{self.bucket_name}/{gcs_path}")
        return f"gs://{self.bucket_name}/{gcs_path}"

    def download_model_from_gcs(self, gcs_path, local_path):
        """從 GCS 下載模型"""
        blob = self.bucket.blob(gcs_path)

        # 創建本地目錄
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # 下載檔案
        blob.download_to_filename(local_path)

        print(f"模型已下載到 {local_path}")
        return local_path

    def upload_voice_model(self, staff_code, model_data, metadata):
        """上傳語音克隆模型到 GCS"""
        version = metadata.get('version', '1.0.0')
        base_path = f"voice_models/{staff_code}/v{version}"

        uploaded_files = {}

        # 上傳模型檔案
        model_files = {
            'gpt_model.ckpt': model_data['gpt_model'],
            'sovits_model.pth': model_data['sovits_model'],
            'reference_audio.wav': model_data['reference_audio']
        }

        for filename, local_path in model_files.items():
            gcs_path = f"{base_path}/{filename}"
            uploaded_files[filename] = self.upload_model_to_gcs(
                local_path, gcs_path, metadata
            )

        # 上傳配置檔案
        config_data = {
            'staff_code': staff_code,
            'version': version,
            'model_files': uploaded_files,
            'metadata': metadata
        }

        config_blob = self.bucket.blob(f"{base_path}/config.json")
        config_blob.upload_from_string(
            json.dumps(config_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )

        return uploaded_files    def dep
loy_model_to_vertex_ai(self, model_path, model_name, version):
        """部署模型到 Vertex AI"""

        # 創建模型資源
        model = aiplatform.Model.upload(
            display_name=f"{model_name}-{version}",
            artifact_uri=model_path,
            serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/pytorch-gpu.1-13:latest",
            serving_container_predict_route="/predict",
            serving_container_health_route="/health",
            description=f"AI Customer Service Model - {model_name} v{version}"
        )

        # 創建端點
        endpoint = aiplatform.Endpoint.create(
            display_name=f"{model_name}-endpoint-{version}",
            description=f"Endpoint for {model_name} model"
        )

        # 部署模型到端點
        deployed_model = model.deploy(
            endpoint=endpoint,
            deployed_model_display_name=f"{model_name}-deployed-{version}",
            machine_type="n1-standard-4",
            accelerator_type="NVIDIA_TESLA_T4",
            accelerator_count=1,
            min_replica_count=1,
            max_replica_count=10,
            traffic_percentage=100
        )

        return {
            'model': model,
            'endpoint': endpoint,
            'deployed_model': deployed_model
        }

    def create_model_version(self, model_name, model_path, version_name, description=""):
        """創建新的模型版本"""

        # 上傳模型到 Model Registry
        model = aiplatform.Model.upload(
            display_name=f"{model_name}-{version_name}",
            artifact_uri=model_path,
            serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/pytorch-gpu.1-13:latest",
            version_aliases=[version_name],
            version_description=description,
            is_default_version=True
        )

        return model

    def list_model_versions(self, model_name):
        """列出模型的所有版本"""
        models = aiplatform.Model.list(
            filter=f'display_name="{model_name}"',
            order_by="create_time desc"
        )

        versions = []
        for model in models:
            versions.append({
                'name': model.display_name,
                'version': model.version_id,
                'create_time': model.create_time,
                'update_time': model.update_time,
                'description': model.version_description
            })

        return versions

    def setup_model_monitoring(self, endpoint_name):
        """設置模型監控"""
        from google.cloud import monitoring_v3

        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{self.project_id}"

        # 創建自定義指標
        descriptor = monitoring_v3.MetricDescriptor()
        descriptor.type = f"custom.googleapis.com/ai_service/{endpoint_name}/prediction_latency"
        descriptor.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.GAUGE
        descriptor.value_type = monitoring_v3.MetricDescriptor.ValueType.DOUBLE
        descriptor.description = "AI model prediction latency"

        descriptor = client.create_metric_descriptor(
            name=project_name,
            metric_descriptor=descriptor
        )

        return descriptor
```

### Kubernetes 部署配置

````yaml
# kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ai-customer-service
  labels:
    name: ai-customer-service

---
# kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ai-service-config
  namespace: ai-customer-service
data:
  DATABASE_URL: "postgresql://user:password@postgres-service:5432/ai_service"
  GCS_BUCKET: "your-project-ai-models"
  REDIS_URL: "redis://redis-service:6379"
  MODEL_CACHE_SIZE: "2Gi"
  MAX_CONCURRENT_REQUESTS: "10"

---
# kubernetes/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ai-service-secrets
  namespace: ai-customer-service
type: Opaque
data:
  jwt-secret: <base64-encoded-jwt-secret>
  db-password: <base64-encoded-db-password>
  gcp-service-account: <base64-encoded-service-account-json>

---
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-customer-service-backend
  namespace: ai-customer-service
  labels:
    app: ai-customer-service
    component: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-customer-service
      component: backend
  template:
    metadata:
      labels:
        app: ai-customer-service
        component: backend
    spec:
      containers:
      - name: flask-app
        image: gcr.io/PROJECT_ID/ai-customer-service:latest
        ports:
        - containerPort: 5000
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: ai-service-config
              key: DATABASE_URL
        - name: GCS_BUCKET
          valueFrom:
            configMapKeyRef:
              name: ai-service-config
              key: GCS_BUCKET
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: ai-service-secrets
              key: jwt-secret
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: "/etc/gcp/service-account.json"
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
          limits:
            memory: "8Gi"
            cpu: "4000m"
            nvidia.com/gpu: 1
        volumeMounts:
        - name: gcp-credentials
          mountPath: /etc/gcp
          readOnly: true
        - name: model-cache
          mountPath: /app/models
        - name: temp-storage
          mountPath: /app/temp
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: gcp-credentials
        secret:
          secretName: ai-service-secrets
          items:
          - key: gcp-service-account
            path: service-account.json
      - name: model-cache
        persistentVolumeClaim:
          claimName: model-cache-pvc
      - name: temp-storage
        emptyDir:
          sizeLimit: 10Gi
      nodeSelector:
        cloud.google.com/gke-accelerator: nvidia-tesla-t4
```### 自
動擴展配置

```yaml
# kubernetes/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-customer-service-hpa
  namespace: ai-customer-service
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-customer-service-backend
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: custom.googleapis.com|ai_service|concurrent_requests
      target:
        type: AverageValue
        averageValue: "8"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60

---
# kubernetes/vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: ai-customer-service-vpa
  namespace: ai-customer-service
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-customer-service-backend
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: flask-app
      minAllowed:
        cpu: 1000m
        memory: 2Gi
      maxAllowed:
        cpu: 8000m
        memory: 16Gi
      controlledResources: ["cpu", "memory"]
````

### GCP 成本優化策略

````python
# 成本優化管理系統
class GCPCostOptimizer:
    def __init__(self, project_id, region="us-central1"):
        self.project_id = project_id
        self.region = region

    def setup_preemptible_instances(self):
        """設置可搶占實例以降低成本"""
        node_pool_config = {
            "name": "preemptible-pool",
            "initial_node_count": 1,
            "config": {
                "machine_type": "n1-standard-4",
                "disk_size_gb": 100,
                "disk_type": "pd-ssd",
                "preemptible": True,  # 可搶占實例，成本降低 80%
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/cloud-platform"
                ],
                "metadata": {
                    "disable-legacy-endpoints": "true"
                },
                "labels": {
                    "node-type": "preemptible",
                    "workload": "ai-inference"
                },
                "taints": [
                    {
                        "key": "preemptible",
                        "value": "true",
                        "effect": "NO_SCHEDULE"
                    }
                ]
            },
            "autoscaling": {
                "enabled": True,
                "min_node_count": 0,
                "max_node_count": 10
            },
            "management": {
                "auto_upgrade": True,
                "auto_repair": True
            }
        }
        return node_pool_config

    def setup_spot_instances(self):
        """設置 Spot 實例配置"""
        spot_config = {
            "machine_type": "n1-standard-4",
            "provisioning_model": "SPOT",
            "instance_termination_action": "STOP",
            "max_run_duration": {
                "seconds": 3600  # 1小時最大運行時間
            },
            "scheduling": {
                "preemptible": True,
                "automatic_restart": False,
                "on_host_maintenance": "TERMINATE"
            }
        }
        return spot_config

    def setup_scheduled_scaling(self):
        """設置定時擴展策略"""
        # 工作時間擴展 (週一到週五 8:00-18:00)
        work_hours_schedule = {
            "name": "work-hours-scale-up",
            "schedule": "0 8 * * 1-5",  # 每週一到週五早上8點
            "time_zone": "Asia/Taipei",
            "target": {
                "min_replicas": 5,
                "max_replicas": 20
            },
            "description": "Scale up during work hours"
        }

        # 非工作時間縮減 (週一到週五 18:00-8:00)
        off_hours_schedule = {
            "name": "off-hours-scale-down",
            "schedule": "0 18 * * 1-5",  # 每週一到週五晚上6點
            "time_zone": "Asia/Taipei",
            "target": {
                "min_replicas": 1,
                "max_replicas": 5
            },
            "description": "Scale down during off hours"
        }

        # 週末最小配置
        weekend_schedule = {
            "name": "weekend-minimal",
            "schedule": "0 0 * * 6,0",  # 週六週日午夜
            "time_zone": "Asia/Taipei",
            "target": {
                "min_replicas": 1,
                "max_replicas": 3
            },
            "description": "Minimal scaling for weekends"
        }

        return [work_hours_schedule, off_hours_schedule, weekend_schedule]

    def setup_budget_alerts(self):
        """設置預算警報"""
        budget_config = {
            "display_name": "AI Customer Service Budget",
            "budget_filter": {
                "projects": [f"projects/{self.project_id}"],
                "services": [
                    "services/6F81-5844-456A",  # Compute Engine
                    "services/95FF-2EF5-5EA1",  # Kubernetes Engine
                    "services/A1E8-BE35-7EBC"   # Cloud Storage
                ]
            },
            "amount": {
                "specified_amount": {
                    "currency_code": "USD",
                    "units": 1000  # $1000 USD per month
                }
            },
            "threshold_rules": [
                {
                    "threshold_percent": 0.5,  # 50% 警報
                    "spend_basis": "CURRENT_SPEND"
                },
                {
                    "threshold_percent": 0.8,  # 80% 警報
                    "spend_basis": "CURRENT_SPEND"
                },
                {
                    "threshold_percent": 1.0,  # 100% 警報
                    "spend_basis": "CURRENT_SPEND"
                }
            ]
        }
        return budget_config

    def optimize_storage_costs(self):
        """優化儲存成本"""
        lifecycle_rules = [
            {
                "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
                "condition": {
                    "age": 30,  # 30天後轉為 Nearline
                    "matchesPrefix": ["models/", "backups/"]
                }
            },
            {
                "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
                "condition": {
                    "age": 90,  # 90天後轉為 Coldline
                    "matchesPrefix": ["backups/", "archives/"]
                }
            },
            {
                "action": {"type": "Delete"},
                "condition": {
                    "age": 365,  # 365天後刪除
                    "matchesPrefix": ["temp/", "cache/", "logs/"]
                }
            }
        ]
        return lifecycle_rules
```### GC
P 部署步驟

#### 1. 環境準備

```bash
# 1. 安裝 Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# 2. 初始化 gcloud
gcloud init
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. 啟用必要的 API
gcloud services enable container.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable sql.googleapis.com
gcloud services enable monitoring.googleapis.com

# 4. 安裝 kubectl
gcloud components install kubectl

# 5. 創建 GKE 集群
gcloud container clusters create ai-customer-service-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=10 \
    --machine-type=n1-standard-4 \
    --disk-size=100GB \
    --enable-autorepair \
    --enable-autoupgrade \
    --accelerator type=nvidia-tesla-t4,count=1
````

#### 2. 容器化應用

```dockerfile
# Dockerfile
FROM nvidia/cuda:11.8-devel-ubuntu20.04

# 設置環境變數
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-pip \
    python3.10-dev \
    ffmpeg \
    libsndfile1 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 設置 Python 別名
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# 設置工作目錄
WORKDIR /app

# 複製需求檔案
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 安裝 PyTorch with CUDA support
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 複製應用程式碼
COPY . .

# 創建必要目錄
RUN mkdir -p /app/models /app/audio_uploads /app/voice_output /app/temp /app/logs

# 設置權限
RUN chmod +x /app/scripts/*.py

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 暴露端口
EXPOSE 5000

# 啟動命令
CMD ["python", "app.py"]
```

#### 3. 建構和推送映像

```bash
# 1. 建構 Docker 映像
docker build -t gcr.io/YOUR_PROJECT_ID/ai-customer-service:latest .

# 2. 推送到 Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/ai-customer-service:latest

# 3. 或使用 Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-customer-service:latest .
```

#### 4. 部署到 GKE

```bash
# 1. 獲取集群憑證
gcloud container clusters get-credentials ai-customer-service-cluster --zone=us-central1-a

# 2. 創建命名空間和資源
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/pvc.yaml

# 3. 部署應用
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml

# 4. 設置自動擴展
kubectl apply -f kubernetes/hpa.yaml
kubectl apply -f kubernetes/vpa.yaml

# 5. 驗證部署
kubectl get pods -n ai-customer-service
kubectl get services -n ai-customer-service
kubectl logs -f deployment/ai-customer-service-backend -n ai-customer-service
```

#### 5. 設置監控和日誌

```yaml
# kubernetes/monitoring.yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: ai-customer-service-monitor
  namespace: ai-customer-service
spec:
  selector:
    matchLabels:
      app: ai-customer-service
  endpoints:
    - port: http
      path: /metrics
      interval: 30s

---
apiVersion: logging.coreos.com/v1
kind: ClusterLogForwarder
metadata:
  name: ai-service-logs
  namespace: ai-customer-service
spec:
  outputs:
    - name: gcp-logging
      type: googleCloudLogging
      googleCloudLogging:
        projectId: YOUR_PROJECT_ID
        logId: ai-customer-service
  pipelines:
    - name: application-logs
      inputRefs:
        - application
      outputRefs:
        - gcp-logging
```

---

## 🔄 混合部署架構

### 架構概念

混合部署結合了本地端和雲端的優勢，適合需要逐步遷移到雲端或有特殊合規要求的企業。

### 混合架構設計

````
┌─────────────────────────────────────────────────────────┐
│                    混合架構                              │
├─────────────────────────────────────────────────────────┤
│  本地端 (On-Premises)          │  雲端 (Cloud)          │
│  ├── 敏感數據處理              │  ├── 模型訓練          │
│  ├── 即時推理服務              │  ├── 大規模儲存        │
│  ├── 核心業務邏輯              │  ├── 備份和災難恢復    │
│  └── 低延遲要求服務            │  └── 彈性擴展服務      │
├─────────────────────────────────────────────────────────┤
│              安全連接 (VPN/專線)                         │
└─────────────────────────────────────────────────────────┘
```### 混合部
署實施方案

```python
# 混合部署管理系統
class HybridDeploymentManager:
    def __init__(self, local_config, cloud_config):
        self.local_manager = LocalModelManager(local_config['base_path'])
        self.cloud_manager = GCPModelManager(
            cloud_config['project_id'],
            cloud_config['region']
        )
        self.sync_config = {
            'sync_interval': 3600,  # 1小時同步一次
            'backup_to_cloud': True,
            'model_distribution': 'hybrid',  # local, cloud, hybrid
            'data_residency': 'local'  # 敏感數據保留在本地
        }

    def distribute_models(self, model_type, staff_code=None):
        """智能分配模型到本地或雲端"""
        if model_type == 'emotion':
            # 情緒識別模型保留在本地以降低延遲
            return 'local'
        elif model_type == 'voice':
            # 語音克隆模型根據使用頻率分配
            usage_stats = self._get_model_usage_stats(staff_code)
            if usage_stats['daily_requests'] > 100:
                return 'local'  # 高頻使用保留在本地
            else:
                return 'cloud'  # 低頻使用放在雲端
        elif model_type == 'pretrained':
            # 預訓練模型在雲端儲存，本地快取
            return 'cloud_with_cache'
        else:
            return 'local'

    def sync_models_to_cloud(self):
        """同步本地模型到雲端備份"""
        local_models = self.local_manager.list_all_models()

        for model_info in local_models:
            model_type = model_info['type']
            staff_code = model_info.get('staff_code')
            local_path = model_info['path']

            # 生成雲端路徑
            if staff_code:
                cloud_path = f"backup/{model_type}/{staff_code}/{model_info['version']}"
            else:
                cloud_path = f"backup/{model_type}/{model_info['version']}"

            # 檢查是否需要同步
            if self._should_sync_model(model_info):
                print(f"同步模型到雲端: {local_path} -> {cloud_path}")
                self.cloud_manager.upload_model_to_gcs(
                    local_path, cloud_path, model_info['metadata']
                )

    def load_model_hybrid(self, model_type, staff_code=None, version='latest'):
        """混合模式載入模型"""
        distribution = self.distribute_models(model_type, staff_code)

        if distribution == 'local':
            return self.local_manager.load_voice_model(staff_code, version)
        elif distribution == 'cloud':
            return self._load_from_cloud_with_cache(model_type, staff_code, version)
        elif distribution == 'cloud_with_cache':
            return self._load_with_intelligent_cache(model_type, staff_code, version)
        else:
            raise ValueError(f"未知的分配策略: {distribution}")

    def _load_from_cloud_with_cache(self, model_type, staff_code, version):
        """從雲端載入模型並快取到本地"""
        cache_key = f"{model_type}_{staff_code}_{version}"
        local_cache_path = f"./cache/models/{cache_key}"

        # 檢查本地快取
        if os.path.exists(local_cache_path):
            cache_age = time.time() - os.path.getmtime(local_cache_path)
            if cache_age < 3600:  # 快取有效期 1 小時
                return self._load_from_cache(local_cache_path)

        # 從雲端下載到快取
        if staff_code:
            cloud_path = f"voice_models/{staff_code}/v{version}"
        else:
            cloud_path = f"{model_type}_models/v{version}"

        self.cloud_manager.download_model_from_gcs(cloud_path, local_cache_path)
        return self._load_from_cache(local_cache_path)

    def setup_data_residency_rules(self):
        """設置數據駐留規則"""
        rules = {
            'sensitive_data': {
                'location': 'local_only',
                'encryption': 'required',
                'backup_allowed': False
            },
            'model_data': {
                'location': 'hybrid',
                'encryption': 'optional',
                'backup_allowed': True
            },
            'training_data': {
                'location': 'local_primary',
                'encryption': 'required',
                'backup_allowed': True,
                'backup_location': 'cloud_encrypted'
            },
            'inference_logs': {
                'location': 'local',
                'retention_days': 30,
                'archive_to_cloud': True
            }
        }
        return rules

    def monitor_hybrid_performance(self):
        """監控混合部署性能"""
        metrics = {
            'local_latency': self._measure_local_latency(),
            'cloud_latency': self._measure_cloud_latency(),
            'cache_hit_rate': self._calculate_cache_hit_rate(),
            'sync_status': self._check_sync_status(),
            'cost_breakdown': self._calculate_cost_breakdown()
        }
        return metrics
````

### 混合部署配置檔案

```yaml
# config/hybrid_config.yaml
hybrid_deployment:
  local:
    enabled: true
    base_path: "./models"
    cache_size: "2GB"
    gpu_enabled: true
    services:
      - emotion_recognition
      - real_time_inference
      - sensitive_data_processing

  cloud:
    enabled: true
    provider: "gcp"
    project_id: "your-project-id"
    region: "us-central1"
    services:
      - model_training
      - large_scale_storage
      - backup_and_recovery
      - batch_processing

  sync:
    interval_seconds: 3600
    backup_enabled: true
    compression_enabled: true
    encryption_enabled: true

  data_residency:
    sensitive_data: "local_only"
    model_weights: "hybrid"
    training_data: "local_primary_cloud_backup"
    inference_logs: "local_with_cloud_archive"

  failover:
    enabled: true
    primary: "local"
    secondary: "cloud"
    health_check_interval: 30
    failover_threshold: 3
```

---

## 📊 部署方案比較與選擇

### 詳細比較表

| 特性             | 本地端部署      | 雲端部署 (GCP) | 混合部署      |
| ---------------- | --------------- | -------------- | ------------- |
| **初期投資**     | 中等 ($20K-50K) | 低 ($5K-10K)   | 高 ($30K-80K) |
| **月度運營成本** | 低 ($500-2K)    | 中等 ($2K-10K) | 中等 ($1K-6K) |
| **擴展性**       | 有限 (手動)     | 無限 (自動)    | 高 (智能)     |
| **延遲**         | 極低 (<100ms)   | 低 (100-300ms) | 極低 (<100ms) |
| **可用性**       | 中等 (95-98%)   | 高 (99.9%+)    | 高 (99.5%+)   |
| **安全性**       | 高 (自控)       | 極高 (企業級)  | 極高 (雙重)   |
| **維護複雜度**   | 高              | 低             | 中等          |
| **數據控制**     | 完全            | 有限           | 高            |
| **災難恢復**     | 手動            | 自動           | 自動          |
| **合規性**       | 高              | 中等           | 高            |

### 選擇建議

#### 選擇本地端部署的情況：

- **小型團隊** (5-20 人)
- **預算有限** 的初創企業
- **數據敏感性極高** 的行業 (金融、醫療)
- **網路環境不穩定** 的地區
- **對延遲要求極高** 的應用

#### 選擇雲端部署的情況：

- **大型企業** (100 人以上)
- **快速擴展** 的業務需求
- **全球化服務** 需求
- **有限的 IT 維護能力**
- **需要高可用性** 的關鍵業務

#### 選擇混合部署的情況：

- **中大型企業** (50-500 人)
- **逐步雲端遷移** 策略
- **複雜的合規要求**
- **不同敏感度的數據** 需要分別處理
- **需要最佳性價比** 的方案#

## 遷移路徑建議

#### 階段一：本地端優化 (0-6 個月)

```
目標：建立穩定的本地端系統
├── 完善本地模型管理系統
├── 建立模型版本控制機制
├── 實作基礎監控和備份
├── 優化推理性能
└── 建立運維流程
```

#### 階段二：混合部署 (6-12 個月)

```
目標：逐步引入雲端能力
├── 模型儲存遷移到 Cloud Storage
├── 資料庫遷移到 Cloud SQL
├── 建立雲端備份機制
├── 實作智能快取策略
└── 設置監控和告警
```

#### 階段三：全雲端部署 (12-18 個月)

```
目標：完全雲端化運營
├── 推理服務遷移到 GKE
├── 使用 Vertex AI 進行模型管理
├── 實作自動擴展和成本優化
├── 建立 CI/CD 流水線
└── 完善災難恢復機制
```

---

## 🔧 運維和監控

### 系統監控指標

#### 核心性能指標

```python
# 監控指標定義
MONITORING_METRICS = {
    'system_performance': {
        'cpu_usage': {'threshold': 80, 'unit': '%'},
        'memory_usage': {'threshold': 85, 'unit': '%'},
        'gpu_usage': {'threshold': 90, 'unit': '%'},
        'disk_usage': {'threshold': 85, 'unit': '%'},
        'network_io': {'threshold': 1000, 'unit': 'Mbps'}
    },
    'application_performance': {
        'request_latency': {'threshold': 2000, 'unit': 'ms'},
        'throughput': {'threshold': 100, 'unit': 'req/min'},
        'error_rate': {'threshold': 1, 'unit': '%'},
        'model_load_time': {'threshold': 30, 'unit': 's'},
        'inference_time': {'threshold': 1500, 'unit': 'ms'}
    },
    'business_metrics': {
        'active_models': {'threshold': None, 'unit': 'count'},
        'daily_requests': {'threshold': None, 'unit': 'count'},
        'user_satisfaction': {'threshold': 4.0, 'unit': 'score'},
        'model_accuracy': {'threshold': 85, 'unit': '%'},
        'cache_hit_rate': {'threshold': 80, 'unit': '%'}
    }
}
```

#### 監控系統實作

```python
# 監控系統
class SystemMonitor:
    def __init__(self, config):
        self.config = config
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()

    def collect_system_metrics(self):
        """收集系統指標"""
        import psutil
        import GPUtil

        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_io': self._get_network_io(),
            'gpu_metrics': self._get_gpu_metrics()
        }

        return metrics

    def collect_application_metrics(self):
        """收集應用指標"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'active_connections': self._get_active_connections(),
            'request_queue_size': self._get_request_queue_size(),
            'model_cache_usage': self._get_cache_usage(),
            'error_count': self._get_error_count(),
            'response_times': self._get_response_times()
        }

        return metrics

    def check_health(self):
        """健康檢查"""
        health_status = {
            'status': 'healthy',
            'checks': {},
            'timestamp': datetime.now().isoformat()
        }

        # 檢查資料庫連接
        try:
            # 執行簡單查詢
            health_status['checks']['database'] = 'healthy'
        except Exception as e:
            health_status['checks']['database'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'unhealthy'

        # 檢查模型載入狀態
        try:
            # 檢查關鍵模型是否載入
            health_status['checks']['models'] = 'healthy'
        except Exception as e:
            health_status['checks']['models'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'unhealthy'

        # 檢查磁碟空間
        disk_usage = psutil.disk_usage('/').percent
        if disk_usage > 90:
            health_status['checks']['disk_space'] = f'warning: {disk_usage}% used'
            health_status['status'] = 'warning'
        else:
            health_status['checks']['disk_space'] = 'healthy'

        return health_status

    def setup_alerts(self):
        """設置告警規則"""
        alert_rules = [
            {
                'name': 'high_cpu_usage',
                'condition': 'cpu_usage > 80',
                'severity': 'warning',
                'notification': ['email', 'slack']
            },
            {
                'name': 'high_memory_usage',
                'condition': 'memory_usage > 85',
                'severity': 'warning',
                'notification': ['email', 'slack']
            },
            {
                'name': 'high_error_rate',
                'condition': 'error_rate > 5',
                'severity': 'critical',
                'notification': ['email', 'slack', 'sms']
            },
            {
                'name': 'model_inference_slow',
                'condition': 'inference_time > 3000',
                'severity': 'warning',
                'notification': ['email']
            }
        ]

        for rule in alert_rules:
            self.alert_manager.add_rule(rule)
```

### 日誌管理

```python
# 日誌管理系統
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 創建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # 文件處理器
        file_handler = logging.FileHandler('logs/ai_service.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # 控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_request(self, request_id, endpoint, method, user_id=None):
        """記錄請求日誌"""
        log_data = {
            'event_type': 'request',
            'request_id': request_id,
            'endpoint': endpoint,
            'method': method,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_data, ensure_ascii=False))

    def log_model_inference(self, model_type, staff_code, inference_time, success=True):
        """記錄模型推理日誌"""
        log_data = {
            'event_type': 'model_inference',
            'model_type': model_type,
            'staff_code': staff_code,
            'inference_time_ms': inference_time,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_data, ensure_ascii=False))

    def log_error(self, error_type, error_message, stack_trace=None, context=None):
        """記錄錯誤日誌"""
        log_data = {
            'event_type': 'error',
            'error_type': error_type,
            'error_message': error_message,
            'stack_trace': stack_trace,
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        self.logger.error(json.dumps(log_data, ensure_ascii=False))
```

---

## 🔐 安全性最佳實踐

### 模型安全

```python
# 模型安全管理
class ModelSecurityManager:
    def __init__(self):
        self.encryption_key = self._generate_encryption_key()
        self.access_control = AccessControlManager()

    def encrypt_model(self, model_path, encrypted_path):
        """加密模型檔案"""
        from cryptography.fernet import Fernet

        fernet = Fernet(self.encryption_key)

        with open(model_path, 'rb') as file:
            original_data = file.read()

        encrypted_data = fernet.encrypt(original_data)

        with open(encrypted_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        # 刪除原始檔案
        os.remove(model_path)

        return encrypted_path

    def decrypt_model(self, encrypted_path, decrypted_path):
        """解密模型檔案"""
        from cryptography.fernet import Fernet

        fernet = Fernet(self.encryption_key)

        with open(encrypted_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(decrypted_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        return decrypted_path

    def validate_model_integrity(self, model_path, expected_hash):
        """驗證模型完整性"""
        import hashlib

        sha256_hash = hashlib.sha256()
        with open(model_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        actual_hash = sha256_hash.hexdigest()

        if actual_hash != expected_hash:
            raise SecurityError(f"模型完整性驗證失敗: {actual_hash} != {expected_hash}")

        return True

    def audit_model_access(self, user_id, model_id, action, success=True):
        """稽核模型存取"""
        audit_log = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'model_id': model_id,
            'action': action,
            'success': success,
            'ip_address': self._get_client_ip(),
            'user_agent': self._get_user_agent()
        }

        # 寫入稽核日誌
        with open('logs/model_access_audit.log', 'a') as f:
            f.write(json.dumps(audit_log) + '\n')
```

### 網路安全

```yaml
# 網路安全配置
network_security:
  firewall_rules:
    - name: "allow-http"
      direction: "INGRESS"
      ports: ["80"]
      source_ranges: ["0.0.0.0/0"]
    - name: "allow-https"
      direction: "INGRESS"
      ports: ["443"]
      source_ranges: ["0.0.0.0/0"]
    - name: "allow-internal"
      direction: "INGRESS"
      ports: ["5000"]
      source_ranges: ["10.0.0.0/8"]

  ssl_configuration:
    enabled: true
    certificate_path: "/etc/ssl/certs/ai-service.crt"
    private_key_path: "/etc/ssl/private/ai-service.key"
    protocols: ["TLSv1.2", "TLSv1.3"]
    ciphers: ["ECDHE-RSA-AES256-GCM-SHA384", "ECDHE-RSA-AES128-GCM-SHA256"]

  rate_limiting:
    enabled: true
    requests_per_minute: 100
    burst_size: 20
    whitelist_ips: ["127.0.0.1", "10.0.0.0/8"]
```

---

## 📈 性能優化

### 模型載入優化

```python
# 模型載入優化
class OptimizedModelLoader:
    def __init__(self):
        self.model_cache = {}
        self.preload_queue = Queue()
        self.cache_stats = {'hits': 0, 'misses': 0}

    def preload_models(self, model_list):
        """預載入常用模型"""
        for model_info in model_list:
            threading.Thread(
                target=self._preload_single_model,
                args=(model_info,)
            ).start()

    def _preload_single_model(self, model_info):
        """預載入單個模型"""
        try:
            model_key = f"{model_info['type']}_{model_info.get('staff_code', 'default')}"

            if model_info['type'] == 'emotion':
                model = self._load_emotion_model(model_info)
            elif model_info['type'] == 'voice':
                model = self._load_voice_model(model_info)

            self.model_cache[model_key] = {
                'model': model,
                'loaded_at': time.time(),
                'access_count': 0
            }

            print(f"預載入模型完成: {model_key}")

        except Exception as e:
            print(f"預載入模型失敗 {model_info}: {e}")

    def get_model(self, model_type, staff_code=None):
        """獲取模型 (帶快取)"""
        model_key = f"{model_type}_{staff_code or 'default'}"

        if model_key in self.model_cache:
            self.cache_stats['hits'] += 1
            self.model_cache[model_key]['access_count'] += 1
            return self.model_cache[model_key]['model']

        self.cache_stats['misses'] += 1

        # 載入模型
        if model_type == 'emotion':
            model = self._load_emotion_model({'type': model_type})
        elif model_type == 'voice':
            model = self._load_voice_model({'type': model_type, 'staff_code': staff_code})

        # 加入快取
        self.model_cache[model_key] = {
            'model': model,
            'loaded_at': time.time(),
            'access_count': 1
        }

        return model

    def cleanup_cache(self, max_age_hours=2):
        """清理過期快取"""
        current_time = time.time()
        expired_keys = []

        for key, cache_info in self.model_cache.items():
            age_hours = (current_time - cache_info['loaded_at']) / 3600
            if age_hours > max_age_hours and cache_info['access_count'] < 5:
                expired_keys.append(key)

        for key in expired_keys:
            del self.model_cache[key]
            print(f"清理過期快取: {key}")

    def get_cache_stats(self):
        """獲取快取統計"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = self.cache_stats['hits'] / total_requests if total_requests > 0 else 0

        return {
            'hit_rate': hit_rate,
            'total_requests': total_requests,
            'cached_models': len(self.model_cache),
            'cache_size_mb': self._calculate_cache_size()
        }
```

這份完整的模型儲存與部署指南涵蓋了：

1. **本地端部署方案** - 完整的硬體需求、安裝步驟和配置
2. **GCP 雲端部署方案** - Kubernetes、自動擴展、成本優化
3. **混合部署架構** - 結合本地和雲端優勢的解決方案
4. **運維監控** - 系統監控、日誌管理、健康檢查
5. **安全性最佳實踐** - 模型加密、存取控制、稽核機制
6. **性能優化** - 模型快取、預載入、資源管理

這個指南為不同規模和需求的企業提供了完整的部署選擇和實施路徑。
