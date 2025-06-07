from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from cineTogether.models.comment_model import Comment


apiComments = Blueprint("apiComments", __name__, url_prefix="/api/comments")

# ------------------ YORUM OLUŞTUR ------------------

@apiComments.route("/create", methods=["POST"])
@jwt_required()
def create_comment():
    try:
        # JWT'den kullanıcıyı al
        current_user_id = get_jwt_identity()

        # Form verilerini al
        post_id = request.form.get("post_id")
        text = request.form.get("text")

        # Gerekli alanlar dolu mu kontrol et
        if not post_id or not text:
            return jsonify({"success": False, "message": "Missing post_id or text"}), 400

        # Yorumu oluştur
        comment = Comment.create_comment(
            post_id=post_id,
            user_id=current_user_id,
            text=text
        )

        return jsonify({
            "success": True,
            "message": "Comment created",
            "comment": {
                "id": comment.id,
                "post_id": comment.post_id,
                "user_id": comment.user_id,
                "text": comment.text,
                "created_at": comment.created_at
            }
        }), 201

    except Exception as e:
        print("ERROR in create_comment():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500



# ------------------ POST'A AİT YORUMLARI GETİR ------------------
@apiComments.route("/post/<int:post_id>", methods=["GET"])
def get_comments_by_post(post_id):
    try:
        comments = Comment.get_comments_by_post(post_id)
        result = [{
            "id": c.id,
            "user_id": c.user_id,
            "text": c.text,
            "created_at": c.created_at
        } for c in comments]

        return jsonify({"success": True, "comments": result, "count": len(result)})

    except Exception as e:
        print("ERROR in get_comments_by_post():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


# ------------------ YORUM SİL (SOFT DELETE) ------------------
@apiComments.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    try:
        user_id = get_jwt_identity()
        deleted = Comment.delete_comment(comment_id)

        if not deleted:
            return jsonify({"success": False, "message": "Comment not found or already inactive"}), 404

        return jsonify({"success": True, "message": "Comment deleted (soft)"})

    except Exception as e:
        print("ERROR in delete_comment():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
