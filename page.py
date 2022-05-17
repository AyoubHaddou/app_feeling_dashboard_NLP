from dataclasses import dataclass, field
import streamlit as st
import streamlit_authenticator as stauth 
import pandas 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine , update 
from models import Coach, Patient, Text 
import datetime 


@dataclass 
class Page:
    selection = st.sidebar.text('Please login')
    info_1 = st.sidebar.text('Free demo account : \nUsername : jsmith \nPassword : 123')
    sess = ""
    col1, col2, col3 = st.columns(3)
    names_all : list = field(default_factory=lambda : [])
    usernames_all : list = field(default_factory= lambda : [])
    hash_password_all : list = field(default_factory=lambda : [])
    image_page = ""
    WordOfDay = ""
    title = ""

    def init_session(self):

        engine = create_engine('sqlite:///feeling_db.sqlite3?check_same_thread=False')
        Session = sessionmaker(bind=engine)
        self.sess = Session()

        coach_all = self.sess.query(Coach).all()
        patient_all = self.sess.query(Patient).all()
        password_all = []

        for coach, patient in zip(coach_all, patient_all):
            coach_name = coach.name
            patient_name = patient.name
            self.names_all.append(coach_name)
            self.names_all.append(patient_name)
            self.usernames_all.append(coach.username)
            self.usernames_all.append(patient.username)
            password_all.append(coach.password)
            password_all.append(patient.password)
     
        self.hash_password_all = stauth.Hasher(password_all).generate()

    def login_streamlit(self):

        authenticator = stauth.Authenticate(self.names_all,self.usernames_all,self.hash_password_all,
            'some_cookie_name','some_signature_key',cookie_expiry_days=30)
        return authenticator.login('Login','main')


    def check_log(self):

        if st.session_state['authentication_status'] == False:
            st.error('Please enter correct username and password')
            with self.col2:
                self.image_page = st.image('coach.gif')

        elif st.session_state['authentication_status']:
            st.sidebar.text('Welcome *%s*' % (st.session_state['name']))
            self.selection = st.sidebar.selectbox('Que souhaitez vous faire ?', ['Rédiger votre texte du jour', 'Modifier votre texte du jour', 'Consulter vos texte', 'Consulter vos progressions'])
            with self.col2:
                self.image_page = st.image('motivation.jpeg')


    def display_content(self):

        if self.selection == 'Rédiger votre texte du jour':
            self.title = st.title('Your day text')
            self.WordOfDay = st.text_area('Rédiger votre texte du jour')
            button = st.button('Publier')
            
            if button and self.WordOfDay:
                actual_username = st.session_state['username']
                current_user = self.sess.query(Coach).filter_by( username = actual_username).first()
                user_text = self.sess.query(Text).filter_by( user_id = current_user.id).all()
                last_date = [0]
                for text in user_text :
                    last_date.append(text.time_created.day)
                date = datetime.datetime.now().day

                if last_date[-1] != date:
                    text = Text(content=self.WordOfDay, emotion_predicted="in coming", user_id=1)
                    self.sess.add(text)
                    self.sess.commit()
                    st.balloons()
                    st.success('Message du jour envoyé!')
                else:
                    st.error('Text already send today. Go to modification space if you need it.')





page = Page()
page.init_session()
page.login_streamlit()
page.check_log()
page.display_content()