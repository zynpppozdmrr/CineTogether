import requests
from cineTogether import createApp, db
from cineTogether.models.movie_model import Movie

app = createApp()
app.app_context().push()

url = "https://imdb-top-100-movies.p.rapidapi.com/"

headers = {
    "x-rapidapi-key": "4237873a6bmsh745ce4400daca11p145b2cjsn2916195cd44f",
    "x-rapidapi-host": "imdb-top-100-movies.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("❌ API bağlantı hatası:", response.status_code)
    exit()

movies = response.json()

for m in movies:
    try:
        if Movie.query.filter_by(title=m.get("title")).first():
            continue

        genres = m.get("genre")
        if isinstance(genres, list):
            genres = ", ".join(genres)

        movie_data = {
            "rank": int(m.get("rank", 0)),
            "title": m.get("title"),
            "description": m.get("description", ""),
            "year": int(m.get("year", 2000)),
            "rating": float(m.get("rating", 0.0)),
            "genre": genres,
            "image": m.get("image"),
            "imdbid": m.get("imdbid"),
            "imdb_link": m.get("imdb_link")
        }

        Movie.add_movie(**movie_data)
        print(f"✅ Eklendi: {movie_data['title']}")

    except Exception as e:
        print(f"⚠️ Hata ({m.get('title')}):", e)
