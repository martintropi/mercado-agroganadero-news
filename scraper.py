import requests
from bs4 import BeautifulSoup
import json

def scraping_agrofy():
    url = "https://news.agrofy.com.ar/ganaderia"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        noticias_list = []

        # Buscamos todos los links que contengan "/ganaderia/" en su URL
        # y que tengan texto (que suele ser el título)
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            titulo = link.get_text(strip=True)
            
            # Filtramos links que sean noticias (suelen tener el slug de la sección)
            if "/ganaderia/" in href and len(titulo) > 20:
                full_url = href if href.startswith('http') else f"https://news.agrofy.com.ar{href}"
                
                # Evitar duplicados
                if not any(n['url'] == full_url for n in noticias_list):
                    noticias_list.append({
                        "titulo": titulo,
                        "url": full_url
                    })
            
            if len(noticias_list) >= 6:
                break

        # Si aún está vacío, imprimimos el HTML para ver qué pasa (solo en logs)
        if not noticias_list:
            print("No se encontraron noticias. Estructura recibida:")
            print(soup.prettify()[:500]) 

        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"Resultado: {len(noticias_list)} noticias guardadas.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scraping_agrofy()
