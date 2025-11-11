# GPT-SoVITS API 完整文档

## 概述

GPT-SoVITS 是一个强大的语音合成系统，提供了完整的API接口来进行语音识别、音频处理、模型训练和语音合成等功能。本文档详细介绍了所有可用的API端点及其使用方法。

## 安装与配置

### Python客户端安装

```bash
pip install gradio_client
```

### 基本使用方法

```python
from gradio_client import Client

# 连接到本地服务器
client = Client("http://localhost:9874/")

# 调用API
result = client.predict(
    # 参数...
    api_name="/api_endpoint_name"
)
```

## API端点分类

### 1. 配置与选择类API

#### 1.1 语言选择配置
**API端点：** `/change_lang_choices`

```python
result = client.predict(
    key="达摩 ASR (中文)",  # 可选值: "达摩 ASR (中文)", "Faster Whisper (多语种)"
    api_name="/change_lang_choices"
)
```

**参数说明：**
- `key`: ASR模型选择，影响可用语言选项

**返回值：**
- 语言代码列表，如 `["zh", "yue"]`

#### 1.2 模型尺寸配置
**API端点：** `/change_size_choices`

```python
result = client.predict(
    key="达摩 ASR (中文)",
    api_name="/change_size_choices"
)
```

**返回值：**
- 模型尺寸选项，如 `["large"]`

#### 1.3 精度配置
**API端点：** `/change_precision_choices`

```python
result = client.predict(
    key="达摩 ASR (中文)",
    api_name="/change_precision_choices"
)
```

**返回值：**
- 数据类型精度选项，如 `["float32"]`

### 2. 语音识别(ASR)类API

#### 2.1 开启语音识别
**API端点：** `/open_asr`

```python
result = client.predict(
    asr_inp_dir="D:\\GPT-SoVITS\\raw\\xxx",      # 输入文件夹路径
    asr_opt_dir="output/asr_opt",                # 输出文件夹路径
    asr_model="达摩 ASR (中文)",                  # ASR模型
    asr_model_size="large",                      # 模型尺寸
    asr_lang="zh",                              # 语言设置
    asr_precision="float32",                    # 数据类型精度
    api_name="/open_asr"
)
```

**返回值：**
- 元组包含4个元素：
  - [0] 语音识别进程输出信息
  - [1] 标注文件路径
  - [2] 文本标注文件
  - [3] 训练集音频文件目录

#### 2.2 关闭语音识别
**API端点：** `/close_asr`

```python
result = client.predict(api_name="/close_asr")
```

### 3. 音频处理类API

#### 3.1 音频切分

**开启音频切分：** `/open_slice`

```python
result = client.predict(
    inp="",                          # 音频输入路径
    opt_root="output/slicer_opt",    # 输出根目录
    threshold="-34",                 # 音量阈值
    min_length="4000",              # 最小长度(ms)
    min_interval="300",             # 最短切割间隔(ms)
    hop_size="10",                  # 音量曲线计算精度
    max_sil_kept="500",             # 静音保留长度(ms)
    _max=0.9,                       # 归一化最大值
    alpha=0.25,                     # 混合比例
    n_parts=4,                      # 进程数
    api_name="/open_slice"
)
```

**关闭音频切分：** `/close_slice`

```python
result = client.predict(api_name="/close_slice")
```

#### 3.2 音频降噪

**开启降噪：** `/open_denoise`

```python
result = client.predict(
    denoise_inp_dir="",                    # 输入文件夹路径
    denoise_opt_dir="output/denoise_opt",  # 输出文件夹路径
    api_name="/open_denoise"
)
```

**关闭降噪：** `/close_denoise`

```python
result = client.predict(api_name="/close_denoise")
```

### 4. 音频标注类API

#### 4.1 标注处理
**API端点：** `/change_label` 和 `/change_label_1`

```python
result = client.predict(
    path_list="D:\\RVC1006\\GPT-SoVITS\\raw\\xxx.list",  # 标注文件路径
    api_name="/change_label"
)
```

### 5. UVR5人声分离类API

#### 5.1 UVR5处理
**API端点：** `/change_uvr5` 和 `/change_uvr5_1`

```python
result = client.predict(api_name="/change_uvr5")
```

### 6. 训练数据预处理类API

#### 6.1 文本分词与特征提取
**开启：** `/open1a`

```python
result = client.predict(
    inp_text="D:\\RVC1006\\GPT-SoVITS\\raw\\xxx.list",  # 文本标注文件
    inp_wav_dir="Hello!!",                              # 训练集音频文件目录 (必需)
    exp_name="xxx",                                     # 实验/模型名
    gpu_numbers="0-0",                                  # GPU卡号
    bert_pretrained_dir="GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large",  # BERT模型路径
    api_name="/open1a"
)
```

**关闭：** `/close1a`

#### 6.2 语音自监督特征提取
**开启：** `/open1b`

```python
result = client.predict(
    inp_text="D:\\RVC1006\\GPT-SoVITS\\raw\\xxx.list",
    inp_wav_dir="Hello!!",  # 必需参数
    exp_name="xxx",
    gpu_numbers="0-0",
    ssl_pretrained_dir="GPT_SoVITS/pretrained_models/chinese-hubert-base",  # SSL模型路径
    api_name="/open1b"
)
```

**关闭：** `/close1b`

#### 6.3 语义Token提取
**开启：** `/open1c`

```python
result = client.predict(
    inp_text="D:\\RVC1006\\GPT-SoVITS\\raw\\xxx.list",
    exp_name="xxx",
    gpu_numbers="0-0",
    pretrained_s2G_path="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2G2333k.pth",
    api_name="/open1c"
)
```

**关闭：** `/close1c`

#### 6.4 一键三连处理
**开启：** `/open1abc`

```python
result = client.predict(
    inp_text="D:\\RVC1006\\GPT-SoVITS\\raw\\xxx.list",
    inp_wav_dir="Hello!!",  # 必需
    exp_name="xxx",
    gpu_numbers1a="0-0",    # 步骤1a GPU
    gpu_numbers1Ba="0-0",   # 步骤1b GPU  
    gpu_numbers1c="0-0",    # 步骤1c GPU
    bert_pretrained_dir="GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large",
    ssl_pretrained_dir="GPT_SoVITS/pretrained_models/chinese-hubert-base",
    pretrained_s2G_path="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2G2333k.pth",
    api_name="/open1abc"
)
```

**关闭：** `/close1abc`

### 7. 模型训练类API

#### 7.1 SoVITS模型训练
**开启：** `/open1Ba`

```python
result = client.predict(
    batch_size=2,                    # 每张显卡的batch_size
    total_epoch=8,                   # 总训练轮数
    exp_name="xxx",                  # 实验/模型名
    text_low_lr_rate=0.4,           # 文本模块学习率权重
    if_save_latest=True,            # 是否仅保存最新权重
    if_save_every_weights=True,     # 是否保存至weights文件夹
    save_every_epoch=4,             # 保存频率
    gpu_numbers1Ba="0",             # GPU卡号
    pretrained_s2G="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2G2333k.pth",  # 预训练G模型
    pretrained_s2D="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2D2333k.pth",  # 预训练D模型
    if_grad_ckpt=False,             # 是否开启梯度检查点
    lora_rank="32",                 # LoRA阶数 (16/32/64/128)
    api_name="/open1Ba"
)
```

**关闭：** `/close1Ba`

#### 7.2 GPT模型训练
**开启：** `/open1Bb`

```python
result = client.predict(
    batch_size=2,
    total_epoch=15,
    exp_name="xxx",
    if_dpo=False,                   # 是否开启DPO训练
    if_save_latest=True,
    if_save_every_weights=True,
    save_every_epoch=5,
    gpu_numbers="0",
    pretrained_s1="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt",
    api_name="/open1Bb"
)
```

**关闭：** `/close1Bb`

### 8. 推理相关API

#### 8.1 获取模型选择列表
**API端点：** `/change_choices`

```python
result = client.predict(api_name="/change_choices")
```

**返回值：**
- 元组包含2个元素：
  - [0] SoVITS模型列表
  - [1] GPT模型列表

#### 8.2 配置TTS推理
**API端点：** `/change_tts_inference` 和 `/change_tts_inference_1`

```python
result = client.predict(
    bert_path="GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large",
    cnhubert_base_path="GPT_SoVITS/pretrained_models/chinese-hubert-base",
    gpu_number="0",                 # GPU卡号，只能填1个整数
    gpt_path="GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt",
    sovits_path="GPT_SoVITS/pretrained_models/s2G488k.pth",
    batched_infer_enabled=False,    # 是否启用并行推理
    api_name="/change_tts_inference"
)
```

### 9. 系统配置API

#### 9.1 同步配置
**API端点：** `/sync`

```python
result = client.predict(
    text="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2G2333k.pth",
    api_name="/sync"
)
```

#### 9.2 版本切换
**API端点：** `/switch_version`

```python
result = client.predict(
    version_="v2",  # 可选值: "v1", "v2", "v4"
    api_name="/switch_version"
)
```

**返回值：**
- 包含12个元素的元组，更新各种配置参数

## 使用建议

### 典型工作流程

1. **数据准备阶段**
   - 使用 `/open_asr` 进行语音识别
   - 使用 `/open_slice` 进行音频切分
   - 使用 `/open_denoise` 进行音频降噪

2. **特征提取阶段**
   - 使用 `/open1abc` 进行一键三连处理，或分别使用：
     - `/open1a` 文本分词与特征提取
     - `/open1b` 语音自监督特征提取  
     - `/open1c` 语义Token提取

3. **模型训练阶段**
   - 使用 `/open1Ba` 训练SoVITS模型
   - 使用 `/open1Bb` 训练GPT模型

4. **推理阶段**
   - 使用 `/change_tts_inference` 配置推理环境
   - 进行语音合成

### 注意事项

- 所有路径使用反斜杠分隔，适用于Windows系统
- GPU编号格式为字符串，如 "0" 或 "0-0"
- 训练过程中可随时使用对应的 `close_` API终止进程
- 建议按顺序执行各个步骤，确保依赖关系正确

## 错误处理

在使用API时，建议添加适当的错误处理：

```python
try:
    result = client.predict(
        # 参数...
        api_name="/api_endpoint"
    )
    print("操作成功:", result)
except Exception as e:
    print("操作失败:", str(e))
```

这份文档涵盖了GPT-SoVITS系统的所有API端点，可以作为开发和使用的完整参考。