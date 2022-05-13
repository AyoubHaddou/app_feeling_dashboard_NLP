from dataclasses import dataclass  
import streamlit as st
import streamlit_authenticator as stauth 
import pandas 

@dataclass 
class Page:
    names = 'John Smith'
    usernames = 'jsmith'
    passwords = '123'

    def login_streamlit(self):


        hashed_passwords = stauth.Hasher(self.passwords).generate()

        authenticator = stauth.Authenticate(self.names,self.usernames,hashed_passwords,
            'some_cookie_name','some_signature_key',cookie_expiry_days=30)


        return authenticator.login('Login','main')



    

page = Page()
page.login_streamlit()