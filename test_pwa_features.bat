@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   🧪 PWA 功能測試
echo ========================================
echo.
echo 正在啟動碳排放追蹤系統...
echo.

REM 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤：找不到 Python
    echo 請先安裝 Python 3.8+
    pause
    exit /b 1
)

REM 啟動 Flask 應用程式
echo ✅ 啟動 Flask 伺服器...
echo.
start /B python app.py

REM 等待伺服器啟動
timeout /t 3 /nobreak >nul

REM 開啟測試頁面
echo ✅ 開啟 PWA 測試頁面...
echo.
start http://localhost:5000/carbon/test-pwa

echo.
echo ========================================
echo   測試項目：
echo ========================================
echo.
echo   1. Service Worker 註冊狀態
echo   2. Manifest 載入檢查
echo   3. 快取功能測試
echo   4. 安裝功能測試
echo   5. 離線功能測試
echo.
echo ========================================
echo   測試完成後，按任意鍵關閉伺服器
echo ========================================
echo.
pause

REM 關閉 Python 程序
taskkill /F /IM python.exe >nul 2>&1

echo.
echo ✅ 測試完成！
echo.
pause
