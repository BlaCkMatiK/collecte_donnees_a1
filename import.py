import duckdb
import os
import pathlib
import sys

# Nom du fichier de la base de données DuckDB
db_file = 'mon_datalake.db'

for file in os.listdir('sources') :

    # Nom du fichier CSV à ingérer
    csv_file = f'sources/{file}'

    # Nom de la table où les données seront stockées
    table_name = pathlib.Path(file).stem

    # Connexion à la base de données
    conn = duckdb.connect(db_file)

    try:
        # Création de la table et ingestion des données depuis le CSV
        conn.execute(f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_file}')
        """)
        
        # Vérification : compter le nombre de lignes insérées
        result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        print(f"Nombre de lignes insérées dans {table_name}: {result[0]}")

        conn.sql(f"""SELECT * FROM {table_name} LIMIT 5""").show()

        # Exemple de requête pour afficher les premières lignes
        # print("\nAperçu des données:")
        # result = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchall()
        # for row in result:
        #     print(row)


    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        # Fermeture de la connexion
        conn.close()