from distutils.log import error
from numpy import insert
import psycopg2
from requests import delete

hostname = 'localhost123'
database = 'demo'
username = 'postgres'
pwd = 'admin'
port_id = 5432

try : 
    conn = psycopg2.connect(
        host = hostname
        database = database
        username = username
        port_id = port_id
    )

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# création de la base de donnée
create_script = """ CREATE TABLE utilisateur ( 
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


# insertion dans la base de donnée 
insert_script = 'INSERT INTO utilisateur (nom,prenom,email,data_naissance,ville,code_postal,date_du_texte,Texte_du_jour,Emotion_majoritaire,Statut) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
insert_values = 
for record in insert_values:
    cur.execute(insert_script,record)
cur.execute(insert_script)
for record in cur.fetchall():
    print(record['name'],record['salary'])


#supprimer élément de la base de donnée
delete_script = 'DELETE FROM utilisateurs WHERE name = %s'
cur.execute(delete_script)

# Affichage  
cur.execute('SELECT * FROM utilisateur')
for record in cur.fetchall():
    print(record['name'],record['salary'])

    conn.commit()

#Mise à jour 
UPDATE 


except Exception as error:
    print(error)
finally:
    if cur is not None: 
        cur.close()
    if cur is not None:
        conn.close()