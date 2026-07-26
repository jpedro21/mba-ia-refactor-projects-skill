from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Recurso não encontrado'}), 404

    @app.errorhandler(500)
    def internal_error(e):
        logger.error('Internal server error: %s', e)
        return jsonify({'error': 'Erro interno do servidor'}), 500
