
@echo off
set "ENV_ROOT=C:\Users\user\anaconda3\envs\cbt_env"
set "ENV_PYTHON=%ENV_ROOT%\python.exe"
set "ENV_PIP=%ENV_ROOT%\Scripts\pip.exe"
set "ENV_PYINSTALLER=%ENV_ROOT%\Scripts\pyinstaller.exe"

REM Libraries to bundle explicitly to fix SSL/DLL errors
set "LIB_BIN=%ENV_ROOT%\Library\bin"
set "SSL_DLL=%LIB_BIN%\libssl-3-x64.dll"
set "CRYPTO_DLL=%LIB_BIN%\libcrypto-3-x64.dll"

echo [1/3] Ensuring PyInstaller is ready...
"%ENV_PIP%" install pyinstaller
if %errorlevel% neq 0 ( exit /b %errorlevel% )

echo [2/3] Cleaning up previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist GeminiCBT_solver.spec del GeminiCBT_solver.spec

echo [3/3] Building executable...
"%ENV_PYINSTALLER%" --noconfirm --onedir --windowed --name "GeminiCBT_solver" ^
    --icon "icon.ico" ^
    --add-binary "%SSL_DLL%;." ^
    --add-binary "%CRYPTO_DLL%;." ^
    --hidden-import "PyQt6" ^
    --hidden-import "google.genai" ^
    --exclude-module "tkinter" ^
    --exclude-module "matplotlib" ^
    --exclude-module "numpy" ^
    --exclude-module "pandas" ^
    --exclude-module "scipy" ^
    --add-data "src;src" ^
    --add-data "icon.ico;." ^
    --clean ^
    main.py

if %errorlevel% neq 0 (
    echo Build failed.
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================================
echo  Build Success!
echo  The executable is in: dist\GeminiCBT_solver\GeminiCBT_solver.exe
echo ========================================================
