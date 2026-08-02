from flask import Flask
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
from controllers.health_controller import HealthController
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
health_ctrl = HealthController(db)

register_routes(app, produto_ctrl, usuario_ctrl, pedido_ctrl, health_ctrl)
register_error_handlers(app)


if __name__ == "__main__":
    get_db()
    logging.info("SERVIDOR INICIADO em http://%s:%s", HOST, PORT)
    app.run(host=HOST, port=PORT, debug=DEBUG)
