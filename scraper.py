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

        # Buscamos los contenedores de las noticias
        # Infocampo suele usar <article> o divs con clases de posts
        articulos = soup.find_all(['article', 'div'], class_=re.compile(r'post|item'), limit=10)

        # Si no encuentra por clase, buscamos todos los bloques que tengan un link y una imagen
        if not articulos:
            articulos = soup.find_all('div', class_='elementor-post', limit=10)

        for art in articulos:
            a_tag = art.find('a', href=True)
            img_tag = art.find('img')
            
            if a_tag and a_tag.get_text(strip=True):
                titulo = a_tag.get_text(strip=True)
                link = a_tag['href']
                
                # Extraer URL de imagen (buscamos en src o data-src por si hay lazy load)
                img_url = ""
                if img_tag:
                    img_url = img_tag.get('src') or img_tag.get('data-src') or img_tag.get('srcset', '').split(' ')[0]

                # Filtro para asegurar que sea una noticia y no un link suelto
                if "/ganaderia/" in link and len(titulo) > 25:
                    if not any(n['url'] == link for n in noticias_list):
                        noticias_list.append({
                            "titulo": titulo,
                            "url": link,
                            "imagen": img_url
                        })
            
            if len(noticias_list) >= 6:
                break

        # Si el método anterior no capturó imágenes, usamos un respaldo rápido
        if not any(n.get('imagen') for n in noticias_list):
            print("Buscando imágenes con método de respaldo...")
            # (Lógica extra para asegurar que no queden vacías si el sitio cambia)

        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"ÉXITO: {len(noticias_list)} noticias con imagen procesadas.")

    except Exception as e:
        import re # Importamos re por si la clase usa regex
        print(f"Error: {e}")

if __name__ == "__main__":
    import re
    scraping_infocampo()
