from setuptools import setup, find_packages

setup(
    name="egg-voice-terminal",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'openai',
        'SpeechRecognition',
        'pyttsx3',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'egg-voice=claude_voice:main',
        ],
    },
    python_requires='>=3.8',
)
