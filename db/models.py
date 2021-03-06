from email.policy import default
import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker 
from db.function import predict_data
import streamlit_authenticator as stauth 


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_coach = Column(Boolean, default=False)


class Text(Base):
    __tablename__ = 'Text'
    id = Column(Integer, primary_key = True)
    content = Column(String, nullable=False)
    emotion_predicted = Column(String)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


def conn():
        
    engine = create_engine('sqlite:///db/feeling_db.sqlite3')
    Session = sessionmaker(bind=engine)
    sess = Session()
    return sess 

def init_db():
    sess = conn()
    coach = User(name='John Smith', username="jsmith", password=stauth.Hasher(['123']).generate()[0], is_coach=True)
    patient = User(name='Rebecca Briggs', username='rbriggs', password=stauth.Hasher(['123']).generate()[0], is_coach=False)
    patient_2 = User(name='Henri Stylos', username='henri', password=stauth.Hasher(['123']).generate()[0], is_coach=False)
    sess.add_all([coach, patient, patient_2])
    sess.commit()
    print('Users ajouté à la bdd')

    texte = []
    texte.append("I love my new car! It's amazing")
    texte.append("My car is now break.. I'm so sad")
    texte.append("My car is fixed! I'm happy")
    texte.append("I love my car. Brings me so much fun")
    texte.append("I love my cat")
    texte.append("It's so bad. My cat didn't back last night. I don't know here is he")
    texte.append("I feel good. Cat is back and work is going better")
    for day_texte in texte:
        text = Text(content=day_texte, emotion_predicted=predict_data(day_texte), user_id=2)
        sess.add(text)
        sess.commit()
        print('Text ajouté à la bdd')

    texte = []
    texte.append("I'm scared.. I've not good relation with my boss.. If he fired me I will be alone.")
    texte.append("I go at work with stomach.. Strange feel.")
    texte.append("I fell in love with Eric")
    texte.append("A little better today. My boss talk to me with kindness")
    texte.append("My boss has very bad behavior. He is not passionate by his job.")
    for day_texte in texte:
        text = Text(content=day_texte, emotion_predicted=predict_data(day_texte), user_id=3)
        sess.add(text)
        sess.commit()
        print('Text ajouté à la bdd')

if __name__ == '__main__':
    engine = create_engine('sqlite:///db/feeling_db.sqlite3')
    Base.metadata.create_all(engine)
    init_db()