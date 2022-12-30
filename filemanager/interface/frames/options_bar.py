"""Internal frame, grandson of root"""

import customtkinter as ctk

from .. import functions


class OptionsBar(ctk.CTkFrame):
    """Definition of the elements related to the option section"""

    def __init__(self, parent: ctk.CTkFrame, root: ctk.CTk) -> None:
        super().__init__(parent)

        self.options = (
            ctk.CTkButton(
                self,
                text="",
                image=functions.new_image("add"),
                command=lambda: functions.window_add(root.data_table.table, root),
            ),
            ctk.CTkButton(
                self,
                text="",
                image=functions.new_image("open"),
                command=lambda: functions.window_open(root.data_table.table, root),
            ),
            ctk.CTkButton(
                self,
                text="",
                image=functions.new_image("edit"),
                command=lambda: functions.window_edit(root.data_table.table, root),
            ),
            ctk.CTkButton(
                self,
                text="",
                image=functions.new_image("delete"),
                command=lambda: functions.window_delete(root.data_table.table, root),
            ),
            ctk.CTkEntry(self, placeholder_text="Search by description..."),
            ctk.CTkButton(
                self,
                text="",
                image=functions.new_image("appearance"),
                command=functions.switch_appearance,
            ),
            ctk.CTkButton(
                self,
                text="",
                image=functions.new_image("backup"),
                command=functions.generate_backup,
            ),
        )

        self.count = 0
        for option in self.options:

            # Entry
            if self.count == 4:
                self.entry_search = option
                self.entry_search.configure(width=350)
                self.entry_search.grid(row=0, column=self.count, padx=10)
                self.entry_search.bind(
                    "<Return>",
                    lambda e: functions.search_description(
                        root.data_table.table, self.entry_search
                    ),
                )
                self.entry_search.focus_get()

            # Buttons
            elif self.count % 2 == 0:
                option.configure(width=50, height=50)
                option.grid(row=0, column=self.count, pady=5, padx=5)

            else:
                option.configure(width=50, height=50)
                option.grid(row=0, column=self.count, pady=5)

            self.count += 1
