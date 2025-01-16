import base64
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from data_loading_script import load_movie_data

def fetch_movie_data():
    """
    Charge les données  et prépare les informations nécessaires.
    """
    # Charger les données en utilisant la fonction de data_loader
    df = load_movie_data()

    # Traiter les colonnes nécessaires
    df['primary_genre'] = df['genres'].apply(lambda x: x.split('|')[0] if pd.notnull(x) else 'Unknown')
    df['release_year'] = df['title'].str.extract(r'\((\d{4})\)', expand=False)  # Extraire l'année du titre

    # Compter les films par genre
    genre_data = df['primary_genre'].value_counts().reset_index()
    genre_data.columns = ['genre', 'count']

    # Compter les films par année
    year_data = df['release_year'].value_counts().sort_index().reset_index()
    year_data.columns = ['year', 'count']

    return genre_data, year_data  # Retourner des DataFrames au lieu de dicts

def generate_plot_base64(genre_data, year_data):
    """
    Génère les graphiques et les retourne en tant qu'images base64.
    """

    # Graphique des genres
    genre_chart = BytesIO()
    plt.figure(figsize=(12, 6))
    plt.bar(genre_data['genre'], genre_data['count'], color='skyblue')
    plt.title('Number of Movies by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(genre_chart, format='png')
    genre_chart.seek(0)  # Retourner au début du fichier
    genre_base64 = base64.b64encode(genre_chart.getvalue()).decode('utf-8')

    # Graphique des années
    year_chart = BytesIO()
    plt.figure(figsize=(12, 6))
    plt.plot(year_data['year'], year_data['count'], marker='o', linestyle='-', color='orange')
    plt.title('Number of Movies by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(ticks=year_data['year'][::5], labels=year_data['year'][::5], rotation=45)
    plt.tight_layout()
    plt.savefig(year_chart, format='png')
    year_chart.seek(0)  # Retourner au début du fichier
    year_base64 = base64.b64encode(year_chart.getvalue()).decode('utf-8')

    return genre_base64, year_base64

def generate_html_report(genre_data, year_data):
    """
    Génère un rapport HTML interactif avec des graphiques pour les données MovieLens.
    """
    genre_base64, year_base64 = generate_plot_base64(genre_data, year_data)

    # Créer le code HTML avec les images en base64
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MovieLens Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .chart-container {{ width: 800px; height: 400px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>MovieLens Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>
        
        <div class="chart-container">
            <h2>Movies by Genre</h2>
            <img src="data:image/png;base64,{genre_base64}" alt="Genre Chart">
        </div>
        <br>
        <div class="chart-container">
            <h2>Movies by Year</h2>
            <img src="data:image/png;base64,{year_base64}" alt="Year Chart">
        </div>
    </body>
    </html>
    """

    # Sauvegarder le fichier HTML
    report_path = 'movielens_report.html'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Rapport HTML généré : {report_path}")

def main():
    """
    Fonction principale pour exécuter le script.
    """
    try:
        # Charger les données
        genre_data, year_data = fetch_movie_data()
        
        # Générer le rapport HTML
        generate_html_report(genre_data, year_data)
        print('Rapport MovieLens généré avec succès')
    except Exception as e:
        print(f'Erreur : {e}')
        exit(1)

if __name__ == '__main__':
    main()
