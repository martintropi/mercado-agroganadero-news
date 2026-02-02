import requests
import json
import re

def scraping_infocampo():
    # URL de la sección ganadería
    url = "https://www.infocampo.com.ar/category/ganaderia/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        content = response.text
        noticias_list = []

        # BUSQUEDA POR PATRÓN: Buscamos URLs que terminen en "/" (como las noticias de Infocampo)
        # y que tengan un texto largo asociado.
        # Este patrón busca: <a href="URL">TITULO</a>
        matches = re.findall(r'href="(https://www.infocampo.com.ar/[^"]+/)"[^>]*>([^<]{35,})</a>', content)

        for url_noticia, titulo in matches:
            # Limpiamos el título de espacios o restos de HTML
            titulo_clean = titulo.strip()
            
            # Filtro: Evitar que sea la misma categoría y evitar duplicados
            if "/category/" not in url_noticia and not any(n['url'] == url_noticia for n in noticias_list):
                noticias_list.append({
                    "titulo": titulo_clean,
                    "url": url_noticia
                })
            
            if len(noticias_list) >= 6:
                break

        # Si el anterior falló, intentamos una búsqueda más agresiva en el texto
        if not noticias_list:
            # Buscamos cualquier link que tenga palabras separadas por guiones (típico de noticias)
            links_emergencia = re.findall(r'https://www.infocampo.com.ar/[a-z0-9-]+/', content)
            for l in links_emergencia:
                if "/category/" not in l and len(l) > 40:
                    # Intentamos inventar un título basado en la URL para no dejarlo vacío
                    tit = l.split('/')[-2].replace('-', ' ').capitalize()
                    if not any(n['url'] == l for n in noticias_list):
                        noticias_list.append({"titulo": tit, "url": l})
                if len(noticias_list) >= 6: break

        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"ÉXITO: {len(noticias_list)} noticias de Infocampo guardadas.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scraping_infocampo()
