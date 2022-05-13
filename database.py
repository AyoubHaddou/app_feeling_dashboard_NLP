from readline import insert_text
import sqlite3
from numpy import insert, reciprocal
from requests import delete


conn = sqlite3.connect('coach_db')
cur = conn.cursor()


# Create table statement

sqlCreateDatabase = "create database coachDB;"
# Create a table in PostgreSQL database

cur.execute(sqlCreateDatabase)


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



def insert_user(nom,prenom,record,email,data_naissance,ville,code_postal,date_du_texte,Texte_du_jour,Emotion_majoritaire,Statut):
    insert_script = f'INSERT INTO utilisateur VALUES {nom,prenom,record,email,data_naissance,ville,code_postal,date_du_texte,Texte_du_jour,Emotion_majoritaire,Statut}'
    conn.commit()
    cur.execute(insert_script)

def delete_db_element(nom):
    delete_script = f'DELETE FROM utilisateurs WHERE name = {nom}'
    cur.execute(delete_script)

def admin_display():
    cur.execute('SELECT * FROM utilisateur')
    conn.commit()
       
def user_display():
    cur.execute('SELECT')

def update_user(Texte_du_jour):
    update_script = f'UPDATE utilisateur SET Texte_du_jour = {Texte_du_jour} WHERE Texte_du_jour = {Texte_du_jour}'
    cur.execute(update_script)

def day_text(Texte_du_jour):
    insert_texte = f'INSERT INTO utilisateur (Texte_du_jour) VALUES {Texte_du_jour}'
    cur.execute(insert_texte)