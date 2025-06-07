from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from cineTogether.models.watchlist_model import Watchlist
from cineTogether.models.movie_model import Movie

apiWatchlists = Blueprint("apiWatchlists", __name__, url_prefix="/api/watchlists")

# ------------------ WATCList'e Film Ekle ------------------
@apiWatchlists.route("/add", methods=["POST"])
@jwt_required()
def add_to_watchlist():
    try:
        user_id = get_jwt_identity()
        movie_id = request.form.get("movie_id")

        if not movie_id:
            return jsonify({"success": False, "message": "movie_id is required"}), 400

        if not Movie.get_by_id(movie_id):
            return jsonify({"success": False, "message": "Movie not found"}), 404

        added = Watchlist.add(user_id=user_id, movie_id=movie_id)
        if not added:
            return jsonify({"success": False, "message": "Movie already in watchlist"}), 400

        return jsonify({"success": True, "message": "Movie added to watchlist"}), 201

    except Exception as e:
        print("ERROR in add_to_watchlist:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


# ------------------ WATCList'ten Film Sil ------------------
@apiWatchlists.route("/remove", methods=["POST"])
@jwt_required()
def remove_from_watchlist():
    try:
        user_id = get_jwt_identity()
        movie_id = request.form.get("movie_id")

        if not movie_id:
            return jsonify({"success": False, "message": "movie_id is required"}), 400

        removed = Watchlist.remove(user_id=user_id, movie_id=movie_id)
        if not removed:
            return jsonify({"success": False, "message": "Movie not in watchlist"}), 404

        return jsonify({"success": True, "message": "Movie removed from watchlist"}), 200

    except Exception as e:
        print("ERROR in remove_from_watchlist:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


# ------------------ KULLANICININ WATCHLIST'İNİ GETİR ------------------
@apiWatchlists.route("/user/<int:user_id>", methods=["GET"])
def get_user_watchlist(user_id):
    try:
        entries = Watchlist.get_by_user(user_id)
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
                    "added_at": entry.added_at
                })

        return jsonify({
            "success": True,
            "user_id": user_id,
            "watchlist": movies,
            "count": len(movies)
        })

    except Exception as e:
        print("ERROR in get_user_watchlist:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
