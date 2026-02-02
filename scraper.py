import requests
import json

def scraping_agrofy():
    # Consultamos directamente a la API de contenido de Agrofy
    # Esta URL devuelve un JSON puro con las últimas noticias
    api_url = "https://news.agrofy.com.ar/_next/data/latest/ganaderia.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=20)
        
        # Si la API directa falla (a veces el token 'latest' cambia), usamos el respaldo
        if response.status_code != 200:
            print(f"API principal falló ({response.status_code}), intentando método alternativo...")
            # Intentamos la URL normal pero pidiendo solo el contenido JSON
            response = requests.get("https://news.agrofy.com.ar/ganaderia", headers=headers)
        
        noticias_list = []
        
        # Intentamos extraer del JSON de la respuesta
        try:
            data = response.json()
            # Navegamos la estructura de datos de Next.js
            posts = data.get('pageProps', {}).get('posts', [])
            for p in posts[:6]:
                noticias_list.append({
                    "titulo": p.get('title'),
                    "url": f"https://news.agrofy.com.ar{p.get('url')}"
                })
        except:
            # Si no es un JSON directo, buscamos el bloque dentro del HTML
            import re
            match = re.search(r'id="__NEXT_DATA__"[^>]*>({.*?})</script>', response.text)
            if match:
                data = json.loads(match.group(1))
                posts = data.get('props', {}).get('pageProps', {}).get('posts', [])
                for p in posts[:6]:
                    noticias_list.append({
                        "titulo": p.get('title'),
                        "url": f"https://news.agrofy.com.ar{p.get('url')}"
                    })

        # Guardar en archivo
        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        if noticias_list:
            print(f"¡LOGRADO! {len(noticias_list)} noticias guardadas.")
        else:
            print("No se encontraron noticias en la estructura de datos.")

    except Exception as e:
        print(f"Error técnico: {e}")

if __name__ == "__main__":
    scraping_agrofy()
