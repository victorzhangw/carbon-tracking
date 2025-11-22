@echo off
chcp 65001 >nul
cls
echo.
echo ════════════════════════════════════════════════════════════
echo   🔍 TTS 系統診斷
echo ════════════════════════════════════════════════════════════
echo.

echo [1/5] 檢查服務狀態...
echo.
echo Flask (端口 5000):
netstat -ano | findstr ":5000" | findstr "LISTENING"
if %ERRORLEVEL% EQU 0 (
    echo    ✅ Flask 正在運行
) else (
    echo    ❌ Flask 未運行
)
echo.

echo GPT-SoVITS (端口 9880):
netstat -ano | findstr ":9880" | findstr "LISTENING"
if %ERRORLEVEL% EQU 0 (
    echo    ✅ GPT-SoVITS 正在運行
) else (
    echo    ❌ GPT-SoVITS 未運行
)
echo.

echo [2/5] 檢查目錄結構...
if exist "genvoice" (
    echo    ✅ genvoice 目錄存在
) else (
    echo    ❌ genvoice 目錄不存在
    mkdir genvoice
    echo    ✅ 已創建 genvoice 目錄
)
echo.

echo [3/5] 檢查參考音頻...
if exist "GPT-SoVITS-v2pro-20250604\TTS\vc.wav" (
    echo    ✅ 參考音頻存在
) else (
    echo    ❌ 參考音頻不存在
)
echo.

echo [4/5] 檢查最近生成的音頻...
dir /b /o-d genvoice\*.wav 2>nul | findstr "tts_"
if %ERRORLEVEL% EQU 0 (
    echo    ✅ 有音頻文件
) else (
    echo    ⚠️  沒有音頻文件
)
echo.

echo [5/5] 測試 TTS 生成...
echo    正在測試...
.\venv\Scripts\python.exe test_tts_direct.py
echo.

echo ════════════════════════════════════════════════════════════
echo   診斷完成
echo ════════════════════════════════════════════════════════════
echo.
echo 💡 如果所有檢查都通過但仍無聲音，請：
echo    1. 重啟 Flask 服務器（關閉窗口後執行 bStart.bat）
echo    2. 檢查瀏覽器開發者工具（F12）的 Console 和 Network
echo    3. 確認瀏覽器沒有靜音
echo.
pause
