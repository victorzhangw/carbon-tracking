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

echo [1/5] 停止舊服務器（如果有）...
REM 停止 Flask (5000)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
REM 停止 GPT-SoVITS WebUI (9874)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9874 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
REM 停止 GPT-SoVITS TTS API (9880)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9880 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
REM 停止所有 GPT-SoVITS 相關進程
taskkill /F /IM python.exe /FI "COMMANDLINE eq *webui.py*" >nul 2>&1
timeout /t 2 /nobreak >nul
echo    ✅ 完成
echo.

echo [2/4] 清理 GPT-SoVITS Python 緩存...
if exist "GPT-SoVITS-v2pro-20250604\__pycache__" (
    rmdir /s /q "GPT-SoVITS-v2pro-20250604\__pycache__" 2>nul
)
if exist "GPT-SoVITS-v2pro-20250604\tools\__pycache__" (
    rmdir /s /q "GPT-SoVITS-v2pro-20250604\tools\__pycache__" 2>nul
)
echo    ✅ 緩存已清理
echo.

echo [3/5] 啟動 GPT-SoVITS WebUI（端口 9874，繁體中文）...
if exist "GPT-SoVITS-v2pro-20250604\go-webui.bat" (
    start "GPT-SoVITS WebUI (繁體中文)" cmd /k "cd GPT-SoVITS-v2pro-20250604 && go-webui.bat"
    timeout /t 5 /nobreak >nul
    echo    ✅ GPT-SoVITS WebUI 已啟動（繁體中文，無 MIT 聲明）
) else (
    echo    ⚠️  未找到 GPT-SoVITS WebUI
)
echo.

echo [4/5] 啟動 GPT-SoVITS TTS API（端口 9880）...
if exist "GPT-SoVITS-v2pro-20250604\api_v2.py" (
    if exist "GPT-SoVITS-v2pro-20250604\runtime\python.exe" (
        start "GPT-SoVITS TTS API" cmd /k "cd GPT-SoVITS-v2pro-20250604 && runtime\python.exe -s api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS\configs\tts_infer.yaml"
        timeout /t 3 /nobreak >nul
        echo    ✅ GPT-SoVITS TTS API 已啟動
    ) else (
        echo    ⚠️  未找到 GPT-SoVITS runtime 環境
    )
) else (
    echo    ⚠️  未找到 GPT-SoVITS TTS API
)
echo.

echo [5/5] 啟動 Flask 服務器（使用虛擬環境）...
start "Flask Server" cmd /k ".\venv\Scripts\python.exe app.py"
timeout /t 5 /nobreak >nul
echo    ✅ 完成
echo.

echo [完成] 打開系統入口頁面...
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
echo   🎤 GPT-SoVITS 服務：
echo      • WebUI (訓練): http://localhost:9874 (繁體中文)
echo      • TTS API: http://localhost:9880
echo.
echo   💡 使用說明：
echo      在入口頁面選擇您要使用的系統模組
echo.
echo   ⚠️  服務器在另外的窗口運行：
echo      • Flask Server (端口 5000)
echo      • GPT-SoVITS WebUI (端口 9874)
echo      • GPT-SoVITS TTS API (端口 9880)
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
