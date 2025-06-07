from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from cineTogether.models.movie_model import Movie
from cineTogether.models.user_model import User
from sqlalchemy import func

apiMovies = Blueprint("apiMovies", __name__, url_prefix="/api/movies")


from flask import Blueprint, jsonify
from cineTogether.models.movie_model import Movie

apiMovies = Blueprint("apiMovies", __name__, url_prefix="/api/movies")

# ------------------ TÜM FİLMLERİ GETİR ------------------
@apiMovies.route("/", methods=["GET"])
def get_all_movies():
    try:
        movies = Movie.get_all()
        result = [{
            "id": m.id,
            "rank": m.rank,
            "title": m.title,
            "description": m.description,
            "year": m.year,
            "rating": m.rating,
            "genre": m.genre,
            "image": m.image,
            "imdbid": m.imdbid,
            "imdb_link": m.imdb_link
        } for m in movies]

        return jsonify({
            "success": True,
            "count": len(result),
            "movies": result
        })

    except Exception as e:
        print("ERROR in get_all_movies():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
    

# ----------------------------Belirli bir filmi ID ile getir--------------------
@apiMovies.route("/<int:id>", methods=["GET"])
def get_movie_by_id(id):
    try:
        movie = Movie.get_by_id(id)
        if not movie:
            return jsonify({"success": False, "message": "Movie not found"}), 404

        return jsonify({
            "success": True,
            "movie": {
                "id": movie.id,
                "rank": movie.rank,
                "title": movie.title,
                "description": movie.description,
                "year": movie.year,
                "rating": movie.rating,
                "genre": movie.genre,
                "image": movie.image,
                "imdbid": movie.imdbid,
                "imdb_link": movie.imdb_link
            }
        })

    except Exception as e:
        print("ERROR in get_movie_by_id():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
    



#-----------------Başlığa göre arama---------------------------------

@apiMovies.route("/search", methods=["GET"])
def search_movies_by_title():
    try:
        query = request.args.get("title", "")
        if not query:
            return jsonify({"success": False, "message": "Search query is missing"}), 400

        # Case-insensitive arama
        movies = Movie.query.filter(func.lower(Movie.title).like(f"%{query.lower()}%")).all()

        result = [{
            "id": m.id,
            "title": m.title,
            "year": m.year,
            "rating": m.rating,
            "genre": m.genre,
            "image": m.image
        } for m in movies]

        return jsonify({
            "success": True,
            "query": query,
            "count": len(result),
            "movies": result
        })

    except Exception as e:
        print("ERROR in search_movies_by_title():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500




#-----------------Genre'ye göre filtreleme---------------------------------

@apiMovies.route("/filter", methods=["GET"])
def filter_movies_by_genre():
    try:
        genre_query = request.args.get("genre", "")
        if not genre_query:
            return jsonify({"success": False, "message": "Genre query is missing"}), 400

        # Veritabanındaki genre alanı: "Drama, Action"
        movies = Movie.query.filter(Movie.genre.ilike(f"%{genre_query}%")).all()

        result = [{
            "id": m.id,
            "title": m.title,
            "year": m.year,
            "rating": m.rating,
            "genre": m.genre,
            "image": m.image
        } for m in movies]

        return jsonify({
            "success": True,
            "genre": genre_query,
            "count": len(result),
            "movies": result
        })

    except Exception as e:
        print("ERROR in filter_movies_by_genre():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500

