from setuptools import setup
import os

APP = ['main.py']  # ton fichier principal
def list_files(folder):
    paths = []
    for root, _, files in os.walk(folder):
        for f in files:
            paths.append(os.path.join(root, f))
    return paths

DATA_FILES = [('resources', list_files('resources'))]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/icon.icns',  # icône du .app
    'packages': ['pygame'],
    'plist': {
        'CFBundleName': 'Angeciel',
        'CFBundleDisplayName': 'Angeciel',
        'CFBundleIdentifier': 'com.moi.Angeciel',
        'CFBundleVersion': '1.0',
        'CFBundleShortVersionString': '1.0.0',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['pygame']
)
