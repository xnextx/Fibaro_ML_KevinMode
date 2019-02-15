import datetime

from flask import Flask, request
from sklearn.externals import joblib
import json
import sys

from train import Training

app = Flask(__name__)


@app.route('/get_lights', methods=['GET', 'POST'])
def get_lights():
    desired_lights = request.args.get('lights').split(",")
    result = {}
    today = datetime.datetime.today()
    minutes_after_midnight = (today.hour * 60) + today.month

    for light_id in desired_lights:
        try:
            rf = joblib.load(f"models/lights_model_{light_id}")
            pred = rf.predict([[minutes_after_midnight, today.month, today.weekday()]])
            result[light_id] = int(pred[0])
        except:
            result[light_id] = "ERROR"
            print("The Light of this ID does not exist : ", sys.exc_info())

    return json.dumps(result)


@app.route('/start_train', methods=['GET'])
def train():
    training = Training()
    training.start()

    return training.get_results()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
