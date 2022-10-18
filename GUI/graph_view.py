import tkinter.ttk as ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from graphs import figure


class Plot_display:
    def __init__(self, master):
        self.master = master
        self.canvas = FigureCanvasTkAgg(figure, master=self.master)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)


class Graph_view(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.selected_joint = tk.StringVar()

        self.joint_combobox = ttk.Combobox(self.master, textvariable=self.selected_joint)
        self.joint_combobox_values = [f"joint_{i}" for i in range(1, 22)]
        self.joint_combobox["values"] = self.joint_combobox_values
        self.joint_combobox['state'] = 'readonly'
        self.joint_combobox.current(0)
        self.graph = Plot_display(self.master)
        self.joint_combobox.pack()