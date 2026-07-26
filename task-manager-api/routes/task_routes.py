from flask import Blueprint, request, jsonify
from controllers.task_controller import TaskController

task_bp = Blueprint('tasks', __name__)
task_ctrl = TaskController()


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    result, error = task_ctrl.get_all()
    if error:
        return jsonify({'error': error}), 500
    return jsonify(result), 200


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    result, error = task_ctrl.get_by_id(task_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(result), 200


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    result, error = task_ctrl.create(request.get_json())
    if error:
        status = 404 if 'não encontrad' in error else 400
        return jsonify({'error': error}), status
    return jsonify(result), 201


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    result, error = task_ctrl.update(task_id, request.get_json())
    if error:
        status = 404 if 'não encontrada' in error else 400
        return jsonify({'error': error}), status
    return jsonify(result), 200


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    error = task_ctrl.delete(task_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify({'message': 'Task deletada com sucesso'}), 200


@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    result, error = task_ctrl.search(
        request.args.get('q', ''),
        request.args.get('status', ''),
        request.args.get('priority', ''),
        request.args.get('user_id', ''),
    )
    return jsonify(result), 200


@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats():
    result, error = task_ctrl.stats()
    return jsonify(result), 200
