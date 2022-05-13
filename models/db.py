import sqlite3

con = sqlite3.connect('coach_db')
cur = con.cursor()

def create_table():
    cur.execute (""" CREATE TABLE utilisateur IF NOT EXIST ( 
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
                    ) """)


def insert_user(nom,prenom,record,email,data_naissance,ville,code_postal,date_du_texte,Texte_du_jour,Emotion_majoritaire,Statut):
    insert_script = f'INSERT INTO utilisateur VALUES {nom,prenom,record,email,data_naissance,ville,code_postal,date_du_texte,Texte_du_jour,Emotion_majoritaire,Statut}'
    cur.execute(insert_script)

def delete_db_element(nom):
    delete_script = f'DELETE FROM utilisateurs WHERE name = {nom}'
    cur.execute(delete_script)

def admin_display():
    cur.execute('SELECT * FROM utilisateur')
       
def user_display():
    cur.execute('SELECT')

def update_user(Texte_du_jour):
    update_script = f'UPDATE utilisateur SET Texte_du_jour = {Texte_du_jour} WHERE Texte_du_jour = {Texte_du_jour}'
    cur.execute(update_script)

def day_text(Texte_du_jour):
    insert_texte = f'INSERT INTO utilisateur (Texte_du_jour) VALUES {Texte_du_jour}'
    cur.execute(insert_texte)