from pathlib import Path

import customtkinter as ctk

from . import functions
from .frames import DataTable, OptionsBar

WIDTH = 800
HEIGHT = 600

FAVICON = Path.cwd() / "filemanager" / "static" / "img" / "favicon.ico"


class FileManager(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.CTk.report_callback_exception = functions.report_callback_exception

        X = (self.winfo_screenwidth() / 2) - (WIDTH / 2)
        Y = (self.winfo_screenheight() / 2) - (HEIGHT / 2)

        self.title("File Manager")
        self.geometry(f"{WIDTH}x{HEIGHT}+{int(X)}+{int(Y)}")
        self.minsize(640, 500)
        self.iconbitmap(FAVICON)

        # Frames
        self.background = ctk.CTkFrame(self)
        self.options_bar = OptionsBar(self.background, self)
        self.container_table = ctk.CTkFrame(self.background)
        self.data_table = DataTable(self.container_table)

        self.background.pack(side="top", fill="both", expand=True)
        self.options_bar.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        self.container_table.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.data_table.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self.background.grid_columnconfigure(0, weight=1)
        self.background.grid_rowconfigure(1, weight=1)
        self.options_bar.columnconfigure(4, weight=2)
        self.data_table.grid_columnconfigure(0, weight=1)
        self.data_table.grid_rowconfigure(0, weight=1)

        self.background.configure(fg_color=("#F5F3BB", "#454652"))
        self.options_bar.configure(fg_color=("#DCDBAC", "#323446"))
        self.container_table.configure(fg_color=("#DCDBAC", "#323446"))
        self.data_table.configure(fg_color=("transparent"))

        # Binds
        self.bind(
            "<Escape>", lambda e: functions.clear_selection(self.data_table.table)
        )
