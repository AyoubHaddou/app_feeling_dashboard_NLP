import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker 


Base = declarative_base()


class Coach(Base):
    __tablename__ = 'Coach'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    patient_id = Column(Integer, ForeignKey('Patient.id'))


class Patient(Base):
    __tablename__ = 'Patient'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    coach_id = Column(Integer, ForeignKey('Coach.id'))

class Text(Base):
    __tablename__ = 'Text'
    id = Column(Integer, primary_key = True)
    content = Column(String, nullable=False)
    emotion_predicted = Column(String)
    user_id = Column(Integer, ForeignKey('Patient.id'), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


def conn():
        
    engine = create_engine('sqlite:///feeling_db.sqlite3')
    Session = sessionmaker(bind=engine)
    sess = Session()
    return sess 

def init_db():
    sess = conn()
    coach = Coach(name='Rocky', password="1234", patient_id=1)
    patient = Patient(name='Junior', password='1234', coach_id=1)
    sess.add_all([coach, patient])
    sess.commit()



if __name__ == '__main__':
    engine = create_engine('sqlite:///feeling_db.sqlite3')
    Base.metadata.create_all(engine)
    init_db()