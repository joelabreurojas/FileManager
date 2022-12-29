"""Alternative way to start the application, with: python -m filemanager"""

from . import create_app

if __name__ == "__main__":
    file_manager = create_app()
    file_manager.mainloop()
