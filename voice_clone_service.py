"""
語音克隆服務 - 整合 GPT-SoVITS v4
支持用戶上傳語音檔並生成對應模擬語音
"""
import os
import sys
import tempfile
import logging
import requests
import json
import subprocess
import shutil
from typing import Optional, Dict, Any, List
from pathlib import Path
import soundfile as sf
import librosa
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import time
import numpy as np

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class GPTSoVITSCloneService:
    def __init__(self, gpt_sovits_path: str = "./GPT-SoVITS-v4-20250422fix"):
        self.gpt_sovits_path = Path(gpt_sovits_path)
        self.api_url = "http://127.0.0.1:9880"
        self.upload_dir = Path("./audio_uploads")
        self.output_dir = Path("./voice_output")
        
        # 創建必要目錄
        self.upload_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # 檢查 GPT-SoVITS 是否存在
        if not self.gpt_sovits_path.exists():
            logger.error(f"GPT-SoVITS 路徑不存在: {self.gpt_sovits_path}")
        
        self.api_process = None
        self.start_api_server()
    
    def start_api_server(self):
        """啟動 GPT-SoVITS API 服務"""
        try:
            # 檢查 API 是否已經運行
            if self.check_api_status():
                logger.info("GPT-SoVITS API 已經在運行")
                return True
            
            logger.info("正在啟動 GPT-SoVITS API 服務...")
            
            # 啟動 API 服務
            api_script = self.gpt_sovits_path / "api_v2.py"
            if not api_script.exists():
                logger.error(f"API 腳本不存在: {api_script}")
                return False
            
            cmd = [
                sys.executable, 
                str(api_script),
                "-a", "127.0.0.1",
                "-p", "9880",
                "-c", str(self.gpt_sovits_path / "GPT_SoVITS/configs/tts_infer.yaml")
            ]
            
            # 在背景啟動 API 服務
            self.api_process = subprocess.Popen(
                cmd,
                cwd=str(self.gpt_sovits_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待服務啟動
            import time
            for i in range(30):  # 等待最多 30 秒
                time.sleep(1)
                if self.check_api_status():
                    logger.info("GPT-SoVITS API 服務啟動成功")
                    return True
            
            logger.error("GPT-SoVITS API 服務啟動失敗")
            return False
            
        except Exception as e:
            logger.error(f"啟動 API 服務失敗: {str(e)}")
            return False
    
    def check_api_status(self) -> bool:
        """檢查 API 服務狀態"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def save_uploaded_audio(self, audio_file, filename: str = None) -> str:
        """保存上傳的音頻文件"""
        try:
            if filename is None:
                filename = f"upload_{hash(audio_file.read())}.wav"
                audio_file.seek(0)  # 重置文件指針
            
            # 確保文件名有正確的副檔名
            if not filename.lower().endswith(('.wav', '.mp3', '.flac', '.m4a')):
                filename += '.wav'
            
            file_path = self.upload_dir / filename
            
            # 保存原始文件
            audio_file.save(str(file_path))
            
            # 轉換為 WAV 格式 (GPT-SoVITS 需要)
            if not filename.lower().endswith('.wav'):
                wav_path = file_path.with_suffix('.wav')
                self.convert_to_wav(str(file_path), str(wav_path))
                os.remove(str(file_path))  # 刪除原始文件
                file_path = wav_path
            
            logger.info(f"音頻文件已保存: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"保存音頻文件失敗: {str(e)}")
            raise
    
    def convert_to_wav(self, input_path: str, output_path: str):
        """轉換音頻格式為 WAV"""
        try:
            # 使用 librosa 讀取音頻
            audio, sr = librosa.load(input_path, sr=None)
            
            # 保存為 WAV 格式
            sf.write(output_path, audio, sr)
            
        except Exception as e:
            logger.error(f"音頻格式轉換失敗: {str(e)}")
            raise
    
    def analyze_audio(self, audio_path: str) -> Dict[str, Any]:
        """分析音頻文件的基本信息"""
        try:
            audio, sr = librosa.load(audio_path, sr=None)
            duration = len(audio) / sr
            
            # 檢測語音活動
            intervals = librosa.effects.split(audio, top_db=20)
            speech_duration = sum([(end - start) / sr for start, end in intervals])
            
            return {
                "duration": duration,
                "sample_rate": sr,
                "speech_duration": speech_duration,
                "silence_ratio": 1 - (speech_duration / duration),
                "quality_score": self.calculate_audio_quality(audio, sr)
            }
            
        except Exception as e:
            logger.error(f"音頻分析失敗: {str(e)}")
            return {}
    
    def calculate_audio_quality(self, audio, sr) -> float:
        """計算音頻質量分數 (0-1)"""
        try:
            # 計算信噪比
            rms = librosa.feature.rms(y=audio)[0]
            snr = np.mean(rms) / (np.std(rms) + 1e-8)
            
            # 計算頻譜質量
            stft = librosa.stft(audio)
            spectral_centroid = librosa.feature.spectral_centroid(S=np.abs(stft))[0]
            spectral_quality = np.mean(spectral_centroid) / (sr / 2)
            
            # 綜合質量分數
            quality = min(1.0, (snr * 0.6 + spectral_quality * 0.4))
            return quality
            
        except:
            return 0.5  # 預設中等質量
    
    def clone_voice(self, 
                   reference_audio_path: str,
                   target_text: str,
                   prompt_text: str = "",
                   language: str = "zh") -> Optional[bytes]:
        """使用 GPT-SoVITS API 克隆語音"""
        try:
            # 如果沒有提供 prompt_text，嘗試自動生成
            if not prompt_text:
                prompt_text = self.generate_prompt_text(reference_audio_path, language)
            
            # 準備 API 請求數據
            payload = {
                "text": target_text,
                "text_lang": language,
                "ref_audio_path": reference_audio_path,
                "prompt_text": prompt_text,
                "prompt_lang": language,
                "top_k": 5,
                "top_p": 1.0,
                "temperature": 1.0,
                "text_split_method": "cut5",
                "batch_size": 1,
                "speed_factor": 1.0,
                "streaming_mode": False,
                "seed": -1,
                "parallel_infer": True,
                "repetition_penalty": 1.35
            }
            
            # 發送請求到 GPT-SoVITS API
            response = requests.post(
                f"{self.api_url}/tts",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                logger.info("語音克隆成功")
                return response.content
            else:
                logger.error(f"語音克隆失敗: {response.status_code}, {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"語音克隆異常: {str(e)}")
            return None
    
    def generate_prompt_text(self, audio_path: str, language: str) -> str:
        """自動生成 prompt 文字 (使用 ASR)"""
        try:
            # 這裡可以整合 ASR 服務來自動識別音頻中的文字
            # 暫時返回預設文字
            default_prompts = {
                "zh": "這是一段參考語音，用於語音克隆。",
                "en": "This is a reference audio for voice cloning.",
                "ja": "これは音声クローニングのための参考音声です。",
                "ko": "이것은 음성 복제를 위한 참조 오디오입니다。"
            }
            return default_prompts.get(language, default_prompts["zh"])
            
        except Exception as e:
            logger.error(f"生成 prompt 文字失敗: {str(e)}")
            return "參考語音"
    
    def batch_clone_voices(self, 
                          reference_audio_path: str,
                          text_list: List[str],
                          prompt_text: str = "",
                          language: str = "zh") -> List[bytes]:
        """批量語音克隆"""
        results = []
        for text in text_list:
            audio_data = self.clone_voice(
                reference_audio_path=reference_audio_path,
                target_text=text,
                prompt_text=prompt_text,
                language=language
            )
            results.append(audio_data)
        return results

# 創建服務實例
clone_service = GPTSoVITSCloneService()

@app.route('/api/voice/upload', methods=['POST'])
def upload_voice():
    """上傳語音文件 API"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': '未提供音頻文件'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': '未選擇文件'}), 400
        
        # 保存上傳的音頻文件
        saved_path = clone_service.save_uploaded_audio(audio_file)
        
        # 分析音頻文件
        analysis = clone_service.analyze_audio(saved_path)
        
        return jsonify({
            'success': True,
            'file_path': saved_path,
            'filename': os.path.basename(saved_path),
            'analysis': analysis,
            'message': '音頻文件上傳成功'
        })
        
    except Exception as e:
        logger.error(f"上傳音頻失敗: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/clone', methods=['POST'])
def clone_voice_api():
    """語音克隆 API"""
    try:
        data = request.get_json()
        
        # 驗證必要參數
        required_fields = ['reference_audio_path', 'target_text']
        if not all(field in data for field in required_fields):
            return jsonify({'error': '缺少必要參數'}), 400
        
        reference_audio_path = data['reference_audio_path']
        target_text = data['target_text']
        prompt_text = data.get('prompt_text', '')
        language = data.get('language', 'zh')
        
        # 檢查參考音頻文件是否存在
        if not os.path.exists(reference_audio_path):
            return jsonify({'error': '參考音頻文件不存在'}), 400
        
        # 執行語音克隆
        audio_data = clone_service.clone_voice(
            reference_audio_path=reference_audio_path,
            target_text=target_text,
            prompt_text=prompt_text,
            language=language
        )
        
        if audio_data:
            # 保存生成的音頻
            output_filename = f"cloned_{hash(target_text)}_{int(time.time())}.wav"
            output_path = clone_service.output_dir / output_filename
            
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            return send_file(
                io.BytesIO(audio_data),
                mimetype='audio/wav',
                as_attachment=True,
                download_name=output_filename
            )
        else:
            return jsonify({'error': '語音克隆失敗'}), 500
            
    except Exception as e:
        logger.error(f"語音克隆 API 錯誤: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/batch-clone', methods=['POST'])
def batch_clone_voice_api():
    """批量語音克隆 API"""
    try:
        data = request.get_json()
        
        # 驗證必要參數
        required_fields = ['reference_audio_path', 'text_list']
        if not all(field in data for field in required_fields):
            return jsonify({'error': '缺少必要參數'}), 400
        
        reference_audio_path = data['reference_audio_path']
        text_list = data['text_list']
        prompt_text = data.get('prompt_text', '')
        language = data.get('language', 'zh')
        
        if not isinstance(text_list, list) or len(text_list) == 0:
            return jsonify({'error': '文字列表不能為空'}), 400
        
        # 執行批量語音克隆
        results = clone_service.batch_clone_voices(
            reference_audio_path=reference_audio_path,
            text_list=text_list,
            prompt_text=prompt_text,
            language=language
        )
        
        # 創建 ZIP 文件包含所有生成的音頻
        import zipfile
        import time
        
        zip_filename = f"batch_cloned_{int(time.time())}.zip"
        zip_path = clone_service.output_dir / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for i, (text, audio_data) in enumerate(zip(text_list, results)):
                if audio_data:
                    audio_filename = f"cloned_{i+1:03d}.wav"
                    zipf.writestr(audio_filename, audio_data)
        
        return send_file(
            str(zip_path),
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_filename
        )
        
    except Exception as e:
        logger.error(f"批量語音克隆 API 錯誤: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/list-uploads', methods=['GET'])
def list_uploaded_files():
    """列出已上傳的音頻文件"""
    try:
        files = []
        for file_path in clone_service.upload_dir.glob("*.wav"):
            stat = file_path.stat()
            files.append({
                'filename': file_path.name,
                'path': str(file_path),
                'size': stat.st_size,
                'created_time': stat.st_ctime,
                'modified_time': stat.st_mtime
            })
        
        # 按修改時間排序
        files.sort(key=lambda x: x['modified_time'], reverse=True)
        
        return jsonify({
            'success': True,
            'files': files,
            'total': len(files)
        })
        
    except Exception as e:
        logger.error(f"列出文件失敗: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/status', methods=['GET'])
def get_service_status():
    """獲取服務狀態"""
    api_status = clone_service.check_api_status()
    
    return jsonify({
        'service_running': True,
        'gpt_sovits_api': api_status,
        'gpt_sovits_path': str(clone_service.gpt_sovits_path),
        'upload_dir': str(clone_service.upload_dir),
        'output_dir': str(clone_service.output_dir)
    })

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    import time
    
    logger.info("啟動語音克隆服務...")
    logger.info(f"GPT-SoVITS 路徑: {clone_service.gpt_sovits_path}")
    logger.info("API 地址: http://localhost:5002")
    
    app.run(host='0.0.0.0', port=5002, debug=True)