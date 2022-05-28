import requests
import matplotlib.pyplot as plt
import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

async def predict_data(data):

    response = await requests.post(url=f"https://coach-life.herokuapp.com/predict/?data={data}")
    return response.text


def make_engine_session():
    engine = create_engine('sqlite:///db/feeling_db.sqlite3?check_same_thread=False')
    Session = sessionmaker(bind=engine)
    return Session()

def emotion_int(df):
    df['emotion_int'] = -1
    df.loc['"sadness"', 'emotion_int'] =  0
    df.loc['"anger"', 'emotion_int'] =  1
    df.loc['"love"', 'emotion_int'] =  2
    df.loc['"surprise"', 'emotion_int'] =  3
    df.loc['"happy"', 'emotion_int'] =  4
    return df 



def df_all(Text, User):
    sess = make_engine_session()
    data_text = []
    user_text = sess.query(Text).all()
    for text in user_text:
        data_text.append({'emotion_predicted' : text.emotion_predicted, 'texte' : text.content, 'time' : text.time_created, 'user_id' : text.user_id})
    df_text = pd.DataFrame(data_text)

    data = []
    users = sess.query(User).filter_by(is_coach=False).all()
    if users :
        for user in users :
            data.append({'id' : user.id, 'name' : user.name, 'username' : user.username })
        # st.dataframe(data_content, data_emotion)
        df_patient = pd.DataFrame(data)

    df_test = df_patient.merge(df_text, left_on=['id'], right_on=["user_id"], how='outer')
    df_test.time = df_test.time.apply(lambda x : str(x)[0:10])
    return df_test

