# scraper.py (versión de depuración)
import cloudscraper
from bs4 import BeautifulSoup
import json

def debug_scraper():
    url = "https://news.agrofy.com.ar/ganaderia"
    scraper = cloudscraper.create_scraper( )
    
    try:
        response = scraper.get(url, timeout=30)
        print(f"Respuesta del servidor: {response.status_code}")
        response.raise_for_status()

        # Guardamos el contenido HTML para poder inspeccionarlo
        html_content = response.text
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("HTML de la página guardado en 'debug_page.html'")

        soup = BeautifulSoup(html_content, 'html.parser')
        next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
        
        if not next_data_script:
            print("Error: No se encontró el script '__NEXT_DATA__'. Revisa 'debug_page.html' para ver el contenido recibido.")
            # Salimos con un código de error para que el workflow falle si es necesario,
            # pero después de haber guardado el archivo de depuración.
            exit(1)

        # Si lo encuentra, procede como antes (esto probablemente no se ejecutará en el primer intento)
        data = json.loads(next_data_script.string)
        articles = data['props']['pageProps']['initialProps']['page']['zones'][0]['widgets'][0]['articles']
        
        noticias_list = []
        for article in articles[:6]:
            titulo = article.get('title', 'Sin título')
            slug = article.get('slug', '')
            full_url = f"https://news.agrofy.com.ar/{slug}" if slug else "URL no encontrada"
            noticias_list.append({"titulo": titulo, "url": full_url} )
            
        output_filename = 'noticias.json'
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se procesaron {len(noticias_list)} noticias.")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        exit(1)

if __name__ == "__main__":
    debug_scraper()
