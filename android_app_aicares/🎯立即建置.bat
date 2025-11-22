@echo off
chcp 65001 >nul
echo ========================================
echo   AI客服系統 - 立即建置 APK
echo ========================================
echo.

echo [檢查] 驗證專案結構...
if not exist "app\src\main\AndroidManifest.xml" (
    echo ❌ 找不到 AndroidManifest.xml
    pause
    exit /b 1
)
echo ✅ AndroidManifest.xml 存在

if not exist "app\src\main\res\drawable\ic_launcher_foreground.xml" (
    echo ❌ 找不到圖示檔案
    pause
    exit /b 1
)
echo ✅ 圖示檔案存在

if not exist "app\src\main\java\com\aicares\app\MainActivity.kt" (
    echo ❌ 找不到 MainActivity.kt
    pause
    exit /b 1
)
echo ✅ MainActivity.kt 存在

echo.
echo [清理] 清理舊的建置檔案...
call gradlew clean >nul 2>&1
echo ✅ 清理完成

echo.
echo [建置] 開始建置 Debug APK...
echo 這可能需要幾分鐘，請稍候...
echo.

call gradlew assembleDebug

if errorlevel 1 (
    echo.
    echo ========================================
    echo   ❌ 建置失敗
    echo ========================================
    echo.
    echo 請檢查上方的錯誤訊息
    echo.
    echo 常見問題：
    echo 1. 網路連線問題 - Gradle 需要下載依賴
    echo 2. Java 版本問題 - 需要 JDK 8 或更高
    echo 3. 記憶體不足 - 關閉其他程式
    echo.
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

if exist "app\build\outputs\apk\debug\app-debug.apk" (
    for %%A in ("app\build\outputs\apk\debug\app-debug.apk") do (
        echo 檔案大小：%%~zA bytes
    )
    echo.
    echo 下一步：
    echo 1. 將 APK 傳到手機
    echo 2. 在手機上點擊安裝
    echo 3. 允許「安裝未知來源」
    echo 4. 完成安裝
    echo.
    echo 或者使用 USB 連接手機，在 Android Studio 中點擊 Run
) else (
    echo ⚠️ 找不到 APK 檔案
)

echo.
pause
