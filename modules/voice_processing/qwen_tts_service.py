#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen TTS 語音合成服務
提供雙語（國語/閩南語）語音合成功能
"""

import os
import base64
import wave

try:
    import dashscope
    DASHSCOPE_AVAILABLE = True
    dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
except ImportError:
    dashscope = None
    DASHSCOPE_AVAILABLE = False

class QwenTTSService:
    """Qwen TTS 語音合成服務"""
    
    def __init__(self, api_key=None):
        """
        初始化 Qwen TTS 服務
        
        Args:
            api_key (str): DashScope API 密鑰
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 庫未安裝，請執行: pip install dashscope")
        
        if not self.api_key:
            raise ValueError("未設置 DASHSCOPE_API_KEY")
    
    def synthesize(self, text, language='mandarin', output_file=None):
        """
        合成語音
        
        Args:
            text (str): 要合成的文本（最多 200 字符）
            language (str): 'mandarin' 或 'minan'
            output_file (str): 輸出文件路徑
        
        Returns:
            str: 音頻文件路徑
        """
        # 限制文本長度
        if len(text) > 200:
            text = text[:200]
            print(f"警告：文本已截斷至 200 字符")
        
        # 選擇語音
        voice = "Ethan" if language == "mandarin" else "Roy"
        
        print(f"開始合成語音：{language}（{voice}），文本長度：{len(text)} 字符")
        
        try:
            # 調用 Qwen TTS API
            response = dashscope.MultiModalConversation.call(
                api_key=self.api_key,
                model="qwen3-tts-flash",
                text=text,
                voice=voice,
                language_type="Chinese",
                speech_rate=0.8,  # 較慢語速，適合長者
                stream=True
            )
            
            # 收集音頻數據
            pcm_data = []
            chunk_count = 0
            
            for chunk in response:
                chunk_count += 1
                if chunk.output is not None:
                    audio = chunk.output.audio
                    if audio.data is not None:
                        wav_bytes = base64.b64decode(audio.data)
                        pcm_data.append(wav_bytes)
                else:
                    # 檢查錯誤
                    if hasattr(chunk, 'code') and chunk.code:
                        raise Exception(f"API 錯誤: {chunk.code} - {getattr(chunk, 'message', '')}")
            
            print(f"收到 {chunk_count} 個數據塊，生成 {len(pcm_data)} 個音頻片段")
            
            # 合併並保存
            if pcm_data and output_file:
                complete_pcm = b''.join(pcm_data)
                
                # 確保輸出目錄存在
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                with wave.open(output_file, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(24000)  # 24kHz
                    wav_file.writeframes(complete_pcm)
                
                print(f"語音文件已保存：{output_file}")
                return output_file
            
            return None
            
        except Exception as e:
            print(f"語音合成失敗: {e}")
            raise
    
    def synthesize_bilingual(self, text, output_dir):
        """
        生成雙語音頻
        
        Args:
            text (str): 要合成的文本
            output_dir (str): 輸出目錄
        
        Returns:
            dict: {'mandarin': 路徑, 'minan': 路徑}
        """
        os.makedirs(output_dir, exist_ok=True)
        
        mandarin_file = os.path.join(output_dir, 'mandarin.wav')
        minan_file = os.path.join(output_dir, 'minan.wav')
        
        results = {}
        
        try:
            results['mandarin'] = self.synthesize(text, 'mandarin', mandarin_file)
        except Exception as e:
            print(f"國語合成失敗: {e}")
            results['mandarin'] = None
        
        try:
            results['minan'] = self.synthesize(text, 'minan', minan_file)
        except Exception as e:
            print(f"閩南語合成失敗: {e}")
            results['minan'] = None
        
        return results

# 創建服務實例
qwen_tts_service = QwenTTSService() if DASHSCOPE_AVAILABLE and os.getenv("DASHSCOPE_API_KEY") else None
