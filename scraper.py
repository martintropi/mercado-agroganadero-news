import requests
from bs4 import BeautifulSoup
import json

def scraping_infocampo():
    url = "https://www.infocampo.com.ar/category/ganaderia/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        noticias_list = []

        # Infocampo organiza sus noticias en etiquetas <article>
        articulos = soup.find_all('article', limit=6)

        for art in articulos:
            # Buscamos el link y el título dentro del artículo
            h2_tag = art.find('h2')
            a_tag = art.find('a')
            
            if h2_tag and a_tag:
                titulo = h2_tag.get_text(strip=True)
                link = a_tag['href']
                
                noticias_list.append({
                    "titulo": titulo,
                    "url": link
                })

        # Si el método anterior falla, probamos con una clase común en su diseño
        if not noticias_list:
            items = soup.select('.post-item', limit=6)
            for item in items:
                link = item.find('a')
                if link:
                    noticias_list.append({
                        "titulo": link.get_text(strip=True),
                        "url": link['href']
                    })

        # Guardar en JSON
        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"ÉXITO: {len(noticias_list)} noticias de Infocampo guardadas.")

    except Exception as e:
        print(f"Error en Infocampo: {e}")

if __name__ == "__main__":
    scraping_infocampo()
