import requests
from bs4 import BeautifulSoup
import json

def scraping_agrofy():
    url = "https://news.agrofy.com.ar/ganaderia"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        noticias_list = []
        
        # Agrofy suele usar estas clases para sus tarjetas de noticias
        # Buscamos los enlaces que contienen los títulos
        articulos = soup.find_all('div', class_='news-card-content')
        
        # Si la clase anterior no funciona, intentamos con una alternativa común
        if not articulos:
            articulos = soup.select('div[class*="card"]')

        for art in articulos[:6]:  # Limitamos a las primeras 6
            link_tag = art.find('a')
            if link_tag:
                titulo = link_tag.get_text(strip=True)
                url_noticia = link_tag['href']
                
                if not url_noticia.startswith('http'):
                    url_noticia = "https://news.agrofy.com.ar" + url_noticia
                
                if titulo:
                    noticias_list.append({
                        "titulo": titulo,
                        "url": url_noticia
                    })

        # Guardar en JSON
        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"Éxito: Se encontraron {len(noticias_list)} noticias.")

    except Exception as e:
        print(f"Error durante el scraping: {e}")

if __name__ == "__main__":
    scraping_agrofy()
