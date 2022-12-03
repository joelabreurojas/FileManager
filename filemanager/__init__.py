from .views.index import FileManager


def create_app():
    file_manager = FileManager()
    return file_manager
