import requests
from bs4 import BeautifulSoup
import json

def scraping_agrofy():
    # El Feed RSS sigue siendo la mejor opción
    url = "https://news.agrofy.com.ar/ganaderia/feed"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        # Usamos 'html.parser' que SIEMPRE está disponible en Python
        soup = BeautifulSoup(response.content, "html.parser")
        
        noticias_list = []
        # En RSS, las noticias están dentro de etiquetas <item>
        items = soup.find_all('item')

        for item in items[:6]:
            # Buscamos el título y el link ignorando mayúsculas/minúsculas
            titulo = item.find('title').get_text() if item.find('title') else "Sin título"
            link = item.find('link').get_text() if item.find('link') else ""
            
            if titulo and link:
                noticias_list.append({
                    "titulo": titulo.strip(),
                    "url": link.strip()
                })

        # Si el parser de HTML no vio los <item>, intentamos una búsqueda manual
        if not noticias_list:
            import re
            titulos = re.findall(r'<title>(.*?)</title>', response.text)
            links = re.findall(r'<link>(.*?)</link>', response.text)
            # El primer título/link suele ser del sitio, los siguientes son noticias
            for t, l in zip(titulos[1:7], links[1:7]):
                noticias_list.append({"titulo": t, "url": l})

        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"ÉXITO: {len(noticias_list)} noticias procesadas.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scraping_agrofy()
