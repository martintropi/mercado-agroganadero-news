import requests
from bs4 import BeautifulSoup
import json
import re

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

        # Infocampo usa una estructura de Elementor para sus listados
        # Buscamos los artículos dentro del feed principal
        articulos = soup.find_all('article', limit=15)

        for art in articulos:
            # 1. Extraer Título y Link
            # Usualmente el título está en un h2 o h3 dentro del article
            h_tag = art.find(['h2', 'h3'])
            a_tag = art.find('a', href=True)
            
            if h_tag and a_tag:
                titulo = h_tag.get_text(strip=True)
                link = a_tag['href']
                
                # 2. Extraer Imagen
                img_tag = art.find('img')
                img_url = ""
                if img_tag:
                    # Intentamos obtener la imagen real (evitando lazy load)
                    img_url = (img_tag.get('data-src') or 
                               img_tag.get('src') or 
                               img_tag.get('srcset', '').split(' ')[0])

                # 3. Filtros: Que sea de ganadería y no sea una categoría
                if "/ganaderia/" in link and "/category/" not in link:
                    # Evitar duplicados
                    if not any(n['url'] == link for n in noticias_list):
                        noticias_list.append({
                            "titulo": titulo,
                            "url": link,
                            "imagen": img_url
                        })
            
            if len(noticias_list) >= 6:
                break

        # Guardar en archivo
        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"ÉXITO: {len(noticias_list)} noticias de ganadería con imagen guardadas.")

    except Exception as e:
        print(f"Error técnico: {e}")

if __name__ == "__main__":
    scraping_infocampo()
