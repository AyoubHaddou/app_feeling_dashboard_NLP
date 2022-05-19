from dataclasses import dataclass, field
import streamlit as st
import streamlit_authenticator as stauth 
import pandas as pd
import numpy as np 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine , update , func 
from models import User, Text 
import datetime 
from function import predict_data
import matplotlib.pyplot as plt

@dataclass 
class Page:
    selection = ""
    info_dashboard = ""
    sess = ""
    col1, col2, col3 = st.columns(3)
    title = ""
    image_page = ""
    WordOfDay = ""
    actual_username = ""
    current_user = ""
    user_text = ""


    def init_session(self):

        engine = create_engine('sqlite:///feeling_db.sqlite3?check_same_thread=False')
        Session = sessionmaker(bind=engine)
        self.sess = Session()
        user_all = self.sess.query(User).all()
        password_all = []
        usernames_all = []
        names_all = []

        for user in user_all:
            coach_name = user.name
            names_all.append(coach_name)
            usernames_all.append(user.username)
            password_all.append(user.password)
     

        # Authentification     
        hash_password_all = stauth.Hasher(password_all).generate()
        authenticator = stauth.Authenticate(names_all, usernames_all,hash_password_all,
                                            'some_cookie_name','some_signature_key',cookie_expiry_days=0)
        authenticator.login('Login','main')



    def session(self):

        if (st.session_state['authentication_status'] == False) or (st.session_state['authentication_status'] == None) :
            self.selection = st.sidebar.text('Please login')
            self.info_dashboard = st.sidebar.text('Free demo account : \nUsername : jsmith \nPassword : 123')
            with self.col2:
                self.image_page = st.image('coach.gif')

            if st.session_state['authentication_status'] == False :
                st.error('Please enter correct username and password')


        elif st.session_state['authentication_status']:
            self.info_dashboard = st.sidebar.text('Welcome *%s*' % (st.session_state['name']))
            self.selection = st.sidebar.selectbox('Que souhaitez vous faire ?', ['Rédiger votre texte du jour', 'Modifier votre texte du jour', 'Consulter vos texte', 'Consulter vos progressions'])
            self.actual_username = st.session_state['username']
            check_a = self.sess.query(User).filter_by( username = self.actual_username, is_coach=True).first()
            check_b = self.sess.query(User).filter_by( username = self.actual_username, is_coach=False).first()
            if check_a :
                self.user_text = self.sess.query(Text).all()
                self.current_user = check_a
            elif check_b :
                self.user_text = self.sess.query(Text).filter_by( user_id = check_b.id).all()
                self.current_user = check_b
            with self.col2:
                self.image_page = st.image('motivation.jpeg')


    def display_content(self):

        if self.selection == 'Rédiger votre texte du jour':
            self.title = st.title('Your day text')
            self.WordOfDay = st.text_area('Rédiger votre texte du jour')
            button = st.button('Publier')
            if button and self.WordOfDay:
                last_date = [0]
                if self.user_text:
                    for text in self.user_text :
                        last_date.append(text.time_created.day)

                date = datetime.datetime.now().day
                if last_date[-1] != date:
                    text = Text(content=self.WordOfDay, emotion_predicted=predict_data(self.WordOfDay), user_id=self.current_user.id)
                    self.sess.add(text)
                    self.sess.commit()
                    st.balloons()
                    st.success('Message du jour envoyé!')
                else:
                    st.error('Text already send today. Go to modification space if you need it.')

        elif self.selection == 'Modifier votre texte du jour':
            self.title = st.title('Day text modification')
            self.WordOfDay = st.text_area('Modifier votre texte du jour :')
            button = st.button('Publier')
            if self.user_text :
                st.write('Le message du jour modifiable est le suivant :')
                st.warning(self.user_text[-1].content)
            elif button and self.WordOfDay :
                self.sess.query(Text).filter(Text.user_id == 1, Text.id == self.sess.query(func.max(Text.id))).update({"content" : self.WordOfDay, "emotion_predicted" :predict_data(self.WordOfDay) }, synchronize_session="fetch")
                self.sess.commit()
                st.success("texte updated with success")
            else:
                st.write('Aucun texte enregistré pour le moment.')
            st.write('--------------------------------')

        elif self.selection == 'Consulter vos texte':
            self.title = st.title('Consult your text and emotions')
            data = []
            result = self.sess.query(Text).filter_by().all()
            if result :
                for text in result:
                    data.append({'emotion_predicted' : text.emotion_predicted, 'texte' : text.content, 'time' : text.time_created, 'modif': text.time_updated})
                # st.dataframe(data_content, data_emotion)
                st.dataframe(data)
            else:
                st.write('Aucun texte enregistré pour le moment.')

        elif self.selection == 'Consulter vos progressions':
            self.title = st.title('Emotions tracker')
            data = []
            if self.user_text :
                for text in self.user_text:
                    data.append({'emotion_predicted' : text.emotion_predicted, 'texte' : text.content, 'time' : text.time_created, 'modif': text.time_updated})
                df = pd.DataFrame(data)
                arr = df.emotion_predicted
                fig, ax = plt.subplots()
                ax.hist(arr, bins=20)
                plt.title('Bar of happyness')
                st.pyplot(fig)
            else:
                st.write('Aucun texte enregistré pour le moment.')

        st.markdown('by M.Zen coaching ')

    def run_page(self):
        self.init_session()
        self.session()
        self.display_content()


page = Page()
page.run_page()