@echo off
echo ========================================
echo     AI 客服語音系統一鍵安裝腳本
echo ========================================
echo.

REM 檢查 conda 是否安裝
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤: 未找到 conda，請先安裝 Anaconda 或 Miniconda
    echo 下載地址: https://www.anaconda.com/products/distribution
    pause
    exit /b 1
)

echo 1. 創建 Python 虛擬環境...
conda create -n GPTSoVits python=3.10 -y
if %errorlevel% neq 0 (
    echo 錯誤: 虛擬環境創建失敗
    pause
    exit /b 1
)

echo.
echo 2. 激活虛擬環境...
call conda activate GPTSoVits

echo.
echo 3. 克隆 GPT-SoVITS 項目...
if not exist "GPT-SoVITS" (
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git
    if %errorlevel% neq 0 (
        echo 錯誤: 項目克隆失敗，請檢查網絡連接
        pause
        exit /b 1
    )
) else (
    echo GPT-SoVITS 目錄已存在，跳過克隆
)

echo.
echo 4. 安裝 GPT-SoVITS 依賴...
cd GPT-SoVITS
pip install -r requirements.txt
pip install -r extra-req.txt --no-deps

echo.
echo 5. 安裝 FFmpeg...
conda install ffmpeg -y

echo.
echo 6. 安裝 API 服務依賴...
cd ..
pip install Flask flask-cors soundfile numpy

echo.
echo 7. 創建必要目錄...
if not exist "GPT-SoVITS\samples" mkdir "GPT-SoVITS\samples"
if not exist "voice-cache" mkdir "voice-cache"

echo.
echo ========================================
echo           安裝完成！
echo ========================================
echo.
echo 接下來需要手動下載預訓練模型:
echo 1. 訪問: https://huggingface.co/lj1995/GPT-SoVITS
echo 2. 下載模型文件到: GPT-SoVITS\GPT_SoVITS\pretrained_models\
echo.
echo 啟動服務:
echo - 運行 start-voice-api.bat 啟動 API 服務
echo - 運行 start-gpt-sovits.bat 啟動 WebUI (可選)
echo.
pause