from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine
from models import Coach, Patient


engine = create_engine('sqlite:///feeling_db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()


def init_db():
    coach = Coach(name='Rocky', password="1234", patient_id=1)
    patient = Patient(name='Junior', password='1234', coach_id=1)
    sess.add_all([coach, patient])
    sess.commit()

init_db()
