from matplotlib import image
from pandas import DataFrame
import streamlit as st
import streamlit_authenticator as stauth 
from .database import day_text


## Home 

#col1, col2, col3 = st.columns(3)

#with col2:
#    st.image('coach.gif')

#names = ['John Smith','Rebecca Briggs']
#usernames = ['jsmith','rbriggs']
#passwords = ['123','456']

#hashed_passwords = stauth.Hasher(passwords).generate()

#authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
#    'some_cookie_name','some_signature_key',cookie_expiry_days=30)

#name, authentication_status, username = authenticator.login('Login','main')

#st.markdown('by M.Zen coaching ')



### Admin 

#st.sidebar.text('Nom : Balboa')
#st.sidebar.text('Prénom : Rocky')
#st.sidebar.selectbox('Que souhaitez vous faire ?', ['Suivis patient', 'Gestion clientèle', 'Statistique générale'])

#col1, col2, col3 = st.columns(3)

#with col2:
#    st.image ('motivation.jpeg')



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
    if button :
        day_text(WordOfDay)
if selection == 'Modifier votre texte du jour':
    WordOfDay = st.text_area('Ecrivez votre texte du jour :')
    st.button('Publier')

if selection == 'Consulter vos texte':
    st.text('hxa')

if selection == 'Consulter vos progressions':
    st.text('zfoczd')
