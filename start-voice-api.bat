@echo off
echo 啟動語音合成 API 服務...

REM 激活虛擬環境
call conda activate GPTSoVits

REM 檢查依賴
pip install Flask flask-cors soundfile numpy >nul 2>&1

REM 啟動簡化 API 服務
echo 正在啟動語音合成 API...
echo API 地址: http://localhost:5001
echo 狀態檢查: http://localhost:5001/api/voice/status
echo.
python simple_voice_api.py

pause