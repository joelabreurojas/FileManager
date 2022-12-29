from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import List

import customtkinter as ctk
from PIL import Image

from ..controller import file_controller
from ..helpers import util
from ..models.entities import File
from .toplevels import EntryWindow, NotificationWindow


def new_image(name: str) -> ctk.CTkImage:
    """Automatize image filling"""

    image_path = Path.cwd() / "filemanager" / "static" / "img"
    return ctk.CTkImage(Image.open(Path(image_path) / f"{name}.png"), size=(30, 30))


def update_table(table: ttk.Treeview, data: List[File]) -> None:
    """Remove and display the data in a table"""

    for child in table.get_children():
        table.delete(child)

    for file in data:
        tag = "gray" if util.expired_file(file) else "red"

        table.insert(
            parent="",
            index="end",
            iid=str(file.id),
            text="",
            values=(
                file.description,
                file.modification,
                file.expiration,
                file.extension,
                file.label,
            ),
            tags=tag,
        )

    for column in table["columns"]:
        table.heading(column, text=column.capitalize())

    sort_column(table, "description")


def sort_column(table: ttk.Treeview, column_: str, reverse: bool = False) -> None:
    """Sort in ascending or descending order a table according to a column"""

    data = [(table.set(item, column_).lower(), item) for item in table.get_children("")]

    data.sort(key=lambda e: e[0], reverse=reverse)

    for index, (_, item) in enumerate(data):
        table.move(item, "", index)

    for column in table["columns"]:
        table.heading(column, text=column.capitalize())

    reference = "⌄" if reverse else "^"
    table.heading(
        column_,
        text=f"{column_.capitalize()} ({reference})",
        command=lambda: sort_column(table, column_, not reverse),
    )


def window_add(table: ttk.Treeview, root: ctk.CTk) -> None:
    """Show add file window"""

    filename = filedialog.askopenfilename(
        initialdir="",
        title="Select file",
        filetypes=(("pdf files", ".pdf"), ("all files", ".*")),
    )

    if not filename:
        return None

    values = util.decompose_file(filename)
    description = values[0]
    extension = values[1]

    window = EntryWindow()
    window.title("New file")
    window.transient(root)
    window.description_entry.insert(0, util.replace_text(description))
    window.accept_button.configure(
        command=lambda: [
            file_controller.create(
                File(
                    description=window.description_entry.get(),
                    extension=extension,
                    expiration=f"{window.year_combobox.get()}/{window.month_combobox.get()}/{window.day_combobox.get()}",
                    label=window.label_entry.get(),
                    path=filename,
                ),
            ),
            window.destroy(),
            update_table(table, file_controller.lists()),
        ]
    )
    root.attributes("-disabled", 1)
    window.bind("<Destroy>", lambda event: root.attributes("-disabled", 0))


def window_open(table: ttk.Treeview, root: ctk.CTk):
    """Open file confirmation window"""

    if not table.selection():
        return None

    selected = table.focus()
    values = table.item(selected, "values")
    description = values[0]
    extension = values[3]
    filename = f"{description}.{extension.lower()}"

    window = NotificationWindow()
    window.title("Open file")
    window.transient(root)
    window.label.configure(text=f"Are you sure to open {util.limit_text(filename)}?")
    window.accept_button.configure(
        command=lambda: [
            file_controller.open(
                File(description=description, extension=extension, path=filename)
            ),
            window.destroy(),
        ]
    )
    root.attributes("-disabled", 1)
    window.bind("<Destroy>", lambda event: root.attributes("-disabled", 0))


def window_edit(table: ttk.Treeview, root: ctk.CTk):
    """Show edit file window"""

    if not table.selection():
        return None

    selected = table.focus()
    values = table.item(selected, "values")
    description = values[0]
    expiration = values[2].split("/")
    extension = values[3]
    label = values[4]
    filename = f"{description}.{extension.lower()}"

    window = EntryWindow()
    window.title("Edit file")
    window.transient(root)
    window.description_entry.insert(0, description)

    if expiration[0] and expiration[1] and expiration[2]:
        window.year_combobox.set(expiration[0])
        window.month_combobox.set(expiration[1])
        window.day_combobox.set(expiration[2])

    if label:
        window.label_entry.insert(0, label)

    window.accept_button.configure(
        command=lambda: [
            file_controller.update(
                File(
                    id=int(selected),
                    description=window.description_entry.get(),
                    expiration=f"{window.year_combobox.get()}/{window.month_combobox.get()}/{window.day_combobox.get()}",
                    extension=extension,
                    label=window.label_entry.get(),
                    path=filename,
                )
            ),
            window.destroy(),
            update_table(table, file_controller.lists()),
        ]
    )
    root.attributes("-disabled", 1)
    window.bind("<Destroy>", lambda event: root.attributes("-disabled", 0))


def window_delete(table: ttk.Treeview, root: ctk.CTk):
    """Show delete file confirmation window"""

    if not table.selection():
        return None

    selected = table.focus()
    values = table.item(selected, "values")
    description = values[0]
    extension = values[3]
    filename = f"{description}.{extension.lower()}"

    window = NotificationWindow()
    window.title("Delete file")
    window.transient(root)
    window.label.configure(text=f"Are you sure to delete {util.limit_text(filename)}?")
    window.accept_button.configure(
        command=lambda: [
            file_controller.delete(
                File(
                    id=int(selected),
                    description=description,
                    extension=extension,
                    path=filename,
                )
            ),
            window.destroy(),
            update_table(table, file_controller.lists()),
        ]
    )
    root.attributes("-disabled", 1)
    window.bind("<Destroy>", lambda event: root.attributes("-disabled", 0))


def switch_appearance():
    """Change the style of the application between ligth and dark mode"""

    mode = ctk.get_appearance_mode()
    if mode == "Light":
        ctk.set_appearance_mode("Dark")
    else:
        ctk.set_appearance_mode("Light")


def generate_backup():
    """Request a route to generate the backup"""

    directory = filedialog.askdirectory()
    file_controller.backup(File(path=directory))


def search_description(table: ttk.Treeview, entry_search: ctk.CTkEntry):
    """Displays the results most similar to the description received"""

    file = File(description=entry_search.get())
    data_ = file_controller.details(file)
    update_table(table, data_)


def clear_selection(table: ttk.Treeview):
    """Deselect a row in case of having one"""

    for selected in table.selection():
        table.selection_remove(selected)


def report_callback_exception(self, exc, val, tb):
    """Show the error notification window"""

    messagebox.showerror(type(val).__name__, message=str(val))
