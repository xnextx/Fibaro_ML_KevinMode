import datetime
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sklearn.externals import joblib
import json
import sys
import os
from train import Training

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)


class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lightId = db.Column(db.Integer(), unique=False, nullable=False)
    state = db.Column(db.Integer(), unique=False, nullable=False)
    timestamp = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Light %r>' % self.lightId


@app.route('/get_lights', methods=['GET'])
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


@app.route('/add_new_sample', methods=['POST'])
def add_new_sample():
    if not request.json:
        abort(400)
    data = request.data
    dataDict = json.loads(data)

    light = Light()
    light.lightId = dataDict['lightId']
    light.state = dataDict['state']
    light.timestamp = dataDict['timestamp']
    db.session.add(light)
    db.session.commit()
    return "OK"


@app.route('/start_training', methods=['GET'])
def start_training():
    training = Training(db.session, Light)
    training.start()
    return json.dumps(training.get_results())

# @app.route('/init_db_from_csv', methods=['GET'])
# def init_db_from_csv():
#     try:
#         """Destroys and creates the database + tables."""
#         import csv
#         with open('input/fibaro_lights_extended_clean.csv', newline='') as csvfile:
#             # num_lines = sum(1 for row in csvfile)
#             reader = csv.DictReader(csvfile)
#             count = sum(1 for _ in reader)
#             csvfile.seek(0)
#             reader = csv.DictReader(csvfile)
#             i = 0
#             for row in reader:
#                 i += 1
#                 print(f"Processing {i}/{count}")
#                 # if i > 2000:
#                 #     break
#
#                 light = Light()
#                 light.lightId = row['lightID']
#                 light.state = 1 if row['state'] == 'on' else 0
#                 light.timestamp = row['timestamp']
#                 db.session.add(light)
#             db.session.commit()
#
#         return '<h1>Success.</h1>'
#     except:
#         print(sys.exc_info())
#         return '<h1>Something is broken.</h1>'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')
