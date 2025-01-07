import os
import subprocess
import sys
import PyInstaller.__main__

def verify_windows_environment():
    """Verify we're running on Windows with required tools"""
    if sys.platform != 'win32':
        print("Error: Windows Store packages can only be built on Windows")
        print("Please run this script on a Windows machine with:")
        print("1. Windows 10 SDK installed")
        print("2. MakeAppx.exe available in PATH")
        print("3. SignTool.exe available in PATH")
        print("4. Windows App Certification Kit installed")
        sys.exit(1)

def build_executable():
    verify_windows_environment()
    # Create Windows executable with Windows-specific configurations
    PyInstaller.__main__.run([
        'egg_voice_gui.py',
        '--onefile',
        '--windowed',
        '--icon=assets/icon.ico',
        '--name=EggVoiceTerminal',
        '--add-data=assets:assets',
        '--target-architecture', '64bit',
        '--exclude-module', 'tkinter',
        '--exclude-module', 'PyQt5',
        '--hidden-import', 'pyaudio',
        '--hidden-import', 'speech_recognition.pocketsphinx',
        '--noconfirm',  # Don't ask for confirmation
        '--clean',  # Clean build directory
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
    """Create Windows AppX package for Store submission"""
    # Validate assets exist
    required_assets = ['StoreLogo.png', 'SplashScreen.png']
    for asset in required_assets:
        if not os.path.exists(f"assets/{asset}"):
            raise FileNotFoundError(f"Required asset missing: {asset}")
    
    # Create package
    subprocess.run([
        "makeappx",
        "pack",
        "/d", "dist/EggVoiceTerminal",
        "/p", "EggVoiceTerminal.appx",
        "/l"  # Enable logging
    ])
    
    # Sign the package
    subprocess.run([
        "signtool",
        "sign",
        "/fd", "SHA256",
        "/a",
        "/tr", "http://timestamp.digicert.com",
        "/td", "SHA256",
        "EggVoiceTerminal.appx"
    ])
    
    # Run Windows App Certification Kit
    subprocess.run([
        "wacktest",
        "EggVoiceTerminal.appx",
        "/reportoutputpath", "wack_report.xml"
    ])
    
    print("AppX package created and signed. WACK report saved to wack_report.xml")

if __name__ == "__main__":
    build_executable()
    create_installer()
    create_appx_package()
