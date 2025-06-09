from flask import Flask, jsonify
from flask_cors import CORS

from api.users import apiUsers
from api.posts import apiPosts 
from api.comments import apiComments
from api.likes import apiLikes
from api.follows import apiFollows
from api.movies import apiMovies  
from api.ratings import apiRatings 
from api.watchlists import apiWatchlists
from api.favorites import apiFavorites 
from api.watched import apiWatched
from api.recommendations import apiRecommendations



from cineTogether import createApp
from cineTogether.initialize_db import createDB


# APP AND DB CREATION ---------------------------------------------------------
app = createApp()
CORS(app)
createDB()
# -----------------------------------------------------------------------------


# BLUEPRINT REGISTERS ---------------------------------------------------------
app.register_blueprint(apiUsers)
app.register_blueprint(apiPosts)
app.register_blueprint(apiComments)
app.register_blueprint(apiLikes)
app.register_blueprint(apiFollows) 
app.register_blueprint(apiMovies)
app.register_blueprint(apiRatings)
app.register_blueprint(apiWatchlists)
app.register_blueprint(apiFavorites) 
app.register_blueprint(apiWatched)
app.register_blueprint(apiRecommendations)

# -----------------------------------------------------------------------------


@app.route("/")
def index():
    return jsonify({"success": True, " ": "Main Page"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
