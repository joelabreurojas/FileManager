from pathlib import Path

import customtkinter as ctk

WIDTH = 300
HEIGHT = 90

FAVICON = Path.cwd() / "filemanager" / "static" / "img" / "favicon.ico"


class NotificationWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        X = (self.winfo_screenwidth() / 2) - (WIDTH / 2)
        Y = (self.winfo_screenheight() / 2) - (HEIGHT / 2)

        self.maxsize(WIDTH, HEIGHT)
        self.minsize(WIDTH, HEIGHT)
        self.geometry(f"{WIDTH}x{HEIGHT}+{int(X)}+{int(Y)}")
        self.iconbitmap(FAVICON)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self)
        self.accept_button = ctk.CTkButton(
            self, text="Accept", font=ctk.CTkFont(weight="bold")
        )

        self.label.grid(row=0, column=0, pady=10)
        self.accept_button.grid(row=1, column=0)

        # Binds
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Return>", lambda e: self.accept_button.command())
