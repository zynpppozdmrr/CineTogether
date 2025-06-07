from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from cineTogether.models.like_model import Like
from cineTogether.models.post_model import Post
from cineTogether.models.user_model import User

apiLikes = Blueprint("apiLikes", __name__, url_prefix="/api/likes")


# ------------------ LIKE OLUŞTUR ------------------
@apiLikes.route("/add", methods=["POST"])
@jwt_required()
def add_like():
    try:
        current_user_id = get_jwt_identity()
        post_id = request.form.get("post_id")

        if not post_id:
            return jsonify({"success": False, "message": "post_id is required"}), 400

        post = Post.get_by_id(post_id)
        if not post:
            return jsonify({"success": False, "message": "Post not found"}), 404

        like = Like.add_like(user_id=current_user_id, post_id=post_id)

        return jsonify({
            "success": True,
            "message": "Like added",
            "like": {
                "post_id": like.post_id,
                "user_id": like.user_id,
                "created_at": like.created_at
            }
        })

    except Exception as e:
        print("ERROR in add_like():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


# ------------------ LIKE SİL ------------------

@apiLikes.route("/remove", methods=["POST"])
@jwt_required()
def remove_like():
    try:
        current_user_id = get_jwt_identity()
        post_id = request.form.get("post_id")

        if not post_id:
            return jsonify({"success": False, "message": "post_id is required"}), 400

        removed = Like.remove_like(user_id=current_user_id, post_id=post_id)

        if not removed:
            return jsonify({"success": False, "message": "Like not found or already removed"}), 404

        return jsonify({"success": True, "message": "Like removed"})

    except Exception as e:
        print("ERROR in remove_like():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
    

# ------------------ POST'A AİT BEĞENİ SAYISI GETİR ------------------
@apiLikes.route("/count/<int:post_id>", methods=["GET"])
def count_likes(post_id):
    try:
        count = Like.count_likes(post_id=post_id)
        return jsonify({"success": True, "post_id": post_id, "like_count": count})
    except Exception as e:
        print("ERROR in count_likes():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
    

# ------------------ POST'A AİT BEĞENİLERİ GETİR ------------------ 
@apiLikes.route("/post/<int:post_id>", methods=["GET"])
def get_likes_by_post(post_id):
    try:
        likes = Like.get_likes_by_post(post_id=post_id)
        result = [  # id olmadığı için sadece user_id ve created_at kullanılır
            {
                "user_id": like.user_id,
                "created_at": like.created_at
            } for like in likes
        ]

        return jsonify({"success": True, "likes": result, "count": len(result)})
    except Exception as e:
        print("ERROR in get_likes_by_post():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


