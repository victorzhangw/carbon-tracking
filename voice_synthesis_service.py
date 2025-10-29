"""
GPT-SoVITS 語音合成服務整合
"""
import requests
import json
import base64
from typing import Optional, Dict, Any
import logging

class GPTSoVITSService:
    def __init__(self, base_url: str = "http://localhost:9874"):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.gpt_sovits_path = "./GPT-SoVITS"  # GPT-SoVITS 項目路徑
    
    def synthesize_speech_direct(
        self, 
        text: str, 
        reference_audio_path: str,
        reference_text: str,
        language: str = "zh",
        speed: float = 1.0
    ) -> Optional[bytes]:
        """
        直接調用 GPT-SoVITS 進行語音合成 (不通過 WebUI)
        """
        try:
            import sys
            import os
            sys.path.append(self.gpt_sovits_path)
            
            # 導入 GPT-SoVITS 模組
            from GPT_SoVITS.inference_webui import get_tts_wav
            
            # 調用合成函數
            audio_data = get_tts_wav(
                ref_wav_path=reference_audio_path,
                prompt_text=reference_text,
                prompt_language=language,
                text=text,
                text_language=language,
                how_to_cut="cut5",
                top_k=20,
                top_p=0.6,
                temperature=0.6,
                ref_free=False
            )
            
            return audio_data
            
        except Exception as e:
            self.logger.error(f"直接語音合成失敗: {str(e)}")
            return None
    
    def synthesize_speech(
        self, 
        text: str, 
        reference_audio_path: str,
        reference_text: str,
        language: str = "zh",
        speed: float = 1.0
    ) -> Optional[bytes]:
        """
        使用 GPT-SoVITS 合成語音
        
        Args:
            text: 要合成的文字
            reference_audio_path: 參考音頻路徑
            reference_text: 參考音頻對應的文字
            language: 語言代碼 (zh/en/ja/ko/yue)
            speed: 語音速度
        
        Returns:
            音頻數據 (bytes) 或 None
        """
        try:
            # 準備請求數據
            payload = {
                "text": text,
                "text_lang": language,
                "ref_audio_path": reference_audio_path,
                "prompt_text": reference_text,
                "prompt_lang": language,
                "top_k": 5,
                "top_p": 1.0,
                "temperature": 1.0,
                "text_split_method": "cut5",
                "batch_size": 1,
                "speed_factor": speed,
                "split_bucket": True,
                "return_fragment": False,
                "fragment_interval": 0.3
            }
            
            # 發送請求到 GPT-SoVITS API
            response = requests.post(
                f"{self.base_url}/tts",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.content
            else:
                self.logger.error(f"語音合成失敗: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"語音合成異常: {str(e)}")
            return None
    
    def clone_voice_from_sample(
        self, 
        audio_file: bytes, 
        sample_text: str,
        target_text: str,
        language: str = "zh"
    ) -> Optional[bytes]:
        """
        從音頻樣本克隆聲音並合成新語音
        """
        try:
            # 保存臨時音頻文件
            temp_audio_path = f"/tmp/voice_sample_{hash(audio_file)}.wav"
            with open(temp_audio_path, "wb") as f:
                f.write(audio_file)
            
            # 使用樣本進行語音合成
            return self.synthesize_speech(
                text=target_text,
                reference_audio_path=temp_audio_path,
                reference_text=sample_text,
                language=language
            )
            
        except Exception as e:
            self.logger.error(f"聲音克隆失敗: {str(e)}")
            return None

# Flask 路由整合
from flask import Flask, request, jsonify, send_file
import io

app = Flask(__name__)
tts_service = GPTSoVITSService()

@app.route('/api/voice/synthesize', methods=['POST'])
def synthesize_voice():
    """語音合成 API"""
    try:
        data = request.get_json()
        
        # 驗證必要參數
        required_fields = ['text', 'reference_audio', 'reference_text']
        if not all(field in data for field in required_fields):
            return jsonify({'error': '缺少必要參數'}), 400
        
        # 合成語音
        audio_data = tts_service.synthesize_speech(
            text=data['text'],
            reference_audio_path=data['reference_audio'],
            reference_text=data['reference_text'],
            language=data.get('language', 'zh'),
            speed=data.get('speed', 1.0)
        )
        
        if audio_data:
            # 返回音頻文件
            return send_file(
                io.BytesIO(audio_data),
                mimetype='audio/wav',
                as_attachment=True,
                download_name='synthesized_voice.wav'
            )
        else:
            return jsonify({'error': '語音合成失敗'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/clone', methods=['POST'])
def clone_voice():
    """聲音克隆 API"""
    try:
        # 獲取上傳的音頻文件
        if 'audio' not in request.files:
            return jsonify({'error': '未提供音頻文件'}), 400
        
        audio_file = request.files['audio']
        sample_text = request.form.get('sample_text', '')
        target_text = request.form.get('target_text', '')
        language = request.form.get('language', 'zh')
        
        if not sample_text or not target_text:
            return jsonify({'error': '缺少文字參數'}), 400
        
        # 克隆聲音
        audio_data = tts_service.clone_voice_from_sample(
            audio_file=audio_file.read(),
            sample_text=sample_text,
            target_text=target_text,
            language=language
        )
        
        if audio_data:
            return send_file(
                io.BytesIO(audio_data),
                mimetype='audio/wav',
                as_attachment=True,
                download_name='cloned_voice.wav'
            )
        else:
            return jsonify({'error': '聲音克隆失敗'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)