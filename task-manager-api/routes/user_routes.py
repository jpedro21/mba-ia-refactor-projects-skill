from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)
user_ctrl = UserController()


@user_bp.route('/users', methods=['GET'])
def get_users():
    result, error = user_ctrl.get_all()
    return jsonify(result), 200


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    result, error = user_ctrl.get_by_id(user_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(result), 200


@user_bp.route('/users', methods=['POST'])
def create_user():
    result, error = user_ctrl.create(request.get_json())
    if error:
        status = 409 if 'cadastrado' in error else 400
        return jsonify({'error': error}), status
    return jsonify(result), 201


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    result, error = user_ctrl.update(user_id, request.get_json())
    if error:
        status = 404 if 'não encontrado' in error else 400
        return jsonify({'error': error}), status
    return jsonify(result), 200


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    error = user_ctrl.delete(user_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200


@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    result, error = user_ctrl.get_user_tasks(user_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(result), 200


@user_bp.route('/login', methods=['POST'])
def login():
    data, error, status = user_ctrl.login(request.get_json())
    if error:
        return jsonify({'error': error}), status
    return jsonify(data), status
