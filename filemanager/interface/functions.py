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
    image_path = Path.cwd() / "filemanager" / "static" / "img"

    return ctk.CTkImage(Image.open(Path(image_path) / f"{name}.png"), size=(30, 30))


def update_table(table: ttk.Treeview, data: List[File]) -> None:
    for child in table.get_children():
        table.delete(child)

    for file in data:
        tag = "gray" if util.expired_file(file.expiration) else "red"

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


def sort_column(table: ttk.Treeview, column: str, reverse: bool = False) -> None:
    data = [(table.set(k, column).lower(), k) for k in table.get_children("")]

    data.sort(key=lambda t: t[0], reverse=reverse)

    for index, (_, child) in enumerate(data):
        table.move(child, "", index)

    for _column in table["columns"]:
        table.heading(_column, text=_column.capitalize())

    reference = "⌄" if reverse else "^"
    table.heading(
        column,
        text=f"{column.capitalize()} ({reference})",
        command=lambda: sort_column(table, column, not reverse),
    )


def window_add(table: ttk.Treeview, root: ctk.CTk) -> None:
    path = filedialog.askopenfilename(
        initialdir="",
        title="Select file",
        filetypes=(("pdf files", ".pdf"), ("all files", ".*")),
    )

    if not path:
        return None

    values = util.decompose_file(path)

    description = util.replace_text(values[0])
    extension = values[1]

    window = EntryWindow()
    window.title("New file")
    window.transient(root)
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
            update_table(table, file_controller.lists()),
        ]
    )
    root.attributes("-disabled", 1)
    window.bind("<Destroy>", lambda event: root.attributes("-disabled", 0))


def window_open(table: ttk.Treeview, root: ctk.CTk):
    if not table.selection():
        return None

    selected = table.focus()
    values = table.item(selected, "values")

    file = f"{values[0]}.{values[3].lower()}"

    window = NotificationWindow()
    window.title("Open file")
    window.transient(root)
    window.label.configure(text=f"Are you sure to open {util.limit_text(file)}?")
    window.accept_button.configure(
        command=lambda: [
            util.open_file(file),
            window.destroy(),
        ]
    )
    root.attributes("-disabled", 1)
    window.bind("<Destroy>", lambda event: root.attributes("-disabled", 0))


def window_edit(table: ttk.Treeview, root: ctk.CTk):
    if not table.selection():
        return None

    selected = table.focus()
    values = table.item(selected, "values")

    description = values[0]
    expiration = values[2].split("/")
    extension = values[3]
    label = values[4]

    file = f"{description}.{extension.lower()}"

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
            util.verify_file(file),
            file_controller.update(
                File(
                    id=int(selected),
                    description=window.description_entry.get(),
                    expiration=f"{window.year_combobox.get()}/{window.month_combobox.get()}/{window.day_combobox.get()}",
                    extension=extension,
                    label=window.label_entry.get(),
                )
            ),
            util.rename_file(
                file, f"{window.description_entry.get()}.{extension.lower()}"
            ),
            window.destroy(),
            update_table(table, file_controller.lists()),
        ]
    )
    root.attributes("-disabled", 1)
    window.bind("<Destroy>", lambda event: root.attributes("-disabled", 0))


def window_delete(table: ttk.Treeview, root: ctk.CTk):
    if not table.selection():
        return None

    selected = table.focus()
    values = table.item(selected, "values")

    file = f"{values[0]}.{values[3].lower()}"

    window = NotificationWindow()
    window.title("Delete file")
    window.transient(root)
    window.label.configure(text=f"Are you sure to delete {util.limit_text(file)}?")
    window.accept_button.configure(
        command=lambda: [
            # util.verify_file(file),
            file_controller.delete(
                File(
                    id=int(selected),
                )
            ),
            util.delete_file(file),
            window.destroy(),
            update_table(table, file_controller.lists()),
        ]
    )
    root.attributes("-disabled", 1)
    window.bind("<Destroy>", lambda event: root.attributes("-disabled", 0))


def switch_appearance():
    mode = ctk.get_appearance_mode()
    if mode == "Light":
        ctk.set_appearance_mode("Dark")
    else:
        ctk.set_appearance_mode("Light")


def generate_backup():
    path = filedialog.askdirectory()

    if path:
        util.generate_backup(path)


def search_description(table: ttk.Treeview, entry_search: ctk.CTkEntry):
    file = File(description=entry_search.get())
    data_ = file_controller.details(file)
    update_table(table, data_)


def clear_selection(table: ttk.Treeview):
    for selected in table.selection():
        table.selection_remove(selected)


def report_callback_exception(self, exc, val, tb):
    messagebox.showerror(type(val).__name__, message=str(val))
