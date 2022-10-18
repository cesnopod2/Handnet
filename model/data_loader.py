import tensorflow as tf
import numpy as np
import os
import pandas as pd

class Hand_dataset_2():
    def __init__(self, processing_type="clean_data"):
        self.data = None
        self.save_path = r"C:\HandNET\data"
        self.data_path = r"C:\HandNET\data\LSTM_data_point_position_features.npy"
        self.info_df = pd.read_pickle(r"C:\HandNET\data\paths_start_stop_label.pkl")
        self.labels = tf.keras.utils.to_categorical(self.info_df["label"].tolist(), num_classes=14).astype(int)
        self.processing_type = processing_type
        self.filename = "LSTM_data_" + self.processing_type + ".npy"
        self.data_path = os.path.join("C:\HandNET\data\LSTM_data", self.filename)

    def get_item(self):
        if not os.path.exists(self.data_path):
            print("file does not exist")
            self.data = self.process()
        else:
            print("file exists, data has been loaded")
            self.data = np.load(self.data_path)
        return self.data, self.labels

    def process(self):

        data = []
        for index in range(0, self.info_df.shape[0]):
            data.append(self.create_gesture_dataframe(self.info_df["path"][index], self.info_df["start_frame"][index],
                                                      self.info_df["stop_frame"][index]))
        print(data[0].shape)
        print("saving data ...")
        final_data = np.array(data)
        np.save(self.data_path, final_data)
        print("data saved.")
        return final_data

    def create_gesture_dataframe(self, path, start_id, stop_id):
        lines = []
        full_gesture = []
        file = open(path, "r")
        for pos, l_num in enumerate(file):

            if start_id <= pos <= stop_id:
                lines.append(l_num)

        for line in lines:
            x = line.split()
            x = list(map(float, x))
            frame_gesture = np.array(x)
            # this is added to adjust data to mediapipe data

            frame_gesture = Hand_dataset_2.change_data_order(frame_gesture)
            # frame_gesture = Hand_dataset_2.normalize_data(frame_gesture)

            frame_gesture = Hand_dataset_2.wrist_reference(frame_gesture)

            full_gesture.append(frame_gesture)

        return Hand_dataset_2.preprocess_data(full_gesture)

    @staticmethod
    def change_data_order(data):
        #         print(f"data shape is : {data.shape}")
        output = np.zeros((63,))
        #         print(output.shape)
        for i in range(0, 63, 21):
            output[0 + i] = data[0 + i]
            output[1 + i] = data[18 + i]
            output[2 + i] = data[19 + i]
            output[3 + i] = data[20 + i]
            output[4 + i] = data[21 + i]
            output[5 + i] = data[14 + i]
            output[6 + i] = data[15 + i]
            output[7 + i] = data[16 + i]
            output[8 + i] = data[17 + i]
            output[9 + i] = data[10 + i]
            output[10 + i] = data[11 + i]
            output[11 + i] = data[12 + i]
            output[12 + i] = data[13 + i]
            output[13 + i] = data[6 + i]
            output[14 + i] = data[7 + i]
            output[15 + i] = data[8 + i]
            output[16 + i] = data[9 + i]
            output[17 + i] = data[1 + i]
            output[18 + i] = data[2 + i]
            output[19 + i] = data[3 + i]
            output[20 + i] = data[4 + i]
        return output

    @staticmethod
    def normalize_data(data):

        processed_data = data / 100
        return processed_data

    @staticmethod
    def wrist_reference(data):
        wrist_data_x = data[0]
        wrist_data_y = data[1]
        wrist_data_z = data[2]

        for i in range(0,63,3):
            data[i] = data[i] - wrist_data_x
            data[i+1] = data[i+1] - wrist_data_y
            data[i+2] = data[i+2] - wrist_data_z

        return data


    @staticmethod
    def preprocess_data(data):

        blank_frame = np.zeros_like(data[0])
        data_len = len(data)
        if data_len > 30:
            data = data[:30]  # check if not 49 index
        else:
            x = (30 - data_len)
            padding = x // 2
            adding = 0
            for i in range(0, padding):
                data.insert(0, blank_frame)
                data.insert(-1, blank_frame)

            if x % 2 == 1:
                data.insert(-1, blank_frame)
            else:
                pass

        return np.array(data)


gestures, labels = Hand_dataset_2("clean_data_mediapipe_test").get_item()

