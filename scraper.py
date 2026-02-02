import requests
from bs4 import BeautifulSoup
import json

def scraping_infocampo():
    # URL específica de Ganadería
    url = "https://www.infocampo.com.ar/category/ganaderia/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        noticias_list = []

        # 1. Apuntamos al contenedor principal de notas para NO traer el clima o laterales
        # Infocampo suele usar esta clase para el listado central
        contenedor_principal = soup.find('div', class_='elementor-posts-container') or soup

        # 2. Buscamos cada artículo dentro de ese contenedor
        articulos = contenedor_principal.find_all(['article', 'div'], class_=re.compile(r'post|item'), limit=15)

        for art in articulos:
            a_tag = art.find('a', href=True)
            img_tag = art.find('img')
            
            if a_tag:
                # El título suele estar en un <h2> o en el texto del link
                h2 = art.find('h2')
                titulo = h2.get_text(strip=True) if h2 else a_tag.get_text(strip=True)
                link = a_tag['href']
                
                # --- LÓGICA DE IMAGEN ---
                img_url = ""
                if img_tag:
                    # Buscamos en orden de prioridad para evitar el 'lazy load' (imágenes que cargan después)
                    img_url = (img_tag.get('data-src') or 
                               img_tag.get('src') or 
                               img_tag.get('srcset', '').split(' ')[0])

                # --- FILTROS CRÍTICOS ---
                # 1. Que el título no sea muy corto
                # 2. Que NO sea una categoría
                # 3. Que NO sea clima (a menos que esté en ganadería)
                if len(titulo) > 30 and "/category/" not in link:
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
        
        print(f"ÉXITO: {len(noticias_list)} noticias de GANADERÍA con imagen guardadas.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import re # Necesario para el re.compile
    scraping_infocampo()
