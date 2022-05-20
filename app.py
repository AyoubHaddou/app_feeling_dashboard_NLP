from dataclasses import dataclass, field
import streamlit as st
import streamlit_authenticator as stauth 
import pandas as pd
import numpy as np 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine , update , func 
from models import User, Text 
import datetime 
from function import predict_data, make_engine_session, emotion_int
import matplotlib.pyplot as plt

@dataclass 
class Page:
    config = st.set_page_config(layout="wide")
    col1, col2, col3 = st.columns(3)
    sess = make_engine_session()
    side_info_dashboard = ""
    side_selection = ""
    current_user = ""
    user_text = ""
    title = ""
    image_page = ""
    WordOfDay = ""
    actual_username = ""


    def login_streamlit(self):

        user_all = self.sess.query(User).all()
        names_all = []
        usernames_all = []
        hash_password_all = []
        for user in user_all:
            names_all.append(user.name)
            usernames_all.append(user.username)
            hash_password_all.append(user.password)

        # Authentification    
        authenticator = stauth.Authenticate(names_all, usernames_all,hash_password_all,
                                            'some_cookie_name','some_signature_key',cookie_expiry_days=0)
        authenticator.login('Login','main')

    def instance_session(self):

        if (st.session_state['authentication_status'] == False) or (st.session_state['authentication_status'] == None) :
            with self.col2:
                self.image_page = st.image('coach.gif')
            self.side_info_dashboard = st.sidebar.text('Free demo account : \nUsername : jsmith \nPassword : 123')
            self.side_selection = st.sidebar.text('Please login')
            if st.session_state['authentication_status'] == False :
                st.error('Please enter correct username and password')

        elif st.session_state['authentication_status']:
            with self.col2:
                self.image_page = st.image('motivation.jpeg')
            self.side_info_dashboard = st.sidebar.text('Welcome *%s*' % (st.session_state['name']))
            side_bar_admin = ['Rédiger votre texte du jour', 'Modifier votre texte du jour', 'Suivit des emotions', 'Ajouter un patient']
            side_bar_user = ['Rédiger votre texte du jour', 'Modifier votre texte du jour', 'Suivit des emotions']
            self.actual_username = st.session_state['username']
            check_a = self.sess.query(User).filter_by( username = self.actual_username, is_coach=True).first()
            check_b = self.sess.query(User).filter_by( username = self.actual_username, is_coach=False).first()
            if check_a :
                self.current_user = check_a
                self.user_text = self.sess.query(Text).all()
                self.side_selection = st.sidebar.selectbox('Que souhaitez vous faire ?', side_bar_admin)
            elif check_b :
                self.current_user = check_b
                self.user_text = self.sess.query(Text).filter_by( user_id = check_b.id).all()
                self.side_selection = st.sidebar.selectbox('Que souhaitez vous faire ?', side_bar_user)



    def add_content(self):

        if self.side_selection == 'Rédiger votre texte du jour':
            self.title = st.title('Your day text')
            self.WordOfDay = st.text_area('Rédiger votre texte du jour')
            button = st.button('Publier')
            if button and self.WordOfDay:
                date_now = datetime.datetime.now().day
                last_post = [0]
                if self.user_text:
                    for text in self.user_text :
                        last_post.append(text.time_created.day)
                if last_post[-1] != date_now:
                    text = Text(content=self.WordOfDay, emotion_predicted=predict_data(self.WordOfDay), user_id=self.current_user.id)
                    self.sess.add(text)
                    self.sess.commit()
                    st.success('Message du jour envoyé!')
                else:
                    st.error('Text already send today. Go to modification space if you need it.')

    def update_content(self):

        if self.side_selection == 'Modifier votre texte du jour':
            self.title = st.title('Day text modification')
            self.WordOfDay = st.text_area('Modifier votre texte du jour :')
            button = st.button('Publier')
            if self.user_text :
                st.write('Le message du jour modifiable est le suivant :')
                st.warning(self.user_text[-1].content)
            else:
                st.write('Aucun texte enregistré pour le moment.')
            if button and self.WordOfDay :
                self.sess.query(Text).filter(Text.user_id == self.current_user.id, Text.id == self.sess.query(func.max(Text.id))).update({"content" : self.WordOfDay, "emotion_predicted" :predict_data(self.WordOfDay) }, synchronize_session="fetch")
                self.sess.commit()
                st.success("texte updated with success")

    def display_data(self):

        if self.side_selection == 'Suivit des emotions':
            self.title = st.title('Consult texts and emotions passed')
            data = []
            result = self.sess.query(Text).filter_by().all()
            if result :
                for text in self.user_text:
                    data.append({'emotion_predicted' : text.emotion_predicted, 'texte' : text.content, 'time' : text.time_created})
                # st.dataframe(data_content, data_emotion)
                st.dataframe(data)
            else:
                st.write('Aucun texte enregistré pour le moment.')


    def plot_graph(self):

        if self.side_selection == 'Suivit des emotions':
            self.title = st.title('Emotions pie and more')
            data = []
            if self.user_text :

                # Make data to plot 
                for text in self.user_text:
                    data.append({'emotion_predicted' : text.emotion_predicted, 'texte' : text.content, 'time' : text.time_created})
                df = pd.DataFrame(data)
                df_pie = df[['emotion_predicted','texte']]
                df_pie['emotion_int'] =  df.emotion_predicted.apply(lambda x : emotion_int(x))

                # Plot pie
                df_pie = df_pie.groupby('emotion_predicted').count().reset_index()
                fig1, ax1 = plt.subplots()
                ax1.pie(df_pie.emotion_int, labels=df_pie.emotion_predicted, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                col_graph1, col_graph2 = st.columns(2)
                with col_graph1:
                    st.pyplot(fig1)

                # Plot hist 
                arr = df.emotion_predicted
                fig, ax = plt.subplots()
                ax.hist(arr, bins=20)
                plt.title('Bar of happyness')
                with col_graph2:
                    st.pyplot(fig)
            else:
                st.write('Aucun texte enregistré pour le moment.')
        

    def run_page(self):
        self.login_streamlit()
        self.instance_session()
        self.add_content()
        self.update_content()
        self.display_data()
        self.plot_graph()
        st.markdown('by M.Zen coaching ')

page = Page()
page.run_page()