from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from cineTogether.models.rating_model import Rating
from cineTogether.models.movie_model import Movie

apiRatings = Blueprint("apiRatings", __name__, url_prefix="/api/ratings")


# ------------------ FİLME PUAN VER ------------------
@apiRatings.route("/", methods=["POST"])
@jwt_required()
def add_rating():
    try:
        user_id = get_jwt_identity()
        movie_id = request.form.get("movie_id")
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        if not movie_id or not rating:
            return jsonify({"success": False, "message": "movie_id and rating are required"}), 400

        try:
            rating = float(rating)
            if rating < 1 or rating > 10:
                return jsonify({"success": False, "message": "Rating must be between 1 and 10"}), 400
        except ValueError:
            return jsonify({"success": False, "message": "Rating must be a number"}), 400

        # Film var mı kontrol et
        if not Movie.get_by_id(movie_id):
            return jsonify({"success": False, "message": "Movie not found"}), 404

        new_rating = Rating.add_rating(user_id=user_id, movie_id=movie_id, rating=rating, comment=comment)
        if not new_rating:
            return jsonify({"success": False, "message": "You have already rated this movie"}), 400

        return jsonify({
            "success": True,
            "message": "Rating added",
            "rating": {
                "movie_id": movie_id,
                "user_id": user_id,
                "rating": rating,
                "comment": comment
            }
        }), 201

    except Exception as e:
        print("ERROR in add_rating:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


# ------------------ Filmin tüm puanlarını getir ------------------

@apiRatings.route("/movie/<int:movie_id>", methods=["GET"])
def get_movie_ratings(movie_id):
    try:
        ratings = Rating.get_ratings_by_movie(movie_id)
        result = [{
            "user_id": r.user_id,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at
        } for r in ratings]

        return jsonify({
            "success": True,
            "movie_id": movie_id,
            "ratings": result,
            "count": len(result)
        })

    except Exception as e:
        print("ERROR in get_movie_ratings:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
    
    
# ------------------ Filmin ortalama puanını getir ------------------
@apiRatings.route("/movie/<int:movie_id>/average", methods=["GET"])
def get_average_rating(movie_id):
    try:
        avg = Rating.get_average_rating(movie_id)
        return jsonify({
            "success": True,
            "movie_id": movie_id,
            "average_rating": avg
        })
    except Exception as e:
        print("ERROR in get_average_rating:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500

# ------------------ Kullanıcının tüm puanlarını getir ------------------
@apiRatings.route("/user/<int:user_id>", methods=["GET"])
def get_user_ratings(user_id):
    try:
        ratings = Rating.query.filter_by(user_id=user_id).all()
        result = [{
            "movie_id": r.movie_id,
            "movie_title": Movie.get_by_id(r.movie_id).title,
            "user_rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at
        } for r in ratings]

        return jsonify({
            "success": True,
            "user_id": user_id,
            "watch_history": result,
            "count": len(result)
        })
    except Exception as e:
        print("ERROR in get_user_ratings:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
