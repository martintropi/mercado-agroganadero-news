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

        # Buscamos TODOS los enlaces <a> en la página
        enlaces = soup.find_all('a', href=True)

        for link in enlaces:
            url_noticia = link['href']
            # Filtro: debe tener 'ganaderia' en la URL y el texto debe ser largo (un título)
            # También evitamos que sea solo el link a la categoría
            titulo = link.get_text(strip=True)
            
            if "/ganaderia/" in url_noticia and len(titulo) > 30:
                # Evitar que se guarden repetidos
                if not any(n['url'] == url_noticia for n in noticias_list):
                    noticias_list.append({
                        "titulo": titulo,
                        "url": url_noticia
                    })
            
            # Frenamos cuando tengamos 6
            if len(noticias_list) >= 6:
                break

        # Guardar en archivo
        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"ÉXITO: {len(noticias_list)} noticias de Infocampo guardadas.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scraping_infocampo()
