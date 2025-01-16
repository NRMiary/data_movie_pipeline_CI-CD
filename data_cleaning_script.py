from data_loading_script import load_movie_data

# Exemple de script de nettoyage et compression en Parquet
def clean_and_compress(input_file, output_file):
    # Charger les données 
    df = load_movie_data()

    # Nettoyer les colonnes et séparer la colonne 'title' en deux : 'title' et 'year_release'
    # Utilisation d'une expression régulière pour extraire l'année à partir de la chaîne comme "Toy Story (1995)"
    df[['title', 'year_release']] = df['title'].str.extract(r'^(.*)\s\((\d{4})\)$')

    # Vérifier que la séparation a bien fonctionné (facultatif)
    print(df[['title', 'year_release']].head())

    # Ne conserver que les 20 premières colonnes
    df = df.iloc[:, :20]  # Sélectionner les 20 premières colonnes 

    # Effectuer un nettoyage de base (par exemple, suppression des valeurs manquantes)
    df.dropna(inplace=True)

    # Compression en format Parquet avec Snappy (par défaut)
    df.to_parquet(output_file, engine='pyarrow', compression='snappy')

if __name__ == "__main__":
    input_file = 'data/movies.csv'  # Remplacez par le chemin de votre fichier CSV
    output_file = 'output_data.parquet'  # Fichier Parquet de sortie
    clean_and_compress(input_file, output_file)
