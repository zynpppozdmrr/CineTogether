from cineTogether.models.user_model import db
from cineTogether.models.post_model import db
from cineTogether import createApp


def createDB():
    app = createApp()
    with app.app_context():
        db.create_all()
    print("Database created successfully.")

 