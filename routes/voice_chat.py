"""
語音互動聊天系統路由
實現語音識別 -> 文字顯示 -> AI回應 -> 語音合成的完整流程
"""

import os
import time
import tempfile
from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
import speech_recognition as sr
from services.ai import analyze_and_respond
from services.gpt_sovits_service import gpt_sovits_service
from database import get_voice_model_by_staff, get_all_voice_models

voice_chat_bp = Blueprint('voice_chat', __name__, url_prefix='/voice_chat')

@voice_chat_bp.route('/demo', methods=['GET'])
def voice_chat_demo():
    """
    語音互動演示頁面
    """
    return render_template('voice_chat_demo.html')

@voice_chat_bp.route('/recognize_speech', methods=['POST'])
def recognize_speech():
    """
    語音識別API
    接收音頻文件，返回識別的文字
    """
    try:
        # 檢查是否有上傳的音頻文件
        if 'audio' not in request.files:
            return jsonify({
                "status": "error",
                "message": "沒有上傳音頻文件"
            }), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({
                "status": "error",
                "message": "沒有選擇文件"
            }), 400
        
        # 保存臨時音頻文件
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, secure_filename(audio_file.filename))
        audio_file.save(temp_path)
        
        print(f"🎤 開始語音識別: {temp_path}")
        
        # 使用SpeechRecognition進行語音識別
        recognizer = sr.Recognizer()
        
        try:
            with sr.AudioFile(temp_path) as source:
                # 調整環境噪音
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.record(source)
            
            # 使用Google語音識別（支持中文）
            try:
                text = recognizer.recognize_google(audio_data, language='zh-TW')
                print(f"✅ 語音識別成功: {text}")
                
                # 清理臨時文件
                os.remove(temp_path)
                os.rmdir(temp_dir)
                
                return jsonify({
                    "status": "success",
                    "text": text,
                    "message": "語音識別成功"
                })
                
            except sr.UnknownValueError:
                print("❌ 無法識別語音內容")
                return jsonify({
                    "status": "error",
                    "message": "無法識別語音內容，請重新錄音"
                }), 400
                
            except sr.RequestError as e:
                print(f"❌ 語音識別服務錯誤: {e}")
                return jsonify({
                    "status": "error",
                    "message": f"語音識別服務錯誤: {str(e)}"
                }), 500
                
        except Exception as e:
            print(f"❌ 音頻處理錯誤: {e}")
            return jsonify({
                "status": "error",
                "message": f"音頻處理錯誤: {str(e)}"
            }), 500
            
    except Exception as e:
        print(f"❌ 語音識別請求錯誤: {e}")
        return jsonify({
            "status": "error",
            "message": f"請求處理失敗: {str(e)}"
        }), 500

@voice_chat_bp.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    """
    獲取AI回應
    接收用戶文字，返回AI分析和回應
    """
    try:
        data = request.get_json()
        user_text = data.get('text', '').strip()
        
        if not user_text:
            return jsonify({
                "status": "error",
                "message": "沒有輸入文字"
            }), 400
        
        print(f"🤖 AI分析用戶輸入: {user_text}")
        
        # 使用 AI分析並生成回應
        ai_result = analyze_and_respond(user_text)
        
        response_text = ai_result.get('response', '')
        sentiment = ai_result.get('sentiment', '未知')
        
        if not response_text:
            return jsonify({
                "status": "error",
                "message": "AI回應生成失敗"
            }), 500
        
        print(f"✅ AI回應生成成功: {response_text}")
        
        return jsonify({
            "status": "success",
            "user_text": user_text,
            "response_text": response_text,
            "sentiment": sentiment,
            "message": "AI回應生成成功"
        })
        
    except Exception as e:
        print(f"❌ AI回應生成錯誤: {e}")
        return jsonify({
            "status": "error",
            "message": f"AI回應生成失敗: {str(e)}"
        }), 500

@voice_chat_bp.route('/generate_response_voice', methods=['POST'])
def generate_response_voice():
    """
    生成回應語音
    接收AI回應文字，生成語音
    """
    try:
        data = request.get_json()
        response_text = data.get('response_text', '').strip()
        staff_code = data.get('staff_code', 'default')
        
        if not response_text:
            return jsonify({
                "status": "error",
                "message": "沒有回應文字"
            }), 400
        
        print(f"🎵 生成回應語音: {response_text}")
        
        # 獲取語音模型
        voice_model = get_voice_model_by_staff(staff_code)
        if not voice_model:
            # 使用任何可用的語音模型
            all_models = get_all_voice_models()
            if all_models:
                voice_model = all_models[0]
                print(f"🔄 使用可用的語音模型: {voice_model['staff_code']}")
            else:
                # 使用默認設置
                voice_model = {
                    'processed_audio_path': './mockvoice/vc.wav',
                    'reference_text': '使用軟件者、傳播軟件導出的聲音者自負全責。如不認可該條款，則不能使用或引用軟件'
                }
                print(f"📝 使用默認語音設置")
        
        # 生成語音
        voice_result = gpt_sovits_service.generate_voice_response(
            text=response_text,
            staff_code=staff_code,
            reference_audio_path=voice_model['processed_audio_path'],
            reference_text=voice_model['reference_text']
        )
        
        print(f"✅ 語音生成成功: {voice_result['audio_url']}")
        
        return jsonify({
            "status": "success",
            "audio_url": voice_result["audio_url"],
            "response_text": response_text,
            "staff_code": staff_code,
            "method": voice_result.get("method", "unknown"),
            "message": "語音生成成功"
        })
        
    except Exception as e:
        print(f"❌ 語音生成錯誤: {e}")
        return jsonify({
            "status": "error",
            "message": f"語音生成失敗: {str(e)}"
        }), 500

@voice_chat_bp.route('/full_conversation', methods=['POST'])
def full_conversation():
    """
    完整對話流程
    語音識別 -> AI回應 -> 語音合成
    """
    try:
        # 檢查是否有上傳的音頻文件
        if 'audio' not in request.files:
            return jsonify({
                "status": "error",
                "message": "沒有上傳音頻文件"
            }), 400
        
        audio_file = request.files['audio']
        staff_code = request.form.get('staff_code', 'default')
        
        # 步驟1：語音識別
        print("🎤 步驟1：語音識別")
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, secure_filename(audio_file.filename))
        audio_file.save(temp_path)
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
        
        user_text = recognizer.recognize_google(audio_data, language='zh-TW')
        print(f"✅ 識別結果: {user_text}")
        
        # 步驟2：AI回應
        print("🤖 步驟2：AI分析")
        ai_result = analyze_and_respond(user_text)
        response_text = ai_result.get('response', '')
        sentiment = ai_result.get('sentiment', '未知')
        print(f"✅ AI回應: {response_text}")
        
        # 步驟3：語音合成
        print("🎵 步驟3：語音合成")
        voice_model = get_voice_model_by_staff(staff_code)
        if not voice_model:
            all_models = get_all_voice_models()
            if all_models:
                voice_model = all_models[0]
            else:
                voice_model = {
                    'processed_audio_path': './mockvoice/vc.wav',
                    'reference_text': '使用軟件者、傳播軟件導出的聲音者自負全責。如不認可該條款，則不能使用或引用軟件'
                }
        
        voice_result = gpt_sovits_service.generate_voice_response(
            text=response_text,
            staff_code=staff_code,
            reference_audio_path=voice_model['processed_audio_path'],
            reference_text=voice_model['reference_text']
        )
        
        # 清理臨時文件
        os.remove(temp_path)
        os.rmdir(temp_dir)
        
        print(f"✅ 完整對話流程完成")
        
        return jsonify({
            "status": "success",
            "user_text": user_text,
            "response_text": response_text,
            "sentiment": sentiment,
            "audio_url": voice_result["audio_url"],
            "staff_code": staff_code,
            "method": voice_result.get("method", "unknown"),
            "message": "對話完成"
        })
        
    except sr.UnknownValueError:
        return jsonify({
            "status": "error",
            "message": "無法識別語音內容，請重新錄音"
        }), 400
        
    except Exception as e:
        print(f"❌ 完整對話流程錯誤: {e}")
        return jsonify({
            "status": "error",
            "message": f"對話處理失敗: {str(e)}"
        }), 500

@voice_chat_bp.route('/get_available_voices', methods=['GET'])
def get_available_voices():
    """
    獲取可用的語音模型列表
    """
    try:
        voice_models = get_all_voice_models()
        
        # 添加默認選項
        available_voices = [{
            "staff_code": "default",
            "name": "默認語音",
            "status": "ready"
        }]
        
        for model in voice_models:
            available_voices.append({
                "staff_code": model.get('staff_code', ''),
                "name": model.get('staff_name', model.get('staff_code', '')),
                "status": model.get('model_status', 'unknown')
            })
        
        return jsonify({
            "status": "success",
            "voices": available_voices,
            "total": len(available_voices)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"獲取語音列表失敗: {str(e)}"
        }), 500