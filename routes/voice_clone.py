"""
語音克隆相關路由
實現完整的語音克隆工作流程
"""

import os
from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
from services.gpt_sovits_service import gpt_sovits_service
from services.ai import analyze_and_respond, analyze_and_respond_with_context
from auth import token_required
from config import allowed_file
from database import save_voice_model_info, get_voice_model_by_staff

voice_clone_bp = Blueprint('voice_clone', __name__, url_prefix='/voice_clone')

@voice_clone_bp.route('/generate_reading_text', methods=['GET'])
def generate_reading_text():
    """
    生成約60秒的閱讀文字
    """
    try:
        duration = request.args.get('duration', 60, type=int)
        reading_text = gpt_sovits_service.generate_reading_text(duration)
        
        return jsonify({
            "status": "success",
            "reading_text": reading_text,
            "estimated_duration": duration,
            "character_count": len(reading_text)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"生成閱讀文字失敗: {str(e)}"
        }), 500

@voice_clone_bp.route('/upload_voice_sample', methods=['POST'])
def upload_voice_sample():
    """
    上傳語音樣本並進行處理
    1. 接收WAV格式音頻文件
    2. 進行切分和降噪處理
    3. 保存處理結果
    """
    try:
        # 檢查文件是否存在
        if 'audio_file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "未找到音頻文件"
            }), 400
        
        audio_file = request.files['audio_file']
        staff_code = request.form.get('staff_code')
        reference_text = request.form.get('reference_text')
        
        # 驗證參數
        if not audio_file or audio_file.filename == '':
            return jsonify({
                "status": "error",
                "message": "未選擇文件"
            }), 400
        
        if not staff_code:
            return jsonify({
                "status": "error",
                "message": "缺少客服代號"
            }), 400
        
        if not reference_text:
            return jsonify({
                "status": "error",
                "message": "缺少參考文字"
            }), 400
        
        # 檢查文件格式
        if not allowed_file(audio_file.filename):
            return jsonify({
                "status": "error",
                "message": "不支援的文件格式，請上傳WAV文件"
            }), 400
        
        # 處理音頻文件
        processed_info = gpt_sovits_service.process_uploaded_audio(audio_file, staff_code)
        
        # 設置語音模型
        model_setup_result = gpt_sovits_service.setup_voice_model(processed_info, reference_text)
        
        # 保存到數據庫
        print(f"🗄️ 保存語音模型到數據庫...")
        print(f"   客服代號: {staff_code}")
        print(f"   原始路徑: {processed_info['original_path']}")
        print(f"   處理路徑: {processed_info['denoised_path']}")
        print(f"   參考文字: {reference_text}")
        
        voice_model_id = save_voice_model_info(
            staff_code=staff_code,
            original_audio_path=processed_info["original_path"],
            processed_audio_path=processed_info["denoised_path"],
            reference_text=reference_text,
            model_status="ready"
        )
        
        if voice_model_id:
            print(f"✅ 語音模型保存成功，ID: {voice_model_id}")
        else:
            print(f"❌ 語音模型保存失敗")
        
        return jsonify({
            "status": "success",
            "message": "語音樣本上傳並處理完成",
            "voice_model_id": voice_model_id,
            "staff_code": staff_code,
            "processed_info": {
                "original_filename": processed_info["filename"],
                "processing_steps": ["切分", "降噪", "特徵提取", "模型設置"],
                "model_status": "ready"
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"語音樣本處理失敗: {str(e)}"
        }), 500

@voice_clone_bp.route('/generate_response_voice', methods=['POST'])
def generate_response_voice():
    """
    回傳的文字生成模擬語音 - 支持多轮对话
    """
    try:
        data = request.get_json()
        
        # 獲取基本參數
        user_input = data.get('user_input')  # 用戶輸入的文字
        staff_code = data.get('staff_code')  # 客服代號
        
        # 獲取多轮对话參數
        response_style = data.get('response_style', 'friendly')  # 回應語調
        conversation_mode = data.get('conversation_mode', 'continuous')  # 對話模式
        conversation_context = data.get('conversation_context', [])  # 對話上下文
        conversation_round = data.get('conversation_round', 0)  # 對話輪次
        
        if not user_input:
            return jsonify({
                "status": "error",
                "message": "缺少用戶輸入文字"
            }), 400
        
        if not staff_code:
            return jsonify({
                "status": "error",
                "message": "缺少客服代號"
            }), 400
        
        print(f" MultiTurns Request:")
        print(f"   Client input: {user_input}")
        print(f"   Dialogue turns: {conversation_round}")
        print(f"   Response Style: {response_style}")
        print(f"   Dialogue Style : {conversation_mode}")
        print(f"   Context message counts: {len(conversation_context)}")
        
        # 1. 使用增强的分析並生成回應（支持上下文）
        ai_response = analyze_and_respond_with_context(
            user_input=user_input,
            conversation_context=conversation_context,
            response_style=response_style,
            conversation_mode=conversation_mode,
            conversation_round=conversation_round
        )
        response_text = ai_response.get('response', '')
        sentiment = ai_response.get('sentiment', '未知')
        confidence = ai_response.get('confidence', 0.95)
        
        if not response_text:
            return jsonify({
                "status": "error",
                "message": "AI回應生成失敗"
            }), 500
        
        # 2. 獲取語音模型信息
        voice_model = get_voice_model_by_staff(staff_code)
        if not voice_model:
            # 如果沒有找到語音模型，創建一個臨時的模型記錄
            print(f"⚠️ 未找到客服代號 {staff_code} 的語音模型，創建臨時模型")
            
            # 檢查是否有上傳的音頻文件
            from database import get_all_voice_models
            all_models = get_all_voice_models()
            
            if all_models:
                # 使用最近上傳的模型作為參考
                latest_model = all_models[0]
                voice_model = {
                    'processed_audio_path': latest_model['processed_audio_path'],
                    'reference_text': latest_model['reference_text']
                }
                print(f"🔄 使用最近的語音模型作為參考: {latest_model['staff_code']}")
            else:
                # 創建一個默認的模型記錄
                
                voice_model = {
                    'processed_audio_path': './TTS/vc.wav',  # 使用相對路徑，適用於Ubuntu
                    'reference_text': '使用軟件者、傳播軟件導出的聲音者自負全責。如不認可該條款，則不能使用或引用軟件'
                }
                
                print(f"📝 創建默認語音模型記錄")
        
        # 3. 使用新的GPT-SoVITS TTS API生成回應語音
        from services.tts import gpt_sovits_tts
        
        print(f"🎵 開始生成語音回應...")
        print(f"📝 LLM Model 回應文字: {response_text[:100]}...")
        print(f"🎤 參考音頻: {voice_model['processed_audio_path']}")
        print(f"📄 參考文字: {voice_model['reference_text']}")
        
        # 使用新的TTS服務生成語音
        generated_audio_path = gpt_sovits_tts.generate_speech(
            text=response_text,
            ref_audio_path=voice_model['processed_audio_path'],
            prompt_text=voice_model['reference_text'],
            text_lang="zh",
            prompt_lang="zh",
            temperature=1.1
        )
        
        if not generated_audio_path:
            return jsonify({
                "status": "error",
                "message": "語音生成失敗，請檢查GPT-SoVITS服務是否正常運行"
            }), 500
        
        # 構建語音結果
        import time
        voice_result = {
            "audio_url": f"/genvoice/{os.path.basename(generated_audio_path)}",
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "audio_path": generated_audio_path
        }
        
        print(f"✅ 語音生成成功: {voice_result['audio_url']}")
        
        return jsonify({
            "status": "success",
            "user_input": user_input,
            "ai_analysis": {
                "sentiment": sentiment,
                "response_text": response_text,
                "confidence": confidence,
                "conversation_round": conversation_round,
                "response_style": response_style
            },
            "voice_output": {
                "audio_url": voice_result["audio_url"],
                "staff_code": staff_code,
                "generated_at": voice_result.get("generated_at")
            },
            "conversation_metadata": {
                "total_context_messages": len(conversation_context),
                "conversation_mode": conversation_mode,
                "is_multi_turn": conversation_round > 0
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"語音回應生成失敗: {str(e)}"
        }), 500

@voice_clone_bp.route('/voice_models', methods=['GET'])
def list_voice_models():
    """
    獲取所有可用的語音模型列表
    """
    try:
        from database import get_all_voice_models
        
        models = get_all_voice_models()
        
        return jsonify({
            "status": "success",
            "voice_models": models,
            "total_count": len(models)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"獲取語音模型列表失敗: {str(e)}"
        }), 500

@voice_clone_bp.route('/voice_model/<staff_code>', methods=['GET'])
def get_voice_model_info(staff_code):
    """
    獲取特定客服的語音模型信息
    """
    try:
        voice_model = get_voice_model_by_staff(staff_code)
        
        if not voice_model:
            return jsonify({
                "status": "error",
                "message": f"未找到客服代號 {staff_code} 的語音模型"
            }), 404
        
        return jsonify({
            "status": "success",
            "voice_model": voice_model
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"獲取語音模型信息失敗: {str(e)}"
        }), 500

@voice_clone_bp.route('/test_voice_generation', methods=['POST'])
def test_voice_generation():
    """
    測試語音生成功能
    """
    try:
        data = request.get_json()
        
        test_text = data.get('test_text', '這是一段測試語音，用來驗證語音克隆效果。')
        staff_code = data.get('staff_code')
        
        if not staff_code:
            return jsonify({
                "status": "error",
                "message": "缺少客服代號"
            }), 400
        
        # 獲取語音模型
        voice_model = get_voice_model_by_staff(staff_code)
        if not voice_model:
            # 如果沒有找到語音模型，嘗試使用任何可用的模型
            from database import get_all_voice_models
            all_models = get_all_voice_models()
            
            if all_models:
                voice_model = all_models[0]  # 使用第一個可用的模型
                print(f"🔄 使用可用的語音模型: {voice_model['staff_code']}")
            else:
                # 創建一個臨時的測試模型
                voice_model = {
                    'processed_audio_path': './TTS/vc.wav',  # 統一使用TTS目錄
                    'reference_text': '這是一個測試語音'
                }
                print(f"📝 使用默認測試模型")
        
        # 使用新的GPT-SoVITS TTS API生成測試語音
        from services.tts import gpt_sovits_tts
        
        print(f"🧪 開始生成測試語音...")
        print(f"📝 測試文字: {test_text}")
        print(f"🎤 參考音頻: {voice_model['processed_audio_path']}")
        
        generated_audio_path = gpt_sovits_tts.generate_speech(
            text=test_text,
            ref_audio_path=voice_model['processed_audio_path'],
            prompt_text=voice_model['reference_text'],
            text_lang="zh",
            prompt_lang="zh",
            temperature=1.1
        )
        
        if not generated_audio_path:
            return jsonify({
                "status": "error",
                "message": "測試語音生成失敗，請檢查GPT-SoVITS服務是否正常運行"
            }), 500
        
        voice_result = {
            "audio_url": f"/genvoice/{os.path.basename(generated_audio_path)}",
            "audio_path": generated_audio_path
        }
        
        return jsonify({
            "status": "success",
            "message": "測試語音生成成功",
            "test_text": test_text,
            "audio_url": voice_result["audio_url"],
            "staff_code": staff_code
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"測試語音生成失敗: {str(e)}"
        }), 500

@voice_clone_bp.route('/demo', methods=['GET'])
def voice_clone_demo():
    """
    語音克隆系統演示頁面
    """
    from flask import render_template
    return render_template('voice_clone_demo.html')