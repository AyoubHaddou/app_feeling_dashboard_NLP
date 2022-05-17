from pandas import DataFrame
from pyparsing import Word
import streamlit as st
import streamlit_authenticator as stauth 
from models import Coach, Patient, Text
import numpy as np 
import datetime 

from sqlalchemy.orm import sessionmaker , column_property
from sqlalchemy import create_engine , update 

from sqlalchemy.sql import select, func 

engine = create_engine('sqlite:///feeling_db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()



## Home 

col1, col2, col3 = st.columns(3)

coach_all = sess.query(Coach).all()
patient_all = sess.query(Patient).all()

names_all = []
usernames_all = []
password_all = []

for coach, patient in zip(coach_all, patient_all):
    coach_name = coach.name
    patient_name = patient.name
    names_all.append(coach_name)
    names_all.append(patient_name)
    usernames_all.append(coach.username)
    usernames_all.append(patient.username)
    password_all.append(coach.password)
    password_all.append(patient.password)


hashed_passwords = stauth.Hasher(password_all).generate()

authenticator = stauth.Authenticate(names_all,usernames_all, hashed_passwords,
   'some_cookie_name','some_signature_key',cookie_expiry_days=0)

name, authentication_status, username = authenticator.login('Login','main')




if st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')
    st.sidebar.text('Please login')
    st.sidebar.text('Free demo account : \nUsername : jsmith \nPassword : 123')
    st.warning('Please enter your username and password')
    with col2:
        st.image('coach.gif')


elif st.session_state['authentication_status'] == None:
    st.sidebar.text('Please login')
    st.sidebar.text('Free demo account : \nUsername : jsmith \nPassword : 123')
    st.warning('Please enter your username and password')
    with col2:
        st.image('coach.gif')


if st.session_state['authentication_status']:
    st.sidebar.text('Welcome *%s*' % (st.session_state['name']))

    with col2:
        st.image ('motivation.jpeg')

    selection = st.sidebar.selectbox('Que souhaitez vous faire ?', ['Rédiger votre texte du jour', 'Modifier votre texte du jour', 'Consulter vos texte', 'Consulter vos progressions'])

    if selection == 'Rédiger votre texte du jour':
        st.title('Your day text')
        WordOfDay = st.text_area('Ecrivez votre texte du jour :')
        button = st.button('Publier')
        
        if button and WordOfDay:
            
            actual_username = st.session_state['username']
            current_user = sess.query(Coach).filter_by( username = actual_username).first()
            user_text = sess.query(Text).filter_by( user_id = current_user.id).all()
            last_date = [0]
            for text in user_text :
                last_date.append(text.time_created.day)
            date = datetime.datetime.now().day
            if last_date[-1] != date:

                text = Text(content=WordOfDay, emotion_predicted="in coming", user_id=1)
                sess.add(text)
                sess.commit()
                st.balloons()
                st.success('Message du jour envoyé!')
            else:
                st.warning('Text already send today. Go to modification space if you need it')
            

    if selection == 'Modifier votre texte du jour':
        st.title('Day text modification')
    
        WordOfDay = st.text_area('Modifier votre texte du jour :')
        button = st.button('Publier')
        if button:
            sess.query(Text).filter_by(user_id = 1).update({"content" : WordOfDay}, synchronize_session="fetch")
            sess.commit()
            st.success("texte updated with success")
        
        st.write('--------------------------------')
        actual_username = st.session_state['username']
        current_user = sess.query(Coach).filter_by( username = actual_username).first()
        user_text = sess.query(Text).filter_by( user_id = current_user.id).all()


        if user_text[-1] :
            st.write('Le message du jour modifiable est le suivant :')
            st.warning(user_text[-1].content)
        else:
            st.write('Aucun texte enregistré pour le moment.')

    if selection == 'Consulter vos texte':
        liste = []
        result = sess.query(Text).all()
        if result :
            for text in result:
                liste.append({'emotion_predicted' : text.emotion_predicted, 'texte' : text.content, 'time' : text.time_created, 'modif': text.time_updated})
            # st.dataframe(liste_content, liste_emotion)
            
            st.dataframe(liste)
        else:
            st.write('Aucun texte enregistré pour le moment.')

    if selection == 'Consulter vos progressions':
        liste = []
        result = sess.query(Text).all()
        if result :
            for text in result:
                liste.append({'emotion_predicted' : text.emotion_predicted, 'texte' : text.content, 'time' : text.time_created, 'modif': text.time_updated})
            # st.dataframe(liste_content, liste_emotion)
            
            st.dataframe(liste)
            st.write('Graph are in coming. ')
        else:
            st.write('Aucun texte enregistré pour le moment.')

st.markdown('by M.Zen coaching ')
