from sklearn.externals import joblib
import numpy as np
import matplotlib.pyplot as plt
from utils import mins_to_dhms
plt.rcdefaults()


light_id = 117
month = 12
week_map = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

try:
    rf = joblib.load(f"models/lights_model_{light_id}")
    for day in range(0, 7):
        objects = []
        performance = []
        for minute in range(0, 1440):
            if minute % 30 == 0:
                pred = rf.predict([[minute, month, day]])
                objects.append(mins_to_dhms(minute))
                performance.append(pred[0])
        # print(pred)

        y_pos = np.arange(len(objects))
        fig_size = plt.rcParams["figure.figsize"]
        fig_size[0] = 25
        fig_size[1] = 5
        plt.rcParams["figure.figsize"] = fig_size
        plt.bar(y_pos, performance, align='center', width=0.1, alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Value')
        plt.title(f"ID:{light_id} - {week_map[day]}")

        plt.show()


except Exception as e:
    print("The Light of this ID does not exist.")

