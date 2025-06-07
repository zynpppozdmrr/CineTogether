# backend/api/follows.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from cineTogether.models.user_model import User
from cineTogether.models.follow_model import Follow

apiFollows = Blueprint("apiFollows", __name__, url_prefix="/api/follows")

@apiFollows.route("/follow", methods=["POST"])
@jwt_required()
def follow_user():
    # THE FIX IS HERE: Convert the identity from the token (which is a string) to an integer.
    
    
    current_user_id = int(get_jwt_identity())
    followee_id = request.form.get("followee_id")

    if not followee_id:
        return jsonify({"success": False, "message": "Missing followee_id"}), 400

    success = Follow.follow(current_user_id, int(followee_id))
    if not success:
        return jsonify({"success": False, "message": "Follow failed"}), 400

    return jsonify({"success": True, "message": f"Now following user {followee_id}"}), 201


@apiFollows.route("/unfollow", methods=["POST"])
@jwt_required()
def unfollow_user():
    # THE FIX IS HERE: Also apply the fix to the unfollow function.
    current_user_id = int(get_jwt_identity())
    followee_id = request.form.get("followee_id")

    if not followee_id:
        return jsonify({"success": False, "message": "Missing followee_id"}), 400

    success = Follow.unfollow(current_user_id, int(followee_id))
    if not success:
        return jsonify({"success": False, "message": "Unfollow failed"}), 400

    return jsonify({"success": True, "message": f"Unfollowed user {followee_id}"}), 200


@apiFollows.route("/followers/<int:user_id>", methods=["GET"])
def get_followers(user_id):
    followers = Follow.get_followers(user_id)
    return jsonify({
        "success": True,
        "user_id": user_id,
        "followers": followers,
        "count": len(followers)
    })

@apiFollows.route("/following/<int:user_id>", methods=["GET"])
def get_following(user_id):
    try:
        following_list = Follow.get_following(user_id)
        return jsonify({
            "success": True,
            "user_id": user_id,
            "following": following_list,
            "count": len(following_list)
        })
    except Exception as e:
        print("ERROR in get_following:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500