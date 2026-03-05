"""
Creates:
1. An .ico file from icon.png
2. A desktop shortcut (.lnk) for CBT Solver
"""
import os
import sys
from pathlib import Path

def create_ico():
    """Convert icon.png to icon.ico"""
    try:
        from PIL import Image
        icon_png = Path(__file__).parent / "icon.png"
        icon_ico = Path(__file__).parent / "icon.ico"
        
        if not icon_png.exists():
            print(f"icon.png not found at {icon_png}")
            return None
        
        img = Image.open(icon_png)
        # Create multi-size ICO file
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        icons = []
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            icons.append(resized)
        
        icons[0].save(str(icon_ico), format='ICO', sizes=[(s, s) for _, s in enumerate([256, 128, 64, 48, 32, 16])], append_images=icons[1:])
        print(f"[OK] icon.ico created: {icon_ico}")
        return str(icon_ico)
    except Exception as e:
        print(f"[ERROR] Failed to create ico: {e}")
        return None


def create_desktop_shortcut():
    """Create a .lnk shortcut on the Desktop."""
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        # Fallback: use PowerShell to create shortcut
        return create_shortcut_powershell()
    
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "CBT Solver.lnk")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    
    project_dir = str(Path(__file__).parent)
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    
    shortcut.Targetpath = pythonw
    shortcut.Arguments = f'"{os.path.join(project_dir, "main.py")}"'
    shortcut.WorkingDirectory = project_dir
    
    icon_path = os.path.join(project_dir, "icon.ico")
    if os.path.exists(icon_path):
        shortcut.IconLocation = icon_path
    
    shortcut.Description = "CBT Solver - Gemini AI 문제 풀이"
    shortcut.save()
    print(f"[OK] Desktop shortcut created: {shortcut_path}")


def create_shortcut_powershell():
    """Fallback: Create shortcut using PowerShell."""
    import subprocess
    
    project_dir = str(Path(__file__).parent).replace("\\", "\\\\")
    desktop = str(Path.home() / "Desktop").replace("\\", "\\\\")
    shortcut_path = f"{desktop}\\\\CBT Solver.lnk"
    
    # Find pythonw.exe
    pythonw = sys.executable.replace("python.exe", "pythonw.exe").replace("\\", "\\\\")
    main_py = f"{project_dir}\\\\main.py"
    icon_ico = f"{project_dir}\\\\icon.ico"
    
    ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$Shortcut.TargetPath = '{pythonw}'
$Shortcut.Arguments = '"{main_py}"'
$Shortcut.WorkingDirectory = '{project_dir}'
$Shortcut.Description = 'CBT Solver - Gemini AI 문제 풀이'
if (Test-Path '{icon_ico}') {{
    $Shortcut.IconLocation = '{icon_ico}'
}}
$Shortcut.Save()
"""
    
    result = subprocess.run(
        ["powershell", "-Command", ps_script],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        # Unescape for display
        display_path = shortcut_path.replace("\\\\", "\\")
        print(f"[OK] Desktop shortcut created: {display_path}")
    else:
        print(f"[ERROR] Failed to create shortcut: {result.stderr}")


if __name__ == "__main__":
    print("=" * 50)
    print("  CBT Solver - Icon & Shortcut Creator")
    print("=" * 50)
    print()
    
    # Step 1: Create ICO file
    print("[1/2] Creating icon.ico ...")
    create_ico()
    
    # Step 2: Create desktop shortcut
    print("[2/2] Creating desktop shortcut ...")
    create_shortcut_powershell()
    
    print()
    print("완료!")
