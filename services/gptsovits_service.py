#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GPT-SoVITS 服務管理
負責啟動和管理 GPT-SoVITS WebUI 進程
"""

import os
import subprocess
import time
import requests
import psutil

class GPTSoVITSService:
    def __init__(self):
        self.process = None
        self.gptsovits_dir = os.path.join(os.getcwd(), "GPT-SoVITS-v2pro-20250604")
        self.webui_url = "http://localhost:9874"
        self.startup_script = os.path.join(self.gptsovits_dir, "go-webui.bat")
        
    def is_running(self):
        """檢查 GPT-SoVITS 是否正在運行"""
        try:
            response = requests.get(self.webui_url, timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def start(self):
        """啟動 GPT-SoVITS WebUI"""
        if self.is_running():
            print("✅ GPT-SoVITS 已經在運行")
            return True
        
        if not os.path.exists(self.startup_script):
            print(f"❌ 找不到啟動腳本: {self.startup_script}")
            return False
        
        try:
            print(f"🚀 啟動 GPT-SoVITS WebUI...")
            # 使用 Popen 在後台啟動進程
            self.process = subprocess.Popen(
                [self.startup_script],
                cwd=self.gptsovits_dir,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            
            # 等待服務啟動（最多等待 30 秒）
            print("⏳ 等待 GPT-SoVITS 啟動...")
            for i in range(30):
                time.sleep(1)
                if self.is_running():
                    print(f"✅ GPT-SoVITS 啟動成功！({i+1} 秒)")
                    return True
                print(f"   等待中... {i+1}/30 秒")
            
            print("⚠️ GPT-SoVITS 啟動超時")
            return False
            
        except Exception as e:
            print(f"❌ 啟動 GPT-SoVITS 失敗: {e}")
            return False
    
    def stop(self):
        """停止 GPT-SoVITS WebUI"""
        try:
            # 嘗試終止進程
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("✅ GPT-SoVITS 進程已停止")
            
            # 查找並終止所有相關進程
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline')
                    if cmdline and any('go-webui' in str(cmd) or 'webui.py' in str(cmd) for cmd in cmdline):
                        proc.terminate()
                        print(f"✅ 終止進程: {proc.info['name']} (PID: {proc.info['pid']})")
                except:
                    pass
            
            return True
        except Exception as e:
            print(f"❌ 停止 GPT-SoVITS 失敗: {e}")
            return False
    
    def get_status(self):
        """獲取服務狀態"""
        return {
            'running': self.is_running(),
            'url': self.webui_url,
            'process_alive': self.process is not None and self.process.poll() is None
        }

# 創建全局實例
gptsovits_service = GPTSoVITSService()
