@echo off
echo 啟動 GPT-SoVITS 服務...

REM 激活虛擬環境
call conda activate GPTSoVits

REM 進入項目目錄
cd ..\..\GPT-SoVITS

REM 啟動 WebUI
echo 正在啟動 GPT-SoVITS WebUI...
echo 訪問地址: http://localhost:9874
echo.
python webui.py

pause