import requests
import json
from bs4 import BeautifulSoup

def scraping_agrofy_corregido():
    """
    Realiza scraping de las noticias de la sección de ganadería de Agrofy News,
    extrayendo los datos desde el objeto JSON __NEXT_DATA__ que utiliza el sitio.
    """
    url = "https://news.agrofy.com.ar/ganaderia"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # 1. Descargar el contenido de la página
        response = requests.get(url, headers=headers, timeout=30)
        # Lanza un error si la petición HTTP no fue exitosa (ej. error 404 o 500)
        response.raise_for_status()
        
        # 2. Analizar el HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Encontrar la etiqueta <script> con id="__NEXT_DATA__"
        next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
        
        if not next_data_script:
            print("Error: No se encontró el script '__NEXT_DATA__'. La estructura de la página puede haber cambiado.")
            return

        # 4. Extraer el contenido del script y cargarlo como JSON
        data = json.loads(next_data_script.string)
        
        # 5. Navegar a través de la estructura del JSON para llegar a la lista de artículos
        # Esta ruta se encontró inspeccionando el contenido del JSON en el navegador
        # y puede cambiar en el futuro si el sitio web se actualiza.
        articles = data['props']['pageProps']['initialProps']['page']['zones'][0]['widgets'][0]['articles']
        
        noticias_list = []
        # Limitar a las primeras 6 noticias como en el script original
        for article in articles[:6]:
            titulo = article.get('title', 'Sin título')
            # La URL completa se construye usando el dominio base y el 'slug' del artículo
            slug = article.get('slug', '')
            if slug:
                full_url = f"https://news.agrofy.com.ar/{slug}"
            else:
                full_url = "URL no encontrada"

            noticias_list.append({
                "titulo": titulo,
                "url": full_url
            } )
            
        # 6. Guardar los resultados en un archivo JSON
        output_filename = 'noticias_agrofy.json'
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se procesaron {len(noticias_list)} noticias.")
        print(f"Los resultados se han guardado en el archivo '{output_filename}'.")
        
        # Opcional: Imprimir los resultados en la consola para verificación rápida
        print("\n--- Noticias Encontradas ---")
        print(json.dumps(noticias_list, indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"Error de red al intentar acceder a la URL: {e}")
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error al procesar la estructura del JSON: {e}.")
        print("Es posible que la estructura de datos de la página haya cambiado.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    scraping_agrofy_corregido()
