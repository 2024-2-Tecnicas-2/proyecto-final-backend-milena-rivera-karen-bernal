import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuración de la autenticación con la API de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='T4e6c49d6d9f043f9ad878cb8d1fb1b1f',  # Reemplaza con tu Client ID de Spotify
    client_secret='e12c8847596942be99f5938e44b34b42T',  # Reemplaza con tu Client Secret
    redirect_uri='https://developer.spotify.com/documentation/web-api/reference/get-playlist',  # La URI de redirección 
    scope='playlist-read-private user-read-private'
))

# Endpoint para obtener recomendaciones musicales
@app.route('/api/recommendations', methods=['GET'])
def obtener_recomendaciones():
    seed_artists = request.args.get('seed_artists', '4NHQUGzhtTLFvgF5SZesLK')  # Artista por defecto
    seed_genres = request.args.get('seed_genres', 'classical,country')  # Géneros por defecto
    seed_tracks = request.args.get('seed_tracks', '0c6xIDDpzE81m2q797ordA')  # Pista por defecto
    limit = request.args.get('limit', 10)  # Límite por defecto de recomendaciones
    mercado = request.args.get('market', 'ES')  # Mercado por defecto

    try:
        # Llamada a la API de Spotify para obtener recomendaciones
        recomendaciones = sp.recommendations(
            seed_artists=[seed_artists],
            seed_genres=seed_genres.split(','),
            seed_tracks=[seed_tracks],
            limit=limit,
            market=mercado
        )
        return jsonify(recomendaciones)  # Devolver la respuesta en formato JSON
    except spotipy.SpotifyException as e:
        return jsonify({'error': str(e)}), 400  # Manejo de errores

# Endpoint para obtener una lista de reproducción por su ID
@app.route('/api/playlist/<playlist_id>', methods=['GET'])
def obtener_playlist(playlist_id):
    mercado = request.args.get('mercado', 'ES')  # Mercado por defecto 'ES'
    campos = 'items(added_by.id,track(name,href,album(name,href)))'  # Campos a devolver

    try:
        # Llamada a la API de Spotify para obtener la lista de reproducción
        playlist = sp.playlist(
            playlist_id=playlist_id,
            market=mercado,
            fields=campos
        )
        return jsonify(playlist)  # Devolver la respuesta en formato JSON
    except spotipy.SpotifyException as e:
        return jsonify({'error': str(e)}), 400  # Manejo de errores

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)
