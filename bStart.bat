@echo off
chcp 65001 >nul
cls
echo.
echo ════════════════════════════════════════════════════════════
echo   🎧 AI 語音互動平台 - 完整啟動
echo ════════════════════════════════════════════════════════════
echo.

REM 檢查虛擬環境
if not exist "venv\Scripts\python.exe" (
    echo ❌ 錯誤：找不到虛擬環境
    echo.
    echo 請先執行以下命令創建虛擬環境：
    echo   python -m venv venv
    echo   .\venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [1/4] 停止舊服務器（如果有）...
REM 停止 Flask (5000)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
REM 停止 GPT-SoVITS (9880)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9880 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 2 /nobreak >nul
echo    ✅ 完成
echo.

echo [2/4] 啟動 GPT-SoVITS TTS 服務（端口 9880）...
REM 檢查 GPT-SoVITS 是否存在
if exist "..\GPT-SoVITS\api_v2.py" (
    start "GPT-SoVITS TTS" cmd /k "cd ..\GPT-SoVITS && conda activate GPTSoVits && python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS\configs\tts_infer.yaml"
    timeout /t 3 /nobreak >nul
    echo    ✅ GPT-SoVITS TTS 服務已啟動
) else (
    echo    ⚠️  未找到 GPT-SoVITS，將以純文字模式運行
    echo    💡 如需語音功能，請安裝 GPT-SoVITS 到上層目錄
)
echo.

echo [3/4] 啟動 Flask 服務器（使用虛擬環境）...
start "Flask Server" cmd /k ".\venv\Scripts\python.exe app.py"
timeout /t 5 /nobreak >nul
echo    ✅ 完成
echo.

echo [4/4] 打開系統入口頁面...
echo.
echo ════════════════════════════════════════════════════════════
echo   🌐 系統已啟動！
echo ════════════════════════════════════════════════════════════
echo.
echo   🚀 系統入口：
echo      http://localhost:5000/portal
echo.
echo   📱 可用模組：
echo      • AI 語音互動平台（含情緒識別系統）
echo      • 碳排放追蹤系統
echo      • 智慧語音關懷系統
echo      • AI 廣播劇系統
echo.
echo   🎤 TTS 服務狀態：
echo      • GPT-SoVITS: http://localhost:9880
echo      • 如未啟動，系統將以純文字模式運行
echo.
echo   💡 使用說明：
echo      在入口頁面選擇您要使用的系統模組
echo.
echo   ⚠️  服務器在另外的窗口運行：
echo      • Flask Server (端口 5000)
echo      • GPT-SoVITS TTS (端口 9880)
echo.
echo   🛑 關閉對應窗口即可停止服務器
echo.
echo ════════════════════════════════════════════════════════════
echo.

timeout /t 2 /nobreak >nul
start http://localhost:5000/portal

echo.
echo 按任意鍵關閉此窗口（Flask 服務器會繼續運行）...
pause >nul
