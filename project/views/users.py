from flask import request, abort
from flask_restx import Namespace, reqparse, Resource

from project.exceptions import ItemNotFound
from project.services import UsersService
from project.setup_db import db
from project.tools.security import auth_required

users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    def get(self):
        page = request.args.get("page")
        if page:
            return UsersService(db.session).get_limit_users(page)
        return UsersService(db.session).get_all_users()


@users_ns.route('/<int:uid>/')
class UserView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(400, "User not found")
    def get(self, uid: int):
        try:
            return UsersService(db.session).get_one(uid)
        except ItemNotFound:
            return "", 404

    def patch(self, uid: int):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad request")
        if not req_json.get("id"):
            req_json["id"] = uid
        try:
            return UsersService(db.session).update(req_json)
        except ItemNotFound:
            abort(404, message="User not found")


@users_ns.route('/<int:uid>/password/')
class UserView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(400, "User not found")
    def put(self, uid: int):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad request")
        if not req_json.get("password_1") or not req_json.get("password_2"):
            abort(400, message="Bad request")
        if not req_json.get("email"):
            abort(400, message="Bad request")
        try:
            return UsersService(db.session).update_pass(req_json)
        except ItemNotFound:
            abort(404, message="User not found")
