
call conda activate cbt_env

echo Installing PyInstaller...
pip install pyinstaller

echo Cleaning up previous builds...
rmdir /s /q build dist

echo Building executable...
pyinstaller --noconfirm --onedir --windowed --name "GeminiCBT" ^
    --exclude-module tkinter ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --hidden-import "PIL._tkinter_finder" ^
    --add-data "src;src" ^
    --icon "NONE" ^
    main.py

echo Build complete. Checks dist/GeminiCBT folder.
