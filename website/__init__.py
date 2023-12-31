from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"  # ustawienei nazwy bazy danych


def create_app():
    app = Flask(__name__)
    app.config[
        "SECRET_KEY"
    ] = "eh2WGSwY@HwO$!S!j32EM*9$36zKJCyvrvu#fRVV3rgs$3@H&whPGXwknMyW#qypW%E#D8yhTPDq$m##Ho6wUkNdIeuWozI8dZM"  # secret key jest tu widoczny bo jest to tylko do portfolio inaczej byłby ukryty ze względów bezpieczeństwa, moze jeszcze tym sie zajmę ale zobaczę

    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #stare do bazy danych na sqlite
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://root:restaurantmanager@localhost/managerdatabase"

    db.init_app(app)

    from .views import views  # biore moje głowne pliki python
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note, Prod  # importuje modele do tworzenia danych w bazie

    with app.app_context():  # tworze te bazy danych
        db.create_all()

    login_manager = LoginManager()  # do ogarniania logujących się
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader  # nadal ogarnianie logowania
    def load_user(id):
        return User.query.get(int(id))

    return app
