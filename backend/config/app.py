import os

from flask import Flask
from flask_compress import Compress
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_talisman import Talisman
from redis import Redis

from config import Config, cache, limiter
from DataDomain.Database import db
from ExternalApi.System.config import system
from ExternalApi.TeamFrontend.config import team_frontend
from ExternalApi.TournamentFrontend.config import tournament_frontend
from ExternalApi.UserFrontend.config import user_frontend


def createApp() -> Flask:

    app = Flask(__name__)
    Config.init_app(app)

    app.register_blueprint(team_frontend,
                           url_prefix='/api/team-frontend')
    app.register_blueprint(tournament_frontend,
                           url_prefix='/api/tournament-frontend')
    app.register_blueprint(user_frontend,
                           url_prefix='/api/user-frontend')
    app.register_blueprint(system, url_prefix='/api/system')

    cache.init_app(app)

    db.init_app(app)

    Migrate(
        app,
        db,
        directory=os.path.join(
            app.config['DATABASE_PATH'],
            'Migration'))

    Talisman(app, content_security_policy={
        'default-src': ["'self'"],
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'img-src': ["'self'"],
    })

    Compress(app)

    return app


app = createApp()

jwt = JWTManager(app)

redis = Redis(
    host=app.config['CACHE_REDIS_HOST'],
    port=app.config['CACHE_REDIS_PORT'],
    db=app.config['CACHE_REDIS_DB'])

limiter.init_app(app)
