import requests
import json
from bs4 import BeautifulSoup

def scraping_agrofy_con_referer_propio():
    """
    Realiza scraping de Agrofy News usando el propio sitio como Referer
    para evitar el error 403 Forbidden de una manera más limpia.
    """
    url = "https://news.agrofy.com.ar/ganaderia"
    
    # Encabezados completos, pero con un Referer más lógico
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        # Usamos la URL base del sitio como Referer.
        'Referer': 'https://news.agrofy.com.ar/',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin', # Cambiado de 'cross-site' a 'same-origin' para que coincida con el Referer
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
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
            
        output_filename = 'noticias_agrofy.json'
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se procesaron {len(noticias_list)} noticias.")
        print(f"Resultados guardados en '{output_filename}'.")
        print("\n--- Noticias Encontradas ---")
        print(json.dumps(noticias_list, indent=2, ensure_ascii=False))

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        print("El servidor rechazó la solicitud. El Referer propio no fue suficiente.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    scraping_agrofy_con_referer_propio()
