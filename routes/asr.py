"""
ASR API 路由
提供語音識別 REST API 接口
"""

import asyncio
import logging
from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
from auth import token_required
from services.asr.coordinator import ASRCoordinator

logger = logging.getLogger(__name__)

# 創建藍圖
asr_bp = Blueprint('asr', __name__, url_prefix='/api/asr')

# 全局 ASR Coordinator 實例（單例模式）
_asr_coordinator = None


def get_asr_coordinator():
    """獲取 ASR Coordinator 單例"""
    global _asr_coordinator
    if _asr_coordinator is None:
        logger.info("初始化 ASR Coordinator...")
        _asr_coordinator = ASRCoordinator(
            whisper_model_size="base",  # 可從配置讀取
            enable_funasr=False,  # FunASR 暫時未啟用
            device="cuda"  # 自動檢測
        )
        logger.info("ASR Coordinator 初始化完成")
    return _asr_coordinator


@asr_bp.route('/recognize', methods=['POST'])
@token_required
def recognize_audio():
    """
    單個音頻識別 API
    
    請求:
        - file: 音頻文件（multipart/form-data）
        - language_hint: 語言提示（可選，zh/zh-TW/minnan）
        - return_details: 是否返回詳細信息（可選，true/false）
        - enable_minnan_optimization: 是否啟用閩南語優化（可選，true/false）
    
    響應:
        {
            "success": true,
            "text": "識別的文本",
            "confidence": 0.85,
            "language": "zh",
            "audio_duration": 5.2,
            "processing_time": 1.5,
            "details": {...}  // 如果 return_details=true
        }
    """
    try:
        # 檢查文件
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '未提供音頻文件'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '文件名為空'
            }), 400
        
        # 讀取音頻數據
        audio_data = file.read()
        
        # 獲取選項
        options = {
            'language_hint': request.form.get('language_hint', 'zh'),
            'return_details': request.form.get('return_details', 'false').lower() == 'true',
            'enable_minnan_optimization': request.form.get('enable_minnan_optimization', 'true').lower() == 'true'
        }
        
        logger.info(f"收到識別請求: {file.filename}, 大小: {len(audio_data)} bytes")
        
        # 執行識別（異步轉同步）
        coordinator = get_asr_coordinator()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            coordinator.recognize(audio_data, options)
        )
        loop.close()
        
        logger.info(f"識別完成: {result.get('text', '')[:50]}...")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"識別失敗: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@asr_bp.route('/batch-recognize', methods=['POST'])
@token_required
def batch_recognize_audio():
    """
    批次音頻識別 API
    
    請求:
        - files: 多個音頻文件（multipart/form-data）
        - language_hint: 語言提示（可選）
        - return_details: 是否返回詳細信息（可選）
    
    響應:
        {
            "success": true,
            "results": [
                {
                    "index": 0,
                    "text": "...",
                    "confidence": 0.85,
                    ...
                },
                ...
            ],
            "total": 3,
            "successful": 3,
            "failed": 0
        }
    """
    try:
        # 檢查文件
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': '未提供音頻文件'
            }), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({
                'success': False,
                'error': '文件列表為空'
            }), 400
        
        # 讀取所有音頻數據
        audio_data_list = []
        for file in files:
            if file.filename:
                audio_data_list.append(file.read())
        
        if not audio_data_list:
            return jsonify({
                'success': False,
                'error': '沒有有效的音頻文件'
            }), 400
        
        # 獲取選項
        options = {
            'language_hint': request.form.get('language_hint', 'zh'),
            'return_details': request.form.get('return_details', 'false').lower() == 'true'
        }
        
        logger.info(f"收到批次識別請求: {len(audio_data_list)} 個文件")
        
        # 執行批次識別
        coordinator = get_asr_coordinator()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(
            coordinator.recognize_batch(audio_data_list, options)
        )
        loop.close()
        
        # 統計結果
        successful = sum(1 for r in results if r.get('success', False))
        failed = len(results) - successful
        
        logger.info(f"批次識別完成: 成功 {successful}/{len(results)}")
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'successful': successful,
            'failed': failed
        }), 200
        
    except Exception as e:
        logger.error(f"批次識別失敗: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@asr_bp.route('/status', methods=['GET'])
@token_required
def get_status():
    """
    獲取 ASR 系統狀態
    
    響應:
        {
            "status": "ready",
            "system_info": {...},
            "uptime": 3600
        }
    """
    try:
        coordinator = get_asr_coordinator()
        system_info = coordinator.get_system_info()
        
        return jsonify({
            'status': 'ready',
            'system_info': system_info
        }), 200
        
    except Exception as e:
        logger.error(f"獲取狀態失敗: {e}", exc_info=True)
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@asr_bp.route('/clear-cache', methods=['POST'])
@token_required
def clear_cache():
    """
    清理系統快取
    
    響應:
        {
            "success": true,
            "message": "快取已清理"
        }
    """
    try:
        coordinator = get_asr_coordinator()
        coordinator.clear_cache()
        
        return jsonify({
            'success': True,
            'message': '快取已清理'
        }), 200
        
    except Exception as e:
        logger.error(f"清理快取失敗: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@asr_bp.route('/health', methods=['GET'])
def health_check():
    """
    健康檢查（無需認證）
    
    響應:
        {
            "status": "healthy",
            "timestamp": "2024-10-29T16:00:00"
        }
    """
    import datetime
    
    try:
        # 簡單檢查 coordinator 是否可用
        coordinator = get_asr_coordinator()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'service': 'ASR API',
            'version': '1.0.0'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }), 503


@asr_bp.route('/test', methods=['GET'])
def test_page():
    """
    ASR 測試頁面
    """
    return render_template('asr_test.html')


@asr_bp.route('/recognize-test', methods=['POST'])
def recognize_audio_test():
    """
    測試用的音頻識別 API（無需認證）
    
    請求:
        - file: 音頻文件（multipart/form-data）
        - language_hint: 語言提示（可選，zh/zh-TW/minnan）
        - return_details: 是否返回詳細信息（可選，true/false）
        - enable_minnan_optimization: 是否啟用閩南語優化（可選，true/false）
    
    響應:
        {
            "success": true,
            "text": "識別的文本",
            "confidence": 0.85,
            "language": "zh",
            "audio_duration": 5.2,
            "processing_time": 1.5,
            "details": {...}  // 如果 return_details=true
        }
    """
    try:
        # 檢查文件
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '未提供音頻文件'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '文件名為空'
            }), 400
        
        # 讀取音頻數據
        audio_data = file.read()
        
        # 獲取選項
        options = {
            'language_hint': request.form.get('language_hint', 'zh'),
            'return_details': request.form.get('return_details', 'false').lower() == 'true',
            'enable_minnan_optimization': request.form.get('enable_minnan_optimization', 'true').lower() == 'true'
        }
        
        logger.info(f"收到測試識別請求: {file.filename}, 大小: {len(audio_data)} bytes")
        
        # 執行識別（異步轉同步）
        coordinator = get_asr_coordinator()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            coordinator.recognize(audio_data, options)
        )
        loop.close()
        
        logger.info(f"測試識別完成: {result.get('text', '')[:50]}...")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"測試識別失敗: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
