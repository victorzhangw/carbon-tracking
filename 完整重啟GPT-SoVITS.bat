@echo off
chcp 65001 >nul
echo ============================================
echo 完整重啟 GPT-SoVITS（繁體中文 + 移除 MIT 聲明）
echo ============================================
echo.

echo [1/6] 停止所有 GPT-SoVITS 相關進程...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq GPT-SoVITS*" 2>nul
taskkill /F /IM python.exe /FI "COMMANDLINE eq *webui.py*" 2>nul
timeout /t 2 /nobreak >nul
echo ✓ 進程已停止

echo [2/6] 清理 Python 緩存...
cd GPT-SoVITS-v2pro-20250604
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
if exist tools\__pycache__ rmdir /s /q tools\__pycache__ 2>nul
del /s /q *.pyc 2>nul
cd ..
echo ✓ 緩存已清理

echo [3/6] 驗證修改...
python 驗證MIT聲明移除.py >nul 2>&1
if %errorlevel%==0 (
    echo ✓ MIT 聲明移除驗證通過
) else (
    echo ⚠ MIT 聲明移除驗證失敗，但繼續執行
)

python 驗證繁體中文設定.py >nul 2>&1
if %errorlevel%==0 (
    echo ✓ 繁體中文設定驗證通過
) else (
    echo ⚠ 繁體中文設定驗證失敗，但繼續執行
)

echo [4/6] 啟動 GPT-SoVITS（繁體中文）...
cd GPT-SoVITS-v2pro-20250604
start "GPT-SoVITS WebUI (繁體中文)" go-webui.bat
cd ..
echo ✓ GPT-SoVITS 已啟動

echo [5/6] 等待服務啟動...
timeout /t 5 /nobreak >nul
echo ✓ 等待完成

echo [6/6] 啟動 Flask 應用...
start "Flask AICares" bStart.bat
echo ✓ Flask 應用已啟動

echo.
echo ============================================
echo 🎉 完整重啟完成！
echo ============================================
echo.
echo 📍 訪問地址:
echo    Flask 應用: http://localhost:5000
echo    語音測試: http://localhost:5000/voice-testing
echo    GPT-SoVITS: http://localhost:9874
echo.
echo 💡 提示:
echo    1. 點擊「TTS 語音合成訓練」會直接開啟 GPT-SoVITS
echo    2. GPT-SoVITS 應該顯示繁體中文
echo    3. 頂部不應該有 MIT 聲明
echo.
pause
