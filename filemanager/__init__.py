import ctypes

from .controller import file_controller
from .helpers import util
from .interface.root import FileManager


def create_app():
    if not (util.DATABASE.exists() and util.STORAGE.exists()):
        file_controller.reset()

    myappid = "filemanager.static.img.favicon"  # Only work in Windows
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    file_manager = FileManager()
    return file_manager
