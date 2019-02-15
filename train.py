# -*-coding:utf-8-*-
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from utils import timestamp_to_minutes_after_midnight

pd.options.mode.chained_assignment = None


class Validator(object):
    def __init__(self):
        self.min_accuracy = 51
        self.min_count_of_samples = 2

    def count_of_samples_are_ok(self, count):
        if count >= self.min_count_of_samples:
            return True
        else:
            return False

    def accuracy_is_ok(self, accuracy):
        if accuracy > self.min_accuracy:
            return True
        else:
            return False


class Training(object):
    def __init__(self, session, Light):

        # self.data = pd.read_csv("input/fibaro_lights_extended_clean.csv")
        self.data = pd.read_sql(session.query(Light).statement, session.bind)
        self.data["datetime"] = pd.to_datetime(self.data['timestamp'], unit='s')
        self.data["minutes after midnight"] = [timestamp_to_minutes_after_midnight(time.time()) for time in self.data['datetime']]
        self.data["day of week"] = self.data["datetime"].dt.dayofweek
        self.data["month"] = self.data["datetime"].dt.month
        self.available_lights = self.data["lightId"].drop_duplicates()
        self.result_info = {}
        # print(self.data.head())

    def get_results(self):
        return self.result_info

    def start(self):
        validate = Validator()
        i = 0
        for light_id in self.available_lights:
            i += 1
            print(f"[Training]{i}/{self.available_lights.__len__()} | Processing lightID:{light_id}")
            # if i == 8:
            #     break
            cur_light_data = self.data[self.data["lightId"] == light_id]
            samples_count = cur_light_data.__len__()
            if not validate.count_of_samples_are_ok(samples_count):
                self.result_info[light_id] = {"success": False, "samples": {samples_count}, "accuracy": None, "msg": "insufficient samples"}
                continue

            data_inputs = cur_light_data[["minutes after midnight", "month", "day of week"]]
            expected_output = cur_light_data[["state"]]
            # expected_output["state"] = np.where(expected_output["state"] == "off", 0, 1)

            inputs_train, inputs_test, expected_output_train, expected_output_test = train_test_split(data_inputs, expected_output, test_size=0.33, random_state=42)

            rf = RandomForestClassifier(n_estimators=100)
            # rf = RandomForestClassifier(n_estimators=100, bootstrap=True, max_features=None, max_depth=5, criterion='gini', min_samples_leaf=1, min_samples_split=2)
            rf.fit(inputs_train, expected_output_train.values.ravel())

            accuracy = round(rf.score(inputs_test, expected_output_test) * 100, 1)
            if not validate.accuracy_is_ok(accuracy):
                self.result_info[light_id] = {"success": False, "samples": samples_count, "accuracy": accuracy, "msg": "insufficient accuracy"}
                continue

            self.result_info[light_id] = {"success": True, "samples": samples_count, "accuracy": accuracy, "msg": ""}
            joblib.dump(rf, f"models/lights_model_{light_id}", compress=9)

# training = Training()
# # training.start()
# # print(training.get_results())
