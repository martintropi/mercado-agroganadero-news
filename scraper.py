import requests
import json
import re

def scraping_agrofy():
    # URL directa de la sección
    url = "https://news.agrofy.com.ar/ganaderia"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9"
    }

    try:
        # 1. Descargamos el contenido crudo
        response = requests.get(url, headers=headers, timeout=30)
        content = response.text
        
        noticias_list = []

        # 2. Buscamos el bloque JSON interno que Agrofy SIEMPRE carga (Next.js)
        # Este bloque contiene los datos reales antes de que se arme la web
        match = re.search(r'\{"title":"[^"]*","url":"/ganaderia/[^"]*"\}', content)
        
        # Buscamos todos los pares de Título y URL usando una expresión regular global
        # Patrón: busca "title":"(texto)","url":"(link)"
        noticias_encontradas = re.findall(r'\{"title":"([^"]*)","url":"(/ganaderia/[^"]*)"\}', content)

        for titulo, link in noticias_encontradas:
            full_url = f"https://news.agrofy.com.ar{link}"
            
            # Evitar duplicados y filtrar ruidos
            if not any(n['url'] == full_url for n in noticias_list):
                # Limpiar caracteres unicode si aparecen
                titulo_limpio = titulo.encode().decode('unicode-escape') if '\\u' in titulo else titulo
                noticias_list.append({
                    "titulo": titulo_limpio,
                    "url": full_url
                })
            
            if len(noticias_list) >= 6:
                break

        # 3. Guardar resultado
        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"Resultado: {len(noticias_list)} noticias procesadas.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scraping_agrofy()
