from flask import Flask, jsonify
from flask_cors import CORS
import logging

from config.settings import SECRET_KEY, DEBUG, HOST, PORT
from database import get_db
from models.produto_model import ProdutoModel
from models.usuario_model import UsuarioModel
from models.pedido_model import PedidoModel
from controllers.produto_controller import ProdutoController
from controllers.usuario_controller import UsuarioController
from controllers.pedido_controller import PedidoController
from views.routes import register_routes
from middlewares.error_handler import register_error_handlers

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = DEBUG
CORS(app)

db = get_db()
produto_ctrl = ProdutoController(ProdutoModel(db))
usuario_ctrl = UsuarioController(UsuarioModel(db))
pedido_ctrl = PedidoController(PedidoModel(db))

register_routes(app, produto_ctrl, usuario_ctrl, pedido_ctrl)
register_error_handlers(app)


@app.route("/health", methods=["GET"])
def health_check():
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    cursor.execute("SELECT COUNT(*) FROM produtos")
    produtos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos = cursor.fetchone()[0]
    return jsonify({
        "status": "ok",
        "database": "connected",
        "counts": {"produtos": produtos, "usuarios": usuarios, "pedidos": pedidos},
        "versao": "1.0.0",
    }), 200


if __name__ == "__main__":
    get_db()
    logging.info("SERVIDOR INICIADO em http://%s:%s", HOST, PORT)
    app.run(host=HOST, port=PORT, debug=DEBUG)
