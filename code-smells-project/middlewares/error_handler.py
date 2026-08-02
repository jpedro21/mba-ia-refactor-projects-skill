from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        logger.error("Internal server error: %s", e)
        return jsonify({"erro": "Erro interno do servidor"}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("Unhandled exception: %s", e)
        return jsonify({"erro": "Erro interno do servidor"}), 500
