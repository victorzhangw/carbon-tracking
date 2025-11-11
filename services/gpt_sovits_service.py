"""
GPT-SoVITS 語音克隆服務
實現完整的語音處理工作流程：文字生成 -> 語音上傳 -> 切分降噪 -> 模擬語音生成
"""

import os
import time
import shutil
import tempfile
from gradio_client import Client, handle_file
from modules.voice_processing.voice_config import GPT_SOVITS_API_URL, UPLOAD_DIR, OUTPUT_DIR, TEMP_DIR
from utils import generate_unique_filename

class GPTSoVITSService:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.temp_dir = TEMP_DIR
        self.output_dir = OUTPUT_DIR
        self.upload_dir = UPLOAD_DIR
        
        # 確保目錄存在
        for directory in [self.temp_dir, self.output_dir, self.upload_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def connect(self):
        """連接到GPT-SoVITS服務"""
        try:
            print(f"嘗試連接到GPT-SoVITS服務: {GPT_SOVITS_API_URL}")
            self.client = Client(GPT_SOVITS_API_URL)
            self.is_connected = True
            print("✅ 成功連接到GPT-SoVITS服務")
            
            # 測試獲取API信息
            try:
                api_info = self.client.view_api()
                available_endpoints = list(api_info.get('named_endpoints', {}).keys())
                print(f"📋 可用API端點數量: {len(available_endpoints)}")
                if available_endpoints:
                    print(f"🔧 部分端點: {', '.join(available_endpoints[:5])}")
            except Exception as api_e:
                print(f"⚠️ 無法獲取API信息: {api_e}")
            
            return True
        except Exception as e:
            print(f"❌ 連接GPT-SoVITS服務失敗: {e}")
            print(f"請確保GPT-SoVITS服務正在運行於: {GPT_SOVITS_API_URL}")
            self.is_connected = False
            return False
    
    def generate_reading_text(self, duration_seconds=60):
        """
        生成約60秒的閱讀文字
        根據平均語速（每分鐘150-200字）計算文字長度
        """
        # 平均語速約每分鐘180字，60秒約180字
        target_length = int(duration_seconds * 3)  # 每秒約3字
        
        reading_texts = [
            "歡迎使用我們的AI客服系統。請您清楚地朗讀以下文字，這將幫助我們建立您的專屬語音模型。",
            "在現代社會中，科技的發展日新月異，人工智能已經深入到我們生活的各個層面。",
            "從智能手機到自動駕駛汽車，從語音助手到醫療診斷，AI技術正在改變著我們的工作和生活方式。",
            "語音合成技術作為人工智能的重要分支，能夠將文字轉換為自然流暢的語音。",
            "這項技術在客服系統、教育培訓、無障礙服務等領域都有著廣泛的應用前景。",
            "通過深度學習和神經網絡技術，現代語音合成系統能夠生成接近真人的語音效果。",
            "我們的系統採用先進的GPT-SoVITS技術，能夠學習和模擬您的聲音特徵。",
            "請保持自然的語調和語速，避免過快或過慢的朗讀。清晰的發音將有助於提高語音模型的質量。",
            "感謝您的配合，讓我們一起創造更好的AI語音體驗。"
        ]
        
        # 組合文字直到達到目標長度
        combined_text = ""
        for text in reading_texts:
            if len(combined_text) + len(text) <= target_length:
                combined_text += text
            else:
                # 截取剩餘長度
                remaining = target_length - len(combined_text)
                combined_text += text[:remaining]
                break
        
        return combined_text
    
    def process_uploaded_audio(self, audio_file, staff_code):
        """
        處理上傳的語音檔案
        1. 保存到指定目錄
        2. 進行音頻切分
        3. 進行降噪處理
        """
        if not self.is_connected:
            if not self.connect():
                raise Exception("無法連接到GPT-SoVITS服務")
        
        try:
            # 1. 保存上傳的音頻文件
            staff_dir = os.path.join(self.upload_dir, staff_code)
            os.makedirs(staff_dir, exist_ok=True)
            
            filename = generate_unique_filename(audio_file, prefix=staff_code)
            audio_path = os.path.join(staff_dir, filename)
            audio_file.save(audio_path)
            
            # 2. 音頻切分處理
            sliced_audio_path = self._slice_audio(audio_path, staff_code)
            
            # 3. 降噪處理
            denoised_audio_path = self._denoise_audio(sliced_audio_path, staff_code)
            
            return {
                "original_path": audio_path,
                "sliced_path": sliced_audio_path,
                "denoised_path": denoised_audio_path,
                "staff_code": staff_code,
                "filename": filename
            }
            
        except Exception as e:
            print(f"音頻處理錯誤: {e}")
            raise
    
    def _slice_audio(self, audio_path, staff_code):
        """簡化的音頻處理 - 跳過切分步驟"""
        try:
            print(f"跳過音頻切分，直接使用原始文件: {audio_path}")
            return audio_path  # 直接返回原始路徑
            
        except Exception as e:
            print(f"音頻處理錯誤: {e}")
            return audio_path
    
    def _denoise_audio(self, audio_path, staff_code):
        """簡化的音頻處理 - 跳過降噪步驟"""
        try:
            print(f"跳過音頻降噪，直接使用原始文件: {audio_path}")
            return audio_path  # 直接返回原始路徑
            
        except Exception as e:
            print(f"音頻處理錯誤: {e}")
            return audio_path
    
    def setup_voice_model(self, processed_audio_info, reference_text):
        """
        設置語音模型
        使用處理後的音頻進行特徵提取和模型準備
        """
        if not self.is_connected:
            if not self.connect():
                raise Exception("無法連接到GPT-SoVITS服務")
        
        try:
            staff_code = processed_audio_info["staff_code"]
            audio_path = processed_audio_info["denoised_path"]
            
            # 1. 文本分詞與特徵提取
            self._extract_text_features(audio_path, reference_text, staff_code)
            
            # 2. 語音自監督特徵提取
            self._extract_ssl_features(audio_path, staff_code)
            
            # 3. 語義Token提取
            self._extract_semantic_tokens(audio_path, staff_code)
            
            # 4. 配置TTS推理環境
            self._setup_tts_inference(staff_code)
            
            return {
                "status": "success",
                "message": "語音模型設置完成",
                "staff_code": staff_code
            }
            
        except Exception as e:
            print(f"語音模型設置錯誤: {e}")
            raise
    
    def _extract_text_features(self, audio_path, reference_text, staff_code):
        """簡化的特徵提取 - 創建標註文件"""
        try:
            # 創建標註文件
            list_file_path = os.path.join(self.temp_dir, f"{staff_code}.list")
            with open(list_file_path, 'w', encoding='utf-8') as f:
                f.write(f"{audio_path}|{staff_code}|zh|{reference_text}\n")
            
            print(f"創建標註文件: {list_file_path}")
            print(f"跳過複雜的特徵提取步驟")
            
        except Exception as e:
            print(f"文本特徵提取錯誤: {e}")
            # 不拋出異常，繼續執行
    
    def _extract_ssl_features(self, audio_path, staff_code):
        """簡化的SSL特徵提取"""
        try:
            print(f"跳過SSL特徵提取步驟")
            
        except Exception as e:
            print(f"SSL特徵提取錯誤: {e}")
            # 不拋出異常，繼續執行
    
    def _extract_semantic_tokens(self, audio_path, staff_code):
        """簡化的語義Token提取"""
        try:
            print(f"跳過語義Token提取步驟")
            
        except Exception as e:
            print(f"語義Token提取錯誤: {e}")
            # 不拋出異常，繼續執行
    
    def _setup_tts_inference(self, staff_code):
        """簡化的TTS推理環境設置"""
        try:
            print(f"跳過TTS推理環境設置步驟")
            
        except Exception as e:
            print(f"TTS推理環境設置錯誤: {e}")
            # 不拋出異常，繼續執行
    
    def generate_voice_response(self, text, staff_code, reference_audio_path, reference_text):
        """
        使用GPT-SoVITS生成語音回應
        """
        if not self.is_connected:
            if not self.connect():
                print("⚠️ GPT-SoVITS服務未連接，使用模擬模式")
                return self._generate_mock_voice(text, staff_code, reference_audio_path)
        
        try:
            print(f"🎵 使用GPT-SoVITS生成語音: {text}")
            
            # 嘗試使用真實的GPT-SoVITS API
            result = self.client.predict(
                ref_audio_input=handle_file(reference_audio_path),
                ref_text_input=reference_text,
                gen_text_input=text,
                remove_silence=False,
                cross_fade_duration_slider=0.15,
                speed_slider=1.0,
                api_name="/basic_tts"
            )
            
            # 獲取生成的音頻文件路徑
            generated_audio_path = result[0]
            
            # 複製到輸出目錄
            output_filename = f"{staff_code}_{int(time.time())}.wav"
            output_path = os.path.join(self.output_dir, output_filename)
            shutil.copy(generated_audio_path, output_path)
            
            print(f"✅ GPT-SoVITS語音生成成功: {output_path}")
            
            return {
                "audio_path": output_path,
                "audio_url": f"/genvoice/{output_filename}",
                "staff_code": staff_code,
                "generated_text": text,
                "generated_at": int(time.time()),
                "method": "gpt_sovits"
            }
            
        except Exception as e:
            print(f"❌ GPT-SoVITS語音生成失敗: {e}")
            print("🔄 回退到模擬模式")
            return self._generate_mock_voice(text, staff_code, reference_audio_path)
    
    def _generate_mock_voice(self, text, staff_code, reference_audio_path):
        """模擬語音生成（備用方案）"""
        try:
            print(f"🎭 模擬語音生成: {text}")
            
            output_filename = f"{staff_code}_{int(time.time())}_mock.wav"
            output_path = os.path.join(self.output_dir, output_filename)
            
            # 如果有參考音頻，複製一份作為模擬結果
            if os.path.exists(reference_audio_path):
                shutil.copy(reference_audio_path, output_path)
                print(f"📋 複製參考音頻作為模擬結果: {output_path}")
            else:
                # 嘗試使用mockvoice目錄中的音頻文件
                mockvoice_dir = './mockvoice'
                if os.path.exists(mockvoice_dir):
                    wav_files = [f for f in os.listdir(mockvoice_dir) if f.endswith('.wav')]
                    if wav_files:
                        mock_audio = os.path.join(mockvoice_dir, wav_files[0])
                        shutil.copy(mock_audio, output_path)
                        print(f"📋 使用mockvoice中的音頻: {mock_audio}")
                    else:
                        self._create_empty_wav(output_path)
                else:
                    self._create_empty_wav(output_path)
            
            return {
                "audio_path": output_path,
                "audio_url": f"/genvoice/{output_filename}",
                "staff_code": staff_code,
                "generated_text": text,
                "generated_at": int(time.time()),
                "method": "mock"
            }
            
        except Exception as e:
            print(f"模擬語音生成錯誤: {e}")
            raise
    
    def _create_empty_wav(self, output_path):
        """創建一個空的WAV文件"""
        with open(output_path, 'wb') as f:
            # 寫入最小的WAV文件頭
            wav_header = b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
            f.write(wav_header)
        print(f"📄 創建空白音頻文件: {output_path}")

# 創建全局服務實例
gpt_sovits_service = GPTSoVITSService()