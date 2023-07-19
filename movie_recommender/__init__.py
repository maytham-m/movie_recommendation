from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .blueprints.main import main
    from .blueprints.recommend import recommend

    app.register_blueprint(main)
    app.register_blueprint(recommend)

    return app
