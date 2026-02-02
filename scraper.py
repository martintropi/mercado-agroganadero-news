import requests
import json
import re

def scraping_infocampo():
    url = "https://www.infocampo.com.ar/category/ganaderia/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        print(f"Iniciando descarga de: {url}")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        content = response.text
        
        noticias_list = []

        # Buscamos enlaces que tengan la estructura de una noticia (slugs largos)
        # El patrón busca enlaces que terminen en / y filtramos los que no son noticias
        links_encontrados = re.findall(r'href="(https://www.infocampo.com.ar/[a-z0-9-]+/)"', content)
        
        for url_noticia in links_encontrados:
            # Filtros para ignorar páginas que no son noticias
            basura = ['/category/', '/tag/', '/contacto/', '/politicas/', '/publicidad/']
            if any(x in url_noticia for x in basura):
                continue
                
            # Extraemos el 'slug' de la URL para crear un título limpio
            # Ejemplo: /vacunas-para-ganado/ -> Vacunas para ganado
            slug = url_noticia.split('/')[-2]
            
            if len(slug) > 25: # Una noticia real suele tener un slug largo
                titulo_deducido = slug.replace('-', ' ').capitalize()
                
                if not any(n['url'] == url_noticia for n in noticias_list):
                    noticias_list.append({
                        "titulo": titulo_deducido,
                        "url": url_noticia
                    })
            
            if len(noticias_list) >= 6:
                break

        # Guardar en archivo JSON
        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"ÉXITO: {len(noticias_list)} noticias de Infocampo guardadas.")

    except Exception as e:
        print(f"Error técnico: {e}")

if __name__ == "__main__":
    scraping_infocampo()
