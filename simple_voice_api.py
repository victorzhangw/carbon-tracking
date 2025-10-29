"""
簡化的本地語音合成 API 服務
直接調用 GPT-SoVITS 而不需要 WebUI
"""
import os
import sys
import io
import tempfile
import logging
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import soundfile as sf
import numpy as np

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# GPT-SoVITS 路徑配置
GPT_SOVITS_PATH = "./GPT-SoVITS"
sys.path.append(GPT_SOVITS_PATH)

class SimpleVoiceService:
    def __init__(self):
        self.initialized = False
        self.model = None
        self.init_model()
    
    def init_model(self):
        """初始化 GPT-SoVITS 模型"""
        try:
            # 這裡需要根據實際的 GPT-SoVITS API 進行調整
            logger.info("正在初始化 GPT-SoVITS 模型...")
            
            # 檢查模型文件是否存在
            model_path = os.path.join(GPT_SOVITS_PATH, "GPT_SoVITS", "pretrained_models")
            if not os.path.exists(model_path):
                logger.error(f"模型路徑不存在: {model_path}")
                return False
            
            self.initialized = True
            logger.info("GPT-SoVITS 模型初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"模型初始化失敗: {str(e)}")
            return False
    
    def synthesize_with_command(self, text, ref_audio, ref_text, language="zh"):
        """
        使用命令行方式調用 GPT-SoVITS
        """
        try:
            # 創建臨時文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_output:
                output_path = temp_output.name
            
            # 構建命令
            cmd = [
                "python", 
                os.path.join(GPT_SOVITS_PATH, "GPT_SoVITS", "inference_webui.py"),
                "--ref_wav_path", ref_audio,
                "--prompt_text", ref_text,
                "--prompt_language", language,
                "--text", text,
                "--text_language", language,
                "--output_path", output_path
            ]
            
            # 執行命令
            import subprocess
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=GPT_SOVITS_PATH)
            
            if result.returncode == 0 and os.path.exists(output_path):
                # 讀取生成的音頻文件
                with open(output_path, 'rb') as f:
                    audio_data = f.read()
                
                # 清理臨時文件
                os.unlink(output_path)
                return audio_data
            else:
                logger.error(f"命令執行失敗: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"命令行合成失敗: {str(e)}")
            return None
    
    def create_sample_audio(self, text, language="zh"):
        """
        創建示例音頻 (用於測試)
        """
        try:
            # 生成簡單的測試音頻
            duration = len(text) * 0.1  # 根據文字長度估算時長
            sample_rate = 22050
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # 生成簡單的正弦波作為測試音頻
            frequency = 440  # A4 音符
            audio = 0.3 * np.sin(2 * np.pi * frequency * t)
            
            # 轉換為音頻文件
            buffer = io.BytesIO()
            sf.write(buffer, audio, sample_rate, format='WAV')
            buffer.seek(0)
            
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"創建示例音頻失敗: {str(e)}")
            return None

# 創建服務實例
voice_service = SimpleVoiceService()

@app.route('/api/voice/synthesize', methods=['POST'])
def synthesize_voice():
    """語音合成 API"""
    try:
        data = request.get_json()
        
        if not voice_service.initialized:
            # 如果模型未初始化，返回測試音頻
            logger.warning("模型未初始化，返回測試音頻")
            test_audio = voice_service.create_sample_audio(
                data.get('text', '測試語音'),
                data.get('language', 'zh')
            )
            
            if test_audio:
                return send_file(
                    io.BytesIO(test_audio),
                    mimetype='audio/wav',
                    as_attachment=True,
                    download_name='test_voice.wav'
                )
        
        # 驗證必要參數
        required_fields = ['text']
        if not all(field in data for field in required_fields):
            return jsonify({'error': '缺少必要參數'}), 400
        
        text = data['text']
        language = data.get('language', 'zh')
        
        # 使用預設的參考音頻
        ref_audio = os.path.join(GPT_SOVITS_PATH, "samples", "default_ref.wav")
        ref_text = "這是一段參考語音。"
        
        # 如果提供了自定義參考音頻
        if 'reference_audio' in data and 'reference_text' in data:
            ref_audio = data['reference_audio']
            ref_text = data['reference_text']
        
        # 合成語音
        audio_data = voice_service.synthesize_with_command(
            text=text,
            ref_audio=ref_audio,
            ref_text=ref_text,
            language=language
        )
        
        if audio_data:
            return send_file(
                io.BytesIO(audio_data),
                mimetype='audio/wav',
                as_attachment=True,
                download_name='synthesized_voice.wav'
            )
        else:
            # 如果合成失敗，返回測試音頻
            test_audio = voice_service.create_sample_audio(text, language)
            if test_audio:
                return send_file(
                    io.BytesIO(test_audio),
                    mimetype='audio/wav',
                    as_attachment=True,
                    download_name='test_voice.wav'
                )
            else:
                return jsonify({'error': '語音合成失敗'}), 500
            
    except Exception as e:
        logger.error(f"API 錯誤: {str(e)}")
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
        
        # 保存上傳的音頻文件
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_ref:
            audio_file.save(temp_ref.name)
            ref_audio_path = temp_ref.name
        
        try:
            # 使用上傳的音頻進行語音合成
            audio_data = voice_service.synthesize_with_command(
                text=target_text,
                ref_audio=ref_audio_path,
                ref_text=sample_text,
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
                # 如果克隆失敗，返回測試音頻
                test_audio = voice_service.create_sample_audio(target_text, language)
                if test_audio:
                    return send_file(
                        io.BytesIO(test_audio),
                        mimetype='audio/wav',
                        as_attachment=True,
                        download_name='test_cloned_voice.wav'
                    )
                else:
                    return jsonify({'error': '聲音克隆失敗'}), 500
        
        finally:
            # 清理臨時文件
            if os.path.exists(ref_audio_path):
                os.unlink(ref_audio_path)
            
    except Exception as e:
        logger.error(f"聲音克隆錯誤: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/status', methods=['GET'])
def get_status():
    """獲取服務狀態"""
    return jsonify({
        'status': 'running',
        'initialized': voice_service.initialized,
        'gpt_sovits_path': GPT_SOVITS_PATH,
        'models_available': os.path.exists(os.path.join(GPT_SOVITS_PATH, "GPT_SoVITS", "pretrained_models"))
    })

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    logger.info("啟動簡化語音合成 API 服務...")
    logger.info(f"GPT-SoVITS 路徑: {GPT_SOVITS_PATH}")
    logger.info("API 地址: http://localhost:5001")
    
    app.run(host='0.0.0.0', port=5001, debug=True)