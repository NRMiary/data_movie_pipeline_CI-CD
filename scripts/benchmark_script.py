import time
import psutil
from memory_profiler import memory_usage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from data_loading_script import load_movie_data

# Transformation des données
def data_transformation(df):
    # Ajout d'une colonne 'length_of_title'
    df['length_of_title'] = df['title'].apply(len)
    return df

# Fonction pour mesurer les ressources utilisées pendant l'exécution
def benchmark_transformation(df):
    # Mesure du temps d'exécution
    start_time = time.time()
    
    # Suivi de l'utilisation mémoire et CPU pendant l'exécution
    def wrapper():
        return data_transformation(df)
    
    # Mesure de l'utilisation de la mémoire pendant la transformation
    mem_usage = memory_usage(wrapper)
    
    # Temps d'exécution
    end_time = time.time()
    execution_time = end_time - start_time

    # Utilisation du CPU (avant et après la transformation)
    cpu_before = psutil.cpu_percent(interval=0.1)
    wrapper()
    cpu_after = psutil.cpu_percent(interval=0.1)
    
    # Créer un rapport PDF
    pdf_filename = "benchmark_report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Ajouter les résultats au PDF
    c.drawString(100, 750, f"Benchmark Report (MovieLens Dataset)")
    c.drawString(100, 730, f"--------------------------")
    c.drawString(100, 710, f"Temps d'exécution: {execution_time:.4f} secondes")
    c.drawString(100, 690, f"Utilisation mémoire (en Mo): {max(mem_usage) - min(mem_usage)} Mo")
    c.drawString(100, 670, f"Utilisation CPU avant: {cpu_before}%")
    c.drawString(100, 650, f"Utilisation CPU après: {cpu_after}%")
    
    # Sauvegarder le fichier PDF
    c.save()

if __name__ == "__main__":
    # Charger les données en utilisant la fonction de data_loader
    df = load_movie_data()
    
    # Vérifiez la structure des données avant de procéder (par exemple, 'title' doit exister dans le dataset)
    print(df.head())

    # Lancer le benchmarking et générer le rapport PDF
    benchmark_transformation(df)
