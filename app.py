from pandas import DataFrame
import streamlit as st
import streamlit_authenticator as stauth 

import sqlite3
from numpy import insert, reciprocal
from requests import delete


conn = sqlite3.connect('coach_db.db')
cur = conn.cursor()


# Create table statement

def create_db():
    create_script = """ CREATE TABLE utilisateur IF NOT EXIST ( 
                    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,  
                    nom VARCHAR(100), 
                    prenom VARCHAR(100), 
                    email VARCHAR(255), 
                    date_naissance DATE, 
                    ville VARCHAR(255), 
                    code_postal VARCHAR(5), 
                    date_du_texte DATE, 
                    Texte_du_jour VARCHAR(500), 
                    Emotion_majoritaire VARCHAR(20), 
                    Statut VARCHAR(10)
                    ) """
    cur.execute(create_script)
    conn.commit()
    conn.close()





def insert_user(nom,prenom,record,email,data_naissance,ville,code_postal,date_du_texte,Texte_du_jour,Emotion_majoritaire,Statut):
    insert_script = f'INSERT INTO utilisateur VALUES {nom,prenom,record,email,data_naissance,ville,code_postal,date_du_texte,Texte_du_jour,Emotion_majoritaire,Statut}'
    cur.execute(insert_script)
    conn.commit()
    conn.close()

def delete_db_element(nom):
    delete_script = f'DELETE FROM utilisateurs WHERE name = {nom}'
    cur.execute(delete_script)
    conn.close()

def admin_display():
    cur.execute('SELECT * FROM utilisateur')
    conn.commit()
    conn.close()
       
def user_display():
    cur.execute('SELECT')
    conn.commit()
    conn.close()

def update_user(Texte_du_jour):
    update_script = f'UPDATE utilisateur SET Texte_du_jour = {Texte_du_jour} WHERE Texte_du_jour = {Texte_du_jour}'
    cur.execute(update_script)
    conn.close()

def day_text(Texte_du_jour):
    insert_texte = f'INSERT INTO utilisateur (Texte_du_jour) VALUES {Texte_du_jour}'
    cur.execute(insert_texte)
    conn.commit()
    conn.close()

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
    st.write(admin_display())

if selection == 'Consulter vos progressions':
    st.text('zfoczd')
