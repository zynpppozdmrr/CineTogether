
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from cineTogether.models.recommendation_model import Recommendation
from cineTogether.models.movie_model import Movie

apiRecommendations = Blueprint("apiRecommendations", __name__, url_prefix="/api/recommendations")

@apiRecommendations.route("/", methods=["GET"])
@jwt_required()
def get_user_recommendations():
    try:
        user_id = get_jwt_identity()
        Recommendation.generate_for_user(user_id)
        recommendations = Recommendation.get_recommendations(user_id)

        result = []
        for r in recommendations:
            movie = Movie.get_by_id(r.movie_id)
            if movie:
                result.append({
                    "movie_id": movie.id,
                    "title": movie.title,
                    "genre": movie.genre,
                    "year": movie.year,
                    "image": movie.image,
                    "score": round(r.score, 2),
                    "recommended_at": r.recommended_at
                })

        return jsonify({
            "success": True,
            "user_id": user_id,
            "recommendations": result,
            "count": len(result)
        })

    except Exception as e:
        print("ERROR in get_user_recommendations:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
