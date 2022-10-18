from graphs import figure_skeleton
import graphs
from graphs import ax1, ax2, ax3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import cv2 as cv
import numpy as np
from PIL import ImageTk, Image
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import queue
import datetime
from graph_view import Graph_view
from data_collector import DataCollector, GUI_DataCollector
from model.model import LSTM_model


class Top_view:
    def __init__(self, master):
        self.master = master
        self.top_frame = tk.Frame(self.master)
        self.label = tk.Label(self.top_frame)
        self.label["text"] = "HandNET"
        self.label.config(font=("Courier", 44))
        self.load_model_button = tk.Button(self.top_frame, text="Load model")
        self.label.pack(side="left")
        self.load_model_button.pack(side="left", padx=20, pady=40)
        self.model_path = None
        self.top_frame.pack()


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
        self.canvas.get_tk_widget().pack()


class Camera_skeleton_display(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.main_frame = tk.Frame(self.master)
        self.tab_controller = ttk.Notebook()
        self.camera_frame = ttk.Frame(self.tab_controller, width=660, height=460)
        self.skeleton_frame = ttk.Frame(self.tab_controller, width=660, height=460)
        self.camera_view = Camera_display(self.camera_frame)
        self.camera_frame.pack()
        self.skeleton_frame.pack()
        self.skeleton_view = Skeleton_display(self.skeleton_frame)
        self.tab_controller.add(self.camera_frame, text="Camera")
        self.tab_controller.add(self.skeleton_frame, text="skeleton")
        self.tab_controller.pack(side="left", anchor="nw")


class Graph_model_data(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.main_frame = tk.PanedWindow(self.master)
        self.tab_controller = ttk.Notebook()
        self.graph_frame = ttk.Frame(self.tab_controller, width=660, height=460)
        self.model_evaluation_frame = ttk.Frame(self.tab_controller, width=660, height=460)
        self.data_collector_frame = ttk.Frame(self.tab_controller, width=660, height=460)
        self.graph_view = Graph_view(self.graph_frame)
        self.graph_frame.pack()
        self.model_evaluation_frame.pack()
        self.data_collector_frame.pack()
        self.model_display = Model_evaluation_display(self.model_evaluation_frame)
        self.data_collector_view = DataCollectorDisplay(self.data_collector_frame)
        self.tab_controller.add(self.graph_frame, text="Join coordinates")
        self.tab_controller.add(self.model_evaluation_frame, text="Model information")
        self.tab_controller.add(self.data_collector_frame, text="Add gesture")
        self.tab_controller.pack()


class Model_evaluation_display(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.graph_label = tk.Label(self.master)

        imgtk = ImageTk.PhotoImage(
            image=Image.fromarray(cv.imread(r"C:\Handnet_git\model\model_info\graph unavailable.png")))
        self.graph_label.imgtk = imgtk
        self.graph_label.configure(image=imgtk)

        self.accuracy_str = tk.StringVar()
        self.precision_str = tk.StringVar()
        self.recall_str = tk.StringVar()
        self.f1_str = tk.StringVar()

        self.accuracy_label = tk.Label(self.master, textvariable=self.accuracy_str)
        self.precision_label = tk.Label(self.master, textvariable=self.precision_str)
        self.recall_label = tk.Label(self.master, textvariable=self.recall_str)
        self.F1_label = tk.Label(self.master, textvariable=self.f1_str)
        self.accuracy_label.pack()
        self.precision_label.pack()
        self.recall_label.pack()
        self.F1_label.pack()
        self.graph_label.pack()

    def update_data(self, info):
        # self.accuracy_str.set(f" Accuracy : {info['accuracy']}")
        # self.precision_str.set(f" Precision : {info['precision']}")
        # self.recall_str.set(f" Recall : {info['recall']}")
        # self.f1_str.set(f" F1 score : {info['F1_score']}")
        #
        # imgtk = ImageTk.PhotoImage(
        #     image=Image.fromarray(cv.imread(info["graph_path"])))
        # self.graph_label.imgtk = imgtk
        # self.graph_label.configure(image=imgtk)

        if info is not None:
            self.accuracy_str.set(f" Accuracy : {info['accuracy']}")
            self.precision_str.set(f" Precision : {info['precision']}")
            self.recall_str.set(f" Recall : {info['recall']}")
            self.f1_str.set(f" F1 score : {info['F1_score']}")

            imgtk = ImageTk.PhotoImage(
                image=Image.fromarray(cv.imread(info["graph_path"])))
            self.graph_label.imgtk = imgtk
            self.graph_label.configure(image=imgtk)
        else:
            messagebox.showinfo("Info", "Model successfully loaded, but information"
                                        " about model can not be uploaded")


class DataCollectorDisplay(ttk.Frame):
    def __init__(self, master):
        self.master = master
        self.gui_data_collector = GUI_DataCollector(self.master)
        self.gui_data_collector.gesture_label.pack()
        self.gui_data_collector.gesture_widget.pack()
        self.gui_data_collector.person_label.pack()
        self.gui_data_collector.person_widget.pack()
        self.gui_data_collector.frame_amount_label.pack()
        self.gui_data_collector.submit_button.pack()
        self.gui_data_collector.frame_amount_label.pack()


class GUI:
    def __init__(self, master, queue, endCommand):
        self.master = master
        self.queue = queue
        self.master.title("HandNET")
        self.master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth(), master.winfo_screenheight()))
        self.statusbar = tk.Frame(self.master, background="#d5e8d4", height=80)
        self.result_frame = tk.Frame(self.master)
        self.main_window = tk.PanedWindow(self.master)

        self.gesture_output = tk.StringVar()
        self.gesture_label = tk.Label(self.result_frame,
                                      textvariable=self.gesture_output)

        self.gesture_label.config(font=("Courier",25))

        self.gesture_label.pack(padx=200)
        self.statusbar.pack(side="bottom", fill="x")
        self.result_frame.pack(side="bottom")

        self.main_window.pack(side="top")
        self.collect_data_logic = False
        self.results = None
        self.model = None
        self.model_path = None
        self.results_to_model = []
        # self.results_to_model_arr = None

        # tkinter part
        self.top_view = Top_view(self.master)
        self.top_view.top_frame.pack()
        # self.main_window.add(self.top_view.top_frame)
        self.camera_display = Camera_skeleton_display(self.main_window)
        self.left_display = Graph_model_data(self.main_window)

        # self.statusbar = tk.Frame(self.master, background="#d5e8d4", height=200)
        # self.statusbar.pack(side="bottom")
        # self.top_view.label.pack(anchor="nw")

        self.main_window.add(self.camera_display.main_frame)
        self.main_window.add(self.left_display.main_frame)
        self.top_view.load_model_button["command"] = self.load_model
        # self.top_view.frame.pack()

        # self.left_display = Graph_view(self.master)

        # self.left_display.tab_controller.pack()
        # self.left_display.graph_view.joint_combobox.pack(side="left", anchor="ne")
        self.camera_display.pack(side=tk.LEFT)
        self.left_display.graph_view.graph.canvas.get_tk_widget().pack(side="bottom", ipadx=20)
        self.left_display.pack(side=tk.LEFT)
        self._gesture_names = ["Zoom", "Swipe right", "Swipe left", "Swipe up", "Swipe down", "Rotate X", "Rotate Y",
                               "Pinch", "Expand"]

        # self.gesture_output = tk.StringVar()
        # self.gesture_label = tk.Label(self.statusbar,
        #                               textvariable=self.gesture_output)
        # self.gesture_label.config(font=("Courier", ))

        self.gesture_label.pack(side="bottom")

        self.left_display.data_collector_view.gui_data_collector.submit_button["command"] = self.create_folders

        self.data_collect_list = []
        self._results_to_graph = None
        self.display_id = 0
        self.frame_counter = 0

        self.data_collector = DataCollector()
        self.collector_frame_counter = 0
        # adding event when cumbobox is clicked
        self.left_display.graph_view.joint_combobox.bind('<<ComboboxSelected>>', self.graph_changed)

        # adding event when x on keyboard is clicked
        self.mistery_button = tk.Button(command=self.start_collecting_data)
        self.master.bind('<x>', self.start_collecting_data)
        self.master.bind('<c>', self.disable_collecting_data)

    def create_folders(self):
        self.data_collector.gesture_name = self.left_display.data_collector_view.gui_data_collector.gesutre_name.get()
        self.data_collector.person_name = self.left_display.data_collector_view.gui_data_collector.person_name.get()

    def start_collecting_data(self, event):
        self.collect_data_logic = True

    def disable_collecting_data(self, event):
        self.collect_data_logic = False
        self.data_collector.save_data(np.array(self.data_collect_list))
        self.data_collect_list = []
        self.collector_frame_counter = 0

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
        self.display_id = self.left_display.graph_view.joint_combobox_values.index(
            self.left_display.graph_view.joint_combobox.get())
        GUI.reset_graph()

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
            graphs.z_skeleton_coordinate = frame_coordinates[:, 2] * 1000

            self.results_to_model.append(frame_to_model)
            self.frame_counter = len(self.results_to_model)

        except AttributeError:
            pass

    def load_model(self):
        self.model_path = filedialog.askopenfilename(title="Select a file",
                                                     filetype=(("h5", "*.h5"), ("hdf5", "*.hdf5")))
        # add here loading model
        self.model = LSTM_model(self.model_path)
        self.left_display.model_display.update_data(self.model.get_model_information())

    def check_and_predict(self):
        if self.frame_counter == 30 and self.model is not None:
            try:
                input_data = np.array(self.results_to_model.copy())
                # print(input_data.shape)
                input_data = np.expand_dims(input_data, axis=0)
                # print(input_data.shape)
                prediction = self.model.make_prediction(input_data)
                print(f" clean prediction values :{prediction}")
                prediction = np.argmax(prediction, axis=1).tolist()

                print(self._gesture_names[prediction[0]])
                self.gesture_output.set(self._gesture_names[prediction[0]])
            except Exception as e:
                raise f"Can not load data into model some exception occurred {e}"
        elif self.frame_counter > 50:
            self.frame_counter = 0
            self.results_to_model = []

        else:
            pass

    def collect_data(self):
        try:
            if self.collect_data_logic:
                resource = []
                for res in self.results.right_hand_landmarks.landmark:
                    resource = resource + [res.x, res.y, res.z]
                self.data_collect_list.append(resource)
        except AttributeError:
            pass

    def update_frame_counter_info(self):
        if self.collector_frame_counter > 30:
            print("stop collecting data :D")

        # self.gui_data_collector.frame_amount_label["text"] = str(self.collector_frame_counter)

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
    def collector_frame_counter(self):
        return self._collector_frame_counter

    @collector_frame_counter.setter
    def collector_frame_counter(self, value):
        self._collector_frame_counter = value
        self.update_frame_counter_info()

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

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        self._results = value
        self.process_data_to_graph()
        self.process_data_to_skeleton()
        self.collect_data()
