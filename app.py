import os
import re
from urllib.parse import urlparse
import requests
from flask import Flask, Response

app = Flask(__name__)

# Enlace RAW de tu lista real en GitHub
URL_LISTA_GITHUB = "https://raw.githubusercontent.com/appsstudios-oficial/listas2026/refs/heads/main/junio2026.m3u"

def ip_a_decimal(ip):
    """Transforma una IP como 181.224.255.210 en un número entero gigante"""
    try:
        octetos = list(map(int, ip.split('.')))
        return (octetos[0] << 24) + (octetos[1] << 16) + (octetos[2] << 8) + octetos[3]
    except:
        return None

def ofuscar_url(url):
    """Busca si el enlace usa IP y la transforma para ofuscarla"""
    try:
        parsed = urlparse(url)
        host = parsed.hostname
        
        # Verificamos si el host es una dirección IP (números y puntos)
        if host and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host):
            ip_decimal = ip_a_decimal(host)
            if ip_decimal:
                # Reemplazamos la IP por el número decimal en el enlace
                nuevo_netloc = f"{ip_decimal}"
                if parsed.port:
                    nuevo_netloc += f":{parsed.port}"
                nuevo_url = parsed._replace(netloc=nuevo_netloc).geturl()
                return nuevo_url
        return url
    except:
        return url

@app.route('/lista.m3u')
def obtener_lista_ofuscada():
    try:
        # Descargamos tu lista real desde GitHub en memoria
        respuesta = requests.get(URL_LISTA_GITHUB, timeout=10)
        if respuesta.status_code != 200:
            return "Error al obtener la lista de GitHub", 500
        
        lineas = respuesta.text.splitlines()
        lista_final = []
        
        # Procesamos línea por línea
        for linea in lineas:
            # Quitamos espacios invisibles al principio y final
            linea_limpia = linea.strip()
            
            # Si la línea es un enlace HTTP, intentamos ofuscarlo
            if linea_limpia.startswith("http://") or linea_limpia.startswith("https://"):
                linea_ofuscada = ofuscar_url(linea_limpia)
                lista_final.append(linea_ofuscada)
            else:
                # Si es una etiqueta (#EXTINF, #EXTM3U), la dejamos igual
                lista_final.append(linea)
                
        contenido_m3u = "\n".join(lista_final)
        
        # Se la entregamos al reproductor como un archivo M3U válido
        return Response(contenido_m3u, mimetype='application/x-mpegurl')
        
    except Exception as e:
        return f"Error en el servidor: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
