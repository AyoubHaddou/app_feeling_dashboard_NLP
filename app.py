from matplotlib import image
from pandas import DataFrame
import streamlit as st
import streamlit_authenticator as stauth 




st.header('BALBOA COACHING')
st.image ('motivation.jpeg')
st.write ('"Toi, moi, personne ne frappe aussi fort que la vie"')

names = ['John Smith','Rebecca Briggs']
usernames = ['jsmith','rbriggs']
passwords = ['123','456']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login','main')

## https://towardsdatascience.com/how-to-add-a-user-authentication-service-in-streamlit-a8b93bf02031 : authentification 





st.sidebar.image('profil.jpeg')
st.sidebar.text('Nom : Balboa')
st.sidebar.text('Prénom : Rocky')
st.sidebar.text('Statut : Coach')
st.sidebar.selectbox('Que souhaitez vous faire ?', ['Suivis patient', 'Gestion clientèle', 'Statistique générale'])

st.header('BALBOA COACHING')
st.image ('motivation.jpeg')
st.write ('"Toi, moi, personne ne frappe aussi fort que la vie"')

 
st.sidebar.image('creed.jpg')
st.sidebar.text('Nom : Creed')
st.sidebar.text('Prénom : Apollo')
st.sidebar.text('Statut : Patient')
selection = st.sidebar.selectbox('Que souhaitez vous faire ?', ['Rédiger votre texte du jour', 'Modifier votre texte du jour', 'Consulter vos texte', 'Consulter vos progressions'])

if selection == 'Rédiger votre texte du jour':
    WordOfDay = st.text_area('Ecrivez votre texte du jour :')

if selection == 'Modifier votre texte du jour':
    st.text('mr')

if selection == 'Consulter vos texte':
    st.text('hxa')

if selection == 'Consulter vos progressions':
    st.text('zfoczd')
