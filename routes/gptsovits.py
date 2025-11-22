#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GPT-SoVITS 路由
處理 GPT-SoVITS WebUI 的啟動和頁面顯示
"""

from flask import Blueprint, render_template, jsonify, redirect
from services.gptsovits_service import gptsovits_service
import threading

gptsovits_bp = Blueprint('gptsovits', __name__)

@gptsovits_bp.route('/tts-training')
def tts_training():
    """TTS 語音合成訓練頁面 - 直接重定向到 GPT-SoVITS WebUI"""
    # 在後台線程啟動 GPT-SoVITS（避免阻塞頁面載入）
    def start_in_background():
        if not gptsovits_service.is_running():
            gptsovits_service.start()
    
    thread = threading.Thread(target=start_in_background, daemon=True)
    thread.start()
    
    # 直接重定向到 GPT-SoVITS WebUI
    return redirect('http://localhost:9874')

@gptsovits_bp.route('/api/gptsovits/status')
def get_status():
    """獲取 GPT-SoVITS 服務狀態"""
    status = gptsovits_service.get_status()
    return jsonify(status)

@gptsovits_bp.route('/api/gptsovits/start', methods=['POST'])
def start_service():
    """手動啟動 GPT-SoVITS 服務"""
    try:
        success = gptsovits_service.start()
        return jsonify({
            'success': success,
            'message': '啟動成功' if success else '啟動失敗'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@gptsovits_bp.route('/api/gptsovits/stop', methods=['POST'])
def stop_service():
    """停止 GPT-SoVITS 服務"""
    try:
        success = gptsovits_service.stop()
        return jsonify({
            'success': success,
            'message': '停止成功' if success else '停止失敗'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
