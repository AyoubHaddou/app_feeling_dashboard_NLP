import mysql.connector 
import sys

sql_create = """
CREATE TABLE utilisateur ( 
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
    );
"""

sql = "INSERT INTO utilisateur (nom,prenom,email,date_naissance,ville,code_postal,Statut) VALUES (Balboa,Rocky,balboarocky@coaching.com,1976-11-21,New York, 1624,Administrateur)"