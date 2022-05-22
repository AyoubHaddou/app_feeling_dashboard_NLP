from dataclasses import dataclass, field
import streamlit as st
import streamlit_authenticator as stauth 
import pandas as pd
import numpy as np 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine , update , func 
from db.models import User, Text 
import datetime 
from db.function import predict_data, make_engine_session, emotion_int, df_all
import matplotlib.pyplot as plt

@dataclass 
class Page:
    config = st.set_page_config(layout="wide")
    title = ""
    col1, col2, col3 = st.columns(3)
    sess = make_engine_session()
    side_info_dashboard = ""
    side_selection = ""
    current_user = ""
    user_text = ""
    image_page = ""
    WordOfDay = ""
    actual_username = ""   
    df_all = ""
    side_logout = ""

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
                self.image_page = st.image('./images/peace.jpg')
            self.side_selection = st.sidebar.text('Please login')
            self.side_info_dashboard = st.sidebar.text('Free demo coach account \nUsername : jsmith \nPassword : 123 \n\nFree demo patient account : \nUsername : rbriggs \nPassword : 123')
            if st.session_state['authentication_status'] == False :
                st.error('Please enter correct username and password')

        elif st.session_state['authentication_status']:
            with self.col2:
                self.image_page = st.image('./images/text_hero.png')
            self.side_info_dashboard = st.sidebar.text('Welcome *%s*' % (st.session_state['name']))
            side_bar_admin = ['Suivit des emotions', 'Gestion des patients', 'Tester votre IA']
            side_bar_user = ['Rédiger votre texte du jour', 'Modifier votre texte du jour', 'Suivit des emotions']
            self.actual_username = st.session_state['username']
            check_a = self.sess.query(User).filter_by( username = self.actual_username, is_coach=True).first()
            check_b = self.sess.query(User).filter_by( username = self.actual_username, is_coach=False).first()
            self.df_all = df_all(Text, User)
            if check_a :
                self.current_user = check_a
                self.user_text = self.sess.query(Text).all()
                self.side_selection = st.sidebar.selectbox('Que souhaitez vous faire ?', side_bar_admin)
            elif check_b :
                self.current_user = check_b
                self.user_text = self.sess.query(Text).filter_by( user_id = check_b.id).all()
                self.side_selection = st.sidebar.selectbox('Que souhaitez vous faire ?', side_bar_user)
            self.side_logout = st.sidebar.button('logout')
            if self.side_logout :
                st.session_state.authentication_status = None
                st.experimental_rerun()


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

    def display_df_main(self):

        if self.side_selection == 'Suivit des emotions':
            self.title = st.title('Consult texts and emotions passed')
            if self.user_text :
                col_graph1, col_graph2 = st.columns(2)
                with col_graph1:
                    choice_date_1 = st.date_input('A partir de :', value=datetime.datetime.strptime('2022-05-01', "%Y-%m-%d").date() )
                with col_graph2:
                    choice_date_2 = st.date_input("Jusqu'à :" )
                
                if self.current_user.is_coach :
                    choice = st.selectbox('Choose your patient by id' , np.append("All", self.df_all.name.unique()))
                    if choice != "All":
                        self.df_all = self.df_all[(self.df_all.time >= str(choice_date_1)) & (self.df_all.time <= str(choice_date_2)) & (self.df_all.name == choice)]
                        st.write(self.df_all.drop('user_id', axis=1))
                    else:
                        self.df_all = self.df_all[(self.df_all.time >= str(choice_date_1)) & (self.df_all.time <= str(choice_date_2))]
                        st.write(self.df_all.drop('user_id', axis=1))
                else:
                    self.df_all = self.df_all[(self.df_all.time >= str(choice_date_1)) & (self.df_all.time <= str(choice_date_2)) & (self.df_all.name == self.current_user.name)]
                    st.write(self.df_all.drop('user_id', axis=1))
            else:
                st.write('Aucun texte enregistré pour le moment.')

    def display_pie_hist(self):

        if self.side_selection == 'Suivit des emotions':
            # Customize matplotlib
            plt.rcParams.update(
                {
                    'text.usetex': False,
                    'font.family': 'stixgeneral',
                }
            )
            self.title = st.title('Emotions pie and more')
            data = []
            if self.user_text :
                col_graph1, col_graph2 = st.columns(2)
                df_pie = self.df_all[['emotion_predicted','texte']].copy()
                df_pie = emotion_int(df_pie)

                # Plot pie
                df_pie = df_pie.groupby('emotion_predicted').count().reset_index()
                fig1, ax1 = plt.subplots()
                ax1.pie(df_pie.emotion_int, labels=df_pie.emotion_predicted, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                with col_graph1:
                    st.pyplot(fig1)         

                # Plot hist 
                arr = self.df_all.emotion_predicted
                fig, ax = plt.subplots()
                ax.hist(arr, bins=20)
                plt.title('Bar of happyness')
                with col_graph2:
                    st.pyplot(fig)
            else:
                st.write('Aucun texte enregistré pour le moment.')


    def add_user(self):
        if self.side_selection == 'Gestion des patients':
            col_graph1, col_graph2 = st.columns(2)
            with col_graph1:
                st.subheader('Ajouter un patient')
                with st.form("my_form"):
                    st.write("Inside the form")
                    name = st.text_input("Full name")
                    username = st.text_input("Username")
                    birthday = st.date_input("Birthday (optionnal)")
                    password = st.text_input("Password", type="password")
                    checkbox_val = st.checkbox("Subscription as coach ?")
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        patient = User(name=name, username=username, password=stauth.Hasher([password]).generate()[0], is_coach=checkbox_val)
                        self.sess.add(patient)
                        self.sess.commit()
                        st.success('Nouveau patient ajouté!')
            with col_graph2:
                st.subheader('Supprimer un patient')
                self.df_all = df_all(Text, User)
                users = self.sess.query(User).filter_by(is_coach=False).all()
                if users :
                    df_petient = self.df_all.groupby('name').count().reset_index()[['name','emotion_predicted']].rename(columns={'emotion_predicted':'text_counts'})
                    st.write(df_petient)
                    patient_list = st.selectbox('Choisir un patient :', df_petient.name)
                    check = st.checkbox(f"Yes I want to delete {patient_list}")
                    to_delete = st.button('Delete')
                    if check : 
                        st.error(f"Do you really want to delete {patient_list} and all associated texts definitely ?")

                    if to_delete and check :
                        user = self.sess.query(User).filter(User.name == patient_list)
                        if user and check:
                            # Je supprime le users + les textes associés

                            patient_to_delete = self.sess.query(User).filter(User.name == patient_list)
                            id_patient_to_delete = patient_to_delete.first().id
                            self.sess.query(Text).filter(Text.user_id == id_patient_to_delete).delete()
                            patient_to_delete.delete()
                            self.sess.commit()
                            st.success('Patient deleted')
                    elif to_delete and (check == False):
                        st.error('Please confirm with checkbox')

                else:
                    st.write('Aucun User enregistré pour le moment.')

    def test_pred(self):
        if self.side_selection == 'Tester votre IA':
            self.title = st.title('Prediction manuel')
            self.WordOfDay = st.text_area('Entrer un paragraphe à prédir')
            button = st.button('Publier')
            if button :
                st.success(f"Sentiment prédit par l'IA : {predict_data(self.WordOfDay)}")
            
    def run_page(self):
        self.login_streamlit()
        self.instance_session()
        self.add_content()
        self.update_content()
        self.display_df_main()
        self.display_pie_hist()
        self.add_user()
        self.test_pred()
        st.markdown('by M.Zen coaching ')

page = Page()
page.run_page()