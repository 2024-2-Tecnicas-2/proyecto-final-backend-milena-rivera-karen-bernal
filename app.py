import time
import base64
import requests
from flask import Flask, render_template, session, redirect, url_for, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# Configuración de Spotify
CLIENT_ID = '6db15bf148f84955a0dbc49f29d637e0'
CLIENT_SECRET = 'f8a01a01a9884b9496ad8dde3e58349c'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPE = 'user-top-read playlist-modify-public user-library-read'

# Asegúrate de usar una clave secreta de Flask para las sesiones
app.secret_key = 'your_flask_secret_key'

# Autenticación de Spotify
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)

# Función para refrescar el token de acceso
def refresh_access_token(refresh_token):
    token_url = "https://accounts.spotify.com/api/token"
    
    # Preparar la autenticación básica de Spotify
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    
    if response.status_code == 200:
        new_tokens = response.json()
        return new_tokens['access_token']
    else:
        print("Error al refrescar el token:", response.status_code)
        return None

# Función para obtener el token de acceso desde la sesión o refrescarlo si ha expirado
def get_spotify_token():
    token_info = session.get("token_info")
    if token_info and 'expires_at' in token_info and token_info['expires_at'] < time.time():
        # Si el token ha expirado, lo refrescamos
        new_access_token = refresh_access_token(token_info['refresh_token'])
        if new_access_token:
            token_info['access_token'] = new_access_token
            token_info['expires_at'] = time.time() + 3600  # El token expira en 1 hora
            session['token_info'] = token_info  # Guardamos el nuevo token en la sesión

    # Si el token está válido, lo devolvemos
    return token_info['access_token'] if token_info else None

# Página de login (mostramos el login.html primero)
@app.route('/login')
def login():
    # Aquí puedes mostrar la página de login antes de la redirección
    return render_template('login.html')

# Redirigir a Spotify para la autenticación
@app.route('/authenticate')
def authenticate():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# Callback de Spotify (maneja el código de autorización y obtiene el token)
@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    return redirect(url_for('index'))

@app.route('/index')
def index():
    # Verificar si el usuario está autenticado
    if not session.get("token_info"):
        return redirect(url_for('login'))

    # Obtener el token de acceso
    access_token = get_spotify_token()
    if not access_token:
        return "No se pudo obtener un token válido", 401

    # Crear objeto de Spotify usando el token de acceso
    sp = spotipy.Spotify(auth=access_token)

    try:
        # Obtener información básica del usuario
        user_info = sp.current_user()  # Esta llamada obtiene información sobre el usuario
        
        # Obtener las recomendaciones basadas en las canciones más escuchadas
        top_tracks = sp.current_user_top_tracks(limit=10)
        top_artists = sp.current_user_top_artists(limit=10)
        
        tracks = [{'name': track['name'], 'artists': track['artists']} for track in top_tracks['items']]
        artists = [{'name': artist['name'], 'id': artist['id']} for artist in top_artists['items']]
        
        # Obtener recomendaciones de artistas
        artist_recommendations = []
        for artist in artists:
            recommendations = sp.recommendations(seed_artists=[artist['id']], limit=5)
            artist_recommendations.extend([{
                'name': track['name'],
                'artists': track['artists'],
                'album': track['album']['name']
            } for track in recommendations['tracks']])
        
        # Eliminar duplicados de recomendaciones
        artist_recommendations = list({v['name']: v for v in artist_recommendations}.values())
    
    except Exception as e:
        print("Error al obtener recomendaciones:", e)
        user_info = None  # Si ocurre un error, evitamos mostrar la info del usuario
        tracks = []
        artist_recommendations = []

    # Enviar la información de usuario y recomendaciones a la plantilla
    return render_template('index.html', recommendations=tracks, artist_recommendations=artist_recommendations, user_info=user_info)

# Ruta por defecto que redirige a la página de login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
