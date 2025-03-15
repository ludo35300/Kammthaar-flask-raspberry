from flask import jsonify, request
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token

from constantes.authentification import Authentification

authentification_controller = Blueprint('authentification_controller', __name__, url_prefix='/authentification', description="Authentification")

@authentification_controller.route('/login', methods=['POST'])

def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username == Authentification.USERNAME and password == Authentification.MOT_DE_PASSE:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Accès non autorisé"}), 401