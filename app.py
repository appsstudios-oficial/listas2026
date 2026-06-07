import requests
import base64
from flask import Flask, Response, request

app = Flask(__name__)

URL_CIFRADA = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2FwcHNzdHVkaW9zLW9maWNpYWwvbGlzdGFzMjAyNi9tYWluL2p1bmlvMjAyNi5tM3U="
CLAVE_ACCESO = "MiTele2026"

@app.route('/lista.m3u')
def obtener_lista():
    clave_recibida = request.args.get('clave')
    if clave_recibida != CLAVE_ACCESO:
        return "No encontrado", 404

    user_agent = request.headers.get('User-Agent', '').lower()
    
    navegadores_web = ['chrome', 'edge', 'firefox', 'opera']
    if any(nav in user_agent for nav in navegadores_web) and not any(rep in user_agent for rep in ['vlc', 'smarters', 'iptv']):
        return "<h1>404 Not Found</h1>The server can not find the requested page.", 404

    try:
        url_real = base64.b64decode(URL_CIFRADA.encode('utf-8')).decode('utf-8')
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_real, headers=headers)
        
        return Response(response.text, mimetype='text/plain')
    except Exception as e:
        return "Error interno", 500

if __name__ == "__main__":
    app.run()
