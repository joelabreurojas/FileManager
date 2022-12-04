import customtkinter as ctk

from ..helpers import util


class EntryWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        WIDTH = 380
        HEIGHT = 220

        X = (self.winfo_screenwidth() / 2) - (WIDTH / 2)
        Y = (self.winfo_screenheight() / 2) - (HEIGHT / 2)

        self.maxsize(WIDTH, HEIGHT)
        self.minsize(WIDTH, HEIGHT)
        self.geometry(f"{WIDTH}x{HEIGHT}+{int(X)}+{int(Y)}")
        self.iconbitmap(r"filemanager\static\img\favicon.ico")

        self.dates = util.generate_dates()

        self.description_label = ctk.CTkLabel(self, text="Description")
        self.description_entry = ctk.CTkEntry(self)
        self.expiration_label = ctk.CTkLabel(self, text="Expiration - (Optional)")
        self.year_combobox = ctk.CTkComboBox(
            self, width=66, values=[""] + self.dates[0]
        )
        self.month_combobox = ctk.CTkComboBox(
            self, width=52, values=[""] + self.dates[1]
        )
        self.day_combobox = ctk.CTkComboBox(self, width=52, values=[""] + self.dates[2])

        for element in [self.year_combobox, self.month_combobox, self.day_combobox]:
            element.configure(
                fg_color="#D3D3D3",
                text_color="black",
                state="readonly",
            )
            element.entry.configure(readonlybackground="#D3D3D3")

        self.label_combobox = ctk.CTkComboBox(
            self, width=180, values=["", "Agreements", "Resolutions"]
        )
        self.accept_button = ctk.CTkButton(self, text="Accept")
        self.label = ctk.CTkLabel(self, text="Label - (Optional)")

        self.description_label.grid(row=0, column=0, columnspan=5, pady=10)
        self.expiration_label.grid(row=2, column=0, columnspan=3)
        self.label.grid(row=2, column=3, pady=10)
        self.description_entry.grid(
            row=1, column=0, columnspan=5, padx=80, pady=5, sticky="ew"
        )
        self.year_combobox.grid(row=4, column=0, padx=5)
        self.month_combobox.grid(row=4, column=1)
        self.day_combobox.grid(row=4, column=2, padx=5)
        self.label_combobox.grid(row=4, column=3, sticky="ew", padx=5)
        self.accept_button.grid(row=5, column=0, columnspan=5, pady=20)


class NotificationWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        WIDTH = 300
        HEIGHT = 90

        X = (self.winfo_screenwidth() / 2) - (WIDTH / 2)
        Y = (self.winfo_screenheight() / 2) - (HEIGHT / 2)

        self.maxsize(WIDTH, HEIGHT)
        self.minsize(WIDTH, HEIGHT)
        self.geometry(f"{WIDTH}x{HEIGHT}+{int(X)}+{int(Y)}")
        self.iconbitmap(r"filemanager\static\img\favicon.ico")
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self)
        self.accept_button = ctk.CTkButton(
            self,
            text="Accept",
        )

        self.label.grid(row=0, column=0, pady=10)
        self.accept_button.grid(row=1, column=0)
