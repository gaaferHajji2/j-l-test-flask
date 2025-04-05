from flask import Flask, jsonify

from flask_smorest import Api

from flask_jwt_extended import JWTManager

from flask_migrate import Migrate

import redis

from rq import Queue

import os

from db import db

import models

from blocklist import BLOCKLSIT


from resources.store_resource import store_blueprint

from resources.item_resource import item_blueprint

from resources.tag_resource import tag_blp

from resources.user_resource import user_blp

from dotenv import load_dotenv

load_dotenv()


def create_app(db_url=None):
    app =Flask(__name__)

    app.config['PROPAGATE_EXCEPTIONS'] = True

    app.config['API_TITLE'] = "Jafar App"

    app.config['API_VERSION'] = "v1"

    app.config['OPENAPI_VERSION'] = '3.0.3'

    app.config['OPENAPI_URL_PREFIX'] = '/'

    app.config['OPENAPI_REDOC_URL'] = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'

    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/docs'

    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    app.config['SQLALCHEMY_DATABASE_URI']= db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app=app)

    conn = redis.from_url(os.getenv('REDIS_URL') or 'redis://localhost:9379')

    app.queue = Queue("emails", connection=conn)

    migrate = Migrate(app=app, db=db)

    api = Api(app=app)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_TOKEN', 'Jafar@Loka@123')

    jwt = JWTManager(app=app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLSIT
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'message': "The Token has been revoked, re-login",
            'error': "Token Revoked",
        }), 401

    @jwt.additional_claims_loader
    def add_claims_to_identity(identity):
        if identity == 1:
            return { "admin" : True  }
        else:
            return { "admin" : False }

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "The Token has been expired, please re-login",
            "error": "Token Expired",
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": "Signature Verification Failed",
            "error": "Invalid Signature"
        }), 401

    @jwt.unauthorized_loader
    def unauthorization_callback(error):
        return jsonify({
            "message": "Request doesn't contain an access token",
            "error": "Authorization Required"
        }), 401

    # not working
    # @app.before_first_request
    # def create_tables():
    #     db.create_all()

    # Here we use flask-migrate to generate the
    # db, so we don't need this lines any more.
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(store_blueprint)

    api.register_blueprint(item_blueprint)

    api.register_blueprint(tag_blp)

    api.register_blueprint(user_blp)

    @app.errorhandler(404)
    def get_not_found(error):
        return {
            "message": error.description
        }, 404
    
    @app.errorhandler(500)
    def ise_handler(error):
        return {
            "message": "ISE Occurred, Please Try Again Later"
        }, 500

    return app

# The Running Command is:
# waitress-serve --listen=*:5000 --call "app:create_app"