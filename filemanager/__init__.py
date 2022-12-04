import ctypes

from .views.index import FileManager


def create_app():
    myappid = "filemanager.static.img.favicon"  # Only work in Windows
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    file_manager = FileManager()
    return file_manager
