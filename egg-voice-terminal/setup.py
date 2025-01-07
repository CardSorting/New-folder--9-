from setuptools import setup, find_packages

setup(
    name="egg-voice-terminal",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'openai',
        'SpeechRecognition',
        'pyttsx3',
        'python-dotenv',
        'PyQt5',
        'pyinstaller',
        'pywin32'
    ],
    entry_points={
        'gui_scripts': [
            'egg-voice=egg_voice_gui:main',
        ],
    },
    options={
        'build_exe': {
            'include_files': [
                ('egg-voice-terminal/assets/', 'assets/')
            ],
            'packages': ['PyQt5', 'speech_recognition', 'pyttsx3'],
            'excludes': ['tkinter']
        }
    },
    python_requires='>=3.8',
)
