@echo off
echo ========================================
echo   測試 Gradle 配置
echo ========================================
echo.

echo [1/3] 檢查 Gradle Wrapper...
if exist gradlew.bat (
    echo ✅ gradlew.bat 存在
) else (
    echo ❌ gradlew.bat 不存在
    pause
    exit /b 1
)

echo.
echo [2/3] 清理專案...
call gradlew clean
if errorlevel 1 (
    echo ❌ 清理失敗
    pause
    exit /b 1
)
echo ✅ 清理成功

echo.
echo [3/3] 測試建置...
call gradlew assembleDebug --stacktrace
if errorlevel 1 (
    echo.
    echo ❌ 建置失敗
    echo 請查看上方錯誤訊息
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 建置成功！
echo ========================================
echo.
echo APK 位置：
echo app\build\outputs\apk\debug\app-debug.apk
echo.
pause
