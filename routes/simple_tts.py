"""
簡單TTS服務路由
直接調用GPT-SoVITS的TTS功能
"""

import os
import time
from flask import Blueprint, request, jsonify, render_template
from voice_config import OUTPUT_DIR
# 注意：此路由使用旧的Gradio客户端方式，已被新的GPT-SoVITS TTS API替代

simple_tts_bp = Blueprint('simple_tts', __name__, url_prefix='/simple_tts')

@simple_tts_bp.route('/demo', methods=['GET'])
def simple_tts_demo():
    """
    簡單TTS演示頁面
    """
    return render_template('simple_tts_demo.html')

@simple_tts_bp.route('/generate', methods=['POST'])
def generate_tts():
    """
    生成TTS語音
    """
    try:
        data = request.get_json()
        
        # 獲取參數
        text = data.get('text', '')

        ref_audio_path = data.get('ref_audio_path', '')
        ref_text = data.get('ref_text', '')
        speed = data.get('speed', 1.0)
        
        if not text.strip():
            return jsonify({
                "status": "error",
                "message": "請輸入要轉換的文字"
            }), 400
        
        print(f"🎵 TTS請求: {text}")
        print(f"📁 參考音頻: {ref_audio_path}")
        print(f"📝 參考文字: {ref_text}")
        
        # 確保輸出目錄存在
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # 使用新的GPT-SoVITS TTS服務
        from services.tts import gpt_sovits_tts
        print(f"✅ 使用新的GPT-SoVITS TTS服務")
        
        # 檢查參考音頻文件是否存在
        if not os.path.exists(ref_audio_path):
            # 嘗試使用mockvoice目錄中的任何音頻文件
            mockvoice_dir = './mockvoice'
            if os.path.exists(mockvoice_dir):
                wav_files = [f for f in os.listdir(mockvoice_dir) if f.endswith('.wav')]
                if wav_files:
                    ref_audio_path = os.path.join(mockvoice_dir, wav_files[0])
                    print(f"🔄 使用mockvoice中的音頻: {ref_audio_path}")
                else:
                    return jsonify({
                        "status": "error",
                        "message": "沒有找到可用的參考音頻文件"
                    }), 400
            else:
                return jsonify({
                    "status": "error",
                    "message": "參考音頻文件不存在"
                }), 400
        
        # 調用新的GPT-SoVITS TTS API
        try:
            # 使用新的TTS服務生成語音
            generated_audio_path = gpt_sovits_tts.generate_speech(
                text=text,
                ref_audio_path=ref_audio_path,
                prompt_text=ref_text,
                temperature=1.0 + (speed - 1.0) * 0.5  # 將speed轉換為temperature
            )
            
            if generated_audio_path:
                # 獲取文件名
                output_filename = os.path.basename(generated_audio_path)
                print(f"✅ TTS生成成功: {generated_audio_path}")
                
                return jsonify({
                    "status": "success",
                    "message": "語音生成成功",
                    "audio_url": f"/genvoice/{output_filename}",
                    "text": text,
                    "ref_audio": ref_audio_path,
                    "ref_text": ref_text
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "語音生成失敗"
                }), 500
            
        except Exception as e:
            print(f"❌ TTS生成失敗: {e}")
            return jsonify({
                "status": "error",
                "message": f"語音生成失敗: {str(e)}"
            }), 500
            
    except Exception as e:
        print(f"❌ TTS請求處理錯誤: {e}")
        return jsonify({
            "status": "error",
            "message": f"請求處理失敗: {str(e)}"
        }), 500

@simple_tts_bp.route('/list_ref_audio', methods=['GET'])
def list_ref_audio():
    """
    列出可用的參考音頻文件
    """
    try:
        audio_files = []
        
        # 檢查mockvoice目錄
        mockvoice_dir = './mockvoice'
        if os.path.exists(mockvoice_dir):
            for file in os.listdir(mockvoice_dir):
                if file.endswith('.wav'):
                    audio_files.append({
                        "path": os.path.join(mockvoice_dir, file),
                        "name": file,
                        "type": "mockvoice"
                    })
        
        # 檢查上傳的音頻文件
        upload_dir = './audio_uploads'
        if os.path.exists(upload_dir):
            for staff_dir in os.listdir(upload_dir):
                staff_path = os.path.join(upload_dir, staff_dir)
                if os.path.isdir(staff_path):
                    for file in os.listdir(staff_path):
                        if file.endswith('.wav'):
                            audio_files.append({
                                "path": os.path.join(staff_path, file),
                                "name": f"{staff_dir}/{file}",
                                "type": "uploaded"
                            })
        
        return jsonify({
            "status": "success",
            "audio_files": audio_files,
            "total": len(audio_files)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"獲取音頻文件列表失敗: {str(e)}"
        }), 500