from flask import abort;

from flask import current_app

from flask.views import MethodView;

from flask_smorest import Blueprint;

from flask_jwt_extended import create_access_token;
from flask_jwt_extended import get_jwt, jwt_required;
from flask_jwt_extended import create_refresh_token;
from flask_jwt_extended import get_jwt_identity;

from passlib.hash import pbkdf2_sha256;

from tasks import send_simple_message;

from models.user_model import UserModel;

from schemas_shape import UserSchema;

from blocklist import BLOCKLSIT;

from db import db;

user_blp = Blueprint("users", __name__, description='The User\'s Requests');


@user_blp.route('/register')
class UserRegisterResource(MethodView):
    @user_blp.arguments(UserSchema)
    def post(self, payload):
        if UserModel.get_user_by_username(payload['username']):
            abort(409, {"message": "User Already Exists"});
        
        user_model_data = UserModel(
            username = payload['username'],
            password = pbkdf2_sha256.hash(payload['password'])
        );

        user_model_data.save_user_data_to_db();

        enqueue_data = current_app.queue.enqueue(
            send_simple_message, 
            to="gaafer.hajji1995@gmail.com",
            subject="Successfull Register",
            message=f"Salam Alekoum {user_model_data.username}, This is for Testing Mailgun Only"
        );

        print(enqueue_data);

        # request_data = send_simple_message(
        #     to="gaafer.hajji1995@gmail.com",
        #     subject="Successfull Register",
        #     message=f"Salam Alekoum {user_model_data.username}, This is for Testing Mailgun Only"
        # );

        # print(request_data);
        # print(request_data.json());

        return {
            "message": "User Created Successfully"
        }, 201;

@user_blp.route('/login')
class UserLoginResource(MethodView):
    @user_blp.arguments(UserSchema)
    def post(self, payload):
        user_model_data = UserModel.get_user_by_username(payload['username']);

        if user_model_data and pbkdf2_sha256.verify(payload['password'], user_model_data.password):
            access_token = create_access_token(
                identity=user_model_data.id,
                fresh=True,
            );

            refresh_token = create_refresh_token(identity=user_model_data.id);

        
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        abort(400);

@user_blp.route('/refresh')
class UserRefreshTokenResource(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity();

        user_token = create_access_token(identity=current_user, fresh=False);

        return {
            "access_token": user_token,
        }


@user_blp.route('/logout')
class UserLogoutResource(MethodView):

    @jwt_required()
    def post(self):
        jti = get_jwt()['jti'];

        BLOCKLSIT.add(jti);

        return {
            "message": "Successfully Logout",
        }


@user_blp.route('/user/<int:user_id>')
class UserDataResource(MethodView):

    @user_blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.get_user_by_id(user_id=user_id);

        return user;

    def delete(self, user_id):
        user = UserModel.get_user_by_id(user_id=user_id);

        user.delete_user_data_by_id();

        return {
            "message": "User Deleted Successfully",
        };