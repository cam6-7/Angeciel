import sys
import os
print("FONCTION RESOURCE PATH :", __file__)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Cas PyInstaller
        base_path = sys._MEIPASS

    elif getattr(sys, 'frozen', False):
        # Cas py2app
        base_path = os.path.join(
            os.path.dirname(sys.executable),
            '..',
            'Resources'
        )

    else:
        # Mode développement
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)