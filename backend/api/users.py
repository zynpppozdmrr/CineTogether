from flask import jsonify, Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from cineTogether.models.user_model import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

apiUsers = Blueprint("apiUser", __name__, url_prefix="/api/users")

# GET ALL USERS
@apiUsers.route("/", methods=["GET"])
def users():
    try:
        all_users = User.get_all()
        users = []

        for user in all_users:
            users.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "bio": user.bio,
                "profile_picture_url": user.profile_picture_url,
                "role": user.role,
                "activated": user.activated,
                "created_at": user.created_at
            })

        return jsonify({"success": True, "data": users, "count": len(users)})
    except Exception as e:
        print("ERROR in users():", e)
        return jsonify({"success": False, "message": "There was an error retrieving users"})


# GET, DELETE, PUT USER BY USERNAME
@apiUsers.route("/<string:username>", methods=["GET", "PUT", "DELETE"])
def user_by_username(username):
    try:
        user = User.get_user_by_username(username)
        if user is None:
            return jsonify({"success": False, "message": "User not found"})

        if request.method == "GET":
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "bio": user.bio,
                "profile_picture_url": user.profile_picture_url,
                "role": user.role,
                "activated": user.activated,
                "created_at": user.created_at
            }
            return jsonify({"success": True, "data": user_data})
        
        elif request.method == "PUT":
            updates = {
                "full_name": request.form.get("full_name"),
                "bio": request.form.get("bio"),
                "profile_picture_url": request.form.get("profile_picture_url"),
                "role": request.form.get("role")
            }

            password = request.form.get("password")
            if password:
                updates["password"] = password  # Hash işlemi update_user içinde yapılacak

            User.update_user(user.id, **updates)
            return jsonify({"success": True, "message": f"User '{username}' updated successfully"})


    

        elif request.method == "DELETE":
            password = request.form.get("password")
            if not password:
                return jsonify({"success": False, "message": "Password is required to delete user"})

            from werkzeug.security import check_password_hash
            if not check_password_hash(user.password, password):
                return jsonify({"success": False, "message": "Invalid password"})

            User.update_user(user.id, activated=False)
            return jsonify({"success": True, "message": f"User '{username}' deactivated (soft delete)"})

    except Exception as e:
        print("ERROR in user_by_username:", e)
        return jsonify({"success": False, "message": "There was an error processing the request"})



# ADD USER
@apiUsers.route("/addUser", methods=["POST"])
def addUser():
    try:
        data = request.form
        required_fields = ["username", "email", "password"]
        if not all(field in data for field in required_fields):
            return jsonify({"success": False, "message": "Missing required fields"})

        user = User.add_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            full_name=data.get("full_name"),
            bio=data.get("bio"),
            profile_picture_url=data.get("profile_picture_url"),
            role=data.get("role", "user")
        )

        return jsonify({"success": True, "message": "User added", "user": {"id": user.id}})
    except Exception as e:
        import traceback
        traceback.print_exc()  # Tüm stack trace'i gösterir
        return jsonify({"success": False, "message": f"There was an error creating the user: {str(e)}"})



# ACTIVATE USER
@apiUsers.route("/activate", methods=["POST"])
def activate_user():
    try:
        username = request.form.get("username")
        if not username:
            return jsonify({"success": False, "message": "Username is required"})

        user = User.get_user_by_username(username)
        if user is None:
            return jsonify({"success": False, "message": "User not found"})

        if user.activated:
            return jsonify({"success": False, "message": "User already activated"})

        User.update_user(user.id, activated=True)

        return jsonify({"success": True, "message": f"User '{username}' activated successfully"})
    except Exception as e:
        print("ERROR in activate_user:", e)
        return jsonify({"success": False, "message": "There was an error activating the user"})



# GET ACTIVE USERS
@apiUsers.route("/active", methods=["GET"])
def get_active_users():
    try:
        users = [
            {
                "id": u.id,
                "username": u.username
            } for u in User.get_all() if u.activated
        ]
        return jsonify({"success": True, "data": users})
    except Exception as e:
        print("ERROR in get_active_users:", e)
        return jsonify({"success": False, "message": "There was an error"})


# GET INACTIVE USERS
@apiUsers.route("/inactive", methods=["GET"])
def get_inactive_users():
    try:
        users = [
            {
                "id": u.id,
                "username": u.username
            } for u in User.get_all() if not u.activated
        ]
        return jsonify({"success": True, "data": users})
    except Exception as e:
        print("ERROR in get_inactive_users:", e)
        return jsonify({"success": False, "message": "There was an error"})


@apiUsers.route("/login", methods=["POST"])
def login():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return jsonify({"success": False, "message": "Missing username or password"}), 400

        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        if not check_password_hash(user.password, password):
            return jsonify({"success": False, "message": "Incorrect password"}), 401

        # ✅ JWT token oluştur
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "profile_picture_url": user.profile_picture_url

            }
        })

    except Exception as e:
        print("ERROR in login():", e)
        return jsonify({"success": False, "message": "There was an error during login"})


@apiUsers.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.get_user_by_id(user_id)

        if user is None:
            return jsonify({"success": False, "message": "User not found"}), 404

        return jsonify({
            "success": True,
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "profile_picture_url": user.profile_picture_url
            }
        })

    except Exception as e:
        print("ERROR in /me:", e)
        return jsonify({"success": False, "message": "There was an error"})