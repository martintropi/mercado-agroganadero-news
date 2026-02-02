import requests
import json
import re

def scraping_agrofy():
    # URL de Agrofy pasada por el traductor de Google para saltar el bloqueo de IP
    proxy_url = "https://translate.google.com/translate?sl=auto&tl=en&u=https://news.agrofy.com.ar/ganaderia"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(proxy_url, headers=headers, timeout=30)
        html = response.text
        noticias_list = []

        # Usamos EXPRESIONES REGULARES: Buscamos cualquier cosa que parezca un link de noticia
        # Patrón: busca hrefs que tengan 'ganaderia' y captura el texto que le sigue
        pattern = r'href="([^"]*ganaderia/[^"]*)"[^>]*>(.*?)</a>'
        matches = re.findall(pattern, html)

        for link, texto in matches:
            # Limpiamos el texto de etiquetas HTML
            clean_text = re.sub('<[^<]+?>', '', texto).strip()
            
            # Filtramos: texto con contenido real y que no sea repetido
            if len(clean_text) > 35:
                # Limpiar la URL de restos de Google Translate
                clean_url = link.split('&')[0].replace('https://translate.google.com/website?sl=auto&tl=en&u=', '')
                if not clean_url.startswith('http'):
                    clean_url = "https://news.agrofy.com.ar" + clean_url

                if not any(n['titulo'] == clean_text for n in noticias_list):
                    noticias_list.append({
                        "titulo": clean_text,
                        "url": clean_url
                    })
            
            if len(noticias_list) >= 6:
                break

        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"Resultado: {len(noticias_list)} noticias extraídas mediante proxy.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scraping_agrofy()
