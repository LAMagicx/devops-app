def sort_desc(Key):
    """Cette fonction trie les collones dans l'ordre décroissant si possible."""
    # print(f"Key: {key}")  # Ajouter du débogage pour voir la clé

    keys = ['msPlayed','danceability','energy','loudness','speechiness','acousticness','instrumentalness','acousticness','liveness','valence','tempo','duration_ms']

    if Key in keys:
        data = list(db.spotify.find().sort({Key : -1}).limit(20))
        return render_template_string(TEMPLATE, tri_desc=data)