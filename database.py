from distutils.log import error
import imp
from readline import insert_text
from numpy import insert, reciprocal
import psycopg2
import psycopg2.extras 
from requests import delete
import sqlite3

hostname = 'localhost123'
database = 'demo'
username = 'mr_zen'
pwd = 'rockybalboa'
port_id = 5432


cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 


# création de la base de donnée
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

#supprimer élément de la base de donnée
delete_script = 'DELETE FROM utilisateurs WHERE name = %s'
cur.execute(delete_script)

# Affichage pour admin
cur.execute('SELECT * FROM utilisateur')
for record in cur.fetchall():
    print(record['nom'],record['prenom'],record['email'],record['data_naissance'],record['ville'],record['code_postal'],record['date_du_texte'],record['Texte_du_jour'],record['Emotion_majoritaire'],record['Statut'])
    conn.commit()

#Affichage utilisateur 
cur.execute('SELECT')

#Mise à jour utilisateur
update_script = 'UPDATE utilisateur SET Texte_du_jour = %s WHERE Texte_du_jour = %s'
cur.execute(update_script)

#Insertion dans la base de donnée client 
insert_texte = 'INSERT INTO utilisateur (Texte_du_jour) VALUES (%s)'
cur.execute(insert_texte)

def insert_user(nom,prenom,record,email,data_naissance,ville,code_postal,date_du_texte,Texte_du_jour,Emotion_majoritaire,Statut):
    # insertion dans la base de donnée admin  
    insert_script = f'INSERT INTO utilisateur VALUES {nom,prenom,record,email,data_naissance,ville,code_postal,date_du_texte,Texte_du_jour,Emotion_majoritaire,Statut}'
    conn.commit()
    cur.execute(insert_script)