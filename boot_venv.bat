@echo off
chcp 65001 >nul
echo ============================================================
echo   啟動 AI 廣播劇系統（使用虛擬環境）
echo ============================================================
echo.

echo [1/2] 啟動虛擬環境...
call venv\Scripts\activate
echo ✅ 虛擬環境已啟動
echo.

echo [2/2] 啟動 Flask 應用...
echo.
echo 系統將在以下地址運行:
echo   • 測試頁面: http://localhost:5000/api/audiobook/test
echo   • 雙語版本: http://localhost:5000/api/audiobook/bilingual
echo   • 基礎版本: http://localhost:5000/api/audiobook/
echo.
echo 按 Ctrl+C 停止服務器
echo.
echo ============================================================
echo.

python app.py
