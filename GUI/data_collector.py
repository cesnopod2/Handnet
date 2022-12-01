import tkinter as tk
import os
import numpy as np


class DataCollector:
    """
    DataCollector class is responsible for handling the whole logic
    from graphical user interface.
    It avoids creating folders with gesture names and person id's, what helps in creating well-structured
    custom datasets with gestures performed by the users.
    """
    def __init__(self):
        self.data_path = r"C:\Users\Filip\Desktop\Final_custom_gesture"
        self.gesture_folder_path = None
        self.person_folder_path = None
        self.essai_file_path = None

        self.gesture_name = None
        self.person_name = None
        self.essai_id = None

    def save_data(self, results):
        pass

    def prepare_directory(self):
        try:
            self.gesture_folder_path = os.path.join(self.data_path, self.gesture_name)
            if os.path.exists(self.gesture_folder_path):
                print(f"Directory of gesture:{self.gesture_name} exists.")
            else:
                os.mkdir(self.gesture_folder_path)
                print(f"Directory of gesture :{self.gesture_name} has successfully created.")

        except Exception:
            pass

    def define_person(self):
        try:
            self.person_folder_path = os.path.join(self.gesture_folder_path, self.person_name)
            if os.path.exists(self.person_folder_path):
                print(f"Directory of person:{self.person_name} in gesture: {self.gesture_name} exists.")
            else:
                os.mkdir(self.person_folder_path)
                print(
                    f"Directory of person :{self.gesture_name} in gesture {self.gesture_name} has successfully created.")
        except Exception:
            pass

    def save_data(self, data):
        try:
            id = len(os.listdir(self.person_folder_path))
            essai_file = f"essai_{id}" + ".npy"
            self.essai_file_path = os.path.join(self.person_folder_path, essai_file)
            if os.path.exists(self.essai_file_path):
                print("Path exists")
            else:
                np.save(self.essai_file_path, data)
                print(f"Creaded essai file")
        except Exception:
            pass

    @property
    def gesture_name(self):
        return self._gesture_name

    @gesture_name.setter
    def gesture_name(self, value):
        self._gesture_name = value
        self.prepare_directory()

    @property
    def person_name(self):
        return self._person_name

    @person_name.setter
    def person_name(self, value):
        self._person_name = value
        self.define_person()


class GUI_DataCollector:
    """

    Class GUI_DataCollector is responsible for displaying data collection view.

    """
    def __init__(self, master):
        self.master = master
        self.gesutre_name = tk.StringVar()
        self.person_name = tk.StringVar()

        self.gesture_widget = tk.ttk.Entry(self.master, textvariable=self.gesutre_name)
        self.person_widget = tk.ttk.Entry(self.master, textvariable=self.person_name)
        self.gesture_label = tk.Label(self.master, text="put gesture name here")
        self.person_label = tk.Label(self.master, text="put person name here")
        self.frame_amount_label = tk.Label(self.master)
        self.submit_button = tk.Button(self.master, text="Submit data collection")
