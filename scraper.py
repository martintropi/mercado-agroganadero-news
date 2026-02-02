# scraper.py
import cloudscraper
import json
from bs4 import BeautifulSoup
import os

def scraping_agrofy_con_cloudscraper():
    """
    Realiza scraping de Agrofy News usando la librería cloudscraper, diseñada
    para eludir protecciones anti-bot como las de Cloudflare.
    Guarda el resultado en un archivo JSON.
    """
    url = "https://news.agrofy.com.ar/ganaderia"
    
    scraper = cloudscraper.create_scraper( ) 
    
    try:
        response = scraper.get(url, timeout=30)
        print(f"Respuesta del servidor: {response.status_code}")
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
        
        if not next_data_script:
            print("Error: No se encontró el script '__NEXT_DATA__'.")
            return

        data = json.loads(next_data_script.string)
        articles = data['props']['pageProps']['initialProps']['page']['zones'][0]['widgets'][0]['articles']
        
        noticias_list = []
        for article in articles[:6]:
            titulo = article.get('title', 'Sin título')
            slug = article.get('slug', '')
            full_url = f"https://news.agrofy.com.ar/{slug}" if slug else "URL no encontrada"
            noticias_list.append({"titulo": titulo, "url": full_url} )
            
        # Nombre del archivo de salida
        output_filename = 'noticias.json'
        
        # Guardar los resultados en el archivo JSON
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se procesaron {len(noticias_list)} noticias.")
        print(f"Resultados guardados en '{output_filename}'.")

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        print("El servidor rechazó la solicitud. cloudscraper no fue suficiente.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # Asegurarnos de que el script se ejecute
    scraping_agrofy_con_cloudscraper()
