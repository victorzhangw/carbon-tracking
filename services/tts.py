"""
新的GPT-SoVITS TTS服务
使用本地API: http://127.0.0.1:9880/tts
"""
import os
import requests
import time
import json
from config import ensure_directories

class GPTSoVITSTTSService:
    def __init__(self):
        self.api_url = "http://127.0.0.1:9880/tts"
        #self.api_url = "http://104.155.214.241:9880/tts"  # 外部服務器備用
        #self.api_url = "https://557584af9714.ngrok-free.app/tts"  # 外部服務器備用
       
        # 使用 GPT-SoVITS 目錄中的參考音頻（相對於 GPT-SoVITS 運行目錄）
        self.default_ref_audio = "TTS/vc.wav"
        self.output_dir = "genvoice"
        ensure_directories()
        
    def generate_speech(self, text, ref_audio_path=None, prompt_text=None, 
                       text_lang="zh", prompt_lang="zh", temperature=1.1,
                       batch_size=20, streaming_mode=False):
        """
        使用GPT-SoVITS API生成语音
        
        Args:
            text: 要轉換的文字
            ref_audio_path: 參考音頻文件路徑
            prompt_text: 提示文字
            text_lang: 文字語言
            prompt_lang: 提示語言
            temperature: 溫度
            batch_size: 批次大小
            streaming_mode: 是否流式模式
            
        Returns:
            生成的音頻文件路徑或None
        """
        try:
            # 使用預設參考音頻如果沒有提供
            if not ref_audio_path:
                ref_audio_path = self.default_ref_audio
            # 使用預設提示文字如果沒有提供
            if not prompt_text:
                prompt_text = "使用軟件者、傳播軟件導出的聲音者自負全責。如不認可該條款，則不能使用或引用軟件"
            # 構建請求數據
            payload = {
                "text": text,
                "text_lang": text_lang,
                "ref_audio_path": ref_audio_path,
                "prompt_lang": prompt_lang,
                "prompt_text": prompt_text,
                "batch_size": batch_size,
                "text_split_method": "cut5",
                "batch_threshold": 0.75,
                "streaming_mode": streaming_mode,
                "temperature": temperature
            }
            
            print(f"🎵 發送TTS請求到: {self.api_url}")
            print(f"📝 文字: {text[:50]}...")
            print(f"🎤 參考音頻: {ref_audio_path}")
            
            # 發送POST請求
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                self.api_url, 
                headers=headers, 
                data=json.dumps(payload),
                timeout=120  # 120秒超时
            )
            
            if response.status_code == 200:
                # 生成輸出檔案名
                timestamp = int(time.time())
                output_filename = f"tts_{timestamp}.wav"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # 保存音頻檔案
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ TTS生成成功: {output_path}")
                return output_path
            else:
                print(f"❌ TTS API錯誤: {response.status_code}")
                print(f"錯誤內容: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ TTS请求超时")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ 無法連接到TTS服務，請確保GPT-SoVITS服務在端口9880運行")
            return None
        except Exception as e:
            print(f"❌ TTS生成錯誤: {e}")
            return None

# 創建全域實例
gpt_sovits_tts = GPTSoVITSTTSService()

# 相容性函數 - 替換原有的f5_tts函數
def f5_tts(text, output_file=None):
    """
    相容原有f5_tts函數的介面
    """
    result = gpt_sovits_tts.generate_speech(text)
    return result

# 相容性函數 - 替換原有的call_basic_tts函數  
def call_basic_tts(file_path, reftext, gen_text, speed=0.55, crossfade=0.15):
    """
    相容原有call_basic_tts函數的介面
    """
    # 使用提供的參考音頻和文字
    result = gpt_sovits_tts.generate_speech(
        text=gen_text,
        ref_audio_path=file_path,
        prompt_text=reftext,
        temperature=1.0 + (speed - 0.55)  # 將speed轉換為temperature
    )
    return result
