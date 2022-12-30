"""Process instantiation module"""

import ctypes

from .controller import file_controller
from .helpers import util
from .interface.root import FileManager


def create_app():
    """Verify data and instantiates the application with a customised icon"""

    if not (util.DATABASE.exists() and util.STORAGE.exists()):
        file_controller.reset()

    # Icon in the taskbar: Only work in Windows
    myappid = "filemanager.static.img.favicon"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    file_manager = FileManager()
    return file_manager
