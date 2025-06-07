from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from cineTogether.models.post_model import Post
from cineTogether.models.user_model import User

apiPosts = Blueprint("apiPosts", __name__, url_prefix="/api/posts")


# ------------------ TÜM AKTİF POSTLARI GETİR ------------------
@apiPosts.route("/", methods=["GET"])
def get_all_posts():
    try:
        posts = Post.get_all()
        result = [{
            "id": post.id,
            "user_id": post.user_id,
            "content": post.content,
            "image_url": post.image_url,
            "is_official": post.is_official,
            "created_at": post.created_at
        } for post in posts]

        return jsonify({"success": True, "posts": result, "count": len(result)})

    except Exception as e:
        print("ERROR in get_all_posts:", e)
        return jsonify({"success": False, "message": "Error while fetching posts"}), 500


# ------------------ BELİRLİ BİR POSTU GETİR ------------------
@apiPosts.route("/<int:id>", methods=["GET"])
def get_post(id):
    post = Post.get_by_id(id)
    if not post:
        return jsonify({"success": False, "message": "Post not found"}), 404

    return jsonify({
        "success": True,
        "post": {
            "id": post.id,
            "content": post.content,
            "image_url": post.image_url,
            "created_at": post.created_at,
            "user_id": post.user_id,
            "is_official": post.is_official
        }
    })


# ------------------ BİR KULLANICIYA AİT AKTİF POSTLARI USERNAME İLE GETİR ------------------
@apiPosts.route("<string:username>", methods=["GET"])
def get_posts_by_username(username):
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        posts = Post.query.filter_by(user_id=user.id, is_active=True).order_by(Post.created_at.desc()).all()
        
        result = [{
            "id": post.id,
            "content": post.content,
            "image_url": post.image_url,
            "created_at": post.created_at,
            "is_official": post.is_official
        } for post in posts]

        return jsonify({"success": True, "posts": result, "count": len(result)})
    
    except Exception as e:
        print("ERROR in get_posts_by_username:", e)
        return jsonify({"success": False, "message": "An error occurred while retrieving posts"}), 500





# ------------------ POST OLUŞTUR (SADECE ADMIN) ------------------
@apiPosts.route("/create", methods=["POST"])
@jwt_required()
def create_post():
    try:
        current_user_id = get_jwt_identity()
        user = User.get_user_by_id(current_user_id)

        if user.role.lower() != "admin":
            return jsonify({"success": False, "message": "Only Admins can create posts"}), 403

        content = request.form.get("content")
        image_url = request.form.get("image_url")

        if not content:
            return jsonify({"success": False, "message": "Post content is required"}), 400

        post = Post.create_post(
            user_id=user.id,
            content=content,
            image_url=image_url,
            is_official=True
        )

        return jsonify({
            "success": True,
            "message": "Post created",
            "post": {
                "id": post.id,
                "content": post.content,
                "created_at": post.created_at
            }
        })

    except Exception as e:
        print("ERROR in create_post():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


# ------------------ POST SİL (SOFT DELETE) ------------------
@apiPosts.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_post(id):
    current_user_id = get_jwt_identity()
    user = User.get_user_by_id(current_user_id)

    if user.role.lower() != "admin":
        return jsonify({"success": False, "message": "Only Admins can delete posts"}), 403

    deleted = Post.delete_post(id)
    if not deleted:
        return jsonify({"success": False, "message": "Post not found or already inactive"}), 404

    return jsonify({"success": True, "message": "Post has been deactivated"})


# ------------------ POST GÜNCELLE (SADECE ADMIN) ------------------

@apiPosts.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_post(id):
    try:
        current_user_id = get_jwt_identity()
        user = User.get_user_by_id(current_user_id)

        if user.role.lower() != "admin":
            return jsonify({"success": False, "message": "Only Admins can update posts"}), 403

        content = request.form.get("content")
        image_url = request.form.get("image_url")

        updated_post = Post.update_post(id, content=content, image_url=image_url)

        if not updated_post:
            return jsonify({"success": False, "message": "Post not found or is inactive"}), 404

        return jsonify({
            "success": True,
            "message": "Post updated successfully",
            "post": {
                "id": updated_post.id,
                "content": updated_post.content,
                "image_url": updated_post.image_url,
                "created_at": updated_post.created_at
            }
        })

    except Exception as e:
        import traceback
        print("ERROR in update_post():", e)
        traceback.print_exc()
        return jsonify({"success": False, "message": "Internal server error"}), 500
 
    
    
# ------------------ AKTİF OLMAYAN POSTLARI GETİR (SADECE ADMIN) ------------------

@apiPosts.route("/inactive", methods=["GET"])
@jwt_required()
def get_inactive_posts():
    try:
        # Giriş yapan kullanıcıyı al
        current_user_id = get_jwt_identity()
        user = User.get_user_by_id(current_user_id)

        # Yalnızca admin yetkisi olanlar görebilsin
        if user.role.lower() != "admin":
            return jsonify({"success": False, "message": "Only admins can view inactive posts"}), 403

        # is_active=False olan postları al
        posts = Post.query.filter_by(is_active=False).order_by(Post.created_at.desc()).all()

        result = [{
            "id": post.id,
            "content": post.content,
            "image_url": post.image_url,
            "created_at": post.created_at,
            "user_id": post.user_id,
            "is_official": post.is_official
        } for post in posts]

        return jsonify({
            "success": True,
            "inactive_posts": result,
            "count": len(result)
        })

    except Exception as e:
        print("ERROR in get_inactive_posts:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500


# ------------------ POST REAKTİVE ET (SADECE ADMIN) ------------------

@apiPosts.route("/<int:id>/reactivate", methods=["POST"])
@jwt_required()
def reactivate_post(id):
    try:
        current_user_id = get_jwt_identity()
        user = User.get_user_by_id(current_user_id)

        # Sadece Admin kullanıcılar re-activate edebilir
        if user.role.lower() != "admin":
            return jsonify({"success": False, "message": "Only Admins can reactivate posts"}), 403

        # Re-activate işlemini modelden yap
        reactivated = Post.reactivate_post(id)

        if not reactivated:
            return jsonify({"success": False, "message": "Post not found or already active"}), 404

        return jsonify({
            "success": True,
            "message": "Post reactivated successfully",
            "post": {
                "id": reactivated.id,
                "content": reactivated.content,
                "created_at": reactivated.created_at,
                "user_id": reactivated.user_id,
                "is_active": reactivated.is_active
            }
        })

    except Exception as e:
        print("ERROR in reactivate_post():", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500
