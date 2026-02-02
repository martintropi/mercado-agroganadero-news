import requests
from bs4 import BeautifulSoup
import json

def scraping_agrofy():
    url = "https://news.agrofy.com.ar/ganaderia"
    # Headers más completos para parecer un navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        noticias_list = []

        # Buscamos todos los links que tengan '/ganaderia/' en la URL
        for link in soup.find_all('a', href=True):
            href = link['href']
            texto = link.get_text(strip=True)
            
            # Filtro: debe ser de ganadería, tener un texto largo (el título) 
            # y no ser el link a la categoría misma
            if "/ganaderia/" in href and len(texto) > 25:
                full_url = href if href.startswith('http') else f"https://news.agrofy.com.ar{href}"
                
                # Evitar duplicados
                if not any(n['url'] == full_url for n in noticias_list):
                    noticias_list.append({
                        "titulo": texto,
                        "url": full_url
                    })
            
            if len(noticias_list) >= 6: break

        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(noticias_list, f, ensure_ascii=False, indent=4)
        
        print(f"Resultado: {len(noticias_list)} noticias encontradas.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scraping_agrofy()
