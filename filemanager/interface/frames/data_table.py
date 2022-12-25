from tkinter import ttk

import customtkinter as ctk
from filemanager.controller import file_controller

from .. import functions


class DataTable(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame) -> None:
        super().__init__(parent)

        self.table = ttk.Treeview(self, selectmode="browse")
        self.table.grid(row=0, column=0, sticky="nsew")

        self.table_style = ttk.Style()
        self.table_style.theme_use("default")
        self.table_style.configure(
            style="Treeview",
            rowheight=20,
            fieldbackground="#C8C4C4",
        )
        self.table_style.map(style="Treeview", background=[("selected", "#3C8CD4")])

        # Columns and headings
        self.table["columns"] = (
            "description",
            "modification",
            "expiration",
            "extension",
            "label",
        )
        self.table["show"] = "headings"

        self.table.column("#0", width=0, stretch=False)
        self.table.heading("#0", text="", anchor="w")

        for col in self.table["columns"]:
            self.table.column(col, anchor="w", minwidth=80, width=0)
            self.table.heading(
                col, command=lambda e=col: functions.sort_column(self.table, f"{e}")
            )

        self.table.tag_configure("gray", background="#E26D5C")
        self.table.tag_configure("red", background="#E0E1DD")

        functions.update_table(self.table, file_controller.lists())

        # Scrolls
        self.scroll_x = ctk.CTkScrollbar(
            self, orientation="horizontal", command=self.table.xview
        )
        self.scroll_x.grid(row=1, column=0, sticky="sew")

        self.scroll_y = ctk.CTkScrollbar(self, command=self.table.yview)
        self.scroll_y.grid(row=0, column=1, sticky="nse")

        self.table.configure(
            xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set
        )
