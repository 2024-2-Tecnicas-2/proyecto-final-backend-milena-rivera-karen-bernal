importar tkinter como tk
desde tkinter importar messagebox
importar spotipy
desde spotipy.oauth2 importar SpotifyOAuth
 
# Configuración de la autenticación con Spotify
def authenticate_spotify():
    prueba:
        # Configura la autenticación de Spotify con tus credenciales
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='T4e6c49d6d9f043f9ad878cb8d1fb1b1f', # Client ID de Spotify
            client_secret='e12c8847596942be99f5938e44b34b42T', # Client Secret
            redirigir_uri=' http://localhost:8888/callback' , # URI de redirección
            alcance='playlist-read-private user-read-private' # Permisos necesarios
        ))
        print("Autenticación exitosa.")
        devuelve sp
    excepto Excepción como e:
        messagebox.showerror("Error de Autenticación", f"No se pudo autenticar con Spotify: {e}")
        return Ninguno
 
# Obtención de las listas de reproducción
def get_user_playlists(sp):
    try:
        playlists = sp.current_user_playlists()['items']
        if not playlists:
            messagebox.showinfo("Información", "No se encontraron playlists.")
        return playlists
    except Excepción como e:
        messagebox.showerror("Error", f"Hubo un problema al obtener las listas de reproducción: {e}")
        return []
 
# listas de reproducción en la interfaz gráfica
def display_playlists_ui(playlists):
    # Limpiar cualquier contenido anterior en el frame izquierdo
    for widget in frame_left.winfo_children():
        widget.destroy()
 
    # Título de las listas de reproducción
    playlist_title = tk.Label(frame_left, text="PLAYLISTS", bg="green", fg="black", font=("Helvetica", 14, "bold"))
    playlist_title.pack(fill=tk.X)
 
    # Mostrar listas de reproducción en botones
    if playlists:
        for i, playlist in enumerate(playlists):
            playlist_name = playlist['name']
            # Crear un botón para cada lista de reproducción
            button = tk.Button(frame_left, text=playlist_name, width=30, bg="gray", fg="white",
                               command=lambda p=playlist_name: open_playlist(p))
            button.pack(pady=5)
 
def open_playlist(playlist_name):
    messagebox.showinfo("Lista de reproducción seleccionada", f"Se ha seleccionado la lista de reproducción: {playlist_name}")
 
# Obtener listas de reproducción y mostrarlas
def obtener_playlists(sp):
    playlists = get_user_playlists(sp)
    display_playlists_ui(playlists)
 
# Interfaz gráfica con Tkinter
def main():
    # Autenticación con Spotify
    sp = authenticate_spotify()
    if not sp:
        return
 
    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Spotify Playlist Interface")
    root.geometry("800x600") 
    root.configure(bg="black") 
 
    global frame_left
    frame_left = tk.Frame(root, bg="black")
    frame_left.pack(side=tk.LEFT, fill=tk.Y)
 
    # Botón para obtener las listas de reproducción desde Spotify
    btn_playlists = tk.Button(root, text="Obtener listas de reproducción", command=lambda: obtener_playlists(sp), width=30, height=2, bg="green", fg= "negro", fuente=("Helvetica", 12))
    btn_playlists.pack(pady=20)
 
    status_label = tk.Label(root, text="Interfaz de Spotify Lista de Reproducción", bg="black", fg="white", font=("Helvetica", 12))
    etiqueta_estado.pack(pady=10)
 
    # Iniciar la interfaz gráfica
    root.mainloop()
 
si __nombre__ == "__principal__":
    principal()
