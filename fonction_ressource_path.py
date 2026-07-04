import sys, os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Cas PyInstaller
        base_path = sys._MEIPASS
    elif getattr(sys, 'frozen', False):
        # Cas py2app
        base_path = os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
    else:
        # Mode dev (lancé depuis PyCharm/terminal)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)