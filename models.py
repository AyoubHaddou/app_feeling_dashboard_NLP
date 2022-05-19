import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker 


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
        
    engine = create_engine('sqlite:///feeling_db.sqlite3')
    Session = sessionmaker(bind=engine)
    sess = Session()
    return sess 

def init_db():
    sess = conn()
    coach = User(name='John Smith', username="jsmith", password="123", is_coach=True)
    patient = User(name='Rebecca Briggs', username='rbriggs', password='123', is_coach=False)
    sess.add_all([coach, patient])
    sess.commit()



if __name__ == '__main__':
    engine = create_engine('sqlite:///feeling_db.sqlite3')
    Base.metadata.create_all(engine)
    init_db()