from flask import Blueprint, render_template
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """主頁面 - 重定向到 Portal"""
    from flask import redirect, url_for
    return redirect('/portal')

@main.route('/voice-clone')
def voice_clone():
    """語音克隆示範頁面"""
    return render_template('voice_clone_demo.html')

@main.route('/voice-chat')
def voice_chat():
    """語音聊天示範頁面"""
    return render_template('voice_interaction_enhanced.html')

@main.route('/realtime-voice')
def realtime_voice():
    """即時語音互動示範頁面"""
    return render_template('voice_interaction_realtime.html')

@main.route('/audiobook-player')
def audiobook_player():
    """AI廣播劇播放器頁面"""
    return render_template('audiobook_player.html')

@main.route('/bilingual-audiobook-player')
def bilingual_audiobook_player():
    """雙語AI廣播劇播放器頁面"""
    return render_template('bilingual_audiobook_player.html')

@main.route('/voice-care')
def voice_care():
    """智慧語音關懷頁面"""
    return render_template('voice_care_dashboard.html')

@main.route('/voice-testing')
def voice_testing():
    """語音測試訓練模組入口頁面"""
    return render_template('voice_testing_hub.html')

@main.route('/health')
def health_check():
    """健康檢查端點"""
    return {'status': 'healthy', 'service': 'AICares'}, 200