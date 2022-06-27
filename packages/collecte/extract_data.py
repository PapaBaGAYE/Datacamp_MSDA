"""Module d'extraction des données issues de la base de données
"""

import pickle
from pymongo import MongoClient
import pandas as pd
from packages.prétraitement.pretraitement_donnees import pretraitement

def extract_mongodb(server_name)->None:
    """Extraire les données du cluster MongoDB

    Args:
        server_name (str): Le nom du cluster
    """
    
    # Recuperation du cluster
    client = MongoClient(server_name)
    
    # Recuperation de la base de données
    db = client.get_database("terrorismAttack_db")
    
    # Recuperation de la collection
    collection = db.terrorismAttack
    
    # initialisation des variables pertinentes
    variables_pertinentes = ['iyear', 'iday', 'imonth', 'nkill', 'country_txt', 'nwound', 'region_txt', 'provstate',
                         'city', 'nkillus', 'nwoundus', 'region_txt', 'latitude', 'longitude',
                         'attacktype1_txt', 'alternative_txt', 'suicide', 'ransompaid', 'nhostkid', 'hostkidoutcome_txt'
                         , 'ransomnote', 'nhours', 'ndays', 'ransompaidus', 'nhostkidus', 'summary', 'motive', 'gname'
                         , 'natlty1_txt', 'kidhijcountry', 'weaptype1_txt', 'weapsubtype1_txt', 'weaptype2_txt', 'weapsubtype2_txt', 'weaptype3_txt', 'weapsubtype3_txt'
                         , 'weaptype4_txt', 'weapsubtype4_txt', 'targtype1_txt', 'targsubtype1_txt', 'targtype2_txt', 'targsubtype2_txt', 'targtype3_txt', 'targsubtype3_txt'
                         , 'claimmode_txt', 'propextent_txt', 'propextent', 'propvalue', 'dbsource'
                         ]
    
    # dictionnaires des projections
    project_columns = {"_id": 0}
    
    project_columns.update({column: 1 for column in variables_pertinentes})
    
    # recuperation du curseur
    curseur = collection.find({},project_columns)
    
    # conversion du curseur en liste
    list_cur = list(curseur)
    
    # conversion des données en DataFrame
    df_terror = pd.DataFrame(list_cur)
    
    # procédons au prétraitement
    df_terror = pretraitement(df_terror)
    
    # exporter les données avec pickle
    with open("packages/data/cleaned/terror_test.txt", "wb") as f:
        pick = pickle.Pickler(f)
        pick.dump(df_terror)
        
    
    
