import pandas as pd

MOVIE_CSV_PATH = "data/movies.csv"

def load_movie_data():
    """
    Charge le fichier CSV contenant les films et prépare les données.
    """
    # Charger le fichier CSV avec pandas
    df = pd.read_csv(MOVIE_CSV_PATH)
    
    return df
