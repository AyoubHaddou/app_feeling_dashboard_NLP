import requests

def predict_data(data):

    response = requests.post(f"http://0.0.0.0:8080/predict/?Data={data}")
    return response.text
