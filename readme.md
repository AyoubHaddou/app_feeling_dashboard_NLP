# Classification des sentiments

I. Intro : 

Ce travail a été réaliser dans le cadre d'un projet pour Simplon. 
Je vous invite la lire la section exercice_info pour prendre connaissances des conditions d'éxercices. 

II. Commande pour l'execution . 

*Si necessaire après un git clone :
- la première étape consiste à lancer la commande : pip install -r requirements.txt. 
- Si vous n'avez pas le fichier feeling_db.sqlite3 dans le sous répertoire db, il faudra executer la commande suivant à partir de la racine du repo : 
pip install -r requirements.txt 
- Enfin, en local il sufffira ensuite d'executer la commande : streamlit run app.py
- Si l'API n'est plus déployer Il faudra run l'api en local (lien dans la partie III) pour profiter de toute les fonctionnalités du site.*

II. Application dashboard pour coach des sentiments 

- Voici le lien vers l'application streamlit : https://share.streamlit.io/ayoubhaddou/app_feeling_dashboard_nlp/main/app.py

III. API et base de données : 
    lien repo : https://github.com/AyoubHaddou/API_feeling_dashboard_NLP
    lien de l'api deployé : https://coach-life.herokuapp.com/

IV. Entrainement du modèle : 
    Voir le colab notebook dans la section preprocessing, ou [clic ici](/preprocessing_model/preprocessing_models_NLP.ipynb)
    
    
V. Data sources : 
- Jeu de donnée Kaggle :  https://www.kaggle.com/datasets/ishantjuyal/emotions-in-text
- Data augmentation : https://data.world/crowdflower/sentiment-analysis-in-text
