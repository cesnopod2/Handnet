from tensorflow import keras
import glob
import os
import json


class LSTM_model:
    def __init__(self, filename):
        self.model = keras.models.load_model(filename)
        self.filename = os.path.split(filename)[-1]
        self.filename = self.filename[:self.filename.index(".")]
        self.json_data = None

    def make_prediction(self, data):
        return self.model.predict(data)

    def get_model_information(self, filepath=r"C:\Handnet_git\model\model_info"):
        file_name = self.filename + ".json"
        json_path = os.path.join(filepath, file_name)
        if os.path.exists(json_path):
            f = open(json_path)
            self.json_data = json.load(f)
        return self.json_data