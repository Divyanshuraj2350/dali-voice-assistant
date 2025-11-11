"""
Setup script to create DALI macOS application
"""
from setuptools import setup

APP = ['dali_gui.py']
DATA_FILES = ['src']
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'dali_icon.icns',
    'plist': {
        'CFBundleName': 'DALI',
        'CFBundleDisplayName': 'DALI Voice Assistant',
        'CFBundleGetInfoString': "Dynamic AI Listening Interface",
        'CFBundleIdentifier': "com.dali.voiceassistant",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSMicrophoneUsageDescription': 'DALI needs microphone access for voice commands.',
        'NSAppleEventsUsageDescription': 'DALI needs to control applications.',
    },
    'packages': ['speech_recognition', 'pyttsx3', 'wikipedia', 'certifi'],
    'includes': ['tkinter', 'pyaudio'],
}

setup(
    name='DALI',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

