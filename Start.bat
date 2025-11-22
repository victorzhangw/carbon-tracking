@echo off
chcp 65001 >nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║          🎧 Qwen 雙語 AI 廣播劇系統 - 正確啟動            ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
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

echo [1/3] 停止現有的 Flask 進程...
echo.
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo    終止進程 PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)
echo    ✅ 完成
echo.

echo [2/3] 等待端口釋放...
timeout /t 2 /nobreak >nul
echo    ✅ 完成
echo.

echo [3/3] 啟動 Flask 應用（使用虛擬環境）...
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo    🌐 系統將在以下地址運行：
echo.
echo       • 雙語播放器：http://localhost:5000/api/audiobook/bilingual
echo       • 測試頁面：  http://localhost:5000/api/audiobook/qwen-test
echo       • 主頁：      http://localhost:5000/
echo.
echo    ⚠️  請確認看到 "✅ Qwen AI廣播劇" 載入成功的訊息
echo.
echo    🛑 按 Ctrl+C 停止服務器
echo.
echo ════════════════════════════════════════════════════════════
echo.

.\venv\Scripts\python.exe app.py

pause
