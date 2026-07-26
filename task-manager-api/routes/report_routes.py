from flask import Blueprint, request, jsonify
from controllers.report_controller import ReportController, CategoryController

report_bp = Blueprint('reports', __name__)
report_ctrl = ReportController()
category_ctrl = CategoryController()


@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    result, error = report_ctrl.summary()
    return jsonify(result), 200


@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
def user_report(user_id):
    result, error = report_ctrl.user_report(user_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(result), 200


@report_bp.route('/categories', methods=['GET'])
def get_categories():
    result, error = category_ctrl.get_all()
    return jsonify(result), 200


@report_bp.route('/categories', methods=['POST'])
def create_category():
    result, error = category_ctrl.create(request.get_json())
    if error:
        return jsonify({'error': error}), 400
    return jsonify(result), 201


@report_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    result, error = category_ctrl.update(cat_id, request.get_json())
    if error:
        return jsonify({'error': error}), 404
    return jsonify(result), 200


@report_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    error = category_ctrl.delete(cat_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify({'message': 'Categoria deletada'}), 200
