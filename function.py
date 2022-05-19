import requests
import matplotlib.pyplot as plt
import pandas as pd 

def predict_data(data):

    response = requests.post(f"http://0.0.0.0:8080/predict/?Data={data}")
    return response.text

def plot_graph(data):

    data = pd.DataFrame({'emotion_predicted' : 0, 'time' : 1, 'emotion_predicted' : 1, 'time' : 2})
    plt.plot(data)
    plt.title("Evolution du patient")
    plt.axis('equal')
    plt.show()
