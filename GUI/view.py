from graphs import figure_skeleton
import graphs

from graphs import ax1, ax2, ax3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import numpy as np
from PIL import ImageTk, Image

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import queue
import datetime
from graph_view import Graph_view


class Top_view:
    """

    """
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.master)
        self.label["text"] = "HandNET"
        self.label.config(font=("Courier", 44))
        self.load_model_button = tk.Button(self.master, text="Load model")
        self.load_model_button.pack(anchor="ne")
        self.model_path = None


class Camera_display(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.camera_label = tk.Label(self.master)
        self.camera_label.pack()


class Skeleton_display(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.canvas = FigureCanvasTkAgg(figure_skeleton, master=self.master)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        # self.canvas.get_tk_widget().pack(side=tk.LEFT)
        self.canvas.get_tk_widget().pack()


class Camera_skeleton_display(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.tab_controller = ttk.Notebook()
        self.camera_frame = ttk.Frame(self.tab_controller, width=660, height=460)
        self.skeleton_frame = ttk.Frame(self.tab_controller, width=660, height=460)
        self.camera_view = Camera_display(self.camera_frame)
        self.camera_frame.pack()
        self.skeleton_frame.pack()
        self.skeleton_view = Skeleton_display(self.skeleton_frame)
        self.tab_controller.add(self.camera_frame, text="Camera")
        self.tab_controller.add(self.skeleton_frame, text="skeleton")


class GUI:
    def __init__(self, master, queue, endCommand):
        self.master = master
        self.queue = queue
        self.results = None
        self.model = None
        self.model_path = None
        self.results_to_model = []
        # self.results_to_model_arr = None

        # tkinter part
        self.top_view = Top_view(self.master)
        self.top_view.label.pack(anchor="nw")
        self.top_view.load_model_button["command"] = self.load_model
        # self.top_view.frame.pack()
        self.camera_display = Camera_skeleton_display(self.master)
        self.camera_display.tab_controller.pack(side="left")
        self.left_display = Graph_view(self.master)
        self.left_display.joint_combobox.pack(side="left", anchor="ne")
        self.camera_display.pack(side=tk.LEFT)
        self.left_display.graph.canvas.get_tk_widget().pack(side="bottom", ipadx=20)
        self.left_display.pack(side=tk.LEFT)
        self._gesture_names = ["Grab", "Tap", "Expand", "Pinch", "Rotation CW", "Rotation CCW", "Swipe Right",
                               "Swipe Left", "Swipe Up", "Swipe Down", "Swipe X", "Swipe V", "Swipe +", "Shake"]

        self.x_data_time = []
        self._results_to_graph = None
        self.display_id = 0
        self.frame_counter = 0

        # adding event when cumbobox is clicked
        self.left_display.joint_combobox.bind('<<ComboboxSelected>>', self.graph_changed)

    def process_incoming(self):
        while self.queue.qsize():
            try:
                (image_data, self.results) = self.queue.get(0)
                imgtk = ImageTk.PhotoImage(image=Image.fromarray(image_data))
                self.camera_display.camera_view.camera_label.imgtk = imgtk
                self.camera_display.camera_view.camera_label.configure(image=imgtk)
            except queue.Empty:
                pass

    def process_data_to_graph(self):
        try:
            result = self.results.right_hand_landmarks.landmark[self.display_id]
            graphs.x_data.append(result.x)
            graphs.y_data.append(result.y)
            graphs.z_data.append(result.z)
            graphs.time_data.append(datetime.datetime.now().strftime('%H:%M:%S.%f'))

            graphs.x_data = graphs.x_data[-20:]
            graphs.y_data = graphs.y_data[-20:]
            graphs.z_data = graphs.z_data[-20:]
            graphs.time_data = graphs.time_data[-20:]

            self._results_to_graph = {
                "x": result.x,
                "y": result.y,
                "z": result.z
            }

        except AttributeError:
            pass

    def graph_changed(self, event):
        self.display_id = self.left_display.joint_combobox_values.index(self.left_display.joint_combobox.get())

    def process_data_to_skeleton(self):
        try:

            frame_coordinates = []
            frame_to_model = []
            # self.frame_counter += 1
            for results in self.results.right_hand_landmarks.landmark:
                temp_ = [results.x, results.y, results.z]
                frame_to_model.append(results.x)
                frame_to_model.append(results.y)
                frame_to_model.append(results.z)
                frame_coordinates.append(np.array(temp_))
            frame_coordinates = np.array(frame_coordinates)
            frame_to_model = np.array(frame_to_model)
            graphs.x_skeleton_coordinate = frame_coordinates[:, 0] * 1000
            graphs.y_skeleton_coordinate = frame_coordinates[:, 1] * 1000
            graphs. z_skeleton_coordinate = frame_coordinates[:, 2] * 1000

            self.results_to_model.append(frame_to_model)
            self.frame_counter = len(self.results_to_model)

        except AttributeError:
            pass

    def load_model(self):
        self.model_path = filedialog.askopenfilename(title="Select a file",
                                                     filetype=(("h5", "*.h5"), ("hdf5", "*.hdf5")))
        # add here loading model
        # self.model = LSTM_model(self.model_path)

    def check_and_predict(self):
        if self.frame_counter == 30 and self.model is not None:
            try:
                input_data = np.array(self.results_to_model.copy())
                print(input_data.shape)
                input_data = np.expand_dims(input_data, axis=0)
                print(input_data.shape)
                # prediction = self.model.make_prediction(input_data)
                # prediction = np.argmax(prediction, axis=1).tolist()
                # print(prediction)
            except Exception as e:
                raise f"Can not load data into model some exception occurred {e}"
            self.frame_counter = 0
            self.results_to_model = []

        else:
            pass

    @staticmethod
    def reset_graph():
        # clear axies and data
        global x_data, y_data, z_data, time_data
        x_data = []
        y_data = []
        z_data = []
        time_data = []
        ax1.clear()
        ax2.clear()
        ax3.clear()

    @property
    def frame_counter(self):
        return self._frame_counter

    @frame_counter.setter
    def frame_counter(self, value):
        self._frame_counter = value
        # print()
        # print("appended to results_to_model")
        self.check_and_predict()

    @property
    def display_id(self):
        return self._display_id

    @display_id.setter
    def display_id(self, value):
        self._display_id = value
        if hasattr(self, "results"):
            GUI.reset_graph()
            self.process_data_to_graph()
            # self.process_data_to_model()

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        self._results = value
        self.process_data_to_graph()
        self.process_data_to_skeleton()
