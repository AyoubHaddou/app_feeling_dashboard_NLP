from pandas import DataFrame
from pyparsing import Word
import streamlit as st
import streamlit_authenticator as stauth 
from models import Coach, Patient, Text
import numpy as np 

from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine , update 

from sqlalchemy.sql import select, func 

engine = create_engine('sqlite:///feeling_db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()



## Home 

col1, col2, col3 = st.columns(3)

with col2:
   st.image('coach.gif')


# names = ['John Smith','Rebecca Briggs']
# usernames = ['jsmith','rbriggs']
# passwords = sess.query(Coach

# hashed_passwords = stauth.Hasher(passwords).generate()

# authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
#    'some_cookie_name','some_signature_key',cookie_expiry_days=5)

# name, authentication_status, username = authenticator.login('Login','main')

# st.markdown('by M.Zen coaching ')



## Admin 

st.sidebar.text('Nom : Balboa')
st.sidebar.text('Prénom : Rocky')
st.sidebar.selectbox('Que souhaitez vous faire ?', ['Suivis patient', 'Gestion clientèle', 'Statistique générale'])

col1, col2, col3 = st.columns(3)

with col2:
   st.image ('motivation.jpeg')



#### Client 

col1, col2, col3 = st.columns(3)

with col2:
    st.image ('motivation.jpeg')

st.sidebar.text('Nom : Creed')
st.sidebar.text('Prénom : Apollo')
selection = st.sidebar.selectbox('Que souhaitez vous faire ?', ['Rédiger votre texte du jour', 'Modifier votre texte du jour', 'Consulter vos texte', 'Consulter vos progressions'])



if selection == 'Rédiger votre texte du jour':
    WordOfDay = st.text_area('Ecrivez votre texte du jour :')
    button = st.button('Publier')
    if button and WordOfDay:
        text = Text(content=WordOfDay, emotion_predicted="in coming", user_id=1)
        sess.add(text)
        sess.commit()
        st.balloons()
        st.success('Message du jour envoyé!')
        

if selection == 'Modifier votre texte du jour':
   
    WordOfDay = st.text_area('Ecrivez votre texte du jour :')
    button = st.button('Publier')
    if button:
        sess.query(Text).filter_by(user_id = 1).filter(Text.id == sess.query(func.max(Text.id))).update({"content" : WordOfDay}, synchronize_session="fetch")
        sess.commit()
        st.success("texte updated with success")
    
    st.write('--------------------------------')
    obj = sess.query(Text).filter_by(user_id = 1).filter(Text.id == sess.query(func.max(Text.id))).first()
    if obj :
        st.write('Le message du jour encore modifiable est le suivant :')
        st.warning(obj.content)
    else:
        st.write('Aucun texte enregistré pour le moment.')

if selection == 'Consulter vos texte':
    liste = []
    result = sess.query(Text).all()
    print('MON PRINT !!!!!!!!!!!! TYPE => ', type(result))
    print('MON PRINT !!!!!!!!!!!! LEN => ', len(result))
    if result :
        for text in result:
            liste.append({'emotion_predicted' : text.emotion_predicted, 'texte' : text.content, 'time' : text.time_created, 'modif': text.time_updated})
        # st.dataframe(liste_content, liste_emotion)
        
        st.dataframe(liste)
    else:
        st.write('Aucun texte enregistré pour le moment.')

if selection == 'Consulter vos progressions':
    st.text('zfoczd')
