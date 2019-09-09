

import tkinter as tk
import requests
from tkinter import messagebox as tkMessageBox
tkMessageBox

class SeeModelView(tk.Frame):
    """See Model View"""

    def __init__(self, parent, close_add_callback, get_data ):
        """Constructor for See Model View"""
        tk.Frame.__init__(self,parent, width=800, height=800)
        self._parent = parent
        self.grid(rowspan=2, columnspan=2)

        self.list_data = []

        self._get_data = get_data

        self._close_add_callback = close_add_callback
        self._create_widgets()


    def _create_widgets(self):
        """Create Widget for SeeModelView"""
        tk.Label(self, text="First Name").grid(row=0)
        tk.Label(self, text="Last Name").grid(row=1)
        tk.Label(self, text="Talent Num").grid(row=2)
        tk.Label(self, text="Date Debut").grid(row=3)
        tk.Label(self, text="Model Type").grid(row=4)
        tk.Label(self, text="Type").grid(row=5)

        self.e1 = tk.Entry(self)
        self.e2 = tk.Entry(self)
        self.e3 = tk.Entry(self)
        self.e4 = tk.Entry(self)
        self.e5 = tk.Entry(self)
        self.e6 = tk.Entry(self)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)
        self.e6.grid(row=5, column=1)

        self._button = tk.Button(self,
                                 text="Edit Model",
                                 command=self._get_data)
        self._button.grid(row=6, column=1, padx=20)

        self._button = tk.Button(self,
                                  text="Close",
                                  command=self._close_add_callback)

        self._button.grid(row=6, column=2, padx=20)

        return

    def get_data(self):
        """Return talent object from entry"""
        return {"first_name": self.e1.get(),
                "last_name": self.e2.get(),
                "talent_num": self.e3.get(),
                "date_debut": self.e4.get(),
                "model_type": self.e5.get(),
                "type": self.e6.get()}


    def set_data(self, talent_object):
        """Set talent object from entry"""
        self.e1.insert(0, talent_object["first_name"])
        self.e2.insert(0, talent_object["last_name"])
        self.e3.insert(0, talent_object["talent_num"])
        self.e4.insert(0, talent_object["date_debut"])
        self.e5.insert(0, talent_object["model_type"])
        self.e6.insert(0, talent_object["type"])


