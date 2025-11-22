@echo off
chcp 65001 >nul
echo ============================================
echo 清理 GPT-SoVITS 緩存並重啟
echo ============================================
echo.

echo [1/4] 停止現有的 GPT-SoVITS 進程...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq GPT-SoVITS*" 2>nul
timeout /t 2 /nobreak >nul

echo [2/4] 清理 Python 緩存文件...
cd GPT-SoVITS-v2pro-20250604
del /s /q __pycache__ 2>nul
del /s /q *.pyc 2>nul
del /s /q tools\__pycache__ 2>nul
del /s /q tools\*.pyc 2>nul
echo 緩存清理完成

echo [3/4] 驗證 webui.py 修改...
findstr /C:"# MIT 協議聲明已隱藏" webui.py >nul
if %errorlevel%==0 (
    echo ✓ webui.py 修改確認
) else (
    echo ✗ webui.py 修改未找到，請檢查文件
    pause
    exit /b 1
)

echo [4/4] 啟動 GPT-SoVITS...
echo.
echo 正在啟動，請等待...
echo 如果看到 MIT 聲明，請按 Ctrl+C 停止並報告問題
echo.
start "GPT-SoVITS WebUI" go-webui.bat

echo.
echo ============================================
echo 啟動完成！
echo 請訪問: http://localhost:9874
echo ============================================
pause
