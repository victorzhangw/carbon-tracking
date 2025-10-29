@echo off
echo 正在安裝 GPT-SoVITS...

REM 創建虛擬環境
conda create -n GPTSoVits python=3.10 -y
call conda activate GPTSoVits

REM 克隆項目
git clone https://github.com/RVC-Boss/GPT-SoVITS.git
cd GPT-SoVITS

REM 安裝依賴
pip install -r requirements.txt
pip install -r extra-req.txt --no-deps

REM 安裝 FFmpeg (如果沒有的話)
conda install ffmpeg -y

echo.
echo GPT-SoVITS 安裝完成！
echo 請手動下載預訓練模型到 GPT_SoVITS/pretrained_models/ 目錄
echo.
pause