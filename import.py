import duckdb
import os


for file in os.listdir('data') :


    # Nom du fichier de la base de données DuckDB
    db_file = 'mon_datalake.db'

    # Nom du fichier CSV à ingérer
    csv_file = 'sources/ci_acte_a.csv'

    # Nom de la table où les données seront stockées
    table_name = 'ma_table'

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

        # Exemple de requête pour afficher les premières lignes
        print("\nAperçu des données:")
        result = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchall()
        for row in result:
            print(row)

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        # Fermeture de la connexion
        conn.close()