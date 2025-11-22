@echo off
chcp 65001 >nul
echo.
echo ════════════════════════════════════════════════════════════
echo   🧪 測試 GPT-SoVITS 環境
echo ════════════════════════════════════════════════════════════
echo.

cd GPT-SoVITS-v2pro-20250604

echo [1/3] 清除環境變量...
set PYTHONPATH=
set PYTHONHOME=
echo    ✅ 完成
echo.

echo [2/3] 測試 Python 版本...
runtime\python.exe --version
echo.

echo [3/3] 測試 torch 導入...
runtime\python.exe -c "import sys; print('Python 路徑:'); [print(f'  - {p}') for p in sys.path[:5]]"
echo.

echo [4/3] 測試 torch 版本...
runtime\python.exe -c "import torch; print(f'✅ PyTorch: {torch.__version__}'); print(f'   位置: {torch.__file__}')"
echo.

echo [5/3] 測試 torchaudio 導入...
runtime\python.exe -c "import torchaudio; print(f'✅ torchaudio: {torchaudio.__version__}'); print(f'   位置: {torchaudio.__file__}')"
echo.

if %ERRORLEVEL% EQU 0 (
    echo ════════════════════════════════════════════════════════════
    echo   ✅ 所有測試通過！
    echo ════════════════════════════════════════════════════════════
) else (
    echo ════════════════════════════════════════════════════════════
    echo   ❌ 測試失敗
    echo ════════════════════════════════════════════════════════════
)

echo.
pause
