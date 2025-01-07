import os
import subprocess
import PyInstaller.__main__

def build_executable():
    # Create Windows executable with Windows-specific configurations
    PyInstaller.__main__.run([
        'egg_voice_gui.py',
        '--onefile',
        '--windowed',
        '--icon=assets/icon.ico',
        '--name=EggVoiceTerminal',
        '--add-data=assets:assets',
        '--target-architecture', '64bit',
        '--win-private-assemblies',
        '--win-no-prefer-redirects',
        '--exclude-module', 'tkinter',
        '--exclude-module', 'PyQt5',
        '--hidden-import', 'pyaudio',
        '--hidden-import', 'speech_recognition.pocketsphinx',
        '--noconfirm',  # Don't ask for confirmation
        '--clean',  # Clean build directory
        '--win-ui-access',  # Enable UI Automation
        '--disable-windowed-traceback'  # Disable traceback in windowed mode
    ])

def create_installer():
    # Create NSIS installer script
    nsis_script = """
    OutFile "EggVoiceTerminal_Installer.exe"
    InstallDir "$PROGRAMFILES\\EggVoiceTerminal"
    
    Section
        SetOutPath $INSTDIR
        File /r dist\\EggVoiceTerminal\\*.*
        CreateShortcut "$SMPROGRAMS\\EggVoiceTerminal.lnk" "$INSTDIR\\EggVoiceTerminal.exe"
        WriteUninstaller "$INSTDIR\\uninstall.exe"
    SectionEnd
    
    Section "Uninstall"
        Delete "$SMPROGRAMS\\EggVoiceTerminal.lnk"
        RMDir /r "$INSTDIR"
    SectionEnd
    """
    
    with open("installer.nsi", "w") as f:
        f.write(nsis_script)
        
    # Run NSIS compiler
    subprocess.run(["makensis", "installer.nsi"])

def create_appx_package():
    # Create Windows AppX package
    subprocess.run([
        "makeappx",
        "pack",
        "/d", "dist/EggVoiceTerminal",
        "/p", "EggVoiceTerminal.appx"
    ])

if __name__ == "__main__":
    build_executable()
    create_installer()
    create_appx_package()
