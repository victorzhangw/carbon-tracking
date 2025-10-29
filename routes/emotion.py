from flask import Blueprint, request, jsonify
from services.emotion_recognition import emotion_recognizer
from services.emotion_recognition_advanced import advanced_emotion_recognizer
from database import get_audio_by_id
import os

emotion_bp = Blueprint('emotion', __name__, url_prefix='/api/emotion')

@emotion_bp.route('/analyze/<audio_id>', methods=['POST'])
def analyze_emotion(audio_id):
    """分析指定音檔的情緒"""
    try:
        # 獲取音檔記錄
        audio = get_audio_by_id(audio_id)
        if not audio:
            return jsonify({"error": "找不到該錄音記錄"}), 404
        
        # 檢查檔案是否存在
        file_path = audio['file_path']
        if not os.path.exists(file_path):
            return jsonify({"error": "音頻檔案不存在"}), 404
        
        # 獲取分析方法參數
        method = request.json.get('method', 'basic') if request.json else 'basic'
        
        # 根據方法選擇分析器
        if method == 'advanced':
            result = advanced_emotion_recognizer.predict_emotion(file_path)
        else:
            result = emotion_recognizer.predict_emotion(file_path)
        
        if "error" in result:
            return jsonify(result), 500
        
        # 加入音檔資訊
        result["audio_info"] = {
            "id": audio_id,
            "name": audio['name'],
            "duration": audio['duration'],
            "staff_name": audio.get('staff_name', '未指定')
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"情緒分析失敗: {e}")
        return jsonify({"error": f"情緒分析失敗: {str(e)}"}), 500

@emotion_bp.route('/batch-analyze', methods=['POST'])
def batch_analyze_emotions():
    """批量分析多個音檔的情緒"""
    try:
        data = request.json
        audio_ids = data.get('audio_ids', [])
        method = data.get('method', 'basic')
        
        if not audio_ids:
            return jsonify({"error": "請提供音檔 ID 列表"}), 400
        
        results = []
        
        for audio_id in audio_ids:
            # 獲取音檔記錄
            audio = get_audio_by_id(audio_id)
            if not audio:
                results.append({
                    "audio_id": audio_id,
                    "error": "找不到該錄音記錄"
                })
                continue
            
            # 檢查檔案是否存在
            file_path = audio['file_path']
            if not os.path.exists(file_path):
                results.append({
                    "audio_id": audio_id,
                    "error": "音頻檔案不存在"
                })
                continue
            
            # 進行情緒分析
            try:
                if method == 'advanced':
                    emotion_result = advanced_emotion_recognizer.predict_emotion(file_path)
                else:
                    emotion_result = emotion_recognizer.predict_emotion(file_path)
                
                emotion_result["audio_id"] = audio_id
                emotion_result["audio_name"] = audio['name']
                results.append(emotion_result)
                
            except Exception as e:
                results.append({
                    "audio_id": audio_id,
                    "error": f"分析失敗: {str(e)}"
                })
        
        return jsonify({
            "message": f"批量分析完成，共處理 {len(audio_ids)} 個音檔",
            "results": results
        }), 200
        
    except Exception as e:
        print(f"批量情緒分析失敗: {e}")
        return jsonify({"error": f"批量分析失敗: {str(e)}"}), 500

@emotion_bp.route('/upload-and-analyze', methods=['POST'])
def upload_and_analyze():
    """上傳音檔並立即進行情緒分析"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "未上傳檔案"}), 400
        
        file = request.files['file']
        method = request.form.get('method', 'basic')
        
        if file.filename == '':
            return jsonify({"error": "未選擇檔案"}), 400
        
        # 暫存檔案進行分析
        import tempfile
        import uuid
        
        temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
        temp_path = os.path.join(tempfile.gettempdir(), temp_filename)
        
        try:
            file.save(temp_path)
            
            # 進行情緒分析
            if method == 'advanced':
                result = advanced_emotion_recognizer.predict_emotion(temp_path)
            else:
                result = emotion_recognizer.predict_emotion(temp_path)
            
            return jsonify(result), 200
            
        finally:
            # 清理暫存檔案
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        print(f"上傳並分析失敗: {e}")
        return jsonify({"error": f"上傳並分析失敗: {str(e)}"}), 500

@emotion_bp.route('/models/status', methods=['GET'])
def get_models_status():
    """獲取情緒識別模型狀態"""
    try:
        basic_status = "可用"
        advanced_status = "未載入"
        
        # 檢查進階模型狀態
        if advanced_emotion_recognizer.model is not None:
            advanced_status = "已載入"
        
        return jsonify({
            "models": {
                "basic": {
                    "status": basic_status,
                    "description": "基於 librosa 的特徵分析"
                },
                "advanced": {
                    "status": advanced_status,
                    "description": "基於 Wav2Vec2 的深度學習模型"
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"獲取模型狀態失敗: {str(e)}"}), 500

@emotion_bp.route('/models/load-advanced', methods=['POST'])
def load_advanced_model():
    """載入進階情緒識別模型"""
    try:
        success = advanced_emotion_recognizer.load_model()
        
        if success:
            return jsonify({"message": "進階模型載入成功"}), 200
        else:
            return jsonify({"error": "進階模型載入失敗"}), 500
            
    except Exception as e:
        return jsonify({"error": f"載入模型失敗: {str(e)}"}), 500