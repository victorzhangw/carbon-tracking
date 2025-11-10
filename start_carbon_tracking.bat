@echo off
echo ========================================
echo   碳排放追蹤系統 - 快速啟動
echo ========================================
echo.

echo 檢查依賴套件...
venv\Scripts\python -c "import whisper" 2>nul
if errorlevel 1 (
    echo 安裝缺少的套件...
    venv\Scripts\pip install openai-whisper -q
    echo.
)

echo 檢查資料庫...
if not exist carbon_tracking.db (
    echo 資料庫不存在，正在建立...
    venv\Scripts\python database_carbon_tracking.py
    echo.
    echo 生成模擬資料...
    venv\Scripts\python generate_mock_carbon_data.py
    echo.
)

echo 測試系統...
venv\Scripts\python test_carbon_system.py
echo.

echo 啟動Flask應用...
echo.
echo ========================================
echo   系統已啟動！
echo ========================================
echo.
echo 請開啟瀏覽器訪問：
echo   首頁：http://localhost:5000/carbon/
echo   儀表板：http://localhost:5000/carbon/dashboard
echo.
echo 按 Ctrl+C 停止伺服器
echo ========================================
echo.

venv\Scripts\python app.py

pause
