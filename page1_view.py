import tkinter as tk
import requests
from tkinter import messagebox as tkMessageBox



class Page1View(tk.Frame):
    """ Page 1 - Actor"""

    def __init__(self, parent, submit_callback, delete_callback, add_callback, update_callback, see_detail_callback):
        """Constructor for Page 1 - Actor"""
        tk.Frame.__init__(self, parent, width=800, height=800)
        self._parent = parent

        self._submit_callback = submit_callback

        self._delete_callback = delete_callback

        self._add_callback = add_callback

        self._update_callback = update_callback

        self._see_detail_callback = see_detail_callback

        self._create_widgets()

    def _create_widgets(self):
        """Create Widget for Page 1 - Actor"""
        self._scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        self._listbox = tk.Listbox(self, yscrollcommand=self._scrollbar.set)
        self._scrollbar.config(command=self._listbox.yview)
        self._listbox.grid(row=0, columnspan=3)
        self._scrollbar.grid(row=0, column=6, sticky=tk.N + tk.S + tk.W + tk.E)

        self._button = tk.Button(self,
                                 text="Display Actor",
                                 command=self._submit_callback)
        self._button.grid(row=1,column=2, padx=25)

        self._button = tk.Button(self,
                                 text="Delete Actor",
                                 command= self._delete_callback)
        self._button.grid(row=2,column=2, padx=25)

        self._button = tk.Button(self,
                                 text="Add Actor",
                                 command= self._add_callback)
        self._button.grid(row=3,column=2,padx=25)


        self._button = tk.Button(self,
                                 text="Update Actor",
                                 command= self._update_callback)
        self._button.grid(row=4,column=2,padx=25)

        self._button = tk.Button(self,
                                 text="See Details",
                                 command=self._see_detail_callback)
        self._button.grid(row=5, column=2,padx=25)

    def get_cur_selection(self):
        """Return index of current selection"""
        index = ''
        try:

            index = self._listbox.curselection()[0]
        except:
            return

        return index

    def _delete_popup(self):
        """Ask for delete confirmation"""
        flag = ""
        if tkMessageBox.askyesno('Verify', 'Really delete?'):
            flag = True
            # quit()
        else:
            tkMessageBox.showinfo('No', 'Quit has been cancelled')
            flag = False
        return flag

    def set_form_data(self, talents):
        """Return name of talent in the listbox"""
        self._listbox.delete(0, tk.END)
     
        for item in talents:
            self._listbox.insert(tk.END, item["first_name"] +" " + item["last_name"])
