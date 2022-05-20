import requests
import matplotlib.pyplot as plt
import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

def predict_data(data):

    response = requests.post(f"http://0.0.0.0:8080/predict/?Data={data}")
    return response.text


def make_engine_session():
    engine = create_engine('sqlite:///feeling_db.sqlite3?check_same_thread=False')
    Session = sessionmaker(bind=engine)

    return Session()

def emotion_int(result):
    if result == '"sadness"' :
        return 0
    elif result == '"anger"' :
        return 1
    elif result == '"love"' :
        return 2
    elif result == '"surprise"' :
        return 3
    elif result == '"fear"' :
        return 4
    elif result == '"happy"' :
        return 5