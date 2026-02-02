import requests
from bs4 import BeautifulSoup
import json
import os

def scraping_agrofy():
    url = "https://news.agrofy.com.ar/ganaderia"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error al acceder: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscamos los contenedores de las noticias
    # Nota: Las clases pueden variar, pero usualmente Agrofy usa selectores consistentes
    noticias_list = []
    articulos = soup.select('.news-card-content, .item-noticia')[:6] # Ajustamos según estructura actual

    for art in articulos:
        titulo_tag = art.select_one('h2, .title')
        link_tag = art.select_one('a')
        
        if titulo_tag and link_tag:
            titulo = titulo_tag.get_text(strip=True)
            link = link_tag['href']
            if not link.startswith('http'):
                link = "https://news.agrofy.com.ar" + link
                
            noticias_list.append({
                "titulo": titulo,
                "url": link
            })

    # Guardar en JSON
    with open('noticias.json', 'w', encoding='utf-8') as f:
        json.dump(noticias_list, f, ensure_ascii=False, indent=4)
    
    print("Archivo noticias.json actualizado correctamente.")

if __name__ == "__main__":
    scraping_agrofy()