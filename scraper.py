import requests
from bs4 import BeautifulSoup
import json
import re

def scraping_agrofy():
    url = "https://news.agrofy.com.ar/ganaderia"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        noticias_list = []

        # Intentamos extraer datos del script JSON interno del sitio (__NEXT_DATA__)
        script_tag = soup.find('script', id='__NEXT_DATA__')
        
        if script_tag:
            data = json.loads(script_tag.string)
            # Navegamos la estructura interna de Agrofy
            items = data.get('props', {}).get('pageProps', {}).get('posts', [])
            
            for post in items[:6]:
                noticias_list.append({
                    "titulo": post.get('title'),
                    "url": f"https://news.agrofy.com.ar{post.get('url')}"
                })
        
        # Si el método anterior falla, usamos una búsqueda de emergencia por texto
        if not noticias_list:
            for link in soup.find_all('a', href=True):
                href = link['href']
                texto = link.get_text(strip=True)
                if "/ganaderia/" in href and len(texto) > 30:
                    url_full = href if href.startswith('http') else f"https://news.agrofy.com.ar{href}"
                    if not any(n['url'] == url_full for n in noticias_list):
                        noticias_list.append({"titulo": texto, "url": url_full})
                if len(noticias_list) >= 6: break

        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"Resultado final: {len(noticias_list)} noticias encontradas.")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    scraping_agrofy()
