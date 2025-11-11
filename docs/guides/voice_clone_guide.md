# 語音克隆系統操作指南

## 🚀 前端操作步驟

### 前置準備

1. **啟動GPT-SoVITS服務**
   ```bash
   # 進入GPT-SoVITS目錄
   cd GPT-SoVITS-v4-20250422fix
   
   # 啟動服務（端口9874）
   python webui.py
   ```

2. **啟動Flask後端**
   ```bash
   python app.py
   ```

3. **訪問演示頁面**
   ```
   http://localhost:5000/voice_clone/demo
   ```

### 步驟1：生成閱讀文字

**API端點**: `GET /voice_clone/generate_reading_text`

**前端操作**:
1. 設置朗讀時長（30-120秒，建議60秒）
2. 點擊「🎯 生成閱讀文字」按鈕
3. 系統會生成適合語音訓練的文字內容

**示例請求**:
```javascript
fetch('/voice_clone/generate_reading_text?duration=60')
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('生成的文字:', data.reading_text);
            console.log('字數:', data.character_count);
        }
    });
```

### 步驟2：上傳語音樣本

**API端點**: `POST /voice_clone/upload_voice_sample`

**前端操作**:
1. 填寫客服代號（例如：CS001）
2. 上傳WAV格式的音頻文件（建議60-90秒）
3. 確認參考文字內容
4. 點擊「📤 上傳並處理語音」

**處理流程**:
- 音頻切分和降噪
- 文本特徵提取
- SSL特徵提取  
- 語義Token提取
- TTS推理環境設置

**示例請求**:
```javascript
const formData = new FormData();
formData.append('audio_file', audioFile);
formData.append('staff_code', 'CS001');
formData.append('reference_text', referenceText);

fetch('/voice_clone/upload_voice_sample', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        console.log('語音模型ID:', data.voice_model_id);
        console.log('處理步驟:', data.processed_info.processing_steps);
    }
});
```

### 步驟3：測試語音生成

**API端點**: `POST /voice_clone/test_voice_generation`

**前端操作**:
1. 輸入測試文字
2. 點擊「🎵 生成測試語音」
3. 播放生成的音頻檢查效果

**示例請求**:
```javascript
fetch('/voice_clone/test_voice_generation', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        test_text: '您好，我是AI客服助手，很高興為您服務。',
        staff_code: 'CS001'
    })
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        // 播放生成的音頻
        const audio = new Audio(data.audio_url);
        audio.play();
    }
});
```

### 步驟4：AI對話測試

**API端點**: `POST /voice_clone/generate_response_voice`

**前端操作**:
1. 輸入用戶問題
2. 點擊「🤖 生成AI回應語音」
3. 系統會：
   - 使用DeepSeek AI分析問題
   - 生成專業回應
   - 用克隆的聲音朗讀回應

**示例請求**:
```javascript
fetch('/voice_clone/generate_response_voice', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        user_input: '我最近感到很焦慮，不知道該怎麼辦？',
        staff_code: 'CS001'
    })
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        console.log('AI分析結果:', data.ai_analysis);
        console.log('情感分析:', data.ai_analysis.sentiment);
        console.log('回應內容:', data.ai_analysis.response_text);
        console.log('語音URL:', data.voice_output.audio_url);
    }
});
```

## 🔧 其他可用API

### 查看語音模型列表
```javascript
fetch('/voice_clone/voice_models')
    .then(response => response.json())
    .then(data => {
        console.log('所有語音模型:', data.voice_models);
    });
```

### 查看特定客服的語音模型
```javascript
fetch('/voice_clone/voice_model/CS001')
    .then(response => response.json())
    .then(data => {
        console.log('CS001的語音模型:', data.voice_model);
    });
```

## ⚠️ 注意事項

### 音頻文件要求
- **格式**: WAV格式
- **時長**: 60-90秒（最少30秒，最多120秒）
- **質量**: 清晰無雜音，安靜環境錄製
- **內容**: 朗讀系統生成的文字

### 客服代號規則
- 唯一標識符（例如：CS001, STAFF_001）
- 用於區分不同客服人員的語音模型
- 一個代號對應一個語音模型

### 錯誤處理
```javascript
.catch(error => {
    console.error('請求失敗:', error);
    // 顯示錯誤提示
});
```

## 🎯 完整示例

以下是一個完整的語音克隆操作示例：

```javascript
// 1. 生成閱讀文字
async function startVoiceCloning() {
    try {
        // 步驟1：生成文字
        const textResponse = await fetch('/voice_clone/generate_reading_text?duration=60');
        const textData = await textResponse.json();
        
        if (textData.status === 'success') {
            console.log('請朗讀以下文字:', textData.reading_text);
            
            // 用戶錄製音頻後...
            
            // 步驟2：上傳語音
            const formData = new FormData();
            formData.append('audio_file', audioFile); // 用戶上傳的文件
            formData.append('staff_code', 'CS001');
            formData.append('reference_text', textData.reading_text);
            
            const uploadResponse = await fetch('/voice_clone/upload_voice_sample', {
                method: 'POST',
                body: formData
            });
            const uploadData = await uploadResponse.json();
            
            if (uploadData.status === 'success') {
                console.log('語音模型設置完成!');
                
                // 步驟3：測試語音
                const testResponse = await fetch('/voice_clone/test_voice_generation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        test_text: '測試語音效果',
                        staff_code: 'CS001'
                    })
                });
                const testData = await testResponse.json();
                
                if (testData.status === 'success') {
                    console.log('測試音頻URL:', testData.audio_url);
                    
                    // 步驟4：AI對話
                    const aiResponse = await fetch('/voice_clone/generate_response_voice', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            user_input: '我需要幫助',
                            staff_code: 'CS001'
                        })
                    });
                    const aiData = await aiResponse.json();
                    
                    if (aiData.status === 'success') {
                        console.log('AI回應:', aiData.ai_analysis.response_text);
                        console.log('語音回應URL:', aiData.voice_output.audio_url);
                    }
                }
            }
        }
    } catch (error) {
        console.error('語音克隆過程出錯:', error);
    }
}
```

## 🎵 音頻播放示例

```javascript
function playGeneratedAudio(audioUrl) {
    const audio = new Audio(audioUrl);
    audio.controls = true;
    audio.preload = 'auto';
    
    audio.addEventListener('loadstart', () => {
        console.log('開始加載音頻');
    });
    
    audio.addEventListener('canplay', () => {
        console.log('音頻可以播放');
        audio.play();
    });
    
    audio.addEventListener('error', (e) => {
        console.error('音頻播放錯誤:', e);
    });
    
    // 添加到頁面
    document.body.appendChild(audio);
}
```

這就是使用當前後端代碼進行語音克隆的完整操作流程！