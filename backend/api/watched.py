from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from cineTogether.models.watched_model import Watched
from cineTogether.models.movie_model import Movie

apiWatched = Blueprint("apiWatched", __name__, url_prefix="/api/watched")


# ------------------ FİLMİ İZLENDİ OLARAK İŞARETLE ------------------
@apiWatched.route("/add", methods=["POST"])
@jwt_required()
def add_to_watched():
    try:
        user_id = get_jwt_identity()
        movie_id = request.form.get("movie_id")

        if not movie_id:
            return jsonify({"success": False, "message": "movie_id is required"}), 400

        if not Movie.get_by_id(movie_id):
            return jsonify({"success": False, "message": "Movie not found"}), 404

        added = Watched.mark_as_watched(user_id=user_id, movie_id=movie_id)
        if not added:
            return jsonify({"success": False, "message": "Movie already marked as watched"}), 400

        return jsonify({"success": True, "message": "Movie marked as watched"}), 201

    except Exception as e:
        print("ERROR in add_to_watched:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


# ------------------ FİLMİ İZLENMEDİ OLARAK İŞARETLE (SİL) ------------------
@apiWatched.route("/remove", methods=["POST"])
@jwt_required()
def remove_from_watched():
    try:
        user_id = get_jwt_identity()
        movie_id = request.form.get("movie_id")

        if not movie_id:
            return jsonify({"success": False, "message": "movie_id is required"}), 400

        removed = Watched.unmark(user_id=user_id, movie_id=movie_id)
        if not removed:
            return jsonify({"success": False, "message": "Movie not marked as watched"}), 404

        return jsonify({"success": True, "message": "Movie removed from watched list"}), 200

    except Exception as e:
        print("ERROR in remove_from_watched:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


# ------------------ KULLANICININ TÜM İZLEDİĞİ FİLMLERİ GETİR ------------------
@apiWatched.route("/user/<int:user_id>", methods=["GET"])
def get_user_watched(user_id):
    try:
        entries = Watched.get_by_user(user_id)
        movies = []

        for entry in entries:
            movie = Movie.get_by_id(entry.movie_id)
            if movie:
                movies.append({
                    "movie_id": movie.id,
                    "title": movie.title,
                    "year": movie.year,
                    "genre": movie.genre,
                    "image": movie.image,
                    "watched_at": entry.watched_at
                })

        return jsonify({
            "success": True,
            "user_id": user_id,
            "watched": movies,
            "count": len(movies)
        })

    except Exception as e:
        print("ERROR in get_user_watched:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
