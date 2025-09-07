from flask import Flask, request
from flask_cors import CORS

import os
import json
import pickle
import numpy as np
import statistics

from datetime import date

app = Flask(__name__)

cors = CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

# Loading all Crop Recommendation Models
crop_xgb_pipeline = pickle.load(
    open("./models/xgb_c.pkl", "rb")
)
crop_rf_pipeline = pickle.load(
    open("./models/rf_c.pkl", "rb")
)
crop_knn_pipeline = pickle.load(
    open("./models/knn_c.pkl", "rb")
)
crop_label_dict = pickle.load(
    open("./models/label_dict.pkl", "rb")
)

def convert(o):
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError

def set_digital_signature(data_dict):
    data_dict['Creator'] = "Chinmay Shivratriwar"
    data_dict['Linkedin'] = "https://www.linkedin.com/in/chinmay-shivratriwar-69560a193"
    data_dict['Date of Request'] = str(date.today())
    return data_dict

def crop_prediction(input_data):
    prediction_data = {
        "xgb_crop_prediction": crop_label_dict[
            crop_xgb_pipeline.predict(input_data)[0]
        ],
        "xgb_crop_probability": max(crop_xgb_pipeline.predict_proba(input_data)[0])
        * 100,
        "rf_crop_prediction": crop_label_dict[crop_rf_pipeline.predict(input_data)[0]],
        "rf_crop_probability": max(crop_rf_pipeline.predict_proba(input_data)[0])
        * 100,
        "knn_crop_prediction": crop_label_dict[
            crop_knn_pipeline.predict(input_data)[0]
        ],
        "knn_crop_probability": max(crop_knn_pipeline.predict_proba(input_data)[0])
        * 100,
    }

    all_predictions = [
            prediction_data["xgb_crop_prediction"],
            prediction_data["rf_crop_prediction"],
            prediction_data["knn_crop_prediction"],
        ]

    all_probs = [
            prediction_data["xgb_crop_probability"],
            prediction_data["rf_crop_probability"],
            prediction_data["knn_crop_probability"],
        ]

    if len(set(all_predictions)) == len(all_predictions):
        prediction_data["final_prediction"] = all_predictions[all_probs.index(max(all_probs))]
    else:
        prediction_data["final_prediction"] = statistics.mode(all_predictions)


    prediction_data = set_digital_signature(prediction_data)
    return prediction_data

@app.route("/predict_crop", methods=["GET", "POST"])
def predictcrop():
    try:
        if request.method == "POST":
            form_values = request.json
            column_names = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
            input_data = np.asarray([float(form_values[i].strip()) for i in column_names]).reshape(
                1, -1
            )
            prediction_data = crop_prediction(input_data)
            json_obj = json.dumps(prediction_data, default=convert)
            return json_obj
    except:
        return json.dumps({"error":"Please Enter Valid Data"}, default=convert)



if __name__ == "__main__":

    app.run(debug=True)
