from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import List

import customtkinter as ctk
from PIL import Image, ImageTk

from ..controller import file_controller
from ..helpers import util
from ..models.entities import File
from ..views.toplevels import EntryWindow, NotificationWindow

FAVICON = Path.cwd() / "filemanager" / "static" / "img" / "favicon.ico"


class FileManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        WIDTH = 800
        HEIGHT = 600

        X = (self.winfo_screenwidth() / 2) - (WIDTH / 2)
        Y = (self.winfo_screenheight() / 2) - (HEIGHT / 2)

        self.title("File Manager")
        self.geometry(f"{WIDTH}x{HEIGHT}+{int(X)}+{int(Y)}")
        self.minsize(640, 500)
        self.iconbitmap(FAVICON)

        # Frames
        self.background_frame = ctk.CTkFrame(self)
        self.background_frame.pack(side="top", fill="both", expand=True)

        self.container_frame = ctk.CTkFrame(self.background_frame)
        self.container_frame.pack(side="top", fill="both", expand=True)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.container_frame.grid_rowconfigure(1, weight=1)

        self.options_frame = ctk.CTkFrame(self.container_frame)
        self.options_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        self.options_frame.columnconfigure(4, weight=2)

        self.table_container_frame = ctk.CTkFrame(self.container_frame)
        self.table_container_frame.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10
        )

        self.table_frame = ctk.CTkFrame(self.table_container_frame)
        self.table_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        # Options section
        self.image_path = Path(__file__).parent.parent / "static" / "img"

        self.elements = (
            ctk.CTkButton(
                self.options_frame,
                image=self.new_image("add"),
                command=self.window_add,
            ),
            ctk.CTkButton(
                self.options_frame,
                image=self.new_image("open"),
                command=self.window_open,
            ),
            ctk.CTkButton(
                self.options_frame,
                image=self.new_image("edit"),
                command=self.window_edit,
            ),
            ctk.CTkButton(
                self.options_frame,
                image=self.new_image("delete"),
                command=self.window_delete,
            ),
            ctk.CTkEntry(
                self.options_frame, placeholder_text="Search by description..."
            ),
            ctk.CTkButton(
                self.options_frame,
                image=self.new_image("appearance"),
                command=self.switch_appearance,
            ),
            ctk.CTkButton(
                self.options_frame,
                image=self.new_image("backup"),
                command=self.generate_backup,
            ),
        )

        self.count = 0
        for element in self.elements:

            # Entry
            if self.count == 4:
                self.entry_search = element
                self.entry_search.configure(width=350)
                self.entry_search.grid(row=0, column=self.count, padx=10)
                self.entry_search.bind("<Return>", lambda e: self.search_description())
                self.entry_search.focus_get()

            # Buttons
            elif self.count % 2 == 0:
                element.configure(text="", width=50, height=50)
                element.grid(row=0, column=self.count, pady=5, padx=5)

            else:
                element.configure(text="", width=50, height=50)
                element.grid(row=0, column=self.count, pady=5)

            self.count += 1

        # Table section
        self.table = ttk.Treeview(self.table_frame, selectmode="browse")
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

        for element in self.table["columns"]:
            self.table.column(element, anchor="w", minwidth=80, width=0)
            self.table.heading(element, text=element.capitalize())

            self.table.heading(
                f"{element}",
                command=lambda element=element: self.sort_column(f"{element}", False),
            )
            if element == "description":
                self.table.heading(
                    f"{element}",
                    command=lambda element=element: self.sort_column(
                        f"{element}", True
                    ),
                )

        self.table.tag_configure("gray", background="#E26D5C")
        self.table.tag_configure("red", background="#E0E1DD")

        self.update_table(file_controller.lists())
        self.bind("<Escape>", lambda e: self.clear_selection())

        # Scrolls
        self.scroll_x = ctk.CTkScrollbar(
            self.table_frame, orientation="horizontal", command=self.table.xview
        )
        self.scroll_x.grid(row=1, column=0, sticky="sew")

        self.scroll_y = ctk.CTkScrollbar(
            self.table_frame, orientation="vertical", command=self.table.yview
        )
        self.scroll_y.grid(row=0, column=1, sticky="nse")

        self.table.configure(
            xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set
        )

    def new_image(self, name: str) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(
            Image.open(Path(self.image_path) / f"{name}.png").resize(
                (35, 35), Image.ANTIALIAS
            )
        )

    def update_table(self, data: List[File]) -> None:
        for record in self.table.get_children():
            self.table.delete(record)

        for record in data:
            tag = "gray" if util.expired_file(File(expiration=record[3])) else "red"

            self.table.insert(
                parent="",
                index="end",
                iid=str(record[0]),
                text="",
                values=(record[1], record[2], record[3], record[4], record[5]),
                tags=tag,
            )

    def sort_column(self, col: str, reverse: bool) -> None:
        l = [(self.table.set(k, col), k) for k in self.table.get_children("")]
        l.sort(key=lambda t: t[0], reverse=reverse)

        for index, (_, k) in enumerate(l):
            self.table.move(k, "", index)

        self.table.heading(col, command=lambda: self.sort_column(col, not reverse))

    def window_add(self) -> None:
        path = filedialog.askopenfilename(
            initialdir="",
            title="Select file",
            filetypes=(("pdf files", ".pdf"), ("all files", ".*")),
        )

        if not path:
            return None

        data = util.decompose_file(path)

        description = data[0]
        extension = data[1]

        window = EntryWindow()
        window.title("New file")
        window.transient(self)
        window.description_entry.insert(0, description)
        window.accept_button.configure(
            command=lambda: [
                file_controller.create(
                    File(
                        description=window.description_entry.get(),
                        extension=extension,
                        expiration=f"{window.year_combobox.get()}/{window.month_combobox.get()}/{window.day_combobox.get()}",
                        label=window.label_entry.get(),
                    )
                ),
                util.copy_file(path, f"{window.description_entry.get()}{extension}"),
                window.destroy(),
                self.update_table(file_controller.lists()),
            ]
        )
        self.attributes("-disabled", 1)
        window.bind("<Destroy>", lambda event: self.attributes("-disabled", 0))

    def window_open(self):
        if not self.table.selection():
            return None

        selected = self.table.focus()
        values = self.table.item(selected, "values")

        file = f"{values[0]}.{values[3].lower()}"

        window = NotificationWindow()
        window.title("Open file")
        window.transient(self)
        window.label.configure(text=f"Are you sure to open {file}?")
        window.accept_button.configure(
            command=lambda: [
                util.open_file(file),
                window.destroy(),
            ]
        )
        self.attributes("-disabled", 1)
        window.bind("<Destroy>", lambda event: self.attributes("-disabled", 0))

    def window_edit(self):
        if not self.table.selection():
            return None

        selected = self.table.focus()
        values = self.table.item(selected, "values")

        description = values[0]
        expiration = values[2].split("/")
        extension = values[3]
        label = values[4]

        window = EntryWindow()
        window.title("Edit file")
        window.transient(self)
        window.description_entry.insert(0, description)
        window.label_entry.insert(0, label)
        window.accept_button.configure(
            command=lambda: [
                file_controller.update(
                    File(
                        id=int(selected),
                        description=window.description_entry.get(),
                        expiration=f"{window.year_combobox.get()}/{window.month_combobox.get()}/{window.day_combobox.get()}",
                        extension=values[3],
                        label=window.label_entry.get(),
                    )
                ),
                util.rename_file(
                    f"{description}.{extension.lower()}",
                    f"{window.description_entry.get()}.{extension.lower()}",
                ),
                window.destroy(),
                self.update_table(file_controller.lists()),
            ]
        )
        self.attributes("-disabled", 1)
        window.bind("<Destroy>", lambda event: self.attributes("-disabled", 0))
        if expiration[0] and expiration[1] and expiration[2]:
            window.year_combobox.set(expiration[0])
            window.month_combobox.set(expiration[1])
            window.day_combobox.set(expiration[2])

    def window_delete(self):
        if not self.table.selection():
            return None

        selected = self.table.focus()
        values = self.table.item(selected, "values")

        file = f"{values[0]}.{values[3].lower()}"

        window = NotificationWindow()
        window.title("Delete file")
        window.transient(self)
        window.label.configure(text=f"Are you sure to delete {file}?")
        window.accept_button.configure(
            command=lambda: [
                file_controller.delete(
                    File(
                        id=int(selected),
                    )
                ),
                util.delete_file(file),
                window.destroy(),
                self.update_table(file_controller.lists()),
            ]
        )
        self.attributes("-disabled", 1)
        window.bind("<Destroy>", lambda event: self.attributes("-disabled", 0))

    def switch_appearance(self):
        mode = ctk.get_appearance_mode()
        if mode == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def generate_backup(self):
        path = filedialog.askdirectory()

        if path:
            util.generate_backup(path)

    def search_description(self):
        file = File(description=self.entry_search.get())
        data = file_controller.details(file)
        self.update_table(data)

    def clear_selection(self):
        for element in self.table.selection():
            self.table.selection_remove(element)

    def report_callback_exception(self, exc, val, tb):
        messagebox.showerror(type(val).__name__, message=str(val))
