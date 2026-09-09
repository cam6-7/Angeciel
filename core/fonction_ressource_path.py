import sys
import os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Cas PyInstaller
        base_path = sys._MEIPASS

    elif getattr(sys, 'frozen', False):
        # Cas py2app
        base_path = os.path.join(
            os.path.dirname(sys.executable),
            '../..',
            'Resources'
        )

    else:
        # Cas pycharm
        base_path = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[0: -1])

    return os.path.join(base_path, relative_path)