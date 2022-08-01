import queue
from view import GUI
import mediapipe as mp
import cv2 as cv
import threading
import sys
import tkinter as tk

from graphs import animate_skeleton, animate_data
import matplotlib.animation as animation
from graphs import figure, figure_skeleton

class ThreadCamera:
    def __init__(self, master):
        self.master = master
        self.queue = queue.Queue()
        self.gui = GUI(master, self.queue, self.end_application)

        self.running = True

        self.camera = cv.VideoCapture(0)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        self.results = None

        # defining camera thread
        self.camera_thread = threading.Thread(target=self.worker_camera_thread)
        self.camera_thread.start()

        self.periodic_call()

    def periodic_call(self):
        self.gui.process_incoming()
        if not self.running:
            sys.exit()

        self.master.after(20, self.periodic_call)

    def worker_camera_thread(self):
        with self.mp_holistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7) as holistic:
            while self.running:
                _, frame = self.camera.read()
                results = holistic.process(frame)
                image = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

                self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks,
                                               self.mp_holistic.HAND_CONNECTIONS)

                self.results = results.right_hand_landmarks
                image = cv.flip(image, 1)
                data = (image, results)
                self.queue.put(data)

    def end_application(self):
        self.camera.release()
        self.running = False



if __name__ == "__main__":
    root = tk.Tk()
    N = 10
    app = ThreadCamera(root)
    ani_coordinates = animation.FuncAnimation(figure, animate_data, interval=1000)
    ani_skeleton = animation.FuncAnimation(figure_skeleton, animate_skeleton, interval=100)
    root.mainloop()