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

        # Buscamos específicamente los divs con clase 'nota'
        notas = soup.find_all('div', class_='nota', limit=10)

        for nota in notas:
            # 1. Extraer Título y Link (están dentro del h3 -> a)
            bloque_texto = nota.find('div', class_='texto data')
            if bloque_texto:
                h3_tag = bloque_texto.find('h3')
                a_tag = h3_tag.find('a') if h3_tag else None
                
                if a_tag:
                    titulo = a_tag.get_text(strip=True)
                    link = a_tag['href']
                    
                    # 2. Extraer Imagen (está dentro del div 'imagen' -> img)
                    img_url = ""
                    bloque_img = nota.find('div', class_='imagen')
                    if bloque_img:
                        img_tag = bloque_img.find('img')
                        if img_tag:
                            # Priorizamos data-src por el lazy loading, sino src
                            img_url = img_tag.get('data-src') or img_tag.get('src') or ""

                    # Evitar duplicados y asegurar que no sea un link vacío
                    if link and not any(n['url'] == link for n in noticias_list):
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
        
        print(f"ÉXITO: {len(noticias_list)} noticias extraídas con la nueva estructura.")

    except Exception as e:
        print(f"Error técnico: {e}")

if __name__ == "__main__":
    scraping_infocampo()
