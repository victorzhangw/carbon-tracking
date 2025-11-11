@echo off
echo 啟動語音克隆服務...

REM 檢查 Python 環境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤: 未找到 Python，請先安裝 Python
    pause
    exit /b 1
)

REM 檢查 GPT-SoVITS 目錄
if not exist "..\..\GPT-SoVITS-v4-20250422fix" (
    echo 錯誤: 未找到 GPT-SoVITS-v4-20250422fix 目錄
    echo 請確保 GPT-SoVITS 已正確安裝
    pause
    exit /b 1
)

REM 安裝必要的依賴
echo 正在安裝依賴...
pip install flask flask-cors librosa soundfile numpy requests

REM 創建必要目錄
if not exist "..\..\audio_uploads" mkdir "..\..\audio_uploads"
if not exist "..\..\voice_output" mkdir "..\..\voice_output"

REM 啟動語音克隆服務
echo.
echo 正在啟動語音克隆服務...
echo API 地址: http://localhost:5002
echo 狀態檢查: http://localhost:5002/api/voice/status
echo.
echo 注意: 首次啟動可能需要較長時間來初始化 GPT-SoVITS
echo.

python ..\..\voice_clone_service.py

pause