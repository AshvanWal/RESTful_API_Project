import tkinter as tk
from top_navbar_view import TopNavbarView
from page1_view import Page1View
from page2_view import Page2View
from bottom_navbar_view import BottomNavbarView
import requests
from tkinter import messagebox as tkMessageBox
from add_model_view import ModelView
from add_actor_view import ActorView

from update_model_view import UpdateModelView
from update_actor_view import UpdateActorView

from see_actor_view import SeeActorView
from see_model_view import SeeModelView
import json


class MainAppController(tk.Frame):
    """ Main Application for GUI """

    def __init__(self, parent):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)

        self._talents = []

        self._top_navbar = TopNavbarView(self, self._page_callback)

        self._page1 = Page1View(self, self._page1_submit_callback_display, self._page1_delete_submit_callback, self._page1_view_popup_callback, self._page1_update_popup_callback, self._page1_see_detail_callback)
        self._page2 = Page2View(self, self._page2_submit_callback_display, self._page2_delete_submit_callback, self._page2_view_popup_callback, self._page2_update_popup_callback,  self._page2_see_detail_callback )
        self._bottom_navbar = BottomNavbarView(self, self._quit_callback)

        self._top_navbar.grid(row=0, columnspan=4, pady=10)
        self._page1.grid(row=1, columnspan=4, pady=10)
        self._curr_page = TopNavbarView.PAGE1
        # Hide Page 2 by default
        self._bottom_navbar.grid(row=2, columnspan=4, pady=10)


    def _page_callback(self):
        """ Handle Switching Between Pages """

        curr_page = self._top_navbar.curr_page.get()
        if (self._curr_page != curr_page and self._curr_page == TopNavbarView.PAGE1):
            self._page1.grid_forget()
            self._page2.grid(row=1, columnspan=4)
            self._curr_page = TopNavbarView.PAGE2
            print("Changed Page 1")
            self._page2_submit_callback_display()
        elif (self._curr_page != curr_page and self._curr_page == TopNavbarView.PAGE2):
            self._page2.grid_forget()
            self._page1.grid(row=1, columnspan=4)
            self._curr_page = TopNavbarView.PAGE1
            self._page1_submit_callback_display()
            print("Changed Page 2")


    def _page1_delete_submit_callback(self):
        """Delete page 1 callback"""

        try:

            items_index = self._page1.get_cur_selection()

            self.talent_object = self._talents[items_index]

            talent_id = self.talent_object["id"]

            url = "http://127.0.0.1:5000/talent_agency/talent/"+str(talent_id)

            flag = self._page1._delete_popup()

            if flag:

                response = requests.delete(url)
            else:
                return

            if response.status_code == 200:
                print("Delete Succeed")
                self._page1_submit_callback_display()

        except:
            return ("Error")

    def _page2_delete_submit_callback(self):
        """Delete page 2 callback"""


        items_index = self._page2.get_cur_selection()

        self.talent_object = self._talents[items_index]

        talent_id = self.talent_object["id"]

        url = "http://127.0.0.1:5000/talent_agency/talent/"+str(talent_id)

        self._page2._delete_popup()

        response = requests.delete(url)

        if response.status_code == 200:
            print("Delete Succeed")
            self._page2_submit_callback_display()

    def _page1_submit_callback_display(self):
        """Page 1 submitting callback"""
        print("Display Succeed 1")

        response = requests.get("http://127.0.0.1:5000/talent_agency/talent/actor")

        if response.status_code == 200:
            self._talents = response.json()
            self._page1.set_form_data(response.json())

    def _page2_submit_callback_display(self):
        """Page 2 submitting callback"""
        print("Display Succeed 2")
        response = requests.get("http://127.0.0.1:5000/talent_agency/talent/model")

        if response.status_code == 200:
            self._talents = response.json()
            self._page2.set_form_data(response.json())


    def _page1_view_popup_callback(self):
        """Page 1 add view callback"""
        print("Add callback")
        self._add_win = tk.Toplevel()
        self._add = ActorView(self._add_win, self._close_add_callback, self._get_data)


    def _page2_view_popup_callback(self):
        """Page 1 add view callback"""
        print("Add callback")
        self._add_win = tk.Toplevel()
        self._add = ModelView(self._add_win, self._close_add_callback, self._get_data)


    def _page1_update_popup_callback(self):
        """Page 1 update callback"""
        print("Update callback")
        try:
            self._update_win = tk.Toplevel()

            self._update = UpdateActorView(self._update_win, self._close_update_callback, self._page1_get_update_data)
            items_index = self._page1.get_cur_selection()
            self.talent_object = self._talents[items_index]

            self._update.set_data(self.talent_object)
        except:
            self._close_update_callback()
            print("Please choose a talent")
            return

    def _page2_update_popup_callback(self):
        """Page 2 update callback"""
        print("Update callback")
        try:
            self._update_win = tk.Toplevel()

            self._update = UpdateModelView(self._update_win, self._close_update_callback, self._page2_get_update_data)
            items_index = self._page2.get_cur_selection()
            self.talent_object = self._talents[items_index]

            self._update.set_data(self.talent_object)
        except:
            self._close_update_callback()
            print("Please choose a talent")
            return

    def  _page1_see_detail_callback(self):
        """Page 1 see detail callback"""
        try:

            print("See details callback")
            self._detail_win = tk.Toplevel()

            self._detail = SeeActorView(self._detail_win, self._close_see_callback, self._page1_see_details_data)

            items_index = self._page1.get_cur_selection()
            talent_object = self._talents[items_index]

            self._detail.set_data(talent_object)

        except:
            self._close_see_callback()
            print("Please choose a talent")
            return

    def _page2_see_detail_callback(self):
        """Page 2 see details callback"""
        try:
            print("See details callback")
            self._detail_win = tk.Toplevel()

            self._detail = SeeModelView(self._detail_win, self._close_see_callback, self._page2_see_details_data)

            items_index = self._page2.get_cur_selection()
            talent_object = self._talents[items_index]

            self._detail.set_data(talent_object)
        except:
            self._close_see_callback()
            print("Please choose a talent")
            return

    def _get_data(self):
        """Return talent object for add"""
        print("Get data...")
        try:
            payload = self._add.get_data()

            url = ' http://127.0.0.1:5000/talent_agency/talent'

            headers = {'content-type': 'application/json'}

            response = requests.post(url, data=json.dumps(payload), headers=headers)

            if payload["type"] == "actor":

                self._page1_submit_callback_display()

            if payload["type"] == "model":
                self._page2_submit_callback_display()

            print("TalentID:",response.text)

            return response.text
        except:
            print("Get data error")

    def _page1_see_details_data(self):
        """"Return talent object for see detail"""
        print("See details data...")
        try:

            payload = self._detail.get_data()

            url = ' http://127.0.0.1:5000/talent_agency/talent'

            headers = {'content-type': 'application/json'}

            response = requests.post(url, data=json.dumps(payload), headers=headers)

            print("TalentID:",response.text)

            return
        except:
            print("Error")

    def _page2_see_details_data(self):
        """"Return talent object for see detail"""
        print("See details data...")
        try:

            payload = self._detail.get_data()

            url = ' http://127.0.0.1:5000/talent_agency/talent'

            headers = {'content-type': 'application/json'}

            response = requests.post(url, data=json.dumps(payload), headers=headers)

            print("TalentID:", response.text)

            return
        except:
            print("Error")

    def _page1_get_update_data(self):
        """"Return talent object for update"""
        try:

            print("Get update data...")

            payload = self._update.get_data()

            url = ' http://127.0.0.1:5000/talent_agency/talent/'

            headers = {'content-type': 'application/json'}

            id = self.talent_object['id']

            response = requests.put(url+str(id), data=json.dumps(payload), headers=headers)

            self._page1_submit_callback_display()

            return
        except:

            print("Error")

    def _page2_get_update_data(self):
        """"Return talent object for update"""
        print("Get update data...")

        try:

            payload = self._update.get_data()

            url = ' http://127.0.0.1:5000/talent_agency/talent/'

            headers = {'content-type': 'application/json'}

            id = self.talent_object['id']

            response = requests.put(url+str(id), data=json.dumps(payload), headers=headers)

            self._page2_submit_callback_display()

            return
        except:
            print("Error")

    def _close_add_callback(self):
        """Closing add popup"""
        self._add_win.destroy()

    def _close_update_callback(self):
        """Closing update popup"""
        self._update_win.destroy()

    def _close_see_callback(self):
        """Closing see details popup"""
        self._detail_win.destroy()

    def _quit_callback(self):
        """Quit popup"""
        self.quit()


if __name__ == "__main__":
    root = tk.Tk()
    MainAppController(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()



