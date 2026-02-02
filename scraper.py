import requests
from bs4 import BeautifulSoup
import json

def scraping_agrofy():
    # El RSS es la puerta trasera oficial para leer noticias sin bloqueos
    url = "https://news.agrofy.com.ar/ganaderia/feed"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        # El RSS es XML, no HTML
        soup = BeautifulSoup(response.content, features="xml")
        
        noticias_list = []
        # En RSS, cada noticia es un <item>
        items = soup.find_all('item')

        for item in items[:6]:
            titulo = item.title.text if item.title else "Sin título"
            link = item.link.text if item.link else ""
            
            if titulo and link:
                noticias_list.append({
                    "titulo": titulo.strip(),
                    "url": link.strip()
                })

        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"ÉXITO: {len(noticias_list)} noticias extraídas vía RSS.")

    except Exception as e:
        print(f"Error en RSS: {e}")

if __name__ == "__main__":
    scraping_agrofy()
