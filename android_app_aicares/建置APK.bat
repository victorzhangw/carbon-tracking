@echo off
echo ========================================
echo   AI客服系統 Android APP - 建置工具
echo ========================================
echo.

echo 正在檢查環境...
where gradlew >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 gradlew
    echo 請確認您在 android_app_aicares 目錄中
    pause
    exit /b 1
)

echo.
echo 選擇建置類型：
echo 1. Debug 版本（開發測試用）
echo 2. Release 版本（正式發布用）
echo.
set /p choice="請輸入選項 (1 或 2): "

if "%choice%"=="1" (
    echo.
    echo 正在建置 Debug 版本...
    call gradlew assembleDebug
    
    if errorlevel 0 (
        echo.
        echo ========================================
        echo   建置成功！
        echo ========================================
        echo.
        echo APK 位置：
        echo app\build\outputs\apk\debug\app-debug.apk
        echo.
        echo 您可以直接安裝此 APK 到手機上測試
        echo.
    ) else (
        echo.
        echo [錯誤] 建置失敗
        echo 請檢查錯誤訊息
    )
) else if "%choice%"=="2" (
    echo.
    echo 正在建置 Release 版本...
    call gradlew assembleRelease
    
    if errorlevel 0 (
        echo.
        echo ========================================
        echo   建置成功！
        echo ========================================
        echo.
        echo APK 位置：
        echo app\build\outputs\apk\release\app-release-unsigned.apk
        echo.
        echo 注意：Release 版本需要簽名才能安裝
        echo 請使用 Android Studio 的 Generate Signed APK 功能
        echo.
    ) else (
        echo.
        echo [錯誤] 建置失敗
        echo 請檢查錯誤訊息
    )
) else (
    echo.
    echo [錯誤] 無效的選項
)

echo.
pause
